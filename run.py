"""
Run simulated annealing
"""

# run example: python3 run.py ...

from timeit import default_timer

start = default_timer()
import os
import sys
import json
import numpy as np

# my modules
import modules.mol as mol
import modules.wrap as wrap
import modules.params as params

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()

###################################
# Load input JSON
with open('input.json', 'r') as file:
    data = json.load(file)
# parameters
run_id = data["run_id"]
molecule = data["molecule"]
start_xyz_file = data["start_xyz_file"]
reference_xyz_file = data["reference_xyz_file"]
target_xyz_file = data["target_xyz_file"]
results_dir = data["results_dir"]
qmin = data["qmin"]
qmax = data["qmax"]
qlen = data["qlen"]
noise = data["noise"]
noise_data_file = data["noise_data_file"]
nrestarts = data["nrestarts"]
constraints = data["constraints"]
# example nested preference...
preference_a = data["preferences"]["a"]
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
    noise_data_file,  # not loaded from param module
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
