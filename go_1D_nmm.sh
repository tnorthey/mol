#!/bin/bash
# go_1d_nmm
# octave:3> q
#q =
# Columns 1 through 13:
#   0.3323   0.4386   0.5449   0.6512   0.7576   0.8639   0.9702   1.0766   1.1829   1.2892   1.3955   1.5019   1.6082
# Columns 14 through 26:
#   1.7145   1.8208   1.9272   2.0335   2.1398   2.2461   2.3525   2.4588   2.5651   2.6715   2.7778   2.8841   2.9904
# Columns 27 through 39:
#   3.0968   3.2031   3.3094   3.4157   3.5221   3.6284   3.7347   3.8410   3.9474   4.0537   4.1600   4.2664   4.3727

#starting_xyz_file="xyz/nmm_geomovie_end.xyz"	# starting xyz filename
starting_xyz_file="xyz/nmm_start.xyz"	# starting xyz filename
step=35			# define the target frame e.g. 01, 20, 30, 40, 50
run_id=""$step"_1d"	# run ID
target_file="data_/nmm/target_$step.dat"  # target filename
noise=0.0
qmin=0.3323
qmax=4.3727
qlen=39
nrestarts=2
results_dir="tmp_"
reference_xyz_file="xyz/nmm_opt.xyz"
constraints="strong"

echo "go script: starting_xyz_file $starting_xyz_file"
echo "go script: target_file $target_file"

python3 run_1D_nmm.py $run_id $starting_xyz_file $target_file $noise $qmin $qmax $qlen $nrestarts $results_dir $reference_xyz_file $constraints

