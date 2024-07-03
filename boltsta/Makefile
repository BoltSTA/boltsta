# ============================================================================
# Copyright (c) 2024, Mabrains LLC
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.

#                    GNU General Public License
#                       Version 3, 29 June 2007

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0

# ============================================================================

TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
VENV_RUN_COMMAND = $(TOP_DIR)/actions_venv/bin/activate

# ======================= 
# ------ ENV SETUP ------ 
# =======================

$(TOP_DIR)/actions_venv:
	@python3 -m venv $(TOP_DIR)/actions_venv

# Install requirements	
env: $(TOP_DIR)/actions_venv
	@. $(VENV_RUN_COMMAND); pip install -r requirements.test.txt -r requirements.txt 

# ========================
# ----- LINTING TEST -----
# ========================

lint_python: env
	@. $(VENV_RUN_COMMAND); flake8 .

# ============================
# ------- BOLTSTA TEST -------
# ============================
.ONESHELL:
tests: env
	@export PYTHONPATH=$(PYTHONPATH):$(TOP_DIR)
	@. $(VENV_RUN_COMMAND); pytest

# =================
# ----- Clean -----
# =================

# remove run dir folder
clean:
	@rm -rf boltsta_run_*
