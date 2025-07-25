#!/bin/bash

# initial submit script which starts from start.xyz
# It loops N (20) times  check/edit ccv_start_initial.sh
JID=$(sbatch --parsable ccv_start_dummy.sh)
sleep 1s

#target_indices_arr=(0 1 0 1 2 1 0 1 2 3 2 1 0 1 2 3 4 3 2 1 2 3 4 5 4 3 2 3 4 5 6 5 4 3 4 5 6 7 6 5 4 5 6 7 8 7 6 5 6 7 8 9 8 7 6 7 8 9 10 9 8 7 8 9 10 11 10 9 8 9 10 11 12 11 10 9 10 11 12 11 10 11 12 11 12)
#target_indices_arr=(0 1 2 1 0 1 2 3 2 1 2 3 4 3 2 3 4 5 4 3 4 5 6 5 4 5 6 7 6 5 6 7 8 7 6 7 8 9 8 7 8 9 10 9 8 9 10 11 10 9 10 11 12 11 10 11 12 11 12)
target_indices_arr=($1 $2)
nsteps=${#target_indices_arr[@]}

target_arr=(10 20 32 35 37 40 45 50 55 60 65 70 75)

### Submit next step, depending on if previous jobs have completed
# each sbatch script does 20 runs.
# Loop over indices in the array, excluding the last one
for ((i = 0; i < nsteps - 1; i++))
#for i in ${!target_indices_arr[@]}  # loop over indices array
do
	prev_ind=${target_indices_arr[$i]}
	next_ind=${target_indices_arr[$i+1]}
	prev_step=${target_arr[$prev_ind]}
	next_step=${target_arr[$next_ind]}
	echo $prev_step
	echo $next_step
	fname=ccv_start.sh
	cp ccv_start_template.sh $fname
	sed -i "s/XX/$prev_step/" $fname
	sed -i "s/YY/$next_step/" $fname
	echo $fname
	JID=$(sbatch --parsable -d afterany:$JID $fname)
done




