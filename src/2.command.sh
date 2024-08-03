#!/bin/bash
SYMS=`cat symbols.txt | tr '\n' ' '`
echo $SYMS
python3 ./one_spread.py -s $SYMS
