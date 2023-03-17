# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

add_library(llvm_lex LLLexer.cc llvm_lexer_token_info.cc)

target_include_directories(llvm_env_lib PUBLIC ${LLVM_INCLUDE_DIRS})
target_link_libraries(
    llvm_env_lib
    service
    service_proto
    boost_filesystem
    grpc++
    fmt::fmt
    nlohmann_json::nlohmann_json
    cpuinfo_internals
    programl_proto
    protobuf::libprotobuf
)
llvm_map_components_to_libnames(llvm_lex core support bitwriter)
