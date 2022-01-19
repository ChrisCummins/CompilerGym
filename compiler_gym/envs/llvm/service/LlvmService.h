// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#pragma once

#include <grpcpp/grpcpp.h>

#include "compiler_gym/service/CompilationService.h"

namespace compiler_gym::llvm_service {

class LlvmCompilationService : CompilationService {
 public:
  [[nodiscard]] grpc::Status init() final override;

  [[nodiscard]] grpc::Status close() final override;
};

}  // namespace compiler_gym::llvm_service
