import numpy as np
'''randomly generate noise via a normal distribution with mu = 0, sigma = 1 '''

N = 1000  # arbitrary array length that gets resized in wrap.py
noise = 1 # "unit" noise
# normal distribution with mean of mu
mu = 0
sigma = noise
noise_array = sigma * np.random.randn(N) + mu
np.savetxt('noise/noise.dat', noise_array)
