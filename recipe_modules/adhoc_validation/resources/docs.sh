#!/bin/bash

# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# Script to generate and upload flutter docs.

set -e

./dev/bots/docs.sh --output dev/docs/api_docs.zip --keep-staging --staging-dir dev/docs
