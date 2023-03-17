# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

add_executable(llvm_env_service RunService.cc)
target_link_options(
    llvm_env_service
    PUBLIC
        -L/private/home/cummins/.conda/envs/compiler_gym/lib # TODO: ${gRPC_DIR}/../
        -lprotobuf
)
llvm_map_components_to_libnames(llvm_libs support core bitwriter irreader transformutils ipo coroutines objcarcopts target codegen x86codegen x86asmparser)
target_link_libraries(
    llvm_env_service
    llvm_env_lib
    protobuf::libprotobuf
    ${llvm_libs}
    ${Protobuf_LIBRARY}
    ${Protobuf_LIBRARIES}
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
    Observation.cc
    ObservationSpaces.cc
)
target_include_directories(
    llvm_env_lib
    PUBLIC ${Boost_INCLUDE_DIR} ${LLVM_INCLUDE_DIRS}
)
llvm_map_components_to_libnames(llvm_libs support core bitwriter irreader transformutils ipo coroutines objcarcopts target codegen x86codegen x86asmparser)
target_link_libraries(
    llvm_env_lib
    boost_filesystem
    cpuinfo_internals
    fmt::fmt
    grpc++
    llvm_lex
    nlohmann_json::nlohmann_json
    programl_proto
    protobuf::libprotobuf
    service
    service_proto
    ${llvm_libs}
)

add_subdirectory(lex)
