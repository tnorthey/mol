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
previous_step=20
next_step=10

# take the best n fits as the starting list
nfits=20
start_list=$(ls -1 tmp_/"$previous_step"_1d_???.*xyz | head -n $nfits)

# run
for i in $start_list
do 
	./go_1D_chd.sh $i $next_step
done

