#!/bin/bash

# Run ClaferSMT from src

# Set the installation directory
CLAFER_SMT=

export PYTHONPATH=.:./src:$PYTHONPATH

export LD_LIBRARY_PATH=$CLAFER_SMT:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$CLAFER_SMT:$DYLD_LIBRARY_PATH

PYTHON3=python3

if [ "$OS" = "Windows_NT" ]; then PYTHON3=python; fi

# First, compile the .cfr file into the Clafer Python IR format .py
# clafer -sm python $name

"$PYTHON3" -OO src/front/ClaferRun.py $@
