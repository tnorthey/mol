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

#./go_1D_chd_qmax8_20.sh
#for i in $(cat XX_start_list_YY.txt) ; do ./go_1D_chd.sh $i "closed"; done
#for i in $(cat XX_start_list_YY.txt) ; do ./go_1D_chd.sh $i "open"; done
for i in $(cat XX_start_list_YY.txt) ; do ./go_1D_chd.sh $i "unrestrained"; done
