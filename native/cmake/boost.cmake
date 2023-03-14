# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

include(FetchContent)

fetchcontent_declare(
    boost
    GIT_REPOSITORY https://github.com/boostorg/boost.git
    GIT_TAG boost-1.81.0
)
set(FETCHCONTENT_QUIET OFF)
fetchcontent_makeavailable(boost)
