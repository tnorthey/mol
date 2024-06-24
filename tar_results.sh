#!/bin/bash

#for i in results_noise*low_constraints_b/
for i in results_noise*traj09?_b/
do
	echo "tarring $i..."
	tar cf ${i%/*}.tar $i
done
