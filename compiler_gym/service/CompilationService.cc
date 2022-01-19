// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#include "compiler_gym/service/CompilationService.h"

using grpc::Status;

namespace compiler_gym {

CompilationService::CompilationService(const boost::filesystem::path& workingDirectory)
    : workingDirectory_(workingDirectory) {}

Status CompilationService::init() { return Status::OK; }

Status CompilationService::close() { return Status::OK; }

}  // namespace compiler_gym
