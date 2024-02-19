#!/bin/bash

step=75
head -n 2 "$step"_1d_000.000*xyz | awk '{print $1, $4}' | grep - > list

#arr=()
while IFS= read -r line; do
  #arr+=("$line")
  A="${line:11:13}"
  echo $A
  num=$(awk "BEGIN {print $A+360; exit}")
  echo $num
  fname="$step"_1d_00${line:0:10}.xyz
  echo $fname
  sed -i "s/$A/$num/" $fname
done < list
