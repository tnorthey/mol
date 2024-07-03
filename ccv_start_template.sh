#!/bin/bash

# Request an hour of runtime:
#SBATCH --time=1:00:00

# Controls the minimum/maximum number of nodes allocated to the job
#SBATCH -N 1

# Default resources are 1 core with 2.8GB of memory.

# Use more memory (4GB):
#SBATCH --mem=4G

# Specify a job name:
#SBATCH -J chd_sa

# Specify an output file
#SBATCH -o MySerialJob-%j.out
#SBATCH -e MySerialJob-%j.error

# Run a command
#module load mpi/openmpi_4.0.5_gcc_10.2_slurm20 eigen/3.4.0 gcc/10.2 intel/2020.2
#module load python/3.7.4
module load python
source .venv/bin/activate

#previous_step=$(echo "ZZ" | awk -F',' '{print $1}')  # take the FIRST step in the ZZ list as the "previous step"
#next_step=$(echo "ZZ" | awk -F',' '{print $NF}')  # second step after the comma is next step
previous_step=XX
next_step=YY

# define run variables
molecule="MOLECULE"
traj=TRAJ
noise=NOISE
noise_file="noise/noise_NOISFILEINDEX.dat"
qmin=QMIN
qmax=QMAX
qlen=QLEN
nrestarts=NRESTARTS
results_dir="RESULTS_DIR"
constraints="CONSTRAINTS"

run_id=""$next_step"_1d"  # run ID
# CHD
#target_file="xyz/target_traj"$traj"/target_"$next_step".xyz"  # target xyz filename
#reference_xyz_file="xyz/chd_reference.xyz"
# NMM
target_file="data_/nmm/target_"$next_step".dat"  # target dat filename
reference_xyz_file="xyz/nmm_opt.xyz"

# create directory if not exists
mkdir -p $results_dir

# take the best n fits as the starting list
nfits=20
start_list=$(ls -1 "$results_dir/$previous_step"_1d_???.*xyz | head -n $nfits)
# run
for starting_xyz_file in $start_list
do 
    echo "submission script: starting_xyz_file $starting_xyz_file"
    echo "submission script: target_file $target_file"
    python3 run.py $run_id $molecule $starting_xyz_file $reference_xyz_file $target_file $results_dir $qmin $qmax $qlen $noise $noise_file $nrestarts $constraints
done

