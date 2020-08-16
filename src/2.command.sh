#!/bin/bash
SYMS=`cat symbols.txt | tr '\n' ' '`
echo $SYMS
python ./mw_roce.py -s $SYMS
echo ''
SYMS=`cat symbols.txt | tr '\n' ' ' | tr '.' '-'`
python ./fnvz_peg.py -s $SYMS