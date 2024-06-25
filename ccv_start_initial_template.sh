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

# define run variables
step=INITIAL_STEP
traj=TRAJ
noise=NOISE
qmax=QMAX
qlen=QLEN
nrestarts=NRESTARTS
results_dir="RESULTS_DIR"
constraints="CONSTRAINTS"

run_id=""$step"_1d"	# run ID
target_xyz_file="xyz/target_traj$traj/target_$step.xyz"  # target xyz filename
reference_xyz_file="xyz/chd_reference.xyz"

# create directory if not exists
mkdir -p $results_dir

ntrials=1
starting_xyz_file="xyz/start.xyz"
for i in $(seq 1 $ntrials); do
    echo "submission script: starting_xyz_file $starting_xyz_file"
    echo "submission script: target_xyz_file $target_xyz_file"
    python3 run_1D_chd.py $run_id $starting_xyz_file $target_xyz_file $traj $noise $qmax $qlen $nrestarts $results_dir $reference_xyz_file $constraints
done
