# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Build generated files from a list of passes.

This script reads from stdin a list of passes (as generated by
extract_passes_from_sources.py) and generates files so that these passes can be
used as an action space by the LLVM environment.

Usage:

    $ make_action_space_genfiles.py <output-directory> < <pass-list>

The following files are generated:

<outdir>/ActionHeaders.h
------------------------
    Example:

        #pragma once #include "llvm/LinkAllPasses.h" #include
        "llvm/Transforms/AggressiveInstCombine/AggressiveInstCombine.h" ...

    This file includes the set of LLVM headers that must be included to use the
    passes.

<outdir>/ActionEnum.h
---------------------
    Example:

        enum class LlvmAction {
          ADD_DISCRIMINATORS_PASS, AGGRESSIVE_DCEPASS, ...
        }

    This defines an enum that names all of the passes.

<outdir>/ActionSwitch.h
-----------------------
    Example:

        #define HANDLE_ACTION(action, handlePass) \
          switch (action) {  \
            case LlvmAction::ADD_DISCRIMINATORS_PASS: \
              handlePass(llvm::createAddDiscriminatorsPass()); \
                break; \
            case LlvmAction::AGGRESSIVE_DCEPASS: \
              handlePass(llvm::createAggressiveDCEPass()); \
                break; \
          ...
        }

    To use the generated switch, call the HANDLE_ACTION() macro using an
    LlvmAction enum value and a handlePass function which accepts a pass
    instance as input.

<outdir>/flags.txt
-------------------------
    Example:

        -add-discriminators -adce ...

    A list of names for each pass.

<outdir>/flag_descriptions.txt
---------------------------------
    Example:

        Add DWARF path discriminators Aggressive Dead Code Elimination ...

    A list of descriptions of each pass.
"""
import json
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

from absl import app, flags, logging
from llvm_pass import Pass
from load_config import load_config

flags.DEFINE_string("outdir", "genfiles", "Output directory")

FLAGS = flags.FLAGS

header = """\
Copyright (c) Facebook, Inc. and its affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.

This file was automatically generated by make_action_space_sources.py.
"""
cxx_header = "\n".join(f"// {line}" for line in header.splitlines())
py_header = "\n".join(f"# {line}" for line in header.splitlines())


def enumname(pass_: Pass) -> str:
    return pass_.flag[1:].replace("-", "_").upper()


def process_pass(pass_, headers, enum_f, switch_f):
    """Extract and process transform passes in header."""
    if pass_.header:
        # Strip a leading "include/" from the header path.
        header = pass_.header
        if header.startswith("include/"):
            header = header[len("include/") :]
        headers.add(header)

    # The name of the pass in UPPER_PASCAL_CASE.
    print(f"  {enumname(pass_)},", file=enum_f)
    print(f"    case LlvmAction::{enumname(pass_)}: \\", file=switch_f)
    print(f"      handlePass({pass_.create_statement}()); \\", file=switch_f)
    print("      break; \\", file=switch_f)


@contextmanager
def write(path: Path):
    with open(path, "w", encoding="utf-8") as f:
        if path.suffix == ".py":
            print(py_header, file=f)
        elif path.suffix == ".h" or path.suffix == ".cc" or path.suffix == ".inc":
            print(cxx_header, file=f)
        else:
            print(header, file=f)

        yield f
    logging.info("Wrote %s", path)


def make_action_sources(config, passes: Iterable[Pass], outdir: Path):
    """Generate the enum and switch content."""
    headers = set(config.LLVM_ACTION_INCLUDES)

    passes = sorted(list(passes), key=lambda p: p.class_name)

    with write(outdir / "ActionSwitch.h") as switch_f, write(
        outdir / "ActionEnum.h"
    ) as enum_f:
        print(file=switch_f)
        print(file=enum_f)
        print("enum class LlvmAction {", file=enum_f)
        print("#define HANDLE_ACTION(action, handlePass) \\", file=switch_f)
        print("  switch (action) {  \\", file=switch_f)
        for pass_ in passes:
            process_pass(pass_, headers, enum_f, switch_f)
        print("};", file=enum_f)
        print("  }", file=switch_f)

    with write(outdir / "ActionHeader.h") as f:
        print(file=f)
        print("#pragma once\n", file=f)
        for header_ in sorted(headers):
            print(f'#include "{header_}"', file=f)

    with write(outdir / "actions.py") as f:
        print("from enum import Enum\n", file=f)
        print("class actions(Enum):", file=f)
        for pass_ in passes:
            print(f"    {enumname(pass_)} = {pass_._asdict()}", file=f)


def main(argv):
    """Main entry point."""
    assert len(argv) == 1, f"Unknown flags: {argv[1:]}"

    outdir = Path(FLAGS.outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    passes = [Pass(**ln) for ln in json.load(sys.stdin)]
    make_action_sources(load_config(), passes, outdir)


if __name__ == "__main__":
    app.run(main)
