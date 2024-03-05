import numpy as np
import sys

fname = sys.argv[1]

arr = np.loadtxt(fname)
#print(arr[:, 4])
print("%12.8f" % np.mean(arr[:, 4]))
