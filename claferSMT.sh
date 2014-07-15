#!/bin/bash

# Run ClaferSMT.egg

export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
PYTHON3=python3

if [ "$OS" = "Windows_NT" ]; then PYTHON3=python; fi

"$PYTHON3" ClaferSMT.egg $@
