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
p_chd = read_input.Input_to_params("tests/input_test_chd.json")
p_nmm = read_input.Input_to_params("tests/input_test_nmm.json")

def call_run_1D(p, mode):
    '''Call function specifically for testing purposes.'''
    w.run_1D(
        mode,
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
    )
    return

def test_wrap_chd_xyz():
    '''Test the run_1D function in modules/wrap.py'''
    mode = "xyz"
    call_run_1D(p_chd, mode)
    target_file = "%s/TARGET_FUNCTION_%s.dat" % (p_chd.results_dir, p_chd.run_id)
    xyz_file = "%s/%s_target.xyz" % (p_chd.results_dir, p_chd.run_id)
    assert os.path.exists(target_file), "%s doesn't exist! It wasn't created..." % target_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file

def test_wrap_nmm_xyz():
    '''Test the run_1D function in modules/wrap.py'''
    mode = "xyz"
    call_run_1D(p_nmm, mode)
    target_file = "%s/TARGET_FUNCTION_%s.dat" % (p_nmm.results_dir, p_nmm.run_id)
    xyz_file = "%s/%s_target.xyz" % (p_nmm.results_dir, p_nmm.run_id)
    assert os.path.exists(target_file), "%s doesn't exist! It wasn't created..." % target_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file

