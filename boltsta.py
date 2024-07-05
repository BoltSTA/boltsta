# =========================================================================================
# Copyright (c) 2024, BoltSta Team
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

# =========================================================================================

"""
Run Static Timing Analysis.

Usage:
  boltsta.py  --library=<library_path> --design=<design_path> --sdc=<sdc_path> [--run_dir=<run_dir_path>]

Options:
    --help -h                    Print this help message.
    --library=<param>            Path to the library file.
    --design=<param>             Path to the design file.
    --sdc=<param>                Path to the SDC file.
    --run_dir=<run_dir_path>     Directory to save all the results [default: pwd]
"""

import logging
import os
from datetime import datetime
import time
from docopt import docopt
import pandas as pd
from typing import Any
from boltsta.sta import run_sta # TODO need to be fixed later


if __name__ == "__main__":
    # arguments
    arguments = docopt(__doc__, version="RUN Static Timing Analysis: 1.0")

    # logs format
    now_str = datetime.utcnow().strftime("sta_run_%Y_%m_%d_%H_%M_%S")

    # checking library file existence
    library_in = arguments["--library"]
    if not os.path.exists(library_in):
        logging.error(f"The library file {library_in} doesn't exist, please check")
        exit(1)

    # checking design file existence
    design_in = arguments["--design"]
    if not os.path.exists(design_in):
        logging.error(f"The design file {design_in} doesn't exist, please check")
        exit(1)

    # checking SDC file existence
    sdc_in = arguments["--sdc"]
    if not os.path.exists(sdc_in):
        logging.error(f"The SDC file {sdc_in} doesn't exist, please check")
        exit(1)

    if (
        arguments["--run_dir"] == "pwd"
        or arguments["--run_dir"] == ""
        or arguments["--run_dir"] is None
    ):
        run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        run_dir = os.path.abspath(arguments["--run_dir"])

    # checking run_dir existence & creation
    if not os.path.isdir(run_dir):
        os.makedirs(run_dir, exist_ok=True)
    else:
        os.makedirs(run_dir, exist_ok=True)

    # logs setup
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(run_dir, "{}.log".format(now_str))),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # set pandas options
    pd.set_option("display.max_rows", None)

    # Calling the main function
    time_start = time.time()
    sta_results = run_sta(library_in, design_in, sdc_in)
    exc_time = time.time() - time_start

    # Save results
    sta_results.to_csv(os.path.join(run_dir, "final_report_sta.csv"), index=False)
    logging.info(f"STA report: \n {sta_results}")

    # Reporting execution time
    logging.info(f"Static Timing Analysis execution time: {exc_time} sec")
