# =========================================================================================
#
# Copyright (c) 2023, Mabrains LLC Confidential
#
# This file is part of Mabrains internal development tools and is not allowed to be shared.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# This banner can not be removed by anyone other than the code author.
#
# =========================================================================================

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


# =================
# ----- Clean -----
# =================

# remove run dir folder
clean:
	@rm -rf boltsta_run_*
