#!/bin/bash

# Run ClaferSMT from src 

export PYTHONPATH=.:./src:$PYTHONPATH
export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
PYTHON3=python3

if [ "$OS" = "Windows_NT" ]; then PYTHON3=python; fi

# First, compile the .cfr file into the Clafer Python IR format .py
# clafer -sm python $name

"$PYTHON3" -OO src/front/ClaferRun.py $@