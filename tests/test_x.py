"""
Test functions for x.py module

The following are tested:
$ grep "def " modules/x.py 
  def __init__(self):
  def read_iam_coeffs(self):
  def atomic_factor(self, atom_number, qvector):
  def compton_spline(self, atomic_numbers, qvector):
  def iam_calc(

Not tested yet:
  def iam_calc_2d(self, atomic_numbers, xyz, qvector):
  def jq_atomic_factors_calc(self, atomic_numbers, qvector):
  def compton_spline_calc(self, atomic_numbers, qvector):
  def Imol_calc(self, atomic_factor_arr, xyz, qvector):
"""

import numpy as np
import os

# my own modules
import modules.mol as mol
import modules.x as xray

# create class objects
m = mol.Xyz()
x = xray.Xray()

#############################
### Initialise some stuff ###
#############################
# read test.xyz (perfectly linear H-O-H with exactly 1 Angstrom OH bonds)
xyzheader, comment, atomlist, xyz = m.read_xyz("xyz/test.xyz")
#xyzheader, comment, atomlist, xyz = m.read_xyz("xyz/chd_opt.xyz")
natoms = len(atomlist)
atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]

# qvector
qlen = 41
qvector = np.linspace(0, 12, qlen, endpoint=True)
#################################
### End Initialise some stuff ###
#################################


def test_read_iam_coeffs():
    aa, bb, cc = x.read_iam_coeffs()
    # check it reads H coeffs correctly
    assert aa[0, 0] == 0.489918
    assert bb[0, 0] == 20.6593
    assert cc[0] == 0.001305


def test_compton_spline():
    compton_array = x.compton_spline(atomic_numbers, qvector)
    # test if splined compton factor == 0 for oxygen at q = 0
    assert round(compton_array[0, 0], 1) == 0, "splined compton factor != 0 at q = 0"
    # test if splined compton factor == 1 for one of the hydrogens at q = 24
    assert (
        round(compton_array[1, -1], 1) == 1
    ), "splined compton factor != 1 for H at q = 24"


def test_atomic_factor():
    atom_number = 6  # atom_number = 1 is hydrogen, etc.
    atom_factor = x.atomic_factor(atom_number, qvector)
    # test if C atomic scattering factor f(q=0) = Nel = 6  (within rounding)
    assert round(atom_factor[0], 2) == 6.0, "C  atomic factor (q = 0) != 6"


# I use this for the IAM calc x-ray and electron tests
compton_array = x.compton_spline(atomic_numbers, qvector)  # compton factors
inelastic = True


def test_iam_calc():
    """x-ray scattering mode"""
    electron_mode = False
    iam, atomic, molecular, compton, pre_molecular = x.iam_calc(
        atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
    )
    # test if H2O I(q=0) = Nel**2 = 10**2  (within rounding)
    assert round(atomic[0], 1) == 66.0, "I_atomic(q = 0) != 66"
    assert round(molecular[0], 1) == 34.0, "I_mol(q = 0) != 34"
    assert round(iam[0], 0) == 100.0, "H2O I_total(q = 0) != 100"
    # test if H2O I(q=24)_inelastic = Nel = 10  (within rounding)
    # assert round(compton[-1], 0) == 10.0, "H2O inelastic scattering term (q = 24) != 10"
    """electron scattering mode"""
    electron_mode = True
    iam, atomic, molecular, compton, pre_molecular = x.iam_calc(
        atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
    )
    # test if H2O I(q=0) = 0 (within rounding)
    assert round(iam[0], 0) == 0.0, "H2O I_total(q = 0) != 0"


def test_iam_calc_ewald():
    #qlen = 41
    #qvector = np.linspace(0, 12, qlen, endpoint=True)
    electron_mode = False
    inelastic = True
    iam_1d, atomic, molecular, compton, pre_molecular = x.iam_calc(
        atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
    )
    (
        iam_3d,
        atomic_3d,
        molecular_3d,
        compton_3d,
        pre_molecular_3d,
        iam_total_rotavg,
        atomic_rotavg,
        molecular_rotavg,
        compton_rotavg,
    ) = x.iam_calc_ewald(atomic_numbers, xyz, qvector, inelastic, compton_array)
    np.savetxt("rotavg.del_%s" % qlen, np.column_stack((qvector, iam_total_rotavg)))
    np.savetxt("iam_1d.del_%s" % qlen, np.column_stack((qvector, iam_1d)))
    np.savetxt("atomic_rotavg.del_%s" % qlen, np.column_stack((qvector, atomic_rotavg)))
    np.savetxt("atomic.del_%s" % qlen, np.column_stack((qvector, atomic)))
    np.savetxt("molecular_rotavg.del_%s" % qlen, np.column_stack((qvector, molecular_rotavg)))
    np.savetxt("molecular.del_%s" % qlen, np.column_stack((qvector, molecular)))
    np.savetxt("compton_rotavg.del_%s" % qlen, np.column_stack((qvector, compton_rotavg)))
    np.savetxt("compton.del_%s" % qlen, np.column_stack((qvector, compton)))
    assert round(atomic_3d[0, 0, 0], 1) == 66.0, "I_atomic(q = 0) != 66"
    assert round(molecular_3d[0, 0, 0], 1) == 34.0, "I_mol(q = 0) != 34"
    assert round(iam_3d[0, 0, 0], 0) == 100.0, "H2O I_total(q = 0) != 100"
    assert round(atomic_rotavg[0], 1) == 66.0, "I_atomic_rotavg(q = 0) != 66"
    assert round(molecular_rotavg[0], 1) == 34.0, "I_mol_rotavg(q = 0) != 34"
    assert round(iam_total_rotavg[0], 1) == 100.0, "H20 I_total_rotavg(q = 0) != 100"
    delta_total = 100 * (iam_1d - iam_total_rotavg) / iam_1d
    delta_atomic = 100 * (atomic - atomic_rotavg) / atomic
    delta_molecular = 100 * (molecular - molecular_rotavg) / molecular
    delta_compton = 100 * (compton - compton_rotavg) / compton
    assert (
        round(np.sum(delta_atomic) / qlen, 1) == 0.0
    ), "Atomic 3d rotavg is not equal to analytic IAM..."
    assert (
        round(np.sum(delta_compton) / qlen, 1) == 0.0
    ), "Compton 3d rotavg is not equal to analytic IAM..."
    assert (
        round(np.sum(delta_molecular) / qlen, 1) < 0.5
    ), "Molecular 3d rotavg is not equal to analytic IAM..."
    assert (
        round(np.sum(delta_total) / qlen, 1) < 0.5
    ), "Ewald rotavg is not equal to analytic IAM..."

