# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

find_package(LLVM 10.0.0 REQUIRED CONFIG)
message(STATUS "Using LLVM ${LLVM_VERSION} from ${LLVM_DIR}")
