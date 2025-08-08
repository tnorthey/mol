import numpy as np
import sys

# my modules
import modules.mol as mol

# create class objects
m = mol.Xyz()

# load xyz
xyz_file = sys.argv[1]
_, _, atomlist, xyz = m.read_xyz(xyz_file)
#print(atomlist)
#print(xyz)

#dihedral_indices = [6, 3, 5, 10]
dihedral_indices = [5, 10, 0, 1]

# dihedral of interest
p0 = np.array(xyz[dihedral_indices[0], :])
p1 = np.array(xyz[dihedral_indices[1], :])
p2 = np.array(xyz[dihedral_indices[2], :])
p3 = np.array(xyz[dihedral_indices[3], :])

dihedral = m.new_dihedral(np.array([p0, p1, p2, p3]))

print('%12.8f' % dihedral)
