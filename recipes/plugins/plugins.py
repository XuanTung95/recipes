# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

DEPS = [
    'flutter/repo_util',
    'flutter/flutter_deps',
    'recipe_engine/context',
    'recipe_engine/path',
    'recipe_engine/properties',
    'recipe_engine/step',
]


def RunSteps(api):
  """Recipe to run flutter plugin tests."""
  plugins_checkout_path = api.path['start_dir'].join('plugins')
  flutter_checkout_path = api.path['start_dir'].join('flutter')
  with api.step.nest('checkout source code'):
    # Check out flutter ToT from master.
    api.repo_util.checkout(
        'flutter',
        checkout_path=flutter_checkout_path,
        ref='refs/heads/stable',
    )
    api.repo_util.checkout(
        'plugins',
        checkout_path=plugins_checkout_path,
        url=api.properties.get('git_url'),
        ref=api.properties.get('git_ref')
    )
  channel = api.properties.get('channel', 'master')
  env, env_prefixes = api.repo_util.flutter_environment(flutter_checkout_path)
  api.flutter_deps.vs_build(env, env_prefixes)
  with api.context(env=env, env_prefixes=env_prefixes,
                   cwd=flutter_checkout_path):
    with api.step.nest('prepare environment'):
      api.step('flutter set channel', ['flutter', 'channel', channel])
      api.step('flutter upgrade', ['flutter', 'upgrade'])
      api.step(
          'flutter config --enable-windows-desktop',
          ['flutter', 'config', '--enable-windows-desktop'],
          infra_step=True,
      )
      api.step('flutter doctor', ['flutter', 'doctor'])
      # Fail fast on dependencies problem.
      timeout_secs = 300
      api.step(
          'download dependencies', ['flutter', 'update-packages'],
          infra_step=True,
          timeout=timeout_secs
      )
      api.step(
          'pub global activate flutter_plugin_tools',
          ['pub', 'global', 'activate', 'flutter_plugin_tools'],
          infra_step=True,
      )
  with api.context(env=env, env_prefixes=env_prefixes,
                   cwd=plugins_checkout_path):
    with api.step.nest('Run plugin tests'):
      api.step(
          'build examples',
          ['bash', 'script/tool_runner.sh', 'build-examples', '--windows']
      )
      api.step(
          'drive examples',
          ['bash', 'script/tool_runner.sh', 'drive-examples', '--windows']
      )


def GenTests(api):
  yield api.test('basic', api.repo_util.flutter_environment_data())
