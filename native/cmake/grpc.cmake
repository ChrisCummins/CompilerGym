# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Find Protobuf installation
set(protobuf_MODULE_COMPATIBLE TRUE)
message(STATUS "Using protobuf ${Protobuf_VERSION}")
set(PROTOC $<TARGET_FILE:protobuf::protoc>)

# Find gRPC installation
find_package(gRPC CONFIG REQUIRED)
message(STATUS "Using gRPC ${gRPC_VERSION}")

set(GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_cpp_plugin>)
