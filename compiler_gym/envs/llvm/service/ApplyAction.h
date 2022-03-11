// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#pragma once

#include "ActionSpace.h"
#include "llvm/Config/llvm-config.h"
#include "llvm/IR/Module.h"
#include "llvm/Pass.h"

#if LLVM_VERSION_MAJOR == 10
#include "compiler_gym/envs/llvm/service/passes/ActionHeaders.h"
#include "compiler_gym/envs/llvm/service/passes/ActionSwitch.h"
#elif LLVM_VERSION_MAJOR == 13
#include "compiler_gym/envs/llvm/service/passes/13.0.1/ActionHeader.h"
#include "compiler_gym/envs/llvm/service/passes/13.0.1/ActionPassBuilder.h"
#include "llvm/Passes/PassBuilder.h"
#else
#error "Unknown LLVM version: " LLVM_VERSION_MAJOR
#endif

#include <grpcpp/grpcpp.h>

namespace compiler_gym::llvm_service {

/**
 * Run the requested action.
 *
 * @param action An action to apply.
 * @param actionHadNoEffect Set to true if LLVM reported that any passes that
 *    were run made no modifications to the module.
 * @return `OK` on success.
 */
[[nodiscard]] grpc::Status applyPassAction(LlvmAction action, llvm::Module& module,
                                           bool& actionHadNoEffect);

}  // namespace compiler_gym::llvm_service
