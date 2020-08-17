#!/bin/bash
SYMS=`cat symbols.txt | tr '\n' ' '`
echo $SYMS
python ./one_spread.py -s $SYMS