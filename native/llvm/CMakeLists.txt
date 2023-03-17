# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

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
    RunService.cc
)

target_include_directories(
    llvm_env_lib
    PUBLIC ${Boost_INCLUDE_DIR} ${LLVM_INCLUDE_DIRS}
)
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
llvm_map_components_to_libnames(llvm_env_lib support core bitwriter irreader transformutils ipo coroutines objcarcopts target codegen x86codegen x86asmparser)
