#import math
import numpy as np
from numpy.typing import NDArray, DTypeLike

######
class CHD_Params:
    """CHD parameters for simulated annealing"""
    def __init__(self):
        """initialise with hard-coded params"""
        self.natoms = 14
        self.nmodes = 36
        self.inelastic=True
        self.pcd_mode=False
        self.sa_starting_temp = 1.0
        self.nmfile = "nm/chd_normalmodes.txt"
        self.hydrogen_modes = np.arange(28, self.nmodes)  # CHD hydrogen modes
        self.sa_mode_indices = np.arange(0, self.nmodes)  # CHD, all modes
        self.ga_mode_indices = np.arange(0, self.nmodes)  # CHD, all modes
        self.sa_nsteps=8000
        self.ga_nsteps=40000
        self.ho_indices1 = np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]])  # chd (C-C bonds)
        self.ho_indices2 = np.array([
            [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ])  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
        self.angular_bool=False   # use HO terms on the angles
        #angular_indices = np.array([[0, 1, 2, 3], 
        #                            [1, 2, 3, 4], 
        #                            [2, 3, 4, 5]])  # chd (C-C-C angles)
        #angular_indices = np.array([[0, 1, 2, 3, 6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1], 
        #                            [1, 2, 3, 4, 0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0], 
        #                            [2, 3, 4, 5, 7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (C-C-C angles, and all C-C-H, H-C-H angles)
        self.angular_indices = np.array([[6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
                                    [0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
                                    [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        self.sa_step_size=0.012
        self.ga_step_size=0.012
        self.sa_harmonic_factor = (10.0, 10.0)
        self.ga_harmonic_factor = (1.0, 10.0)
        self.sa_angular_factor=0.0
        self.ga_angular_factor=0.0
        self.nrestarts = 5    # it restarts from the xyz_best of the previous restart
        self.non_h_modes_only=False  # only include "non-hydrogen" modes
        self.hf_energy=False  # run PySCF HF energy
        self.rmsd_indices = np.array([0, 1, 2, 3, 4, 5])  # chd
        self.bond_indices = np.array([0, 5])   # chd ring-opening bond
        self.angle_indices = np.array([0, 3, 5])   # angle
        self.dihedral_indices = np.array([0, 1, 4, 5])  # chd ring-opening dihedral

