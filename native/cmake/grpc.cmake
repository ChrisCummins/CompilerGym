# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Find Protobuf installation
find_package(PkgConfig REQUIRED)
pkg_search_module(PROTOBUF REQUIRED protobuf)
find_program(PROTOC protoc)
message(STATUS "Using protobuf: ${PROTOBUF_VERSION}")

# TODO(cummins): Same as above but for gRPC:
# Find gRPC installation
find_package(gRPC CONFIG REQUIRED)
message(STATUS "Using gRPC ${gRPC_VERSION}")

set(GRPC_CPP_PLUGIN $<TARGET_FILE:gRPC::grpc_cpp_plugin>)
include_directories(
    SYSTEM
    $<TARGET_PROPERTY:gRPC::grpc++,INTERFACE_INCLUDE_DIRECTORIES>
)
