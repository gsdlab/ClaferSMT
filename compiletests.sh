#!/bin/bash

for i in `find test -name '*'`
do
    echo $i
    addclafertest $i
done