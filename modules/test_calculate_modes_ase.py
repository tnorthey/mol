from ase.io import read
#from ase.calculators.xtb import XTB
import ase.calculators.xtb
from ase.optimize import BFGS
from ase.vibrations import Vibrations

# Step 1: Load molecule
atoms = read("start.xyz")  # Can also be .mol, .sdf, etc.

# Step 2: Attach the XTB calculator
atoms.calc = XTB(method="GFN2-xTB")  # or "GFN1-xTB"

# Step 3: Optimize the structure
opt = BFGS(atoms)
opt.run(fmax=0.01)

# Step 4: Run vibrational analysis
vib = Vibrations(atoms)
vib.run()

# Step 5: Summary
vib.summary()

# Step 6: Access displacement vectors for each normal mode
for i in range(len(vib.get_frequencies())):
    mode = vib.get_mode(i)  # N x 3 array of displacement vectors
    freq = vib.get_frequencies()[i]
    print(f"Mode {i+1}: {freq:.2f} cm^-1")
    print(mode)

