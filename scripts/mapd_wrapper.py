import numpy as np
import sys
#
# my modules
import modules.mol as mol

# create class objects
m = mol.Xyz()

rmsd_bool = True
bond_print = False

xyz1 = str(sys.argv[1])
xyz2 = str(sys.argv[2])
# print('reading %s' % xyz1)
# print('reading %s' % xyz2)
header, comment, atomlist, xyz = m.read_xyz(xyz1)
header, comment, atomlist, target_xyz = m.read_xyz(xyz2)

non_h_indices = np.array([0, 1, 2, 3, 4, 5])  # chd
#non_h_indices = np.array([0, 1, 2, 3, 4])  # chf3
#non_h_indices = np.array([0, 1, 2, 3])  # chf3
# non_h_indices = np.array([0,1,3,5,6,10,12])  # nmm

# Kabsch rotation to target
if rmsd_bool:
    rmsd, r = m.rmsd_kabsch(xyz, target_xyz, non_h_indices)
    # print('rotating...')
    # xyz_rotated = np.dot(xyz, r.as_matrix())
    # print('RMSD = %10.8f' % rmsd)

# MAPD
#mapd = m.mapd_function(xyz, target_xyz, non_h_indices, bond_print) 
#print("CHI2 = %s, MAPD = %10.9f (percent), RMSD = %10.9f (Angstroms)" % (xyz1[-14:-4], mapd, rmsd))
#print("RMSD = %10.9f (Angstroms)" % rmsd)
print("%10.9f %s" % (rmsd, xyz1[-14:-4]))

#print('%s %10.8f' % (xyz1[3:-4], rmsd))

#outfile = "xyz_rotated.xyz"
#print('writing %s' % outfile)
#m.write_xyz(outfile, "rmsd: %s" % str(rmsd), atomlist, xyz_rotated)
