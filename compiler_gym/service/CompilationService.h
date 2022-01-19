// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#pragma once

#include <grpcpp/grpcpp.h>

#include <optional>
#include <vector>

#include "boost/filesystem.hpp"
#include "compiler_gym/service/proto/compiler_gym_service.pb.h"

namespace compiler_gym {

class CompilationService {
 public:
  [[nodiscard]] virtual grpc::Status init();

  [[nodiscard]] virtual grpc::Status close();

  CompilationService(const boost::filesystem::path& workingDirectory);

  virtual ~CompilationService() = default;

 protected:
  /**
   * Get the working directory.
   *
   * The working directory is a local filesystem directory that this
   * CompilationSession can use to store temporary files such as build
   * artifacts. The directory exists.
   *
   * \note If you need to store very large files for a CompilationSession then
   *    consider using an alternate filesystem path as, when possible, an
   *    in-memory filesystem will be used for the working directory.
   *
   * \note A single working directory may be shared by multiple
   *    CompilationSession instances. Do not assume that you have exclusive
   *    access.
   *
   * @return A path.
   */
  inline const boost::filesystem::path& workingDirectory() { return workingDirectory_; }

 private:
  const boost::filesystem::path workingDirectory_;
};

}  // namespace compiler_gym
