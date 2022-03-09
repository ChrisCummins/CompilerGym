# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Filter a list of LLVM passes.

This scripts reads a list of passes from stdin and for each, calls
config.include_pass() to determine whether it should be printed to stdout.
"""
import json
import sys
from typing import Iterable

import config
from absl import app, logging
from llvm_pass import Pass


def filter_passes(pass_iterator: Iterable[Pass]) -> Iterable[Pass]:
    """Apply the config.include_pass() filter to an input sequence of passes.

    :param pass_iterator: An iterator over Pass objects.
    :returns: A subset of the input Pass iterator.
    """
    total_count = 0
    selected_count = 0

    for pass_ in pass_iterator:
        total_count += 1
        if config.include_pass(pass_):
            selected_count += 1
            logging.debug(
                "Selected %s pass (%s) from %s",
                pass_.class_name,
                pass_.flag,
                pass_.source,
            )
            yield pass_

    logging.info(
        "Selected %d of %d LLVM passes (%.1f%%)",
        selected_count,
        total_count,
        selected_count / total_count * 100,
    )


def main(argv):
    """Main entry point."""
    assert len(argv) == 1, f"Unrecognized arguments: {argv[1:]}"

    passes = [Pass(**ln) for ln in json.load(sys.stdin)]
    filtered_passes = filter_passes(passes)
    print(json.dumps([p._asdict() for p in filtered_passes], indent=2))


if __name__ == "__main__":
    app.run(main)
