#!/bin/bash

for step in 10 20 32 35 37 40 44 50 55 60 65 70 75
do
	echo "step $step has N xyz files:"
	ls tmp_/"$step"_1d_000.*xyz | wc -l
done
