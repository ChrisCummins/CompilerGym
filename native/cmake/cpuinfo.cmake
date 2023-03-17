# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

include(FetchContent)

fetchcontent_declare(
    cpuinfo
    GIT_REPOSITORY https://github.com/pytorch/cpuinfo
    GIT_TAG de2fa78ebb431db98489e78603e4f77c1f6c5c57
)
fetchcontent_makeavailable(cpuinfo)

# include(ExternalProject)

# externalproject_add(
#     cpuinfo
#     PREFIX "${CMAKE_CURRENT_BINARY_DIR}/cpuinfo"
#     GIT_REPOSITORY "https://github.com/pytorch/cpuinfo.git"
#     GIT_TAG de2fa78ebb431db98489e78603e4f77c1f6c5c57
#     CMAKE_ARGS -DCPUINFO_LIBRARY_TYPE=static
#     USES_TERMINAL_CONFIGURE TRUE
#     USES_TERMINAL_BUILD TRUE
#     USES_TERMINAL_INSTALL TRUE
# )

# include(build_external_cmake_project)
# build_external_cmake_project(
#     NAME cpuinfo
#     SRC_DIR   "${CMAKE_CURRENT_LIST_DIR}/cpuinfo"
# )

# get_cmake_property(_variableNames VARIABLES)
# list (SORT _variableNames)
# foreach (_variableName ${_variableNames})
#     message(STATUS "${_variableName}=${${_variableName}}")
# endforeach()

# find_package(PkgConfig)
# pkg_check_modules(CpuInfo REQUIRED IMPORTED_TARGET libcpuinfo)
# add_library(CpuInfo::cpuinfo ALIAS PkgConfig::CpuInfo)
