// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#include "compiler_gym/envs/llvm/service/LlvmService.h"

#include "compiler_gym/envs/llvm/service/BenchmarkFactory.h"

using grpc::Status;

namespace compiler_gym::llvm_service {

Status LlvmCompilationService::init() { return Status::OK; }

Status LlvmCompilationService::close() {
  // BenchmarkFactory::getSingleton(workingDirectory()).close();
  return Status::OK;
}

}  // namespace compiler_gym::llvm_service
