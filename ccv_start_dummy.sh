#!/bin/bash

# Request an hour of runtime:
#SBATCH --time=0:00:10


# Controls the minimum/maximum number of nodes allocated to the job
#SBATCH -N 1

# Default resources are 1 core with 2.8GB of memory.

# Use more memory (1GB):
#SBATCH --mem=1G

# Specify a job name:
#SBATCH -J dummy

# Specify an output file
#SBATCH -o MySerialJob-%j.out
#SBATCH -e MySerialJob-%j.error

# Run a command
#module load mpi/openmpi_4.0.5_gcc_10.2_slurm20 eigen/3.4.0 gcc/10.2 intel/2020.2
#module load python/3.7.4

echo "dummy job"
sleep 1s
