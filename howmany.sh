#!/bin/bash

for step in 10 20 30 35 40 50 60
do
	echo "step $step has N xyz files:"
	ls tmp_/"$step"_1d_000.*xyz | wc -l
done
