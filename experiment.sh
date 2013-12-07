#!/bin/bash

SRC_DIR=./src
CLAFERZ3_DIR=.

clafer -sm python $name

cd $SRC_DIR
python3 front/Z3Run.py ../${name%.*}.py
rm ../${name%.*}.py
