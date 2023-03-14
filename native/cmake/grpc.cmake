# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

include(FetchContent)

fetchcontent_declare(
    gRPC
    GIT_REPOSITORY https://github.com/grpc/grpc
    GIT_TAG v1.52.1
)
set(FETCHCONTENT_QUIET OFF)
fetchcontent_makeavailable(gRPC)

# Make protobuf generation rules available.
set(protobuf_MODULE_COMPATIBLE TRUE)
find_package(Protobuf REQUIRED)
set(PROTO_INCLUDES
    ${CMAKE_INSTALL_PREFIX}/include
    ${CMAKE_BINARY_DIR}/_deps/grpc-src/third_party/protobuf/src/
)
