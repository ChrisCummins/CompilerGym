# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""The :code:`compiler_gym.wrappers` module provides a set of classes that can
be used to transform an environment in a modular way.

For example:

    >>> env = compiler_gym.make("llvm-v0")
    >>> env = TimeLimit(env, n=10)
    >>> env = CycleOverBenchmarks(
    ...     env,
    ...     benchmarks=[
    ...         "benchmark://cbench-v1/crc32",
    ...         "benchmark://cbench-v1/qsort",
    ...     ],
    ... )

.. warning::

    CompilerGym environments are incompatible with the `OpenAI Gym wrappers
    <https://github.com/openai/gym/tree/master/gym/wrappers>`_. This is because
    CompilerGym extends the environment API with additional arguments and
    methods. You must use the wrappers from this module when wrapping
    CompilerGym environments. We provide a set of base wrappers that are
    equivalent to those in OpenAI Gym that you can use to write your own
    wrappers.
"""
from compiler_gym.wrappers.commandline import (
    CommandlineWithTerminalAction,
    ConstrainedCommandline,
)
from compiler_gym.wrappers.core import (
    ActionWrapper,
    CompilerEnvWrapper,
    ObservationWrapper,
    RewardWrapper,
)
from compiler_gym.wrappers.datasets import (
    CycleOverBenchmarks,
    CycleOverBenchmarksIterator,
    IterateOverBenchmarks,
    RandomOrderBenchmarks,
)
from compiler_gym.wrappers.llvm import RuntimePointEstimateReward
from compiler_gym.wrappers.time_limit import TimeLimit

from .validation import ValidateBenchmarkAfterEveryStep

__all__ = [
    "ActionWrapper",
    "CommandlineWithTerminalAction",
    "CompilerEnvWrapper",
    "ConstrainedCommandline",
    "CycleOverBenchmarks",
    "CycleOverBenchmarksIterator",
    "IterateOverBenchmarks",
    "ObservationWrapper",
    "RandomOrderBenchmarks",
    "RewardWrapper",
    "RuntimePointEstimateReward",
    "TimeLimit",
    "ValidateBenchmarkAfterEveryStep",
]
