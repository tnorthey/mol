#!/bin/bash

# initial submit script which starts from start.xyz
# It loops N (20) times  check/edit ccv_start_initial.sh

# define run variables
initial_step=18
molecule="nmm"
noise=_NOISE_
noise_file="noise/noise__NOISEFILEINDEX_.dat"
qmin="0.3323"
qmax="4.3727"
qlen=39
#qmax=_QMAX_
#qlen=_QMAX_1
nrestarts=2
traj=_TRAJ_
constraints="_CONSTRAINTS_"
ending="_ENDING_"
### NB switch to low constraints in the run.py file
results_dir="results_noise"$noise"_qmax"$qmax"_nrestarts"$nrestarts"_traj"$traj"_"$constraints"_constraints_"$ending""
# create directory if not exists
mkdir -p $results_dir

# RUN CCV_START_INITIAL
fname=ccv_start_initial_"$results_dir".sh
cp ccv_start_initial_template.sh $fname
sed -i "s/INITIAL_STEP/$initial_step/" $fname
sed -i "s/MOLECULE/$molecule/" $fname
sed -i "s/TRAJ/$traj/" $fname
sed -i "s/NOISE/$noise/" $fname
sed -i "s/NOISE_FILE/$noise_file/" $fname
sed -i "s/QMIN/$qmin/" $fname
sed -i "s/QMAX/$qmax/" $fname
sed -i "s/QLEN/$qlen/" $fname
sed -i "s/NRESTARTS/$nrestarts/" $fname
sed -i "s/RESULTS_DIR/$results_dir/" $fname
sed -i "s/CONSTRAINTS/$constraints/" $fname
#JID=$(sbatch --parsable $fname)
#sleep 1s

JID=$(sbatch --parsable ccv_start_dummy.sh)
sleep 1s

#target_indices_arr=(0 1 0 1 2 1 0 1 2 3 2 1 0 1 2 3 4 3 2 1 2 3 4 5 4 3 2 3 4 5 6 5 4 3 4 5 6 7 6 5 4 5 6 7 8 7 6 5 6 7 8 9 8 7 6 7 8 9 10 9 8 7 8 9 10 11 10 9 8 9 10 11 12 11 10 9 10 11 12 11 10 11 12 11 12)
#target_indices_arr=(0 1 2 1 0 1 2 3 2 1 2 3 4 3 2 3 4 5 4 3 4 5 6 5 4 5 6 7 6 5 6 7 8 7 6 7 8 9 8 7 8 9 10 9 8 9 10 11 10 9 10 11 12 11 10 11 12 11 12)
#target_indices_arr=(0 1 2 1 0 1 2 3 2 1 2 3 4 3 2 3 4 5 4 3 4 5 6 5 4 5 6 7 6 5 6 7 8 7 6 7 8 9 8 7 8 9 10 9 8 9 10 11 10 9 10 11 12 11 10 11 12 11 12 11 10 9 8 7 6 5 4 3 2 1 0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11 12 12 11 11 10 10 9 9 8 8 7 7 6 6 5 5 4 4 3 3 2 2 1 1)  # CHD traj sequence
target_indices_arr=(0 1 2 1 0 1 2 3 2 1 2 3 4 3 2 3 4 5 4 3 4 5 6 5 4 5 6 7 6 5 6 7 8 7 6 7 8 9 8 7 8 9 10 9 8 9 10 9 8 7 6 5 4 3 2 1 0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 9 9 8 8 7 7 6 6 5 5 4 4 3 3 2 2 1 1)  # NMM sequence
#target_indices_arr=(0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11 12 12 11 11 10 10 9 9 8 8 7 7 6 6 5 5 4 4 3 3 2 2 1 1)
#target_indices_arr=(0 0 0 0 0 0 0 0 0 0)
#target_indices_arr=()
nsteps=${#target_indices_arr[@]}

#target_arr=(10 20 32 35 37 40 45 50 55 60 65 70 75)  # CHD
#target_arr=(18 19 20 21 22 23 24 25 26 27 28)  # NMM
target_arr=(27 28 29 30 31 32 33 34 35 36 37)  # NMM
#target_arr=(20)

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
	fname=ccv_start_"$results_dir".sh
	cp ccv_start_template.sh $fname
	sed -i "s/XX/$prev_step/" $fname
	sed -i "s/YY/$next_step/" $fname
        sed -i "s/MOLECULE/$molecule/" $fname
        sed -i "s/TRAJ/$traj/" $fname
	sed -i "s/NOISE/$noise/" $fname
        sed -i "s/NOISE_FILE/$noise_file/" $fname
        sed -i "s/QMIN/$qmin/" $fname
	sed -i "s/QMAX/$qmax/" $fname
	sed -i "s/QLEN/$qlen/" $fname
	sed -i "s/NRESTARTS/$nrestarts/" $fname
	sed -i "s/RESULTS_DIR/$results_dir/" $fname
        sed -i "s/CONSTRAINTS/$constraints/" $fname
	echo $fname
	JID=$(sbatch --parsable -d afterany:$JID $fname)
done
