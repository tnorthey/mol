import numpy as np
import molecule
import sys

qmax_index = int(sys.argv[1])
k = float(sys.argv[2])

# k = 0.01  # damping factor

filename = "iam_molecular.dat"

# read .dat file of Imol(q) - iam_molecular.dat
print('reading %s' % filename)
A = np.loadtxt(filename)
q = A[ : qmax_index, 0]
print(q)
qlen = len(q)
fmol = A[ : qmax_index, 1]
#print(fmol)

# Carbon atomic factor:
x = molecule.Xray()
atom_number = 6  # Carbon
fc = x.atomic_factor(atom_number, q)

# code the sine transform .....

# code: implement f(r) = int_q qM(q) * sin(qr) * e^-kq^2, 
# with qM(q) = q Imol(q) / fc(q)^2

qM = q * fmol / fc ** 2

# integral
rlen = 401
rmax = 5.5
r = np.linspace(0, rmax, rlen, endpoint=True)
#print(r)

fr = np.zeros(rlen)

for j in range(rlen):
    for i in range(qlen):
        fr[j] += qM[i] * np.sin( q[i] * r[j] ) * np.exp( - k * q[i] ** 2 ) / qlen

# normalise
fr /= np.max(fr)

qmax = int(qlen / 10)
qmax_str = str(qmax).zfill(2)
np.savetxt( 'radial_function_qmax%s.dat' % qmax_str, np.column_stack(( r, fr )) )

###

