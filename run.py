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
import modules.read_input as read_input

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()
p = read_input.Input_to_params()

w.run_1D(
    p.run_id,  # not loaded from param module
    p.start_xyz_file,  # not loaded from param module
    p.reference_xyz_file,  # not loaded from param module
    p.target_xyz_file,  # not loaded from param module
    p.results_dir,  # not loaded from param module
    p.qvector,  # not loaded from param module
    p.noise_value,  # not loaded from param module
    p.noise_data_file,  # not loaded from param module
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
    p.sa_harmonic_factor,  # not loaded from param module
    p.ga_harmonic_factor,  # not loaded from param module
    p.sa_angular_factor,
    p.ga_angular_factor,
    p.nrestarts,  # not loaded from param module
    p.non_h_modes_only,
    p.hf_energy,
    p.rmsd_indices,
    p.bond_indices,
    p.angle_indices,
    p.dihedral_indices,
)

print("Total time: %3.2f s" % float(default_timer() - start))
