"""
Run simulated annealing
"""

# run example: python3 run.py ...

from timeit import default_timer

start = default_timer()
import os
import sys
import numpy as np

# my modules
import modules.mol as mol
import modules.wrap as wrap
import modules.params as params

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()

###################################
# command line arguments
run_id = str(sys.argv[1])  # define a string to label the start of the output filenames
molecule = str(sys.argv[2])
start_xyz_file = str(sys.argv[3])
reference_xyz_file = str(sys.argv[4])
target_xyz_file = str(sys.argv[5])
results_dir = str(sys.argv[6])
qmin = float(sys.argv[7])
qmax = float(sys.argv[8])
qlen = int(sys.argv[9])
noise = float(sys.argv[10])
nrestarts = int(sys.argv[11])
constraints = str(sys.argv[12])  # "strong" or "weak" else constraints default to 0
###################################

# load parameters
p = params.Params(molecule)

ACC, ACH = 0.0, 0.0  # default is 0 constraints
if constraints == "strong":
    ACC, ACH = 10.0, 10.0
if constraints == "weak":
    ACC, ACH = 0.0, 1.0
sa_harmonic_factor = (ACC, ACH)
ga_harmonic_factor = (0.1 * ACC, ACH)

qvector = np.linspace(qmin, qmax, qlen, endpoint=True)

w.run_1D(
    run_id,  # not loaded from param module
    start_xyz_file,  # not loaded from param module
    reference_xyz_file,  # not loaded from param module
    target_xyz_file,  # not loaded from param module
    results_dir,  # not loaded from param module
    qvector,  # not loaded from param module
    noise,  # not loaded from param module
    p.inelastic,
    p.pcd_mode,
    p.sa_starting_temp,
    p.nmfile,
    p.hydrogen_modes,
    p.sa_mode_indices,
    p.ga_mode_indices,
    p.sa_nsteps,
    p.ga_nsteps,
    p.ho_indices1,
    p.ho_indices2,
    p.angular_bool,
    p.angular_indices1,
    p.angular_indices2,
    p.sa_step_size,
    p.ga_step_size,
    sa_harmonic_factor,  # not loaded from param module
    ga_harmonic_factor,  # not loaded from param module
    p.sa_angular_factor,
    p.ga_angular_factor,
    nrestarts,  # not loaded from param module
    p.non_h_modes_only,
    p.hf_energy,
    p.rmsd_indices,
    p.bond_indices,
    p.angle_indices,
    p.dihedral_indices,
)

print("Total time: %3.2f s" % float(default_timer() - start))
