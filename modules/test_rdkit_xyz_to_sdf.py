from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import RWMol
from rdkit.Geometry import Point3D
#from rdkit.Chem import PeriodicTable
from rdkit.Chem import rdchem
import numpy as np

# Step 1: Read XYZ file manually
def read_xyz(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    num_atoms = int(lines[0])
    atom_lines = lines[2:2 + num_atoms]

    symbols = []
    coords = []
    for line in atom_lines:
        parts = line.strip().split()
        symbols.append(parts[0])
        coords.append([float(x) for x in parts[1:4]])
    return symbols, np.array(coords)

symbols, coords = read_xyz("start.xyz")

# Step 2: Build RDKit molecule
mol = RWMol()
atom_indices = []
for symbol in symbols:
    atom = Chem.Atom(symbol)
    idx = mol.AddAtom(atom)
    atom_indices.append(idx)

# Step 3: Add bonds based on distance (very simple guess)
from rdkit.Chem import rdMolTransforms

def guess_bonds(mol, coords, cutoff=1.8):
    ''' Guess bonds only by distance cutoff '''
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(coords[i] - coords[j])
            if dist < cutoff:
                mol.AddBond(i, j, Chem.rdchem.BondType.SINGLE)

# guess_bonds(mol, coords)

#pt = PeriodicTable.GetPeriodicTable()
pt = rdchem.GetPeriodicTable()

def add_bonds_smart(mol, coords, scale=1.2):
    n = len(coords)
    for i in range(n):
        ri = pt.GetRcovalent(mol.GetAtomWithIdx(i).GetAtomicNum())
        for j in range(i + 1, n):
            rj = pt.GetRcovalent(mol.GetAtomWithIdx(j).GetAtomicNum())
            max_bond = (ri + rj) * scale
            dist = np.linalg.norm(coords[i] - coords[j])
            if dist <= max_bond:
                mol.AddBond(i, j, Chem.rdchem.BondType.SINGLE)

# Then call:
add_bonds_smart(mol, coords)

# Step 4: Add 3D coordinates
conf = Chem.Conformer(len(symbols))
for i, pos in enumerate(coords):
    conf.SetAtomPosition(i, Point3D(*pos))
mol.AddConformer(conf)

mol = mol.GetMol()  # Finalize edits
Chem.SanitizeMol(mol)

# Step 5: Optimize (optional, depends on coordinates)
#AllChem.UFFOptimizeMolecule(mol)

# Step 6: Save to SDF
writer = Chem.SDWriter("converted.sdf")
writer.write(mol)
writer.close()

print("✅ Saved as converted.sdf")

