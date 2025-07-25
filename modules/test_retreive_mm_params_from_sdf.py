from openff.toolkit.topology import Molecule, Topology
from openff.toolkit.typing.engines.smirnoff import ForceField
from openmm import HarmonicBondForce
from openmm import HarmonicAngleForce
from openmm import unit
from rdkit import Chem
import numpy as np
import sys

# Step 1: Load the SDF with RDKit WITHOUT removing hydrogens
rdkit_mol = Chem.SDMolSupplier("converted.sdf", removeHs=False)[0]

# Step 2: Convert to OpenFF Molecule, preserving explicit atoms
off_mol = Molecule.from_rdkit(rdkit_mol, allow_undefined_stereo=True, hydrogens_are_explicit=True)

# Step 3: Build the Topology
top = Topology.from_molecules(off_mol)

# Step 4: Check atom counts
print("RDKit atoms:", rdkit_mol.GetNumAtoms())
print("OpenFF molecule atoms:", off_mol.n_atoms)
print("OpenFF topology atoms:", top.n_atoms)

# Now add the forcfield
ff = ForceField("openff_unconstrained-2.0.0.offxml")
#ff = ForceField("openff-2.1.0.offxml")  # this one restrains C-H bonds and doesn't give me the bond strengths

# Create an OpenMM system
openmm_system = ff.create_openmm_system(top)
print("OpenMM system created with", openmm_system.getNumParticles(), "particles.")

# Get the HarmonicBondForce from the OpenMM system
bond_force = next(f for f in openmm_system.getForces() if isinstance(f, HarmonicBondForce))

# Get the list of atoms for type info
atoms = list(top.atoms)
print(atoms)

nbonds = bond_force.getNumBonds()
print(f"nbonds from bond_force: {nbonds}")
k_kcal_per_ang2_array = np.zeros(nbonds)
print(k_kcal_per_ang2_array)

# Loop through the bonds in the OpenMM system
for bond_index in range(nbonds):
    atom1_idx, atom2_idx, length, k = bond_force.getBondParameters(bond_index)

    atom1 = atoms[atom1_idx]
    atom2 = atoms[atom2_idx]

    length_angstrom = length.value_in_unit(unit.angstrom)
    k_kcal_per_ang2 = k.value_in_unit(unit.kilocalories_per_mole / unit.angstrom**2)
    k_kcal_per_ang2_array[bond_index] = k_kcal_per_ang2

    print(f"Bond {bond_index}: {atom1.symbol}-{atom2.symbol} "
          f"({atom1_idx}-{atom2_idx})")
    print(f"  Length: {length_angstrom:.3f} Å")
    print(f"  Force constant: {k_kcal_per_ang2} kcal/(mol Å^2)")

print('Final array:')
print(k_kcal_per_ang2_array)

angles_bool = False
if angles_bool:
    #### Angles
    # Find the angle force in the system
    angle_force = next(f for f in openmm_system.getForces() if isinstance(f, HarmonicAngleForce))
    
    print(f"Number of angle terms: {angle_force.getNumAngles()}")
    
    # Get the atoms list for atom symbols
    atoms = list(top.atoms)

    # Loop through all angles
    for angle_index in range(angle_force.getNumAngles()):
        a1_idx, a2_idx, a3_idx, theta0, k = angle_force.getAngleParameters(angle_index)
    
        a1 = atoms[a1_idx]
        a2 = atoms[a2_idx]
        a3 = atoms[a3_idx]
    
        angle_deg = theta0.value_in_unit(unit.degree)
        k_kcal_per_rad2 = k.value_in_unit(unit.kilocalories_per_mole / unit.radian**2)
    
        print(f"Angle {angle_index}: {a1.symbol}-{a2.symbol}-{a3.symbol} "
              f"({a1_idx}-{a2_idx}-{a3_idx})")
        print(f"  Equilibrium angle: {angle_deg:.2f}°")
        print(f"  Force constant: {k_kcal_per_rad2:.2f} kcal/(mol·rad²)")

