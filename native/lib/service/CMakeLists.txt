# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Protocol buffers.

get_filename_component(service_proto "compiler_gym_service.proto" ABSOLUTE)
get_filename_component(service_proto_path "${service_proto}" PATH)

set(service_proto_srcs
    "${generated_header_dir}/compiler_gym/service/compiler_gym_service.pb.cc"
)
set(service_proto_hdrs
    "${generated_header_dir}/compiler_gym/service/compiler_gym_service.pb.h"
)
set(service_grpc_srcs
    "${generated_header_dir}/compiler_gym/service/compiler_gym_service.grpc.pb.cc"
)
set(service_grpc_hdrs
    "${generated_header_dir}/compiler_gym/service/compiler_gym_service.grpc.pb.h"
)

add_custom_command(
    OUTPUT
        "${service_proto_srcs}"
        "${service_proto_hdrs}"
        "${service_grpc_srcs}"
        "${service_grpc_hdrs}"
    COMMAND ${PROTOC}
    ARGS
        --grpc_out
        "${generated_header_dir}/compiler_gym/service"
        --cpp_out
        "${generated_header_dir}/compiler_gym/service"
        -I
        "${service_proto_path}"
        --plugin=protoc-gen-grpc="${GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${service_proto}"
    DEPENDS "${service_proto}"
)

add_library(
    service_proto
    ${service_grpc_srcs}
    ${service_grpc_hdrs}
    ${service_proto_srcs}
    ${service_proto_hdrs}
)
target_link_libraries(
    service_proto
    gRPC::grpc++_reflection
    grpc++
    protobuf::libprotobuf
)

# C++ library.

add_library(
    service
    BenchmarkCache.cc
    CompilationSession.cc
    CreateAndRunCompilerGymServiceImpl.cc
    Proto.cc
)
target_link_libraries(service service_proto grpc++ magic_enum)
