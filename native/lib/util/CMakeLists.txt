# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

add_library(util RunfilesPath.cc Subprocess.cc)

target_include_directories(util PUBLIC ${Boost_INCLUDE_DIR})
target_link_libraries(util service_proto boost_filesystem grpc++ fmt::fmt)
