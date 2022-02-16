// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#pragma once

#include "compiler_gym/service/proto/compiler_gym_service.pb.h"

namespace compiler_gym::llvm_service {

// TODO(github.com/facebookresearch/CompilerGym/issues/568):
#ifndef LLVM_VERSION_MAJOR
#define LLVM_VERSION_MAJOR 10
#endif

#if LLVM_VERSION_MAJOR == 10
#include "compiler_gym/envs/llvm/service/passes/ActionEnum.h"
#elif LLVM_VERSION_MAJOR == 13
#include "compiler_gym/envs/llvm/service/passes/13.0.1/ActionEnum.h"
#else
#error "Unknown LLVM version: " LLVM_VERSION_MAJOR
#endif

/**
 * The available action spaces for LLVM.
 *
 * \note Implementation housekeeping rules - to add a new action space:
 *   1. Add a new entry to this LlvmActionSpace enum.
 *   2. Add a new switch case to getLlvmActionSpaceList() to return the
 *      ActionSpace.
 *   3. Add a new switch case to LlvmSession::step() to compute
 *      the actual action.
 *   4. Run `bazel test //compiler_gym/...` and update the newly failing tests.
 */
enum class LlvmActionSpace {
  PASSES_ALL,  ///< The full set of transform passes for LLVM.
};

/**
 * Get the list of LLVM action spaces.
 *
 * @return A list of ActionSpace instances.
 */
std::vector<ActionSpace> getLlvmActionSpaceList();

}  // namespace compiler_gym::llvm_service
