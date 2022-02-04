// Copyright (c) Facebook, Inc. and its affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.
#include <gflags/gflags.h>
#include <glog/logging.h>
#include <grpcpp/grpcpp.h>

#include <deque>
#include <future>
#include <string>

#include "boost/filesystem.hpp"
#include "compiler_gym/service/proto/BenchmarkBroker.grpc.pb.h"
#include "compiler_gym/service/proto/BenchmarkBroker.pb.h"

DEFINE_string(
    working_dir, "",
    "The working directory to use. Must be an existing directory with write permissions.");
DEFINE_string(port, "0",
              "The port to listen on. If 0, an unused port will be selected. The selected port is "
              "written to <working_dir>/port.txt.");

// Increase maximum message size beyond the 4MB default as inbound message
// may be larger (e.g., in the case of IR strings).
constexpr size_t kMaxMessageSizeInBytes = 512 * 1024 * 1024;

namespace compiler_gym::runtime {

struct BenchmarkWithId {
  int id;
  Benchmark benchmark;
};

class BenchmarkBrokerService final : public compiler_gym::BenchmarkBroker::Service {
 public:
  BenchmarkBrokerService() : nextId_(0){};

  grpc::Status GetBenchmark(grpc::ServerContext* context, const GetBenchmarkRequest* request,
                            GetBenchmarkReply* reply) final override;

  grpc::Status PutBenchmark(grpc::ServerContext* context, const PutBenchmarkRequest* request,
                            PutBenchmarkReply* reply) final override;

  grpc::Status ClientSwapBenchmark(grpc::ServerContext* context,
                                   const ClientSwapBenchmarkRequest* request,
                                   ClientSwapBenchmarkReply* reply) final override;

 private:
  std::deque<BenchmarkWithId> q_;
  int nextId_;
};

grpc::Status BenchmarkBrokerService::GetBenchmark(grpc::ServerContext* context,
                                                  const GetBenchmarkRequest* request,
                                                  GetBenchmarkReply* reply) {
  return grpc::Status::OK;
}

grpc::Status BenchmarkBrokerService::PutBenchmark(grpc::ServerContext* context,
                                                  const PutBenchmarkRequest* request,
                                                  PutBenchmarkReply* reply) {
  return grpc::Status::OK;
}

grpc::Status BenchmarkBrokerService::ClientSwapBenchmark(grpc::ServerContext* context,
                                                         const ClientSwapBenchmarkRequest* request,
                                                         ClientSwapBenchmarkReply* reply) {
  return grpc::Status::OK;
}

}  // namespace compiler_gym::runtime

int main(int argc, char** argv) {
  gflags::SetUsageMessage("...");

  // Parse the command line arguments and die if any are unrecognized.
  gflags::ParseCommandLineFlags(&argc, &argv, /*remove_flags=*/true);
  if (argc > 1) {
    std::cerr << "ERROR: unknown command line argument '" << argv[1] << '\'';
    exit(1);
  }

  FLAGS_alsologtostderr = true;
  google::InitGoogleLogging(argv[0]);

  compiler_gym::runtime::BenchmarkBrokerService service;

  grpc::ServerBuilder builder;
  builder.RegisterService(&service);

  builder.SetMaxMessageSize(kMaxMessageSizeInBytes);

  // Start a channel on the port.
  int port;
  std::string serverAddress = "0.0.0.0:" + (FLAGS_port.empty() ? "0" : FLAGS_port);
  builder.AddListeningPort(serverAddress, grpc::InsecureServerCredentials(), &port);

  // Start the server.
  std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
  CHECK(server) << "Failed to build RPC service";

  LOG(INFO) << "Service listening on port " << port;

  server->Wait();
}
