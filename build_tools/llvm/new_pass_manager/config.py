from typing import Set

# A list of pass names that should be excluded from the action space.
EXCLUDED_PASS_CLASSES: Set[str] = {
    "AddressSanitizerPass",  # Unwanted instrumentation pass.
    "BlockExtractorPass",  # Program rewriter.
    "BoundsCheckingPass",  # Instrumentation pass.
    "CGProfilePass",  # Unwanted instrumentation pass.
    "ControlHeightReductionPass",  # Profile-guided optimization pass.
    "DataFlowSanitizerPass",  # Unwanted instrumentation pass.
    "GCOVProfilerPass",  # Unwanted instrumentation pass.
    "HelloWorldPass",  # Debugging pass.
    "HWAddressSanitizerPass",  # Unwanted instrumentation pass.
    "InstrOrderFilePass",  # Unwanted instrumentation pass.
    "InstrProfiling",  # Profile-guided optimization pass.
    "InternalizePass",  # Unsafe for compilation.
    "LoopExtractorPass",  # Program rewriter.
    "LoopFusePass",  # FIXME(cummins): Not yet fully tested.
    "LowerAtomicPass",  # Unsafe rewrite, breaks thread safety.
    "LowerInvokePass",  # Unsafe rewrite, changes exception handling semantics.
    "MemProfilerPass",  # Unwanted instrumentation pass.
    "MetaRenamerPass",  # Unwanted rewriter.
    "ModuleAddressSanitizerPass",  # Unwanted instrumentation pass.
    "ModuleMemProfilerPass",  # Unwanted instrumentation pass.
    "ModuleSanitizerCoveragePass",  # Unwanted instrumentation pass.
    "ObjCARCAPElimPass",  # Irrelevant Objective-C Reference Counting pass.
    "ObjCARCContractPass",  # Irrelevant Objective-C Reference Counting pass.
    "ObjCARCExpandPass",  # Irrelevant Objective-C Reference Counting pass.
    "ObjCARCOptPass",  # Irrelevant Objective-C Reference Counting pass.
    "PGOIndirectCallPromotion",  # Profile-guided optimization pass.
    "PGOInstrumentationGen",  # Profile-guided optimization pass.
    "PGOInstrumentationGenCreateVar",  # Profile-guided optimization pass.
    "PGOInstrumentationUse",  # Profile-guided optimization pass.
    "PGOMemOPSizeOpt",  # Profile-guided optimization pass.
    "PoisonCheckingPass",  # Unwanted instrumentation pass.
    "RewriteStatepointsForGC",  # Irrelevant garbage collection pass.
    "RewriteSymbolPass",  # Unwanted rewriter.
    "SampleProfileLoaderPass",  # Profile-guided optimization pass.
    "StripGCRelocates",  # Irrelevant garbage collection pass.o
    "ThreadSanitizerPass",  # Unwanted instrumentation pass.
    "WarnMissedTransformationsPass",  # Unneeded debugging pass.
}
