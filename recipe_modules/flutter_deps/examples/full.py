# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from recipe_engine.post_process import DoesNotRun, Filter, StatusFailure

DEPS = [
    'flutter/flutter_deps',
    'recipe_engine/assertions',
    'recipe_engine/path',
    'recipe_engine/platform',
    'recipe_engine/properties',
]


def RunSteps(api):
  env = {}
  env_prefixes = {}
  api.flutter_deps.open_jdk(env, env_prefixes, 'v1')
  api.assertions.assertTrue(env.get('JAVA_HOME'))
  api.flutter_deps.goldctl(env, env_prefixes, 'v2')
  api.assertions.assertTrue(env.get('GOLDCTL'))
  #api.assertions.assertEqual(
  #    env_prefixes.get('PATH'), [api.path['cache'].join('java', 'bin')]
  #)
  env_prefixes = {}
  env = {}
  api.flutter_deps.chrome_and_driver(env, env_prefixes, 'v3')
  api.assertions.assertTrue(env.get('CHROME_NO_SANDBOX'))
  api.assertions.assertTrue(env.get('CHROME_EXECUTABLE'))
  api.assertions.assertEqual(
      env_prefixes.get('PATH'), [
          api.path['cache'].join('chrome', 'chrome'),
          api.path['cache'].join('chrome', 'drivers')
      ]
  )
  api.flutter_deps.go_sdk(env, env_prefixes, 'v4')
  api.flutter_deps.dashing(env, env_prefixes, 'v5')
  api.flutter_deps.vpython(env, env_prefixes, 'v6')
  deps = api.properties.get("dependencies", [])
  api.flutter_deps.required_deps(env, env_prefixes, deps)
  with api.assertions.assertRaises(ValueError):
    api.flutter_deps.required_deps(
        env, env_prefixes, [{'dependency': 'does_not_exist'}]
    )
  api.flutter_deps.android_sdk(env, env_prefixes, '')
  api.flutter_deps.flutter_engine(env, env_prefixes)


def GenTests(api):
  yield api.test('basic')
  yield api.test(
      'mac', api.platform('mac', 64),
      api.properties(
          dependencies=[{"dependency": "xcode"},
                        {'dependency': 'chrome_and_driver'}]
      )
  )
  yield api.test('flutter_engine',
      api.properties(
          isolated_hash='abceqwe',
      )
  )
  yield api.test(
      'goldTryjob',
      api.properties(gold_tryjob=True, git_ref='refs/pull/1/head')
  )
