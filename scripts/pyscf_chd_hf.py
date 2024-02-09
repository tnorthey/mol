'''
CHD HF energy
'''
import sys
import numpy as np
from pyscf import gto, scf

xyz_file = sys.argv[1]

mol = gto.Mole()
mol = gto.M(atom=xyz_file)
mol.basis = '6-31g*'
mol.build()
rhf_mol = scf.RHF(mol)  # run RHF
e_mol = rhf_mol.kernel()
print("%12.8f" % e_mol)
