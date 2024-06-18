"""
Run the simulated annealing function for CHD
Strategy 1: Generate a lot of initial conditions via short "hot" SA runs,
    start from the best structure from that -> N restarts of longer "cooler" SA runs
    - This should find a reasonably close starting point from the ICs,
    then optimise it further with the subsequent longer runs
"""
# run example: python3 run_1D_chd.py $run_id $starting_xyz_file $target_xyz_file $noise $qmax $qlen $nrestarts $results_dir

import os
import sys
import numpy as np
from timeit import default_timer

# my modules
import modules.mol as mol
import modules.wrap as wrap

start = default_timer()

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()

###################################
# command line arguments
run_id = str(sys.argv[1])  # define a string to label the start of the output filenames
start_xyz_file = str(sys.argv[2])
target_xyz_file = str(sys.argv[3])
traj = str(sys.argv[4])
noise = float(sys.argv[5])
qmax = int(sys.argv[6])
qlen = int(sys.argv[7])
nrestarts = int(sys.argv[8])
results_dir = str(sys.argv[9])
###################################

ACH = 10.0

w.nmm_1D(
    run_id,
    start_xyz_file,
    target_xyz_file,
    qvector=np.linspace(1e-9, qmax, qlen, endpoint=True),
    noise = noise,
    sa_starting_temp = 1.0,
    #sa_mode_indices = np.arange(0, 28),  # CHD, "non-hydrogen" modes
    #ga_mode_indices = np.arange(0, 28),  # CHD, "non-hydrogen" modes
    sa_mode_indices = np.arange(0, 36),  # CHD, all modes
    ga_mode_indices = np.arange(0, 36),  # CHD, all modes
    sa_nsteps = 8000,
    ga_nsteps = 40000,
    sa_step_size = 0.012,
    ga_step_size = 0.012,
    sa_harmonic_factor = (10.0, ACH),
    ga_harmonic_factor = (1.0, ACH),
    #sa_harmonic_factor = (0.0, 1.0),
    #ga_harmonic_factor = (0.0, 1.0),
    #sa_angular_factor = 1.0,
    #ga_angular_factor = 1.0,
    sa_angular_factor = 0.1,
    ga_angular_factor = 0.1,
    nrestarts = nrestarts,    # it restarts from the xyz_best of the previous restart
    non_h_modes_only=True,  # only include "non-hydrogen" modes
    hf_energy=True,   # calculate HF energy (PySCF) at the end
    results_dir=results_dir,
)

print("Total time: %3.2f s" % float(default_timer() - start))
