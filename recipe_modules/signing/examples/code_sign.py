# Copyright 2023 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import contextlib
from recipe_engine.post_process import (Filter)

DEPS = [
    'flutter/signing',
    'recipe_engine/assertions',
    'recipe_engine/platform',
    'recipe_engine/properties',
    'recipe_engine/raw_io',
]


def RunSteps(api):
  files_to_sign = ['file1.zip']
  api.signing.code_sign(files_to_sign=files_to_sign)


def GenTests(api):
  yield api.test(
      'non_mac', api.platform.name('linux'),
      api.properties(expected_result=False)
  )
  yield api.test(
      'mac_require_signing', api.platform.name('mac'),
      api.properties(expected_result=True)
  )
  yield api.test(
      'no_signing_identity', api.platform.name('mac'),
      api.properties(expected_result=False)
  )
