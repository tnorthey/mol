"""
Test wrap.py module
"""
import os
import sys
import numpy as np

# my modules
import modules.mol as mol
import modules.wrap as wrap
import modules.read_input as read_input

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()
p = read_input.Input_to_params()

def test_wrap_chd():
    '''Test the run_1D function in modules/wrap.py'''
    w.run_1D(
        p.run_id,
        p.start_xyz_file,
        p.reference_xyz_file,
        p.target_xyz_file,
        p.results_dir,
        p.qvector,
        p.noise_value,
        p.noise_data_file,
        p.inelastic,
        p.pcd_mode,
        p.ewald_mode,
        p.sa_starting_temp,
        p.nmfile,
        p.hydrogen_mode_indices,  # CHD hydrogen modes
        p.sa_mode_indices,  # CHD, all modes
        p.ga_mode_indices,  # CHD, all modes
        p.sa_nsteps,
        p.ga_nsteps,
        p.bonds_bool,  # use HO terms on the bonds
        p.ho_indices1,  # chd (C-C bonds)
        p.ho_indices2,  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
        p.angles_bool,   # use HO terms on the angles
        p.angular_indices1,
        p.angular_indices2,
        p.sa_step_size,
        p.ga_step_size,
        p.sa_harmonic_factor,
        p.ga_harmonic_factor,
        p.sa_angular_factor,
        p.ga_angular_factor,
        p.nrestarts,
        p.non_h_modes_only,  # only include "non-hydrogen" modes
        p.hf_energy,  # run PySCF HF energy
        p.rmsd_indices,  # chd
        p.bond_indices,    # chd ring-opening bond
        p.angle_indices,    # angle
        p.dihedral_indices,    # chd ring-opening dihedral
        #run_id,
        #start_xyz_file,
        #reference_xyz_file,
        #target_xyz_file,
        #results_dir,
        #qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        #noise = 0.0,
        #noise_data_file = "noise/noise.dat",
        #inelastic=True,
        #pcd_mode=False,
        #ewald_mode=True,
        #sa_starting_temp = 1.0,
        #nmfile = "nm/chd_normalmodes.txt",
        #hydrogen_modes = np.arange(28, nmodes),  # CHD hydrogen modes
        #sa_mode_indices = np.arange(0, nmodes),  # CHD, all modes
        #ga_mode_indices = np.arange(0, nmodes),  # CHD, all modes
        #sa_nsteps=80,
        #ga_nsteps=20,
        #ho_indices1 = np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]),  # chd (C-C bonds)
        #ho_indices2 = np.array([
        #    [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
        #    [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        #]),  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
        #angular_bool=False,   # use HO terms on the angles
        ##angular_indices = np.array([[0, 1, 2, 3], 
        ##                            [1, 2, 3, 4], 
        ##                            [2, 3, 4, 5]])  # chd (C-C-C angles)
        ##angular_indices = np.array([[0, 1, 2, 3, 6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1], 
        ##                            [1, 2, 3, 4, 0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0], 
        ##                            [2, 3, 4, 5, 7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]])  # chd (C-C-C angles, and all C-C-H, H-C-H angles)
        #angular_indices1 = np.array([[6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
        #                            [0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
        #                            [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]]),  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        #angular_indices2 = np.array([[6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
        #                            [0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
        #                            [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]]),  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        #sa_step_size=0.012,
        #ga_step_size=0.012,
        ##sa_step_size=0.02,
        ##ga_step_size=0.02,
        #sa_harmonic_factor = (ACC, ACH),
        #ga_harmonic_factor = (0.1 * ACC, ACH),
        #sa_angular_factor=0.1,
        #ga_angular_factor=0.1,
        #nrestarts = 2,
        #non_h_modes_only=False,  # only include "non-hydrogen" modes
        #hf_energy=False,  # run PySCF HF energy
        #rmsd_indices = np.array([0, 1, 2, 3, 4, 5]),  # chd
        #bond_indices = np.array([0, 5]),    # chd ring-opening bond
        #angle_indices = np.array([0, 3, 5]),    # angle
        #dihedral_indices = np.array([0, 1, 4, 5]),    # chd ring-opening dihedral
    )

    target_file = "%s/TARGET_FUNCTION_%s.dat" % (p.results_dir, p.run_id)
    xyz_file = "%s/%s_target.xyz" % (p.results_dir, p.run_id)
    assert os.path.exists(target_file), "%s doesn't exist! It wasn't created..." % target_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file


def _test_wrap_nmm():
    ###################################
    run_id = "test_nmm"
    start_xyz_file = "xyz/nmm_start.xyz"
    target_xyz_file = "xyz/nmm_target.xyz"
    reference_xyz_file = "xyz/nmm_opt.xyz"
    ACC = 0.0
    ACH = 1.0 
    results_dir = "tmp_"
    nmodes = 48
    ###################################
    w.run_1D(
        run_id,
        start_xyz_file,
        reference_xyz_file,
        target_xyz_file,
        results_dir,
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        noise = 0.1,
        noise_data_file = "noise/noise.dat",
        inelastic=True,
        pcd_mode=False,
        ewald_mode=False,
        sa_starting_temp = 1.0,
        nmfile = "nm/nmm_normalmodes.txt",
        hydrogen_modes = np.arange(38, nmodes),  # CHD hydrogen modes
        sa_mode_indices = np.arange(0, nmodes),  # CHD, all modes
        ga_mode_indices = np.arange(0, nmodes),  # CHD, all modes
        sa_nsteps=20,
        ga_nsteps=20,
        ho_indices1 = np.array([
                        [3, 3, 3, 0, 0, 10, 5], 
                        [6, 5, 1, 1, 12, 12, 10]]),  # nmm (C-C, C-N, or C-O bonds): 3-6, 3-5, 3-1, 0-1, 0-12, 10-12, 5-10
        ho_indices2 = np.array([
                        [6, 6, 6, 1, 1, 0,  0,  10, 10, 5,  5 ],
                        [7, 8, 9, 2, 4, 14, 15, 11, 13, 16, 17],
        ]),  # nmm (C-H bonds)
        angular_bool=False,   # use HO terms on the angles
        angular_indices1 = np.array([[0, 0], [1, 1], [2, 2]]),
        angular_indices2 = np.array([[0, 0], [1, 1], [2, 2]]),
        sa_step_size=0.012,
        ga_step_size=0.012,
        sa_harmonic_factor = (ACC, ACH),
        ga_harmonic_factor = (0.1 * ACC, ACH),
        sa_angular_factor=0.1,
        ga_angular_factor=0.1,
        nrestarts = 1,    # it restarts from the xyz_best of the previous restart
        non_h_modes_only=False,  # only include "non-hydrogen" modes
        hf_energy=True,  # run PySCF HF energy
        rmsd_indices = np.array([3, 5, 6, 10, 12, 0, 1]),  # nmm
        bond_indices = np.array([0, 5]),   # chd ring-opening bond
        angle_indices = np.array([6, 3, 12]),   # nmm methyl group angle
        dihedral_indices = np.array([0, 1, 4, 5]),  # chd ring-opening dihedral
    )

    target_file = "%s/TARGET_FUNCTION_%s.dat" % (results_dir, run_id)
    xyz_file = "%s/%s_target.xyz" % (results_dir, run_id)
    assert os.path.exists(target_file), "%s doesn't exist! It wasn't created..." % target_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file
