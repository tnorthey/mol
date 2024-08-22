import sys
import numpy as np

# my modules
import modules.mol as mol
import modules.x as xray

# create class objects
m = mol.Xyz()
x = xray.Xray()

xyz_file = str(sys.argv[1])

#qmin, qmax, qlen = 0.1, 24, 241
qmin, qmax, qlen = 0.00000000001, 24, 241
qvector = np.linspace(qmin, qmax, qlen, endpoint=True)

_, _, atomlist, xyz = m.read_xyz(xyz_file)

electron_mode=False
inelastic = True
atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
compton_array = x.compton_spline(atomic_numbers, qvector)
 
# """calculate IAM molecular scattering curve for atoms, xyz, qvector"""
iam, atomic, molecular, compton = x.iam_calc(
        atomic_numbers,
        xyz,
        qvector,
        electron_mode,
        inelastic,
        compton_array,
    )

np.savetxt('iam_total.dat', np.column_stack(( qvector, iam )) )
np.savetxt('iam_atomic.dat', np.column_stack(( qvector, atomic )) )
np.savetxt('iam_molecular.dat', np.column_stack(( qvector, molecular )) )
np.savetxt('iam_compton.dat', np.column_stack(( qvector, compton )) )

