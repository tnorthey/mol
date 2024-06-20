"""
Run simulated annealing for CHD
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
reference_xyz_file = str(sys.argv[10])
constraints = str(sys.argv[11])  # "strong" or "weak"
###################################

if constraints == "strong":
    ACC = 10.0
    ACH = 10.0 
elif constraints == "weak":
    ACC = 0.0
    ACH = 1.0 
else:
    print('error: constraints = "strong" or "weak"')

w.run_1D(
    run_id,
    start_xyz_file,
    reference_xyz_file,
    target_xyz_file,
    qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
    inelastic=True,
    pcd_mode=False,
    noise = noise,
    sa_starting_temp = 1.0,
    nmfile = "nm/chd_normalmodes.txt",
    hydrogen_modes = np.arange(28, nmodes),  # CHD hydrogen modes
    #sa_mode_indices = np.arange(0, 28),  # CHD, "non-hydrogen" modes
    #ga_mode_indices = np.arange(0, 28),  # CHD, "non-hydrogen" modes
    sa_mode_indices = np.arange(0, 36),  # CHD, all modes
    ga_mode_indices = np.arange(0, 36),  # CHD, all modes
    sa_nsteps=8000,
    ga_nsteps=40000,
    ho_indices1 = np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]),  # chd (C-C bonds)
    ho_indices2 = np.array([
        [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
        [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
    ]),  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
    angular_bool=False,   # use HO terms on the angles
    #angular_indices = np.array([[0, 1, 2, 3], 
    #                            [1, 2, 3, 4], 
    #                            [2, 3, 4, 5]])  # chd (C-C-C angles)
    #angular_indices = np.array([[0, 1, 2, 3, 6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1], 
    #                            [1, 2, 3, 4, 0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0], 
    #                            [2, 3, 4, 5, 7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (C-C-C angles, and all C-C-H, H-C-H angles)
    angular_indices = np.array([[6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
                                [0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
                                [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]]),  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
    sa_step_size=0.012,
    ga_step_size=0.012,
    sa_harmonic_factor = (ACC, ACH),
    ga_harmonic_factor = (0.1 * ACC, ACH),
    sa_angular_factor=0.1,
    ga_angular_factor=0.1,
    nrestarts = nrestarts,    # it restarts from the xyz_best of the previous restart
    non_h_modes_only=False,  # only include "non-hydrogen" modes
    hf_energy=True,  # run PySCF HF energy
    results_dir=results_dir,
    rmsd_indices = np.array([0, 1, 2, 3, 4, 5]),  # chd
    bond_indices = np.array([0, 5]),   # chd ring-opening bond
    angle_indices = np.array([0, 3, 5]),   # angle, probably don't care about
    dihedral_indices = np.array([0, 1, 4, 5]),  # chd ring-opening dihedral
)

print("Total time: %3.2f s" % float(default_timer() - start))
