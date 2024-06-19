"""
Test wrap.py module
"""
import os
import sys
import numpy as np

# my modules
import modules.mol as mol
import modules.wrap as wrap

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()

def test_wrap():
    ###################################
    run_id = "test"
    start_xyz_file = "xyz/start.xyz"
    target_xyz_file = "xyz/target.xyz"
    reference_xyz_file = "xyz/chd_reference.xyz"
    ACC = 0.0
    ACH = 1.0 
    results_dir = "tmp_"
    ###################################
    w.run_1D(
        run_id,
        start_xyz_file,
        reference_xyz_file,
        target_xyz_file,
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        inelastic=True,
        pcd_mode=False,
        noise = 0.1,
        sa_starting_temp = 1.0,
        nmfile = "nm/chd_normalmodes.txt",
        hydrogen_modes = np.arange(28, 36),  # CHD hydrogen modes
        sa_mode_indices = np.arange(0, 36),  # CHD, all modes
        ga_mode_indices = np.arange(0, 36),  # CHD, all modes
        sa_nsteps=80,
        ga_nsteps=40,
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
        nrestarts = 1,
        non_h_modes_only=False,  # only include "non-hydrogen" modes
        hf_energy=False,  # run PySCF HF energy
        results_dir=results_dir,
        rmsd_indices = np.array([0, 1, 2, 3, 4, 5]),  # chd
        bond_indices = np.array([0, 5]),    # chd ring-opening bond
        angle_indices = np.array([0, 3, 5]),    # angle
        dihedral_indices = np.array([0, 1, 4, 5]),    # chd ring-opening dihedral
    )

    target_file = "%s/TARGET_FUNCTION_%s.dat" % (results_dir, run_id)
    xyz_file = "%s/%s_target.xyz" % (results_dir, run_id)
    assert os.path.exists(target_file), "%s doesn't exist! It wasn't created..." % target_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file
