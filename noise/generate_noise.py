import numpy as np
'''randomly generate noise via a normal distribution with mu = 0, sigma = 1 '''

N = 1000  # arbitrary array length that gets resized in wrap.py
noise = 1 # "unit" noise
# normal distribution with mean of mu
mu = 0
sigma = noise

for i in range(20):
    noise_array = sigma * np.random.randn(N) + mu
    i_str = str(i).zfill(2)
    np.savetxt(f'noise_{i_str}.dat', noise_array)
