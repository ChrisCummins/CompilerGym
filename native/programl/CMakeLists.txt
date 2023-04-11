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

llvm_map_components_to_libnames(
    llvm_libs
    support
    core
    bitwriter
    irreader
    ipo
    coroutines
    objcarcopts
    target
    codegen
    x86codegen
    x86asmparser
)

add_library(
    programl
    graph/features.cc
    graph/program_graph_builder.cc
    graph/format/node_link_graph.cc
    ir/llvm/llvm.cc
    ir/llvm/internal/program_graph_builder.cc
    ir/llvm/internal/program_graph_builder_pass.cc
    ir/llvm/internal/text_encoder.cc
    ${program_graph_proto_srcs}
    ${program_graph_proto_hdrs}
)
target_link_libraries(
    programl
    labm8
    ${llvm_libs}
    ${PROTOBUF_LDFLAGS}
    ${GRPC_LDFLAGS}
    ${GRPCPP_LDFLAGS}
    -Wl,-rpath,${GRPC_LIBDIR}
)
target_include_directories(programl PUBLIC ${LLVM_INCLUDE_DIRS})
target_compile_options(
    programl
    PRIVATE
        # NOTE(cummins): Workaround for libprotobuf bug.
        -DNDEBUG
)
