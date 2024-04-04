#!/bin/bash

for step in 20 35 40 45 50 55 60 65 70 75
do
	echo "step $step has N xyz files:"
	ls tmp_/"$step"_1d_000.*xyz | wc -l
done
