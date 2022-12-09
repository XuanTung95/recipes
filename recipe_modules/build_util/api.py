# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from recipe_engine import recipe_api


class BuildUtilApi(recipe_api.RecipeApi):
  """Gn and Ninja wrapper functions."""

  def __init__(self, *args, **kwargs):
    super(BuildUtilApi, self).__init__(*args, **kwargs)
    self._initialized = None

  def _initialize(self):
    if self._initialized:
      return
    if not self.m.properties.get('no_goma', False):
      self.m.goma.ensure()
    self._initialized = True

  def run_gn(self, gn_args, checkout_path):
    """Run a gn command with the given arguments.

    Args:
      gn_args(list): A list of strings to be passed to the gn command.
      checkout_path(Path): A path object with the checkout location.
    """
    self._initialize()
    gn_cmd = ['python', checkout_path.join('flutter/tools/gn')]
    if not self.m.properties.get('no_goma', False):
      gn_cmd.append('--goma')
    if self.m.properties.get('no_lto', False) and '--no-lto' not in gn_args:
      gn_args += ('--no-lto',)
    gn_cmd.extend(gn_args)
    env = {}
    if not self.m.properties.get('no_goma', False):
      self.m.goma.set_path(self.m.goma.goma_dir)
      env = {'GOMA_DIR': self.m.goma.goma_dir}
    with self.m.context(env=env):
      self.m.step('gn %s' % ' '.join(gn_args), gn_cmd)

  def _build_goma(self, config, checkout_path, targets, tool):
    """Builds using ninja and goma.

    Args:
      config(str): A string with the configuration to build.
      checkout_path(Path): A path object with the checkout location.
      targets(list): A list of string with the ninja targets to build.
    """
    self._initialize()
    build_dir = checkout_path.join('out/%s' % config)
    goma_jobs = self.m.properties.get('goma_jobs', '200')
    ninja_args = [tool, '-j', goma_jobs, '-C', build_dir]
    ninja_args.extend(targets)
    self.m.goma.set_path(self.m.goma.goma_dir)
    env = {'GOMA_DIR': self.m.goma.goma_dir}
    with self.m.context(
        env=env), self.m.goma.build_with_goma(), self.m.depot_tools.on_path():
      name = 'build %s' % ' '.join([config] + list(targets))
      self.m.step(name, ninja_args)

  def _build_no_goma(self, config, checkout_path, targets, tool):
    """Builds using ninja without goma.

    Args:
      config(str): A string with the configuration to build.
      checkout_path(Path): A path object with the checkout location.
      targets(list): A list of string with the ninja targets to build.
    """
    self._initialize()
    build_dir = checkout_path.join('out/%s' % config)
    ninja_args = [tool, '-C', build_dir]
    ninja_args.extend(targets)
    with self.m.depot_tools.on_path():
      name = 'build %s' % ' '.join([config] + list(targets))
      self.m.step(name, ninja_args)

  def build(self, config, checkout_path, targets):
    """Builds using ninja.

    Args:
      config(str): A string with the configuration to build.
      checkout_path(Path): A path object with the checkout location.
      targets(list): A list of string with the ninja targets to build.
    """
    ninja_path = checkout_path.join('flutter', 'third_party', 'ninja', 'ninja')
    if not self.m.properties.get('no_goma', False):
      self._build_goma(config, checkout_path, targets, ninja_path)
    else:
      self._build_no_goma(config, checkout_path, targets, ninja_path)
