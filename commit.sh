#!/bin/bash

ClaferZ3 -mtest -tall -g6 -n -1 --profiling
#ClaferZ3 -mtest -tpositive -g6 -n -1
if [ "$#" -ne 1 ]; then
    echo "No commit, forgot message."
    exit
fi
git commit -a -m $1