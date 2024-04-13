#!/bin/bash

# initial submit script which starts from start.xyz
# It loops N (20) times, check/edit ccv_start_initial.sh
JID=$(sbatch --parsable ccv_start_initial.sh)
sleep 1s

target_arr=("0,1" "1,0" "0,1")

### Submit next step, depending on if previous jobs have completed
# each sbatch script does 20 runs.
for i in ${target_arr[@]}
do
	fname=ccv_start.sh
	cp ccv_start_template.sh $fname
	sed -i "s/ZZ/$i/" $fname
	echo $fname
	JID=$(sbatch --parsable -d afterany:$JID $fname)
done




