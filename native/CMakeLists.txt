# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

cmake_minimum_required(VERSION 3.22)
project(CompilerGym)

set(COMPILER_GYM_VERSION 0.3.0)

include(ExternalProject)

set(CMAKE_CXX_STANDARD 17)

include(cmake/boost.cmake)
include(cmake/fmt.cmake)
include(cmake/grpc.cmake)
include(cmake/llvm.cmake)
include(cmake/magic_enum.cmake)

# Add the project headers to the default include paths
set(generated_header_dir ${CMAKE_BINARY_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${generated_header_dir})

add_subdirectory(lib)
add_subdirectory(llvm)
