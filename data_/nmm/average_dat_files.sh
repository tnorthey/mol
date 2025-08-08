#!/bin/bash

paste target_[3-9]?.dat | paste *.dat | awk '{
    sum = 0
    for (i = 1; i <= NF; i++) sum += $i
    print sum / NF
}'


