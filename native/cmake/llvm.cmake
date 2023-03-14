# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

fetchcontent_declare(
    llvm
    GIT_REPOSITORY https://github.com/llvm/llvm-project
    GIT_TAG llvmorg-10.0.0
)
set(FETCHCONTENT_QUIET OFF)

fetchcontent_makeavailable(llvm)
