# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import importlib.util
from pathlib import Path

from absl import flags

flags.DEFINE_string("config", "", "Path to config.py")

FLAGS = flags.FLAGS


def load_config():
    config = FLAGS.config
    assert Path(config).is_file(), f"Config file not found: {config}"

    spec = importlib.util.spec_from_file_location("config", config)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
