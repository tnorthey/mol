#!/bin/bash

A=$1
B=$2
./submit_all_XX_YY.sh $A $B
sleep 30s
./submit_all_XX_YY.sh $B $A
