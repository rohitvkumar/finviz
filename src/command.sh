#!/bin/bash
while read line;
do \
python ./mw_roce.py -s $line | tr '\n' ''; \
python ./fnvz_peg.py -s $line | tr '\n' ''; \
echo $line ; \
done < symbols.txt
