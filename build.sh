#!/bin/bash

set -e

# variables
target="../$1"

# install dependencies
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install cython

# add release files
mkdir -p release
cd release
export PROJECT_PATH="$target"
python ../compile.py build_ext --inplace
rm -rf build
find . -type d | xargs cp -r -t "$target"
rm -rf release