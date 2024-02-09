'''
CHD HF energy
'''
import sys
import pyscf.gto as gto
import numpy as np

#xyz_file = sys.argv[1]

mol = gto.Mole()
atomlist = ['H', 'H']
xyz = [[0, 0, 1], [0, 0, 0]]
arr = []
for i in range(len(atomlist)):
    arr.append((atomlist[i], xyz[i]))
mol.atom = arr
print(mol.atom)
#mol = gto.M(atom=xyz_file)
mol.basis = '6-31g*'
mol.build()
# run RHF
mf = mol.RHF().run()
    
