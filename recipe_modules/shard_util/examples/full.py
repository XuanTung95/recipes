# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from recipe_engine.post_process import DoesNotRun, Filter, StatusFailure

PYTHON_VERSION_COMPATIBILITY = 'PY2'

DEPS = [
    'flutter/shard_util',
    'recipe_engine/platform',
    'recipe_engine/properties',
]


def RunSteps(api):
  builds = api.shard_util.schedule_builds()
  api.shard_util.collect_builds(builds)


def GenTests(api):
  yield api.test(
      'postsubmit', api.properties(subshards=['0', '1_last']),
      api.platform.name('win')
  )
  props = {
      'subshards': ['0', '1_last'], 'git_url': 'https://abc', 'git_ref': 'abc',
      'dependencies': [{"dependency": "android_sdk"},
                       {"dependency": "chrome_and_driver"}],
      '$depot_tools/osx_sdk': {"sdk_version": "11a420a"},
      '$flutter/osx_sdk': {"sdk_version": "11a420a"},
      'gems': [["cocoapods",
                "1.6.0"]], 'drone_dimensions': ['os=Windows Server']
  }
  yield api.test(
      'presubmit', api.properties(**props), api.platform.name('linux')
  )
