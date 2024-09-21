#!/bin/bash
# go_1d_chd: callable like this: ./go_1D_chd.sh $i $next_step $noise $qmax $qlen $nrestarts $results_dir $reference_xyz_file $constraints

molecule="CHD"
starting_xyz_file="xyz/start.xyz"	# starting xyz filename
reference_xyz_file="xyz/chd_reference.xyz"
step=20			# define the target frame e.g. 20, 30, 40, 50
traj="094"
run_id=""$step"_1d"	# run ID
target_file="xyz/target_traj$traj/target_$step.xyz"  # target xyz filename
results_dir="tmp_"
qmin="1e-9"
qmax=8
qlen=81
noise=0.0
noise_data_file="noise/noise.dat"
nrestarts=2
constraints="weak"

echo "go script: starting_xyz_file $starting_xyz_file"
echo "go script: target_file $target_file"

python3 run.py $run_id $molecule $starting_xyz_file $reference_xyz_file $target_file $results_dir $qmin $qmax $qlen $noise $noise_data_file $nrestarts $constraints

#bestxyz=$(ls -1 tmp_/"$run_id"_???.????????.xyz | head -n 1) 
#bestdat=$(ls -1 tmp_/"$run_id"_???.????????.dat | head -n 1) 
#cp $bestxyz tmp_/"$run_id"_best.xyz
#cp $bestdat tmp_/"$run_id"_best.dat
