# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

llvm_map_components_to_libnames(
    llvm_libs
    support
    core
    bitwriter
    irreader
    transformutils
    ipo
    coroutines
    objcarcopts
    target
    codegen
    x86codegen
    x86asmparser
)

add_executable(llvm_env_service RunService.cc)
target_link_libraries(
    llvm_env_service
    llvm_env_lib
    gflags
    glog
    ${llvm_libs}
    ${PROTOBUF_LDFLAGS}
    ${GRPC_LDFLAGS}
    ${GRPCPP_LDFLAGS}
)

add_library(
    llvm_env_lib
    ActionSpace.cc
    Autophase.cc
    Benchmark.cc
    BenchmarkDynamicConfig.cc
    BenchmarkFactory.cc
    Cost.cc
    InstCount.cc
    LlvmSession.cc
    Observation.cc
    ObservationSpaces.cc
)
target_include_directories(
    llvm_env_lib
    PUBLIC ${Boost_INCLUDE_DIR} ${LLVM_INCLUDE_DIRS}
)
target_link_libraries(
    llvm_env_lib
    boost_filesystem
    cpuinfo_internals
    fmt::fmt
    llvm_lex
    nlohmann_json::nlohmann_json
    programl
    service
    service_proto
    util
    ${llvm_libs}
    # TODO(cummins): protobuf and grpc flags
)

add_subdirectory(lex)
