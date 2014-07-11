#!/bin/bash

export PYTHONPATH=.:./src::$PYTHONPATH

# First, compile the .cfr file into the Clafer Python IR format .py
# clafer -sm python $name

python -OO src/front/ClaferRun.py $@