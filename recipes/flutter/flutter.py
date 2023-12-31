# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from contextlib import contextmanager
import re

from PB.go.chromium.org.luci.buildbucket.proto import build as build_pb2
from PB.go.chromium.org.luci.buildbucket.proto import common as common_pb2
from PB.go.chromium.org.luci.buildbucket.proto \
  import builds_service as builds_service_pb2
from RECIPE_MODULES.flutter.flutter_bcid.api import BcidStage
from google.protobuf import struct_pb2

DEPS = [
    'flutter/adhoc_validation',
    'flutter/flutter_bcid',
    'flutter/flutter_deps',
    'flutter/os_utils',
    'flutter/repo_util',
    'recipe_engine/context',
    'recipe_engine/defer',
    'recipe_engine/path',
    'recipe_engine/properties',
    'recipe_engine/step',
]


def RunSteps(api):
  """Recipe to run flutter sdk tests."""
  api.flutter_bcid.report_stage(BcidStage.START.value)
  # Collect memory/cpu/process before task execution.
  api.os_utils.collect_os_info()
  api.os_utils.print_pub_certs()

  # Trigger validation tests. This is to optimize resources usage
  # when don't need to run in shards.
  # include UTF-8 char in path to test for resilience
  checkout_path = api.path['start_dir'].join('Á flutter sdk')
  api.flutter_bcid.report_stage(BcidStage.FETCH.value)
  with api.step.nest('checkout source code'):
    api.repo_util.checkout(
        'flutter',
        checkout_path=checkout_path,
        url=api.properties.get('git_url'),
        ref=api.properties.get('git_ref')
    )

  env, env_prefixes = api.repo_util.flutter_environment(checkout_path)
  api.flutter_deps.required_deps(
      env, env_prefixes, api.properties.get('dependencies', [])
  )
  with api.context(env=env, env_prefixes=env_prefixes, cwd=checkout_path):
    with api.step.nest('prepare environment'):
      deferred = []
      deferred.append(
          api.defer(api.step, 'flutter doctor', ['flutter', 'doctor'])
      )
      deferred.append(
          api.defer(
              api.step,
              'download dependencies',
              ['flutter', 'update-packages', '-v'],
              infra_step=True,
          )
      )
      api.defer.collect(deferred)

    deferred = []
    deferred.append(
        api.defer(
            api.adhoc_validation.run,
            api.properties.get('validation_name'),
            api.properties.get('validation'), env, env_prefixes,
            api.properties.get('secrets', {})
        )
    )
    # This is to clean up leaked processes.
    deferred.append(api.defer(api.os_utils.kill_processes))
    # Collect memory/cpu/process after task execution.
    deferred.append(api.defer(api.os_utils.collect_os_info))
    api.defer.collect(deferred)


def GenTests(api):
  yield api.test(
      'validators',
      api.properties(
          validation='analyze',
          validation_name='dart analyze',
          android_sdk_license='android_license',
          android_sdk_preview_license='android_preview_license'
      ), api.repo_util.flutter_environment_data()
  )
