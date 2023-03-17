# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Protocol buffers.

set(program_graph_proto_srcs
    "${generated_header_dir}/programl/program_graph.pb.cc"
    "${generated_header_dir}/programl/util.pb.cc"
    "${generated_header_dir}/programl/features.pb.cc"
)
set(program_graph_proto_hdrs
    "${generated_header_dir}/programl/program_graph.pb.h"
    "${generated_header_dir}/programl/util.pb.h"
    "${generated_header_dir}/programl/features.pb.h"
)

add_custom_command(
    OUTPUT ${program_graph_proto_srcs} ${program_graph_proto_hdrs}
    COMMAND ${PROTOC}
    ARGS
        --cpp_out
        "${generated_header_dir}/programl"
        -I
        ${CMAKE_CURRENT_LIST_DIR}
        ${CMAKE_CURRENT_LIST_DIR}/program_graph.proto
        ${CMAKE_CURRENT_LIST_DIR}/util.proto
        ${CMAKE_CURRENT_LIST_DIR}/features.proto
    DEPENDS program_graph.proto util.proto features.proto
)

add_library(
    programl_proto
    ${program_graph_proto_srcs}
    ${program_graph_proto_hdrs}
)
target_link_libraries(
    programl_proto
    grpc++
    protobuf::libprotobuf
    gRPC::grpc++_reflection
)
