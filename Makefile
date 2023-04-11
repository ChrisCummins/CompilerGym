# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
define HELP
Available targets:

Basic Commands
--------------

    make all
        Build the native compiled code and install Python dependencies.

    make test
        Run the unit tests.

    make install
        Install the python package.

	make dev-init
		Install the optional packages for development.

Tidying up
-----------

    make clean
        Remove build artifacts.

    make uninstall
        Uninstall the python package.
endef
export HELP

.DEFAULT_GOAL := all

# This project name.
PROJECT := compiler_gym

# The path of the repository reoot.
SOURCE_ROOT := $(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))

# Output and installation directories.
BUILD_DIR ?= /dev/shm/$(USER)/$(PROJECT)/build
INSTALL_DIR ?= /dev/shm/$(USER)/$(PROJECT)/install

# Configurable paths to binaries.
CMAKE ?= cmake
RM ?= rm
PYTHON ?= python

# Building the code.

all: # TODO: DEBUG: $(BUILD_DIR)/requirements.txt
	$(CMAKE) \
		-S $(SOURCE_ROOT)/native \
		-B $(BUILD_DIR) \
		-DCMAKE_INSTALL_PREFIX=$(INSTALL_DIR) \
		-GNinja
	$(CMAKE) --build $(BUILD_DIR) --config Release

clean:
	$(RM) -rf $(BUILD_DIR) $(INSTALL_DIR)

# Tests.

test: install-test-requirements
	$(PYTHON) -m pytest tests $(PYTEST_ARGS)

# Install.

.PHONY: install uninstall

install: all
	$(PYTHON) -m pip install -e $(SOURCE_ROOT)

install-test-requirements: $(BUILD_DIR)/requirements-test.txt

uninstall:
	$(PYTHON) -m pip uninstall -y $(PROJECT)

# Utility targets.

.PHONY: help dev-init

dev-init:
	$(PYTHON) -m pip install requiremts-dev.txt
	pre-commit install

help:
	@echo "$$HELP"

# Install python dependencies.

$(BUILD_DIR)/requirements.txt: $(SOURCE_ROOT)/compiler_gym/requirements.txt
	mkdir -pv $(BUILD_DIR)
	cp -v $< $@
	$(PYTHON) -m pip install -r $@

$(BUILD_DIR)/compiler_gym/requirements-test.txt: $(SOURCE_ROOT)/tests/requirements.txt
	mkdir -pv $(BUILD_DIR)
	cp -v $< $@
	$(PYTHON) -m pip install -r $@
