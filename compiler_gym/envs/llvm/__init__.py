# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Register the LLVM environments."""
import os
from itertools import product

# from compiler_gym.envs.llvm.compute_observation import compute_observation
from compiler_gym.envs.llvm.llvm_benchmark import (
    ClangInvocation,
    get_system_library_flags,
    make_benchmark,
    make_benchmark_from_clang_command_line,
)
from compiler_gym.envs.llvm.llvm_env import LlvmEnv
from compiler_gym.envs.llvm.specs import observation_spaces, reward_spaces
from compiler_gym.service import ConnectionOpts
from compiler_gym.util.registration import register
from compiler_gym.util.runfiles_path import runfiles_path

__all__ = [
    "ClangInvocation",
    # "compute_observation",
    "get_system_library_flags",
    "LLVM_SERVICE_BINARY",
    "LlvmEnv",
    "make_benchmark",
    "make_benchmark_from_clang_command_line",
    "observation_spaces",
    "reward_spaces",
]

LLVM_SERVICE_BINARY = runfiles_path(
    "compiler_gym/envs/llvm/service/compiler_gym-llvm-service"
)


def _register_llvm_gym_service():
    """Register an environment for each combination of LLVM
    observation/reward/benchmark."""
    observation_spaces = {"autophase": "Autophase", "ir": "Ir"}
    reward_spaces = {"ic": "IrInstructionCountOz", "codesize": "ObjectTextSizeOz"}

    register(
        id="llvm-v0",
        entry_point="compiler_gym.envs.llvm:LlvmEnv",
        kwargs={
            "service": LLVM_SERVICE_BINARY,
            "connection_settings": ConnectionOpts(
                script_env={
                    # TODO(cummins): Horrible hack to build against custom LLVM.
                    "LD_PRELOAD": os.path.expanduser("~/tmp/libstdc++.so.6")
                }
            ),
        },
    )

    for reward_space in reward_spaces:
        register(
            id=f"llvm-{reward_space}-v0",
            entry_point="compiler_gym.envs.llvm:LlvmEnv",
            kwargs={
                "service": LLVM_SERVICE_BINARY,
                "reward_space": reward_spaces[reward_space],
            },
        )

    for observation_space, reward_space in product(observation_spaces, reward_spaces):
        register(
            id=f"llvm-{observation_space}-{reward_space}-v0",
            entry_point="compiler_gym.envs.llvm:LlvmEnv",
            kwargs={
                "service": LLVM_SERVICE_BINARY,
                "observation_space": observation_spaces[observation_space],
                "reward_space": reward_spaces[reward_space],
            },
        )


_register_llvm_gym_service()
