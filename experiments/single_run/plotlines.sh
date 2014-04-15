#!/bin/bash

#chartfile outfile log2(numsplits) numheuristics

gnuplot -e "myylabel='time'" -e "mytitle='Effect of #Splits on Solving Time'" -e "file='$1'"  -e "outfile='$2.png'" -e "xr='$3'" -e "numheuristics='$4'" linesplot