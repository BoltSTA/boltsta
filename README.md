BoltSTA Open Source Tool
========================

[![License](https://img.shields.io/badge/license-GPLv3-blue)](/LICENSE)

[<p align="center"><img src="images/mabrains.png" width="700">](http://mabrains.com/)


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
  - [About Mabrains](#about-mabrains)
  - [Contact-Us](#contact-us)
  - [License](#license)


## Introduction


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

### From PyPi

To install the package, please use the following command:

```bash
# To Be Added
```

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

**TO BE ADDED**

### Example

**TO BE ADDED**

## About Mabrains

Mabrains was founded to achieve the main purpose to change the world of Chip Design using AI. Empowering the world with a new methodologies and techniques that would disrupt the status quo in the EDA industry.

We have contributed in developing many PDKs for Open Source Tools. For more information, please refer to [Mabrains-Github](https://github.com/mabrains).

## Contact-Us

Requests for more information about BoltSTA and other open source technologies can be [submitted via this web form](https://mabrains.com/#contactus).

## License

The BoltSTA is released under the [GNU General Public License - Version 3](/LICENSE)

The copyright details (which should also be found at the top of every file) are;

```
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
```