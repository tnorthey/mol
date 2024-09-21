#!/bin/bash
# go_1d_chd: callable like this: ./go_1D_chd.sh $i $next_step $noise $qmax $qlen $nrestarts $results_dir $reference_xyz_file $constraints

molecule="NMM"
starting_xyz_file="xyz/nmm_start.xyz"	# starting xyz filename
step="25"			# define the target frame e.g. 01, 20, 30, 40, 50
run_id=""$step"_1d"	# run ID
target_file="data_/nmm/target_$step.dat"  # target filename
qmin="0.3323"
qmax="4.3727"
qlen=39
noise=0.0
noise_file="noise/noise.dat"
nrestarts=5
results_dir="tmp_"
reference_xyz_file="xyz/nmm_opt.xyz"
constraints="strong"

echo "go script: starting_xyz_file $starting_xyz_file"
echo "go script: target_file $target_file"

python3 run.py $run_id $molecule $starting_xyz_file $reference_xyz_file $target_file $results_dir $qmin $qmax $qlen $noise $noise_file $nrestarts $constraints

#bestxyz=$(ls -1 tmp_/"$run_id"_???.????????.xyz | head -n 1) 
#bestdat=$(ls -1 tmp_/"$run_id"_???.????????.dat | head -n 1) 
#cp $bestxyz tmp_/"$run_id"_best.xyz
#cp $bestdat tmp_/"$run_id"_best.dat
