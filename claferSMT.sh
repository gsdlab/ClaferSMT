#!/bin/bash

# Run ClaferSMT.egg

# Set the installation directory
CLAFER_SMT=

export LD_LIBRARY_PATH=$CLAFER_SMT:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$CLAFER_SMT:$DYLD_LIBRARY_PATH

export PATH=$CLAFER_SMT:$PATH
PYTHON3=python3

if [ "$OS" = "Windows_NT" ]; then PYTHON3=python; fi

"$PYTHON3" "$CLAFER_SMT/ClaferSMT.egg" $@
