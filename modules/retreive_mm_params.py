from openff.toolkit.topology import Molecule, Topology
from openff.toolkit.typing.engines.smirnoff import ForceField
from openmm import HarmonicBondForce
from openmm import unit
import numpy as np

class Retreive_mm_params:
    def __init__(self):
        pass

    def create_topology_from_sdf(self, sdf_file, ff_file="openff_unconstrained-2.0.0.offxml")
        '''creates an OpenMM system (topology, forcefield) from the sdf_file'''

        # Load molecule from sdf
        molecule = Molecule.from_file(sdf_file)

        # Optionally generate conformers if none present or to optimize
        # molecule.generate_conformers()
        
        # Create topology from this molecule
        topology = Topology.from_molecules([molecule])
        
        #print(f"Number of atoms: {topology.n_atoms}")
        #print(f"Number of bonds: {topology.n_bonds}")
        #print("Atoms:", [atom.symbol for atom in molecule.atoms])
        
        # Create topology from the molecule
        topology = Topology.from_molecules([molecule])
        
        #print(f"Topology created with {topology.n_atoms} atoms and {topology.n_bonds} bonds.")
        
        # Now add the forcfield
        ff = ForceField(ff_file)
        #ff = ForceField("openff-2.1.0.offxml")  # this one restrains C-H bonds and doesn't give me the bond strengths
        
        # Create an OpenMM system
        openmm_system = ff.create_openmm_system(topology)
        #print("OpenMM system created with", openmm_system.getNumParticles(), "particles.")
        return openmm_system
 
    def retreive_lengths_k_values(self, openmm_system):
        '''gets the bond-lengths and bond-strengths from the OpenMM system (topology, forcefield)'''
       
        # Get the HarmonicBondForce from the OpenMM system
        bond_force = next(f for f in openmm_system.getForces() if isinstance(f, HarmonicBondForce))
        
        # Get the list of atoms for type info
        atoms = list(topology.atoms)

        nbonds = bond_force.getNumBonds()
        k_kcal_per_ang2_array = np.zeros(nbonds)
        length_angstrom_array = np.zeros(nbonds)

        # Loop through the bonds in the OpenMM system
        for bond_index in range(nbonds):
            atom1_idx, atom2_idx, length, k = bond_force.getBondParameters(bond_index)
        
            #atom1 = atoms[atom1_idx]
            #atom2 = atoms[atom2_idx]
        
            length_angstrom = length.value_in_unit(unit.angstrom)
            length_angstrom_array[bond_index] = length_angstrom
            k_kcal_per_ang2 = k.value_in_unit(unit.kilocalories_per_mole / unit.angstrom**2)
            k_kcal_per_ang2_array[bond_index] = k_kcal_per_ang2
        
            #print(f"Bond {bond_index}: {atom1.symbol}-{atom2.symbol} "
            #      f"({atom1_idx}-{atom2_idx})")
            #print(f"  Length: {length_angstrom:.3f} Å")
            #print(f"  Force constant: {k_kcal_per_ang2} kcal/(mol Å^2)")

        return length_angstrom_array, k_kcal_per_ang2_array
        
