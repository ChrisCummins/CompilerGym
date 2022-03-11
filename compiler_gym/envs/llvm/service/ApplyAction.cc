#include "ApplyAction.h"

using grpc::Status;

namespace compiler_gym::llvm_service {

Status applyPassAction(LlvmAction action, llvm::Module& module, bool& actionHadNoEffect) {
#if LLVM_VERSION_MAJOR == 10

#ifdef EXPERIMENTAL_UNSTABLE_GVN_SINK_PASS
  // NOTE(https://github.com/facebookresearch/CompilerGym/issues/46): The
  // -gvn-sink pass has been found to have nondeterministic behavior so has
  // been disabled in compiler_gym/envs/llvm/service/pass/config.py. Invoking
  // the command line was found to produce more stable results.
  if (action == LlvmAction::GVNSINK_PASS) {
    RETURN_IF_ERROR(runOptWithArgs({"-gvn-sink"}));
    actionHadNoEffect = true;
    return Status::OK;
  }
#endif

// Use the generated HANDLE_PASS() switch statement to dispatch to runPass().
#define HANDLE_PASS(pass) actionHadNoEffect = !runPass(pass);
  HANDLE_ACTION(action, HANDLE_PASS)
#undef HANDLE_PASS

#elif LLVM_VERSION_MAJOR == 13
  llvm::LoopAnalysisManager LAM;
  llvm::FunctionAnalysisManager FAM;
  llvm::CGSCCAnalysisManager CGAM;
  llvm::PassBuilder PB;
  llvm::ModuleAnalysisManager module_analysis_manager;

  PB.registerModuleAnalyses(module_analysis_manager);
  PB.registerCGSCCAnalyses(CGAM);
  PB.registerFunctionAnalyses(FAM);
  PB.registerLoopAnalyses(LAM);
  PB.crossRegisterProxies(LAM, FAM, CGAM, module_analysis_manager);

  llvm::ModulePassManager pass_manager = createActionPipeline(action);

  pass_manager.run(module, module_analysis_manager);
#else
#error "Unknown LLVM version: " LLVM_VERSION_MAJOR
#endif

  return Status::OK;
}

}  // namespace compiler_gym::llvm_service
