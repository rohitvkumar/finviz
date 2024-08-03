#!/bin/bash
filename=$1
str=""
while read line; do
# reading each line
str="$str $line"
done < $filename
echo $str
