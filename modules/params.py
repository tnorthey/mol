# import math
import numpy as np


######
class Params:
    """parameters for simulated annealing"""

    def __init__(self, molecule):
        """initialise with hard-coded params"""
        if molecule.lower() == "chd":
            """CHD params"""
            self.natoms = 14
            self.nmodes = 3 * self.natoms - 6
            self.inelastic = True
            self.pcd_mode = False
            self.sa_starting_temp = 1.0
            self.nmfile = "nm/chd_normalmodes.txt"
            self.hydrogen_modes = np.arange(28, self.nmodes)  # CHD hydrogen modes
            self.sa_mode_indices = np.arange(0, self.nmodes)  # CHD, all modes
            self.ga_mode_indices = np.arange(0, self.nmodes)  # CHD, all modes
            self.sa_nsteps = 8000
            self.ga_nsteps = 40000
            self.ho_indices1 = np.array(
                [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]
            )  # chd (C-C bonds)
            self.ho_indices2 = np.array(
                [
                    [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
                    [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
                ]
            )  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
            self.angular_bool = False  # use HO terms on the angles
            # angular_indices = np.array([[0, 1, 2, 3],
            #                            [1, 2, 3, 4],
            #                            [2, 3, 4, 5]])  # chd (C-C-C angles)
            # angular_indices = np.array([[0, 1, 2, 3, 6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
            #                            [1, 2, 3, 4, 0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
            #                            [2, 3, 4, 5, 7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (C-C-C angles, and all C-C-H, H-C-H angles)
            self.angular_indices = np.array(
                [
                    [6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
                    [0, 5, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
                    [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6],
                ]
            )  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
            self.sa_step_size = 0.012
            self.ga_step_size = 0.012
            self.sa_harmonic_factor = (10.0, 10.0)
            self.ga_harmonic_factor = (1.0, 10.0)
            self.sa_angular_factor = 0.0
            self.ga_angular_factor = 0.0
            self.nrestarts = 5  # it restarts from the xyz_best of the previous restart
            self.non_h_modes_only = False  # only include "non-hydrogen" modes
            self.hf_energy = False  # run PySCF HF energy
            self.rmsd_indices = np.array([0, 1, 2, 3, 4, 5])  # chd
            self.bond_indices = np.array([0, 5])  # chd ring-opening bond
            self.angle_indices = np.array([0, 3, 5])  # angle
            self.dihedral_indices = np.array([0, 1, 4, 5])  # chd ring-opening dihedral

        elif molecule.lower() == "nmm":
            """NMM params"""
            self.natoms = 18
            self.nmodes = 3 * self.natoms - 6
            self.inelastic = True
            self.pcd_mode = True
            self.sa_starting_temp = 1.0
            self.nmfile = "nm/nmm_normalmodes.txt"
            self.hydrogen_modes = np.arange(38, self.nmodes)  # NMM hydrogen modes
            self.sa_mode_indices = np.arange(0, self.nmodes)  # NMM all modes
            self.ga_mode_indices = np.arange(0, self.nmodes)  # NMM all modes
            self.sa_nsteps = 8000
            self.ga_nsteps = 40000
            self.ho_indices1 = np.array(
                [
                    [3, 3, 3, 0, 0, 10, 5, 1, 1, 0, 0, 5, 3, 1, 5, 3, 0],
                    [6, 5, 1, 1, 12, 12, 10, 5, 12, 3, 10, 12, 10, 6, 6, 12, 12],
                ]
            )  # nmm (C-C, C-N, or C-O bonds): 3-6, 3-5, 3-1, 0-1, 0-12, 10-12, 5-10, and 2nd nearest neighbours across ring
            self.ho_indices2 = np.array(
                [
                    [6, 6, 6, 1, 1, 0, 0, 10, 10, 5, 5, 7, 7, 8, 2, 16, 11, 14],
                    [7, 8, 9, 2, 4, 14, 15, 11, 13, 16, 17, 9, 8, 9, 4, 17, 13, 15],
                ]
            )  # nmm C-H bonds, and H-H "bonds"
            self.angular_bool = (False,)  # use HO terms on the angles
            self.angular_indices = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
            self.sa_step_size = 0.012
            self.ga_step_size = 0.012
            self.sa_harmonic_factor = (10.0, 10.0)
            self.ga_harmonic_factor = (1.0, 10.0)
            self.sa_angular_factor = 0.0
            self.ga_angular_factor = 0.0
            self.nrestarts = 5  # it restarts from the xyz_best of the previous restart
            self.non_h_modes_only = False  # only include "non-hydrogen" modes
            self.hf_energy = False  # run PySCF HF energy
            self.rmsd_indices = np.array([3, 5, 6, 10, 12, 0, 1])  # nmm
            self.bond_indices = np.array([0, 5])  # chd ring-opening bond
            self.angle_indices = np.array([6, 3, 12])  # nmm methyl group angle
            self.dihedral_indices = np.array([0, 1, 4, 5])  # chd ring-opening dihedral

        else:
            print("No parameters were loaded... choose chd or nmm.")
