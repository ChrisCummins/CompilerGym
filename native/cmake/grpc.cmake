# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Find Protobuf installation
find_package(PkgConfig REQUIRED)
pkg_search_module(PROTOBUF REQUIRED protobuf)
find_program(PROTOC protoc)
message(STATUS "Using protobuf: ${PROTOBUF_VERSION}")
message(STATUS "Protobuf compiler: ${PROTOC}")

# Find gRPC installation
pkg_search_module(GRPC REQUIRED grpc)
pkg_search_module(GRPCPP REQUIRED grpc++)
include_directories(SYSTEM ${GRPC_INCLUDEDIR})
find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin)
message(STATUS "Using gRPC: ${GRPC_VERSION}")
message(STATUS "gRPC C++ plugin: ${GRPC_CPP_PLUGIN}")
