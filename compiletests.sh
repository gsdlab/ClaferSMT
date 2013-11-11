#!/bin/bash

touch src/test/__init__.py
for i in `find test -name '*'`
do
    echo $i
    addclafertest $i
done