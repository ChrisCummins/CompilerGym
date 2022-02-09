#!/usr/bin/env bash
#
# TODO(cummins): DO NOT MERGE! This script is for testing and debugging
# purposes. Use this script to swap out the LLVM binaries downloaded by the
# CompilerGym environment for another set of binaries.
#
# Usage:
#
#     ./packaging/hot_swap_llvm_binaries.sh /path/to/compiler_gym/clang /path/to/new/llvm/bins
#
# To compute the first argument run the following command and copy it's output:
#
#     $ python -c 'from compiler_gym.third_party import llvm; print(llvm.clang_path())'
#     /dev/shm/compiler_gym_cec/site_data/llvm-v0/bin/clang
#
# The second argument should be the directory containing the llvm binaries you
# wish to use instead, e.g. ~/src/llvm-project-13.0.1.src/install/bin.
#
# To test whether this script worked, run:
#
#     $ python -c 'import compiler_gym; env = compiler_gym.make("llvm-v0"); env.reset(); env.close(); print("It works!")'
set -eu
chmod 755 "$1"/*

for bin in $(find "$1" -type f); do
  dst="$(realpath $bin)"
  src="$2/$(basename $dst)"

  if [[ ! -f "$src" ]]; then
    echo "fatal: File not found $src"
  fi

  cp -Lv "$src" "$dst"
done
