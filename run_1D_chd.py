"""
Run the simulated annealing function for CHD
Strategy 1: Generate a lot of initial conditions via short "hot" SA runs,
    start from the best structure from that -> N restarts of longer "cooler" SA runs
    - This should find a reasonably close starting point from the ICs,
    then optimise it further with the subsequent longer runs
"""
import numpy as np
import sys
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
target_xyz_files_string = str(sys.argv[3])
target_indices_string = str(sys.argv[4])
ringclosed = str(sys.argv[5])
reference_xyz_file = "xyz/chd_reference.xyz"
###################################
# split target xyz files into list
target_xyz_files = target_xyz_files_string.split(',')
print(target_xyz_files)
target_indices = target_indices_string.split(',')
print(target_indices)

ACH = 10.0
if ringclosed == 'closed':
  ACC = 10.0  
elif ringclosed == 'open':
  ACC = 1.0
else:
  print("ringclosed must equal 'closed' or 'open'")

w.chd_1D(
    run_id,
    start_xyz_file,
    target_xyz_files,
    qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
    noise = 0.00,
    sa_nsteps = 800,
    ga_nsteps = 800,
    sa_step_size = 0.018,
    sa_starting_temp = 1.0,
    sa_harmonic_factor = (ACC, ACH),
    sa_angular_factor = 1.0,
    ga_harmonic_factor = (ACC, ACH),
    ga_angular_factor = 1.0,
    nrestarts = 1,
    ntrials = 1,
    timesteps = target_indices,
    non_h_modes_only=True,  # only include "non-hydrogen" modes
    hf_energy=True,   # calculate HF energy (PySCF) at the end
    pcd_mode=False,    # use percent difference instead of absolute signal
)

print("Total time: %3.2f s" % float(default_timer() - start))
