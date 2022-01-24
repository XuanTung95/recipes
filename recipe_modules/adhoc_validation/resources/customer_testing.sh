#!/bin/bash

# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

set -e
git fetch origin $GIT_BRANCH:$GIT_BRANCH
cd dev/customer_testing/
bash ci.sh
