# import math
import numpy as np
import json

######
class Input_to_params:
    """read parameters for simulated annealing"""

    def __init__(self):
        """initialise with hard-coded params"""

        ###################################
        # Load input JSON
        with open("input.json", "r") as file:
            data = json.load(file)
        ### Parameters
        # run params
        self.run_id = str(data["run_params"]["run_id"])
        self.molecule = str(data["run_params"]["molecule"])
        molecule = self.molecule
        print(f'molecule: {molecule}')
        self.results_dir = str(data["run_params"]["results_dir"])
        # xyz file params
        self.start_xyz_file = str(data["xyz_files"]["start_xyz_file"])
        self.reference_xyz_file = str(data["xyz_files"]["reference_xyz_file"])
        self.target_xyz_file = str(data["xyz_files"]["target_xyz_file"])
        # scattering_params params
        self.inelastic = bool(data["scattering_params"]["inelastic_bool"])
        self.pcd_mode = bool(data["scattering_params"]["pcd_mode_bool"])
        self.ewald_mode = bool(data["scattering_params"]["ewald_mode_bool"])
        # q params
        self.qmin = float(data["scattering_params"]["q"]["qmin"])
        self.qmax = float(data["scattering_params"]["q"]["qmax"])
        self.qlen = int(data["scattering_params"]["q"]["qlen"])
        # noise params
        self.noise_value = float(data["scattering_params"]["noise"]["noise_value"])
        self.noise_data_file = str(data["scattering_params"]["noise"]["noise_data_file"])
        # simulated annealing params
        self.sa_starting_temp = float(
            data["simulated_annealing_params"]["sa_starting_temp"]
        )
        self.sa_nsteps = int(data["simulated_annealing_params"]["sa_nsteps"])
        self.ga_nsteps = int(data["simulated_annealing_params"]["ga_nsteps"])
        self.sa_step_size = float(data["simulated_annealing_params"]["sa_step_size"])
        self.ga_step_size = float(data["simulated_annealing_params"]["ga_step_size"])
        self.nrestarts = int(
            data["simulated_annealing_params"]["nrestarts"]
        )  # it restarts from the xyz_best of the previous restart
        self.bonds_bool = bool(data["simulated_annealing_params"]["bonds_bool"])

        self.sa_harmonic_factor = np.array(
            data["simulated_annealing_params"]["sa_harmonic_factor"]
        )
        self.ga_harmonic_factor = np.array(
            data["simulated_annealing_params"]["ga_harmonic_factor"]
        )
        self.angles_bool = bool(data["simulated_annealing_params"]["angles_bool"])
        self.sa_angular_factor = np.array(
            data["simulated_annealing_params"]["sa_angular_factor"]
        )
        self.ga_angular_factor = np.array(
            data["simulated_annealing_params"]["ga_angular_factor"]
        )
        self.non_h_modes_only = bool(
            data["simulated_annealing_params"]["non_h_modes_only_bool"]
        )  # only include "non-hydrogen" modes
        self.hf_energy = bool(
            data["simulated_annealing_params"]["hf_energy_bool"]
        )  # run PySCF HF energy

        # molecule params
        self.natoms = int(data["molecule_params"][molecule]["natoms"])
        self.nmodes = int(data["molecule_params"][molecule]["nmodes"])
        self.nmfile = str(data["molecule_params"][molecule]["nmfile"])
        self.hydrogen_mode_range = np.array(
            data["molecule_params"][molecule]["hydrogen_mode_range"]
        )
        self.sa_mode_range = np.array(
            data["molecule_params"][molecule]["sa_mode_range"]
        )
        self.ga_mode_range = np.array(
            data["molecule_params"][molecule]["ga_mode_range"]
        )
        self.ho_indices1 = np.array(data["molecule_params"][molecule]["ho_indices1"])
        self.ho_indices2 = np.array(data["molecule_params"][molecule]["ho_indices2"])
        self.angular_indices1 = np.array(
            data["molecule_params"][molecule]["angular_indices1"]
        )
        self.angular_indices2 = np.array(
            data["molecule_params"][molecule]["angular_indices1"]
        )
        self.rmsd_indices = np.array(data["molecule_params"][molecule]["rmsd_indices"])
        self.bond_indices = np.array(data["molecule_params"][molecule]["bond_indices"])
        self.angle_indices = np.array(
            data["molecule_params"][molecule]["angle_indices"]
        )
        self.dihedral_indices = np.array(
            data["molecule_params"][molecule]["dihedral_indices"]
        )

        ### other variables
        self.qvector = np.linspace(self.qmin, self.qmax, self.qlen, endpoint=True)
        self.hydrogen_mode_indices = np.arange(
            self.hydrogen_mode_range[0], self.hydrogen_mode_range[1]
        )
        self.sa_mode_indices = np.arange(self.sa_mode_range[0], self.sa_mode_range[1])
        self.ga_mode_indices = np.arange(self.ga_mode_range[0], self.ga_mode_range[1])

        ###################################
        # print values
        print("reading the following parameters...")
        print(self.run_id)
        print(self.molecule)
        print(self.start_xyz_file)
        print(self.reference_xyz_file)
        print(self.target_xyz_file)
        print(self.results_dir)
        print(self.qmin)
        print(self.qmax)
        print(self.qlen)
        print(self.noise_value)
        print(self.noise_data_file)
        print(self.nrestarts)
        print(f'self.angles_bool: {self.angles_bool}')

        # if molecule.lower() == "chd":
        #    """CHD params"""
        #    self.natoms = 14
        #    self.nmodes = 3 * self.natoms - 6
        #    self.nmfile = "nm/chd_normalmodes.txt"
        #    self.hydrogen_modes = np.arange(28, self.nmodes)  # CHD hydrogen modes
        #    self.sa_mode_indices = np.arange(0, self.nmodes)  # CHD, all modes
        #    self.ga_mode_indices = np.arange(0, self.nmodes)  # CHD, all modes
        #    self.ho_indices1 = np.array(
        #        [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]
        #    )  # chd (C-C bonds)
        #    self.ho_indices2 = np.array(
        #        [
        #            [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
        #            [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        #        ]
        #    )  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
        #    self.angular_bool = False  # use HO terms on the angles
        #    # angular_indices = np.array([[0, 1, 2, 3],
        #    #                            [1, 2, 3, 4],
        #    #                            [2, 3, 4, 5]])  # chd (C-C-C angles)
        #    # angular_indices = np.array([[0, 1, 2, 3, 6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
        #    #                            [1, 2, 3, 4, 0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
        #    #                            [2, 3, 4, 5, 7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (C-C-C angles, and all C-C-H, H-C-H angles)
        #    self.angular_indices1 = np.array(
        #        [
        #            [6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
        #            [0, 5, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
        #            [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6],
        #        ]
        #    )  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        #    self.angular_indices2 = np.array(
        #        [
        #            [6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
        #            [0, 5, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
        #            [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6],
        #        ]
        #    )  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        #    self.rmsd_indices = np.array([0, 1, 2, 3, 4, 5])  # chd
        #    self.bond_indices = np.array([0, 5])  # chd ring-opening bond
        #    self.angle_indices = np.array([0, 3, 5])  # angle
        #    self.dihedral_indices = np.array([0, 1, 4, 5])  # chd ring-opening dihedral

        # elif molecule.lower() == "nmm":
        #    """NMM params"""
        #    self.natoms = 18
        #    self.nmodes = 3 * self.natoms - 6
        #    self.inelastic = True
        #    self.pcd_mode = True
        #    self.sa_starting_temp = 0.2
        #    self.nmfile = "nm/nmm_normalmodes.txt"
        #    self.hydrogen_modes = np.arange(38, self.nmodes)  # NMM hydrogen modes
        #    self.sa_mode_indices = np.arange(0, self.nmodes)  # NMM all modes
        #    self.ga_mode_indices = np.arange(0, self.nmodes)  # NMM all modes
        #    self.sa_nsteps = 8000
        #    self.ga_nsteps = 40000
        #    self.ho_indices1 = np.array(
        #        [
        #            [3, 3, 3, 0, 0, 10, 5, 1, 1, 0, 0, 5, 3, 1, 5, 3, 0],
        #            [6, 5, 1, 1, 12, 12, 10, 5, 12, 3, 10, 12, 10, 6, 6, 12, 12],
        #        ]
        #    )  # nmm (C-C, C-N, or C-O bonds): 3-6, 3-5, 3-1, 0-1, 0-12, 10-12, 5-10, and 2nd nearest neighbours across ring
        #    self.ho_indices2 = np.array(
        #        [
        #            [6, 6, 6, 1, 1, 0, 0, 10, 10, 5, 5, 7, 7, 8, 2, 16, 11, 14],
        #            [7, 8, 9, 2, 4, 14, 15, 11, 13, 16, 17, 9, 8, 9, 4, 17, 13, 15],
        #        ]
        #    )  # nmm C-H bonds, and H-H "bonds"
        #    self.angular_bool = False  # use HO terms on the angles
        #    self.angular_indices1 = np.array([[5, 10,5,7,7,8,7,8,9,3,3,4,3, 3, 16,13,15,15,13],
        #                                      [10,12,3,6,6,6,6,6,6,1,1,1,5, 5, 5, 10,0 ,0 ,10],
        #                                      [12,0, 1,8,9,9,3,3,3,4,2,2,16,17,17,11,14,12,12]])
        #    self.angular_indices2 = np.array([[ 6,6 ],
        #                                      [ 3,3 ],
        #                                      [ 1,5 ]])
        #    self.sa_step_size = 0.012
        #    self.ga_step_size = 0.012
        #    self.sa_harmonic_factor = (10.0, 10.0)
        #    self.ga_harmonic_factor = (1.0, 10.0)
        #    self.sa_angular_factor = (10.0, 1.0)
        #    self.ga_angular_factor = (1.0, 1.0)
        #    self.nrestarts = 5  # it restarts from the xyz_best of the previous restart
        #    self.non_h_modes_only = False  # only include "non-hydrogen" modes
        #    self.hf_energy = True # run PySCF HF energy
        #    self.rmsd_indices = np.array([3, 5, 6, 10, 12, 0, 1])  # nmm
        #    self.bond_indices = np.array([6, 12])  # nmm N-O distance
        #    self.angle_indices = np.array([6, 3, 12])  # nmm methyl group angle
        #    self.dihedral_indices = np.array([6, 3, 10, 5])  # nmm torsion

        # else:
        #    print("No parameters were loaded... choose chd or nmm.")
