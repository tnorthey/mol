# import math
import numpy as np
import json
import sys


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
        # mode
        self.mode = str(data["mode"])
        mode = self.mode.lower()  # lower case mode string
        ## handle the case when mode does not equal "dat" or "xyz"
        try:
            if not (mode == "dat" or mode == "xyz"):
                raise ValueError(
                    'mode value must equal "dat" or "xyz"! (case insensitive). Exiting...'
                )
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)  # exit program with error message.
        # run params
        self.run_id = str(data["run_params"]["run_id"])
        self.molecule = str(data["run_params"]["molecule"])
        molecule = self.molecule
        print(f"molecule: {molecule}")
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
        self.noise_data_file = str(
            data["scattering_params"]["noise"]["noise_data_file"]
        )
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
        # print("reading the following parameters...")
        # print(self.run_id)
        # print(self.molecule)
        # print(self.start_xyz_file)
        # print(self.reference_xyz_file)
        # print(self.target_xyz_file)
        # print(self.results_dir)
        # print(self.qmin)
        # print(self.qmax)
        # print(self.qlen)
        # print(self.noise_value)
        # print(self.noise_data_file)
        # print(self.nrestarts)
        # print(f'self.angles_bool: {self.angles_bool}')
