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
target_file = str(sys.argv[3])
noise = float(sys.argv[4])
qmin = float(sys.argv[5])
qmax = float(sys.argv[6])
qlen = int(sys.argv[7])
nrestarts = int(sys.argv[8])
results_dir = str(sys.argv[9])
reference_xyz_file = str(sys.argv[10])
constraints = str(sys.argv[11])  # "strong" or "weak"
###################################

nmodes = 48   # 3 * 18 - 6

if constraints == "strong":
    print('using strong constraints')
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
    target_file,
    qvector=np.linspace(qmin, qmax, qlen, endpoint=True),
    inelastic=True,
    pcd_mode=True,
    noise = noise,
    sa_starting_temp = 1.0,
    nmfile = "nm/nmm_normalmodes.txt",
    hydrogen_modes = np.arange(38, nmodes),  # NMM hydrogen modes
    sa_mode_indices = np.arange(0, nmodes),  # NMM all modes
    ga_mode_indices = np.arange(0, nmodes),  # NMM all modes
    sa_nsteps=60000,
    ga_nsteps=60000,
    ho_indices1 = np.array([
                    [3, 3, 3, 0, 0,  10, 5,  1, 1,  0, 0,  5,  3,  1, 5, 3,  0], 
                    [6, 5, 1, 1, 12, 12, 10, 5, 12, 3, 10, 12, 10, 6, 6, 12, 12]]),  # nmm (C-C, C-N, or C-O bonds): 3-6, 3-5, 3-1, 0-1, 0-12, 10-12, 5-10, and 2nd nearest neighbours across ring
    ho_indices2 = np.array([
                    [6, 6, 6, 1, 1, 0,  0,  10, 10, 5,  5,  7, 7, 8, 2, 16, 11, 14],
                    [7, 8, 9, 2, 4, 14, 15, 11, 13, 16, 17, 9, 8, 9, 4, 17, 13, 15]]),  # nmm C-H bonds, and H-H "bonds"
    angular_bool=False,   # use HO terms on the angles
    angular_indices = np.array([[0, 0, 0],
                                [1, 1, 1],
                                [2, 2, 2]]),
    sa_step_size=0.012,
    ga_step_size=0.012,
    sa_harmonic_factor = (ACC, ACH),
    ga_harmonic_factor = (1.0 * ACC, ACH),
    sa_angular_factor=0.1,
    ga_angular_factor=0.1,
    nrestarts = nrestarts,    # it restarts from the xyz_best of the previous restart
    non_h_modes_only=False,  # only include "non-hydrogen" modes
    hf_energy=True,  # run PySCF HF energy
    results_dir=results_dir,
    rmsd_indices = np.array([3, 5, 6, 10, 12, 0, 1]),  # nmm
    bond_indices = np.array([0, 5]),   # chd ring-opening bond
    angle_indices = np.array([6, 3, 12]),   # nmm methyl group angle
    dihedral_indices = np.array([0, 1, 4, 5]),  # chd ring-opening dihedral
)

print("Total time: %3.2f s" % float(default_timer() - start))
