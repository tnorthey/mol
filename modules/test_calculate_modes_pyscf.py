import numpy as np
from pyscf import gto, scf, hessian
from pyscf.hessian import thermo

# === Build PySCF molecule ===
mol = gto.Mole()
mol.atom = "start.xyz"
mol.build()
mol.basis = "sto-3g"  # Use "def2-SVP" or similar for better accuracy
mol.unit = "Angstrom"
mol.build()

# === Run SCF calculation ===
mf = scf.RHF(mol)
mf.kernel()

# === Compute Hessian and run frequency analysis ===
hess = hessian.RHF(mf).kernel()
results = thermo.harmonic_analysis(mol, hess)
#print(results)
frequencies_cm1 = results["freq_wavenumber"]
mode_vectors = results["norm_mode"]  # normal modes

# Save to .npy files
np.save("normal_modes.npy", mode_vectors)
np.save("frequencies_cm1.npy", frequencies_cm1)

# === Print results ===
print("\nVibrational frequencies (cm^-1):")
for i, freq in enumerate(frequencies_cm1):
    print(f"Mode {i+1}: {freq:.2f} cm^-1")

print("\nFirst displacement vector (Mode 1):")
natoms = mol.natm
mode0 = mode_vectors[0].reshape((natoms, 3))
print(mode0)

