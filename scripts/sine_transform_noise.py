'''
example run: python sine_transform.y 81 0.01 1
'''

import numpy as np
import sys

# my modules
import modules.mol as mol
import modules.x as xray
# create class objects
m = mol.Xyz()
x = xray.Xray()

qmax_index = int(sys.argv[1])  # index of qmax = len(qvector) e.g. 41, 81
k = float(sys.argv[2])         # damping factor, e.g. 0.01
sigma = float(sys.argv[3])     # noise width, e.g. 1, 2, 4, 8, ...

noisefile = "noise/noise.dat"
filename = "sine_transform/iam_molecular.dat"

# read .dat file of Imol(q) - iam_molecular.dat
print('reading %s' % filename)
A = np.loadtxt(filename)
noise = np.loadtxt(noisefile)
noise = noise[:qmax_index]

q = A[ : qmax_index, 0]
print(q)
qlen = len(q)
fmol = A[ : qmax_index, 1]
#print(fmol)

# Carbon atomic factor:
atom_number = 6  # Carbon
fc = x.atomic_factor(atom_number, q)

# code the sine transform .....

# code: implement f(r) = int_q qM(q) * sin(qr) * e^-kq^2, 
# with qM(q) = q Imol(q) / fc(q)^2

fmol_noise = fmol + sigma * noise

qM = q * fmol_noise / fc ** 2

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
qmax_str = str(qmax).zfill(1)
noise_str = str(sigma).zfill(1)
np.savetxt( 'sine_transform/radial_function_qmax%s_noise%s.dat' % (qmax_str, noise_str), np.column_stack(( r, fr )) )

###

