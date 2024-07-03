BoltSTA Open Source Tool
========================

[![License](https://img.shields.io/badge/license-GPLv3-blue)](/LICENSE)

[<p align="center"><img src="images/BoltSTA.jpeg" width="700">](images/BoltSTA.jpeg)


# Table of contents
- [BoltSTA Open Source Tool](#boltsta-open-source-tool)
- [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Current-Status](#current-status)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [From PyPi](#from-pypi)
    - [Build From Source](#build-from-source)
  - [Script Usage](#script-usage)
    - [Example](#example)
  - [Contact-Us](#contact-us)
  - [License](#license)


## Introduction
Static Timing Analysis (STA) is an important step in the digital ASIC design flow. It is used to verify the timing of Digital Circuits and make sure they work correctly under the specified frequency, and check for any setup or hold violations. Checks are done by analyzing the propagation delays of signals through the combinational logic paths in the circuit that lie between two registers (if reg-reg path), input and a register (if in-reg path), or register to output (if reg-out path). Unlike dynamic simulation, which requires test vectors and considers the actual data values, STA focuses purely on the timing characteristics of the circuit.

## Current-Status

> :warning: We are currently treating the current content as an **experimental preview!**

The tool will be tagged with a production version when ready to do.

## Folder Structure
```
📁 boltsta
 ┣ 📁boltsta                    Includes boltsta tool script.
 ┣ 📁images                     Contains images used for illustration.
 ┣ 📁.github                    Includes CI workflows for github actions.
 ┣ 📜Makefile                   To make some tests for boltsta tool.
 ┣ 📜requirements.txt           List of python packages required for tool installation.
 ┣ 📜requirements.test.txt      List of python packages required for testing purpose.
 ┣ 📜boltsta.py                 Python script for sta analysis. 
 ┣ 📜setup.py                   Python script used for package setup.
 ┣ 📜AUTHORS.md                 This file contains authors of the project.
 ┣ 📜.flake8                    Includes flake8 configuration setup.
 ┣ 📜.gitignore                 Excludes certain local files from being pushed to Git.
 ┗ 📜README.md                  This file that describes the contents.
```

## Prerequisites

At a minimum:

- python 3.9+
- python3-venv

To install a virtual environment for ubuntu 22.04:

```bash
python3 -m pip install --user virtualenv
# OR
sudo apt-get install -y python3-venv
```

## Installation

### Build From Source

To install the BoltSTA from source, you could run the following commands:

```bash
git clone https://github.com/mabrains/boltsta.git
cd boltsta/

python3 -m venv ./env
source ./env/bin/activate

python3 setup.py install
```

## Script Usage
The tool is used to perform Static Timing Analysis(STA) checks step done after Synthesis, and report any violation. The timing checks analyzed are Setup and Hold checks.  
The requirements to run the tool are:  
1. The liberty file (.lib): the library file that the tool will extract cell information from. It can be specified by ```--library=<library_path>```.
2. The verilog netlist design (.v): the design that the tool will analyze written in structural verilog. This design should be the output from synthesis step in the ASIC flow. It can be specified by ```--design=<design_path>```.
3. The SDC constraints (.sdc): the constraints file written in TCL format holding important timing and Clock information necessary for the design. It can be specified by ```--sdc=<sdc_path>```.  

The output from the tool will be the setup and hold timing reports showing the detailed delay analysis and slack calculation. It will also report if the clock requirement is violated or met.  
The tool will take the required files and run the timing analysis and save the reports in your run directory specified by ```--run_dir=<run_dir_path>```.  
```bash  
python3 boltsta.py (--help| -h)
  python3 boltsta.py (--library=<library_path>) (--design=<design_path>) (--sdc=<sdc_path>) [--run_dir=<run_dir_path>]
```  

**Options**
- ```--help```                   Prints this help message.
- ```--library=<library_path>``` The library file used to get cells' information.
- ```--design=<design_path>```   The verilog netlist to analyze.
- ```--sdc=<sdc_path>```         The constraints file holding clock and other timing information.  

  


### Example

```bash
python3 boltsta.py --library=tests/sky130_fd_sc_hd__ff_100C_1v65.lib --design=tests/andor.v --sdc=tests/andor.sdc --run_dir=reports_path
```

You should expect output of timing analysis of the single reg-reg path contained in the andor.v design.
## Contact-Us

Please refer to the [AUTHORS.md](AUTHORS.md) section.

## License

The BoltSTA is released under the [GNU General Public License - Version 3](/LICENSE)

The copyright details (which should also be found at the top of every file) are;

```
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
```
