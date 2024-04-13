#!/bin/bash

for step in 10 20 32 35 37 40 45 50 55 60 65 70 75
#for step in {0..9}
#for step in {0..12}
do
        echo "step $step has N xyz files:"
        ls tmp_/"$step"_1d_???.*xyz | wc -l
done
