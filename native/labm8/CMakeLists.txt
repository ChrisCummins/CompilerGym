# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

add_library(
    labm8
    logging.cc
    status.cc
    statusor.cc
    string.cc
    stringpiece.cc
)
target_include_directories(labm8 PUBLIC ${Boost_INCLUDE_DIR})
