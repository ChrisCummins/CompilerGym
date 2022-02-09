#pragma once
#include "llvm/LinkAllPasses.h"
#include "llvm/Transforms/Coroutines.h"
#include "llvm/Transforms/IPO.h"
#include "llvm/Transforms/Instrumentation.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Utils.h"

namespace llvm {
FunctionPass* createEarlyCSEMemSSAPass() { return createEarlyCSEPass(/*UseMemorySSA=*/true); }
}  // namespace llvm
