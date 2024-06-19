"""
Test sa.py module

The following functions are tested:
$ grep "def " modules/sa.py 
def read_nm_displacements(self, fname, natoms):
def uniform_factors(self, nmodes, displacement_factors):
def displacements_from_wavenumbers(self, wavenumbers, step_size, exponential=False):
def simulate_trajectory(
def atomic_pre_molecular(self, atomic_numbers, qvector, aa, bb, cc, electron_mode=False):
def simulated_annealing_modes_ho(
def get_angle_3d(a, b, c):
"""

import numpy as np
import os

# my own modules
import modules.mol as mol
import modules.x as xray
import modules.sa as sa

# create class objects
m = mol.Xyz()
x = xray.Xray()
sa = sa.Annealing()

#############################
### Initialise some stuff ###
#############################
# qvector
qlen = 241
qvector = np.linspace(1e-9, 24, qlen, endpoint=True)
inelastic = True
electron_mode = False  # x-rays

def xyz2iam(xyz, atomlist):
    """convert xyz file to IAM signal"""
    atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
    compton_array = x.compton_spline(atomic_numbers, qvector)
    iam, atomic, molecular, compton = x.iam_calc(
        atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
    )
    return iam

# define target_function
start_xyz_file = "xyz/chd_opt.xyz"
reference_xyz_file = "xyz/chd_opt.xyz"
target_xyz_file = "xyz/target.xyz"
_, _, atomlist, starting_xyz = m.read_xyz(start_xyz_file)
_, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
_, _, atomlist, target_xyz = m.read_xyz(target_xyz_file)
atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
starting_iam = xyz2iam(starting_xyz, atomlist)
reference_iam = xyz2iam(reference_xyz, atomlist)
target_iam = xyz2iam(target_xyz, atomlist)

aa, bb, cc = x.read_iam_coeffs()
compton, atomic_total, pre_molecular = x.atomic_pre_molecular(
    atomic_numbers,
    qvector,
    aa,
    bb,
    cc,
    electron_mode,
)

noise_bool = False
noise = 4
### ADDITION OF RANDOM NOISE
if noise_bool:
    mu = 0  # normal distribution with mean of mu
    sigma = noise
    noise_array = sigma * np.random.randn(qlen) + mu
    target_iam += noise_array
###

#target_function = 100 * (target_iam / reference_iam - 1)
target_function = target_iam

nmfile = "nm/chd_normalmodes.txt"
natoms = starting_xyz.shape[0]
displacements = sa.read_nm_displacements(nmfile, natoms)
nmodes = displacements.shape[0]

# mode_indices = np.arange(0, 28)  # CHD, this removes hydrogen modes
mode_indices = np.arange(0, nmodes)  # CHD, all modes
print("including modes:")
print(mode_indices)

sa_step_size_array = 0.01 * np.ones(nmodes)

# CHD specific; notably not indices 0, 5 (the ring-opening)

ho_indices1 = np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]])  # chd (C-C bonds)
# ho_indices = [
#    [0, 1, 2, 3, 4, 6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
#    [1, 2, 3, 4, 5, 7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
# ]  # chd (C-C and C-H bonds)

ho_indices2 = np.array([
    [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
    [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
])  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)

angular_bool = False
angular_factor = 0.1
angular_indices = np.array([[6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1], 
                            [0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0], 
                            [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (non-C-C-C angles: C-C-H, H-C-H angles)

starting_temp = 0.2
nsteps = 40
harmonic_factor = (0.1, 0.1)
pcd_mode = True
xyz_save = True
twod_mode = False


#################################
### End Initialise some stuff ###
#################################


def test_simulated_annealing_modes_ho():
    """test the simulated annealing function ..."""
    # Run simulated annealing
    (
        f_best,
        f_xray_best,
        predicted_best,
        xyz_best,
    ) = sa.simulated_annealing_modes_ho(
        atomic_numbers,
        starting_xyz,
        displacements,
        mode_indices,
        target_function,
        reference_iam,
        qvector,
        compton,
        atomic_total,
        pre_molecular,
        aa,
        bb,
        cc,
        sa_step_size_array,
        ho_indices1,
        ho_indices2,
        angular_indices,
        starting_temp,
        nsteps,
        inelastic,
        harmonic_factor,
        angular_factor,
        pcd_mode,
        electron_mode,
        twod_mode,
        angular_bool,
    )

    # it outputs xyz correctly (correct shape)
    assert xyz_best.shape == starting_xyz.shape, "xyz_best.shape != starting_xyz.shape"
    assert (
        f_best >= f_xray_best
    ), "total target function should be greater (or equal) than x-ray component"
    assert (
        predicted_best.shape == target_function.shape
    ), "predicted_best.shape != target_function.shape"
