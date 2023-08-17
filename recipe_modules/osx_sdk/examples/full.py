# Copyright 2018 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

DEPS = [
    'flutter/os_utils',
    'flutter/osx_sdk',
    'recipe_engine/file',
    'recipe_engine/path',
    'recipe_engine/platform',
    'recipe_engine/properties',
    'recipe_engine/raw_io',
    'recipe_engine/step',
]


def RunSteps(api):
  with api.osx_sdk('mac'):
    api.step('gn', ['gn', 'gen', 'out/Release'])
    api.step('ninja', ['ninja', '-C', 'out/Release'])
  with api.osx_sdk('mac', devicelab=True):
    api.step('gn', ['gn', 'gen', 'out/Release'])
    api.step('ninja', ['ninja', '-C', 'out/Release'])


def GenTests(api):
  for platform in ('linux', 'mac', 'win'):
    yield (api.test(platform) + api.platform.name(platform))

  yield api.test(
      'explicit_version', api.platform.name('mac'),
      api.properties(
          **{
              '$flutter/osx_sdk': {
                  'sdk_version': 'deadbeef', 'toolchain_ver': '123abc',
                  'cleanup_cache': True
              }
          }
      )
  )

  sdk_app_path = api.path['cache'].join(
      'osx_sdk', 'xcode_deadbeef', 'XCode.app'
  )

  yield api.test(
      'explicit_runtime_version',
      api.platform.name('mac'),
      api.properties(
          **{
              '$flutter/osx_sdk': {
                  'sdk_version': 'deadbeef', 'toolchain_ver': '123abc',
                  'runtime_versions': ['ios-13-0', 'ios-14-0']
              }
          }
      ),
      api.step_data(
          'list runtimes',
          stdout=api.raw_io.output_text(
              '== Runtimes ==\n' +
              'iOS 13.0 - com.apple.CoreSimulator.SimRuntime.iOS-13-0\n' +
              'iOS 14.0 - com.apple.CoreSimulator.SimRuntime.iOS-14-0'
          )
      ),
      api.os_utils.is_symlink(False),
  )

  yield api.test(
      'no_runtime_version',
      api.platform.name('mac'),
      api.properties(
          **{
              '$flutter/osx_sdk': {
                  'sdk_version': 'deadbeef',
                  'toolchain_ver': '123abc',
              }
          }
      ),
      api.os_utils.is_symlink(False),
      api.path.exists(sdk_app_path),
  )

  yield api.test(
      'automatic_version',
      api.platform.name('mac'),
      api.platform.mac_release('10.15.6'),
  )

  yield api.test(
      'ancient_version',
      api.platform.name('mac'),
      api.platform.mac_release('10.1.0'),
  )
