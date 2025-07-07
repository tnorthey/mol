from openff.toolkit.topology import Molecule

# Load the molecule from XYZ; OpenFF will use RDKit to infer bonds
molecule = Molecule.from_file("start.xyz", file_format="xyz", allow_undefined_stereo=True)

print(molecule)
