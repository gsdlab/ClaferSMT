#!/bin/bash

SRC_DIR=./src
name=$1

# First, compile the .cfr file into the Clafer Python IR format .py
# clafer -sm python $name

cd $SRC_DIR
python front/ClaferRun.py ../${name%.*}.py
rm ../${name%.*}.py
