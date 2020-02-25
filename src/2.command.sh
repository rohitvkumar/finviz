#!/bin/bash
ARGS="-s"
while read line; do ARGS="$ARGS $line"; done
while read line; do python ./mw_roce.py -s $line | tr '\n' ' '; python ./ROA_ROE_finviz.py -s $line | tr '\n' ' '; echo $line ;done < symbols.txt
