from openbabel import openbabel, pybel

# Step 1: Load molecule from XYZ
mol = next(pybel.readfile("xyz", "start.xyz"))

# Step 2: Add hydrogens and generate 3D structure
#mol.addh()
#mol.make3D()  # Optionally improve geometry

# Step 3: (Optional) optimize geometry with UFF
#mol.localopt(forcefield="uff")

# Step 4: Write to SDF — this will now include correct bond orders
mol.write("sdf", "converted.sdf", overwrite=True)

