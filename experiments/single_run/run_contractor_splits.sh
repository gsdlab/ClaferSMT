#!/bin/bash

MLClaferZ3 ~/git/ClaferZ3/src/test/contractorPackaging_medium.py -g20 -n 20 -c 4  --verboseprint --experimentnumsplit  4 8 16 32 64 128 256 --heuristicsfile contractorsplits --timeout 500