# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Configuration for building an action space from a list of LLVM passes."""
from typing import Dict, Set

# A set of headers that must be included to use the generated pass list.
LLVM_ACTION_INCLUDES: Set[str] = {
    "llvm/LinkAllPasses.h",
    # A handle of coroutine utility passes are not pulled in by the
    # LinkAllPasses.h header.
    "llvm/Transforms/Coroutines.h",
}


def pass_name_to_create_statement(name: str):
    """Translate the name of class that defines a pass into a C++ snippet to
    construct a pointer to an instance of this pass. E.g. given input
    "AddDiscriminatorsPass", return "createAddDiscriminatorsPass()".
    """
    if name in _CREATE_STATEMENT_MAP:
        return _CREATE_STATEMENT_MAP[name]

    create_name = _CREATE_PASS_NAME_MAP.get(name, name)
    return f"llvm::create{create_name}()"


# A mapping form the name of a pass as define in a INITIALIZE_PASS(name, ...)
# macro invocation to a C++ snippet to create an instance of the pass.
_CREATE_STATEMENT_MAP: Dict[str, str] = {
    "EarlyCSEMemSSAPass": "llvm::createEarlyCSEPass(/*UseMemorySSA=*/true)",
}


# A mapping from the name of a pass as defined in a INITIALIZE_PASS(name, ...)
# macro invocation to the name of the pass as defined in the createPASS();
# factory function. Not all passes are named consistently.
_CREATE_PASS_NAME_MAP: Dict[str, str] = {
    "ADCELegacyPass": "AggressiveDCEPass",
    "AddDiscriminatorsLegacyPass": "AddDiscriminatorsPass",
    "AggressiveInstCombinerLegacyPass": "AggressiveInstCombinerPass",
    "AlignmentFromAssumptions": "AlignmentFromAssumptionsPass",
    "Annotation2MetadataLegacy": "Annotation2MetadataLegacyPass",
    "AnnotationRemarksLegacy": "AnnotationRemarksLegacyPass",
    "ArgPromotion": "ArgumentPromotionPass",
    "AssumeSimplifyPassLegacyPass": "AssumeSimplifyPass",
    "BarrierNoop": "BarrierNoopPass",
    "BDCELegacyPass": "BitTrackingDCEPass",
    "BlockExtractor": "BlockExtractorPass",
    "BlockExtractorLegacyPass": "BlockExtractorPass",
    "BreakCriticalEdges": "BreakCriticalEdgesPass",
    "CalledValuePropagationLegacyPass": "CalledValuePropagationPass",
    "CallSiteSplittingLegacyPass": "CallSiteSplittingPass",
    "CanonicalizeAliasesLegacyPass": "CanonicalizeAliasesPass",
    "CanonicalizeFreezeInLoops": "CanonicalizeFreezeInLoopsPass",
    "CFGSimplifyPass": "CFGSimplificationPass",
    "CFGuard": ["CFGuardCheckPass", "CFGuardDispatchPass"],
    "ConstantHoistingLegacyPass": "ConstantHoistingPass",
    "ConstantMergeLegacyPass": "ConstantMergePass",
    "ConstantPropagation": "ConstantPropagationPass",
    "ConstraintElimination": "ConstraintEliminationPass",
    "CoroCleanupLegacy": "CoroCleanupLegacyPass",
    "CoroEarlyLegacy": "CoroEarlyLegacyPass",
    "CoroElideLegacy": "CoroElideLegacyPass",
    "CoroSplitLegacy": "CoroSplitLegacyPass",
    "CorrelatedValuePropagation": "CorrelatedValuePropagationPass",
    "CrossDSOCFI": "CrossDSOCFIPass",
    "DAE": "DeadArgEliminationPass",
    "DataFlowSanitizer": "DataFlowSanitizerPass",
    "DataFlowSanitizerLegacyPass": "DataFlowSanitizerLegacyPassPass",
    "DCELegacyPass": "DeadCodeEliminationPass",
    "DeadInstElimination": "DeadInstEliminationPass",
    "DFAJumpThreadingLegacyPass": "DFAJumpThreadingPass",
    "DivRemPairsLegacyPass": "DivRemPairsPass",
    "DSELegacyPass": "DeadStoreEliminationPass",
    "EarlyCSELegacyPass": "EarlyCSEPass",
    "EarlyCSEMemSSALegacyPass": "EarlyCSEMemSSAPass",
    "EliminateAvailableExternallyLegacyPass": "EliminateAvailableExternallyPass",
    "EntryExitInstrumenter": "EntryExitInstrumenterPass",
    "FixIrreducible": "FixIrreduciblePass",
    "Float2IntLegacyPass": "Float2IntPass",
    "FunctionImportLegacyPass": "FunctionImportPass",
    "FunctionSpecializationLegacyPass": "FunctionSpecializationPass",
    "GCOVProfilerLegacyPass": "GCOVProfilerPass",
    "GlobalDCELegacyPass": "GlobalDCEPass",
    "GlobalOptLegacyPass": "GlobalOptimizerPass",
    "GlobalSplit": "GlobalSplitPass",
    "GuardWideningLegacyPass": "GuardWideningPass",
    "GVNHoistLegacyPass": "GVNHoistPass",
    "GVNLegacyPass": "GVNPass",
    "GVNSinkLegacyPass": "GVNSinkPass",
    "HotColdSplittingLegacyPass": "HotColdSplittingPass",
    "ICPPass": "IPConstantPropagationPass",
    "IndVarSimplifyLegacyPass": "IndVarSimplifyPass",
    "InferAddressSpaces": "InferAddressSpacesPass",
    "InjectTLIMappingsLegacy": "InjectTLIMappingsLegacyPass",
    "InstNamer": "InstructionNamerPass",
    "InstrOrderFileLegacyPass": "InstrOrderFilePass",
    "InternalizeLegacyPass": "InternalizePass",
    "IPCP": "IPConstantPropagationPass",
    "IPSCCPLegacyPass": "IPSCCPPass",
    "IRCELegacyPass": "InductiveRangeCheckEliminationPass",
    "IROutlinerLegacyPass": "IROutlinerPass",
    "JumpThreading": "JumpThreadingPass",
    "LCSSAWrapperPass": "LCSSAPass",
    "LegacyLICMPass": "LICMPass",
    "LegacyLoopSinkPass": "LoopSinkPass",
    "LibCallsShrinkWrapLegacyPass": "LibCallsShrinkWrapPass",
    "LoadStoreVectorizerLegacyPass": "LoadStoreVectorizerPass",
    "LoopDataPrefetchLegacyPass": "LoopDataPrefetchPass",
    "LoopDeletionLegacyPass": "LoopDeletionPass",
    "LoopDistributeLegacy": "LoopDistributePass",
    "LoopExtractor": "LoopExtractorPass",
    "LoopExtractorLegacyPass": "LoopExtractorPass",
    "LoopFlattenLegacyPass": "LoopFlattenPass",
    "LoopFuseLegacy": "LoopFusePass",
    "LoopGuardWideningLegacyPass": "LoopGuardWideningPass",
    "LoopIdiomRecognizeLegacyPass": "LoopIdiomPass",
    "LoopInstSimplifyLegacyPass": "LoopInstSimplifyPass",
    "LoopInterchange": "LoopInterchangePass",
    "LoopInterchangeLegacyPass": "LoopInterchangePass",
    "LoopLoadElimination": "LoopLoadEliminationPass",
    "LoopPredicationLegacyPass": "LoopPredicationPass",
    "LoopReroll": "LoopRerollPass",
    "LoopRerollLegacyPass": "LoopRerollPass",
    "LoopRotateLegacyPass": "LoopRotatePass",
    "LoopSimplify": "LoopSimplifyPass",
    "LoopSimplifyCFGLegacyPass": "LoopSimplifyCFGPass",
    "LoopStrengthReduce": "LoopStrengthReducePass",
    "LoopUnroll": "LoopUnrollPass",
    "LoopUnrollAndJam": "LoopUnrollAndJamPass",
    "LoopUnswitch": "LoopUnswitchPass",
    "LoopVectorize": "LoopVectorizePass",
    "LoopVersioningLegacyPass": "LoopVersioningPass",
    "LoopVersioningLICM": "LoopVersioningLICMPass",
    "LoopVersioningLICMLegacyPass": "LoopVersioningLICMPass",
    "LowerAtomicLegacyPass": "LowerAtomicPass",
    "LowerConstantIntrinsics": "LowerConstantIntrinsicsPass",
    "LowerExpectIntrinsic": "LowerExpectIntrinsicPass",
    "LowerGuardIntrinsicLegacyPass": "LowerGuardIntrinsicPass",
    "LowerInvokeLegacyPass": "LowerInvokePass",
    "LowerMatrixIntrinsicsLegacyPass": "LowerMatrixIntrinsicsPass",
    "LowerMatrixIntrinsicsMinimalLegacyPass": "LowerMatrixIntrinsicsMinimalPass",
    "LowerSwitch": "LowerSwitchPass",
    "LowerSwitchLegacyPass": "LowerSwitchPass",
    "LowerWidenableConditionLegacyPass": "LowerWidenableConditionPass",
    "MemCpyOptLegacyPass": "MemCpyOptPass",
    "MemorySanitizerLegacyPass": "MemorySanitizerLegacyPassPass",
    "MemProfilerLegacyPass": "MemProfilerPass",
    "MergedLoadStoreMotionLegacyPass": "MergedLoadStoreMotionPass",
    "MergeFunctionsLegacyPass": "MergeFunctionsPass",
    "MetaRenamer": "MetaRenamerPass",
    "ModuleAddressSanitizerLegacyPass": "ModuleAddressSanitizerLegacyPassPass",
    "ModuleSanitizerCoverageLegacyPass": "ModuleSanitizerCoverageLegacyPassPass",
    "NameAnonGlobalLegacyPass": "NameAnonGlobalPass",
    "NaryReassociateLegacyPass": "NaryReassociatePass",
    "NewGVNLegacyPass": "NewGVNPass",
    "ObjCARCAPElim": "ObjCARCAPElimPass",
    "ObjCARCContract": "ObjCARCContractPass",
    "ObjCARCContractLegacyPass": "ObjCARCContractPass",
    "ObjCARCExpand": "ObjCARCExpandPass",
    "ObjCARCOpt": "ObjCARCOptPass",
    "ObjCARCOptLegacyPass": "ObjCARCOptPass",
    "PAEval": "PAEvalPass",
    "PartialInlinerLegacyPass": "PartialInliningPass",
    "PartiallyInlineLibCallsLegacyPass": "PartiallyInlineLibCallsPass",
    "PlaceSafepoints": "PlaceSafepointsPass",
    "PostInlineEntryExitInstrumenter": "PostInlineEntryExitInstrumenterPass",
    "PromoteLegacyPass": "PromoteMemoryToRegisterPass",
    "PruneEH": "PruneEHPass",
    "ReassociateLegacyPass": "ReassociatePass",
    "RedundantDbgInstElimination": "RedundantDbgInstEliminationPass",
    "RegToMem": "DemoteRegisterToMemoryPass",
    "ReversePostOrderFunctionAttrsLegacyPass": "ReversePostOrderFunctionAttrsPass",
    "RewriteSymbolsLegacyPass": "RewriteSymbolsPass",
    "SampleProfileLoaderLegacyPass": "SampleProfileLoaderPass",
    "ScalarizerLegacyPass": "ScalarizerPass",
    "SCCPLegacyPass": "SCCPPass",
    "SeparateConstOffsetFromGEP": "SeparateConstOffsetFromGEPPass",
    "SeparateConstOffsetFromGEPLegacyPass": "SeparateConstOffsetFromGEPPass",
    "SimpleInliner": "FunctionInliningPass",
    "SingleLoopExtractor": "SingleLoopExtractorPass",
    "SinkingLegacyPass": "SinkingPass",
    "SLPVectorizer": "SLPVectorizerPass",
    "SpeculativeExecutionLegacyPass": "SpeculativeExecutionPass",
    "SROALegacyPass": "SROAPass",
    "StraightLineStrengthReduce": "StraightLineStrengthReducePass",
    "StraightLineStrengthReduceLegacyPass": "StraightLineStrengthReducePass",
    "StripDeadDebugInfo": "StripDeadDebugInfoPass",
    "StripDeadPrototypesLegacyPass": "StripDeadPrototypesPass",
    "StripDebugDeclare": "StripDebugDeclarePass",
    "StripNonDebugSymbols": "StripNonDebugSymbolsPass",
    "StripNonLineTableDebugInfo": "StripNonLineTableDebugInfoPass",
    "StripSymbols": "StripSymbolsPass",
    "StructurizeCFG": "StructurizeCFGPass",
    "StructurizeCFGLegacyPass": "StructurizeCFGPass",
    "TailCallElim": "TailCallEliminationPass",
    "ThreadSanitizerLegacyPass": "ThreadSanitizerLegacyPassPass",
    "UnifyFunctionExitNodes": "UnifyFunctionExitNodesPass",
    "UnifyFunctionExitNodesLegacyPass": "UnifyFunctionExitNodesPass",
    "UnifyLoopExitsLegacyPass": "UnifyLoopExitsPass",
    "VectorCombineLegacyPass": "VectorCombinePass",
}


def include_pass(pass_: Dict[str, str]) -> bool:
    """Determine whether the pass should be included in the generated C++ sources."""
    if pass_["class_name"] in _EXCLUDED_PASSES:
        return False

    return (
        "lib/Transforms" in pass_["source"] or f"Targets/{_TARGET}" in pass_["source"]
    )


# A list of pass names that should be excluded from the action space.
_EXCLUDED_PASSES: Set[str] = {
    # Irrelevant garbage collection passes.
    "StripGCRelocates",
    "PlaceBackedgeSafepointsImpl",
    "PlaceSafepointsPass",
    "RewriteStatepointsForGclegacyPass",
    # Irrelevant Objective-C Automatic Reference Counting passes.
    "ObjCARCAAWrapperPass",
    "ObjCARCAPElim",
    "ObjCARCAPElimPass",
    "ObjCARCContractPass",
    "ObjCARCExpandPass",
    "ObjCARCOptPass",
    # Doesn't use legacy pass constructor API, or requires additional
    # constructor arguments that are not available.
    "WholeProgramDevirt",
    "MakeGuardsExplicitLegacyPass",
    "LowerTypeTests",
    # Unneeded debugging passes.
    "WriteThinLTOBitcode",
    "PredicateInfoPrinterLegacyPass",
    "WarnMissedTransformationsLegacy",
    "DAH",  # Bugpoint only.
    "MetaRenamerPass",
    "PAEvalPass",
    "BarrierNoop",  # Used for debugging pass manager.
    "StripNonLineTableDebugInfoPass",  # Debug stripping.
    "StripDeadDebugInfoPass",  # Debug stripping.
    "LoopExtractorPass",  # Pulls out loops into functions. Changes semantics.
    "SingleLoopExtractorPass",  # Pulls out loops into functions. Changes semantics.
    "BlockExtractorPass",  # Pulls out blocks into functions. Changes semantics.
    # Unwanted instrumentation passes.
    "BoundsCheckingLegacyPass",  # Inserts traps on illegal access. Changes semantics.
    "ASanGlobalsMetadataWrapperPass",
    "AddressSanitizerLegacyPass",
    "HWAddressSanitizerLegacyPass",
    "SampleProfileLoaderPass",
    "MemorySanitizerLegacyPassPass",
    "ThreadSanitizerLegacyPassPass",
    "ModuleAddressSanitizerLegacyPassPass",
    "FunctionImportPass",
    "DataFlowSanitizerPass",
    "InstrOrderFilePass",
    "PostInlineEntryExitInstrumenter",
    # Profile-guided optimization or profiling.
    "PGOIndirectCallPromotionLegacyPass",
    "PGOInstrumentationUseLegacyPass",
    "PGOInstrumentationGenCreateVarLegacyPass",
    "PGOInstrumentationGenLegacyPass",
    "PGOInstrumentationUseLegacyPass",
    "PGOMemOpsizeOptLegacyPass",
    "PgomemOpsizeOptLegacyPass",
    "InstrProfilingLegacyPass",
    "ControlHeightReductionLegacyPass",
    # Unneeded symbol rewriting pass.
    "RewriteSymbolsPass",
    # Microsoft's Control Flow Guard checks on Windows targets.
    # https://llvm.org/doxygen/CFGuard_8cpp.html
    "CFGuardCheckPass",
    "CFGuardDispatchPass",
    # We don't want to change the visibility of symbols.
    "InternalizePass",
    # NOTE(github.com/facebookresearch/CompilerGym/issues/103): The
    # -structurizecg has been found to break the semantics of cBench benchmarks
    # ghostscript and tiff2bw.
    "StructurizeCFGPass",
    # NOTE(github.com/facebookresearch/CompilerGym/issues/46): The -gvn-sink
    # pass has been found to produce different states when run multiple times
    # on the same input.
    "GVNSinkPass",
    # LLVM 13.0.1:
    "AssumeBuilderPassLegacyPass",
    "ForceFunctionAttrsLegacyPass",
    "InferFunctionAttrsLegacyPass",
    "LoopVersioningPass",  # TODO(cummins): Link error using LLVM 13.0.1
    "MemProfilerPass",
    "ModuleMemProfilerLegacyPass",
    "ModuleSanitizerCoverageLegacyPassPass",
    "PostOrderFunctionAttrsLegacyPass",
    "PostOrderFunctionAttrsLegacyPass",
    "RegToMemLegacy",
    "SimpleLoopUnswitchLegacyPass",
    "StripGCRelocatesLegacy",
    # TODO(cummins): This pass hangs on LLVM 13.0.1:
    "AttributorCGSCCLegacyPass",
}

# The name of the LLVM target to extract architecture-specific transforms for.
_TARGET = "X86"
