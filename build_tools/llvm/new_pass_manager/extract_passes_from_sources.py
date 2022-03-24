# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Extract a list of passes from LLVM.

Prints information about the passes as JSON to stdout.

Usage:

    $ python extract_passes_from_llvm_source_tree.py \
        --llvm_root=/path/to/llvm/install/dir \
        > passes.json
"""
import concurrent
import json
import os
import shlex
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from multiprocessing import cpu_count
from pathlib import Path
from typing import Dict, Iterable, List

import clang
import clang.cindex as cl
from absl import app, flags, logging
from clang.cindex import CursorKind

flags.DEFINE_string("llvm_root", "", "Path to the LLVM source tree.")

FLAGS = flags.FLAGS


def qualified_name(cursor: clang.cindex.Cursor) -> str:
    """Return a fully-qualified name for a cursor."""
    if cursor is None or cursor.kind == CursorKind.TRANSLATION_UNIT:
        return ""
    else:
        prefix = qualified_name(cursor.semantic_parent)
        if prefix != "":
            return f"{prefix}::{cursor.spelling}"
        return cursor.spelling


def get_llvm_structs_and_classes(translation_unit) -> Iterable[str]:
    """Extract qualified names of all structs and classes in a translation unit."""
    for c in translation_unit.cursor.walk_preorder():
        try:
            if (
                c.kind == clang.cindex.CursorKind.CLASS_DECL
                or c.kind == clang.cindex.CursorKind.STRUCT_DECL
            ):
                name = qualified_name(c.referenced)
                if not name.startswith("llvm::"):
                    continue
                name = name[len("llvm::") :]
                # Nested namespace, ignore it.
                if ":" in name:
                    continue
                yield name
        except ValueError:
            logging.debug("Ignoring unknown cursor kind error")


@lru_cache
def get_llvm_cxx_flags(llvm_root: Path) -> List[str]:
    """Get the C++ flags needed to compile LLVM sources."""
    return shlex.split(
        subprocess.check_output(
            [str(llvm_root / "bin" / "llvm-config"), "--cxxflags"],
            universal_newlines=True,
        )
    )


def can_compile(
    header: str, pass_: str, pass_manager: str, cxx_flags: List[str]
) -> bool:
    """Try and compile a test file using the given pass and pass manager."""
    with tempfile.TemporaryDirectory(prefix="CompilerGym-") as tmpdir:
        tmpdir = Path(tmpdir)
        with open(tmpdir / "test.cc", "w", encoding="utf-8") as f:
            f.write(
                f"""\
#include "{header}"
void M() {{
    llvm::{pass_manager} PM;
    PM.addPass(llvm::{pass_}());
}}
"""
            )
        try:
            subprocess.check_call(
                [
                    str(Path(FLAGS.llvm_root) / "bin" / "clang++"),
                    "-c",
                    str(tmpdir / "test.cc"),
                    "-o",
                    str(tmpdir / "test.o"),
                ]
                + cxx_flags,
                timeout=60,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False


def module_pass_test(header: Path, name: str, pass_manager, cxx_flags, header_relpath):
    if can_compile(header, name, "ModulePassManager", cxx_flags):
        logging.info("Found module pass %s in %s", name, header_relpath)
        return {
            "class_name": name,
            "create_statement": f"llvm::{name}()",
            "header": header_relpath,
            "type": "ModulePass",
        }


def function_pass_test(
    header: Path, name: str, pass_manager, cxx_flags, header_relpath
):
    if can_compile(header, name, "FunctionPassManager", cxx_flags):
        logging.info("Found function pass %s in %s", name, header_relpath)
        return {
            "class_name": name,
            "create_statement": f"llvm::{name}()",
            "header": header_relpath,
            "type": "FunctionPass",
        }


def extract_passes_from_file(
    executor: ThreadPoolExecutor,
    futures,
    header: Path,
) -> None:
    """Extract passes from a file."""
    cxx_flags = get_llvm_cxx_flags(Path(FLAGS.llvm_root))
    idx = clang.cindex.Index.create()
    tu = idx.parse(
        str(header),
        args=["-xc++", "-std=c++14"],
        options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
    )

    header_relpath = os.path.relpath(header, os.path.join(FLAGS.llvm_root, "include"))

    for name in get_llvm_structs_and_classes(tu):
        futures.append(
            executor.submit(
                module_pass_test,
                header,
                name,
                "ModulePassManager",
                cxx_flags,
                header_relpath,
            )
        )
        futures.append(
            executor.submit(
                function_pass_test,
                header,
                name,
                "FunctionPassManager",
                cxx_flags,
                header_relpath,
            )
        )


def extract_all_passes(llvm_root: Path) -> List[Dict[str, str]]:
    """Extract passes from the LLVM source tree."""
    assert llvm_root.is_dir(), f"Not a directory: {llvm_root}"
    os.chdir(llvm_root)

    cl.Config.set_library_file(str(llvm_root / "lib" / "libclang.so"))

    # Get the names of all files which contain a pass class definition.
    try:
        include_root = llvm_root / "include/llvm/Transforms"
        find = subprocess.check_output(
            [
                "find",
                str(include_root),
                "-type",
                "f",
                "-name",
                "*.h",
            ],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError:
        logging.error(
            "Failed to find any LLVM headers in %s",
            llvm_root,
        )
        sys.exit(1)

    matching_paths = set(find.strip().splitlines())

    logging.info(
        "Processing %s files from %s/include/llvm/Transforms",
        len(matching_paths),
        llvm_root,
    )
    paths = [Path(path) for path in matching_paths]

    passes: List[Dict[str, str]] = []
    futures = []
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        for path in paths:
            extract_passes_from_file(executor, futures, path)

        for future in concurrent.futures.as_completed(futures):
            pass_ = future.result()
            if pass_ is not None:
                passes.append(pass_)

    passes.sort(key=lambda p: p["class_name"])

    return passes


def main(argv):
    assert len(argv) == 1, f"Unknown argument: {argv[1:]}"

    passes = extract_all_passes(Path(FLAGS.llvm_root))
    if not passes:
        logging.error("No passes found in %s", FLAGS.llvm_root)
        sys.exit(1)

    logging.info("Extracted %d passes from LLVM", len(passes))
    print(json.dumps(passes, indent=2))


if __name__ == "__main__":
    app.run(main)
