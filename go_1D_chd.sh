#!/bin/bash
# go_1d_chd: callable like this: ./go_1D_chd.sh $i $next_step $noise $qmax $qlen $nrestarts $results_dir $reference_xyz_file $constraints

molecule="CHD"
starting_xyz_file="xyz/start.xyz"	# starting xyz filename
step=20			# define the target frame e.g. 20, 30, 40, 50
run_id=""$step"_1d"	# run ID
traj="094"
target_xyz_file="xyz/target_traj$traj/target_$step.xyz"  # target xyz filename
noise=0.0
qmin="1e-9"
qmax=8
qlen=81
nrestarts=2
results_dir="tmp_"
reference_xyz_file="xyz/chd_reference.xyz"
constraints="weak"

echo "go script: starting_xyz_file $starting_xyz_file"
echo "go script: target_xyz_file $target_xyz_file"

python3 run.py $run_id $molecule $starting_xyz_file $reference_xyz_file $target_xyz_file $results_dir $qmin $qmax $qlen $noise $nrestarts $constraints

#bestxyz=$(ls -1 tmp_/"$run_id"_???.????????.xyz | head -n 1) 
#bestdat=$(ls -1 tmp_/"$run_id"_???.????????.dat | head -n 1) 
#cp $bestxyz tmp_/"$run_id"_best.xyz
#cp $bestdat tmp_/"$run_id"_best.dat
