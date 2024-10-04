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

def test_wrap_chd_xyz():
    '''Test the run_1D function in modules/wrap.py'''
    w.run(p_chd)
    target_function_file = "%s/TARGET_FUNCTION_%s.dat" % (p_chd.results_dir, p_chd.run_id)
    xyz_file = "%s/%s_target.xyz" % (p_chd.results_dir, p_chd.run_id)
    assert os.path.exists(target_function_file), "%s doesn't exist! It wasn't created..." % target_function_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file

def test_wrap_nmm_xyz():
    '''Test the run_1D function in modules/wrap.py'''
    w.run(p_nmm)
    target_function_file = "%s/TARGET_FUNCTION_%s.dat" % (p_nmm.results_dir, p_nmm.run_id)
    xyz_file = "%s/%s_target.xyz" % (p_nmm.results_dir, p_nmm.run_id)
    assert os.path.exists(target_function_file), "%s doesn't exist! It wasn't created..." % target_function_file
    assert os.path.exists(xyz_file), "%s doesn't exist! It wasn't created..." % xyz_file

