#!/bin/bash

ClaferSMT -mtest -tall -g6 -n -1 --profiling --cprofiling #x--usebitvectors
#ClaferSMT -mtest -tpositive -g6 -n -1
if [ "$#" -ne 1 ]; then
    echo "No commit, forgot message."
    exit
fi
git commit -a -m $1