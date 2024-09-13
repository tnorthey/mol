import os
import numpy as np
from numpy import linalg as LA
from pyscf import gto, scf

# my modules
import modules.mol as mol
import modules.x as xray
import modules.sa as sa

# create class objects
m = mol.Xyz()
x = xray.Xray()
sa = sa.Annealing()


#############################
class Wrapper:
    """wrapper functions for simulated annealing strategies"""

    def __init__(self):
        pass

    def run_1D(
        self,
        run_id,
        start_xyz_file,
        reference_xyz_file,
        target_file,
        results_dir="tmp_",
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        noise=0,
        noise_data_file="noise/noise.dat",
        inelastic=True,
        pcd_mode=False,
        ewald_mode=False,
        sa_starting_temp=0.2,
        nmfile="nm/chd_normalmodes.txt",
        hydrogen_modes=np.arange(28, 36),  # CHD hydrogen modes
        sa_mode_indices=np.arange(0, 28),  # CHD, "non-hydrogen" modes
        ga_mode_indices=np.arange(0, 28),  # CHD, "non-hydrogen" modes
        sa_nsteps=8000,
        ga_nsteps=40000,
        ho_indices1=np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]),  # chd (C-C bonds)
        ho_indices2=np.array(
            [
                [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
                [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
            ]
        ),  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
        angular_bool=False,  # use HO terms on the angles
        angular_indices1=np.array(
            [
                [6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
                [0, 5, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
                [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6],
            ]
        ),  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        angular_indices2=np.array(
            [
                [6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1],
                [0, 5, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0],
                [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6],
            ]
        ),  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        sa_step_size=0.01,
        ga_step_size=0.01,
        sa_harmonic_factor=(0.01, 0.01),
        ga_harmonic_factor=(0.01, 0.01),
        sa_angular_factor=(0.1, 0.1),
        ga_angular_factor=(0.1, 0.1),
        nrestarts=5,
        non_h_modes_only=False,  # only include "non-hydrogen" modes
        hf_energy=True,  # run PySCF HF energy
        rmsd_indices=np.array([0, 1, 2, 3, 4, 5]),  # chd non-hydrogen atoms
        bond_indices=np.array([0, 5]),  # e.g. chd ring-opening bond
        angle_indices=np.array([6, 3, 12]),  # e.g. NMM methyl group motion angle
        dihedral_indices=np.array([0, 1, 4, 5]),  # e.g. chd ring-opening dihedral
    ):
        """
        simple fitting to CHD 1D data
        """
        #############################
        ######### Inputs ############
        # run_id : define a number to label the start of the output filenames
        # start_xyz_file : xyz file containing starting positions of the atoms
        # target_xyz_file : xyz file containing target positions of the atoms
        #
        #############################

        qmin, qmax, qlen = qvector[0], qvector[-1], len(qvector)
        electron_mode = False
        twod_mode = False
        aa, bb, cc = x.read_iam_coeffs()
        tlen = 1 * qlen
        plen = 2 * qlen  # more grid points in phi because it spans more
        th_min, th_max = 0, np.pi
        ph_min, ph_max = 0, 2 * np.pi
        th = np.linspace(th_min, th_max, tlen, endpoint=True)
        ph = np.linspace(
            ph_min, ph_max, plen, endpoint=False
        )  # skips 2pi as f(0) = f(2pi)
        def xyz2iam(xyz, atomic_numbers, compton_array, ewald_mode):
            """convert xyz file to IAM signal"""
            if ewald_mode:
                (
                    iam,
                    atomic,
                    molecular,
                    compton,
                    pre_molecular,
                    iam_total_rotavg,
                    atomic_rotavg,
                    molecular_rotavg,
                    compton_rotavg,
                ) = x.iam_calc_ewald(
                    atomic_numbers,
                    xyz,
                    qvector,
                    inelastic,
                    compton_array,
                )
            else:
                iam, atomic, molecular, compton, pre_molecular = x.iam_calc(
                    atomic_numbers,
                    xyz,
                    qvector,
                    electron_mode,
                    inelastic,
                    compton_array,
                )
            return iam, atomic, compton, pre_molecular

        def spherical_rotavg(f):
            # rotatational average includes area element sin(th)dth*dph
            # first sum over phi,
            f_rotavg_phi = np.sum(f, axis=2)
            # multiply by the sin(th) term,
            for j in range(tlen):
                f_rotavg_phi[:, j] *= np.sin(th[j])
            dth = th[1] - th[0]
            dph = (ph_max - ph_min) / plen
            f_rotavg = (
                np.sum(f_rotavg_phi, axis=1) * dth * dph / (4 * np.pi)
            )
            return f_rotavg

        #############################
        ### arguments             ###
        #############################
        _, _, atomlist, starting_xyz = m.read_xyz(start_xyz_file)
        _, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        compton_array = x.compton_spline(atomic_numbers, qvector)
        starting_iam, atomic, compton, pre_molecular = xyz2iam(
            starting_xyz, atomic_numbers, compton_array, ewald_mode
        )
        reference_iam, atomic, compton, pre_molecular = xyz2iam(
            reference_xyz, atomic_numbers, compton_array, ewald_mode
        )

        natoms = starting_xyz.shape[0]
        displacements = sa.read_nm_displacements(nmfile, natoms)
        nmodes = displacements.shape[0]

        # hydrogen modes damped
        sa_h_mode_modification = np.ones(nmodes)
        for i in hydrogen_modes:
            sa_h_mode_modification[i] = 0.2
        sa_step_size_array = sa_step_size * np.ones(nmodes) * sa_h_mode_modification

        #############################
        ### end arguments         ###
        #############################

        ### Rarely edit after this...

        #############################
        ### Initialise some stuff ###
        #############################

        print(f"Target: {target_file}")
        filename, target_file_ext = os.path.splitext(target_file)
        target_function_file = "%s/TARGET_FUNCTION_%s.dat" % (results_dir, run_id)

        if target_file_ext == ".xyz":
            # read from target xyz file
            _, _, atomlist, target_xyz = m.read_xyz(target_file)
            target_iam, atomic, compton, pre_molecular = xyz2iam(target_xyz, atomic_numbers, compton_array, ewald_mode)

            # target_iam_file = "tmp_/TARGET_IAM_%s.dat" % run_id
            # save target IAM file before noise is added
            # print("Saving data to %s ..." % target_iam_file)
            # np.savetxt(target_iam_file, np.column_stack((qvector, target_iam)))

            ### ADDITION OF RANDOM NOISE
            noise_file_bool = True
            # noise_data_file = "noise/noise.dat"
            print(f"checking if {noise_data_file} exists...")
            if noise_file_bool and os.path.exists(noise_data_file):
                # read the noise from a file
                print(f"Yes. Reading noise data from {noise_data_file}")
                noise_array = np.loadtxt(noise_data_file)
                # resize to length of q and scale magnitude
                noise_array = noise * noise_array[0:qlen]
            else:
                print(f"{noise_data_file} does not exist.")
                # generate random noise here instead of reading from file
                mu = 0  # normal distribution with mean of mu
                sigma = noise
                print(
                    "Randomly generating noise from normal dist... sigma = %3.2f"
                    % sigma
                )
                noise_array = sigma * np.random.randn(qlen) + mu
            # if Ewald mode the noise_array has to be 3D
            if ewald_mode:
                noise_array_3d = np.zeros((qlen, tlen, plen))
                for i in range(plen):
                    for j in range(tlen):
                        noise_array_3d[:, j, i] = noise_array
                noise_array = noise_array_3d  # redefine as the 3D array
            target_function = target_iam + noise_array  # define target_function
        elif target_file_ext == ".dat":
            # if target file is a data file, read as target_function
            target_function = np.loadtxt(target_file)
            excitation_factor = 0.057
            target_function /= excitation_factor
            target_xyz = starting_xyz  # added simply to run the rmsd analysis later compared to this
        else:
            print("Error: target_file must be a .xyz or .dat file!")

        # save target function to file if it doesn't exist
        #if not os.path.exists(target_function_file):
        print("Saving data to %s ..." % target_function_file)
        if ewald_mode:
            target_function_r = spherical_rotavg(target_function)
            target_function = target_function_r

        np.savetxt(
            target_function_file, np.column_stack((qvector, target_function))
        )
        print(target_function)

        # load target function from file
        # if os.path.exists(target_function_file):
        #    print("Loading data from %s ..." % target_function_file)
        #    target_function = np.loadtxt(target_function_file)[:, 1]
        #    print(target_function)
        # else:
        #    target_function = target_iam
        #    print("Saving data to %s ..." % target_function_file)
        #    np.savetxt(target_function_file, np.column_stack((qvector, target_function)))

        #################################
        ### End Initialise some stuff ###
        #################################
        # start
        xyz_best = starting_xyz  # initialise xyz_best
        for i in range(nrestarts):
            starting_xyz = xyz_best  # each restart starts at the previous xyz_best
            if i < nrestarts - 1:  # annealing mode
                print(f"Run {i}: SA")
                nsteps = sa_nsteps
                starting_temp = sa_starting_temp
                harmonic_factor = sa_harmonic_factor
                angular_factor = sa_angular_factor
                mode_indices = sa_mode_indices
            else:  # greedy algorithm mode
                print(f"Run {i}: GA")
                nsteps = ga_nsteps
                starting_temp = 0
                harmonic_factor = ga_harmonic_factor
                angular_factor = ga_angular_factor
                mode_indices = ga_mode_indices
            # Run simulated annealing
            (
                f_best,
                f_xray_best,
                predicted_best,
                xyz_best,
            ) = sa.simulated_annealing_modes_ho(
                atomic_numbers,
                starting_xyz,
                displacements,
                mode_indices,
                target_function,
                reference_iam,
                qvector,
                compton,
                atomic,
                pre_molecular,
                aa,
                bb,
                cc,
                sa_step_size_array,
                ho_indices1,
                ho_indices2,
                angular_indices1,
                angular_indices2,
                starting_temp,
                nsteps,
                inelastic,
                harmonic_factor,
                angular_factor,
                pcd_mode,
                electron_mode,
                ewald_mode,
                angular_bool,
            )
            print("f_best (SA): %9.8f" % f_best)

        ### analysis on xyz_best
        # bond-length of interest
        bond_distance = np.linalg.norm(
            xyz_best[bond_indices[0], :] - xyz_best[bond_indices[1], :]
        )
        # angle of interest
        p0 = np.array(xyz_best[angle_indices[0], :])
        p1 = np.array(xyz_best[angle_indices[1], :])  # central point
        p2 = np.array(xyz_best[angle_indices[2], :])
        angle_degrees = m.angle_2p_3d(p0, p1, p2)
        # dihedral of interest
        p0 = np.array(xyz_best[dihedral_indices[0], :])
        p1 = np.array(xyz_best[dihedral_indices[1], :])
        p2 = np.array(xyz_best[dihedral_indices[2], :])
        p3 = np.array(xyz_best[dihedral_indices[3], :])
        dihedral = m.new_dihedral(np.array([p0, p1, p2, p3]))
        rmsd_target_bool = True
        if rmsd_target_bool:
            # rmsd compared to target
            # Kabsch rotation to target
            rmsd, r = m.rmsd_kabsch(xyz_best, target_xyz, rmsd_indices)
            # MAPD compared to target
            mapd = m.mapd_function(xyz_best, target_xyz, rmsd_indices)
            # save target xyz
            m.write_xyz(
                "%s/%s_target.xyz" % (results_dir, run_id),
                ".dat file case: starting_xyz (not target_xyz)",
                atomlist,
                target_xyz,
            )
        else:
            bond_distance, angle_degrees, dihedral = 0, 0, 0
            rmsd, mapd, e_mol = 0, 0, 0
        # HF energy with PySCF
        if hf_energy:
            mol = gto.Mole()
            arr = []
            for i in range(len(atomlist)):
                arr.append((atomlist[i], xyz_best[i]))
            mol.atom = arr
            mol.basis = "6-31g*"
            mol.build()
            rhf_mol = scf.RHF(mol)  # run RHF
            e_mol = rhf_mol.kernel()
        else:
            e_mol = 0
        # encode the analysis values into the xyz header
        header_str = "%12.8f %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f" % (
            f_xray_best,
            rmsd,
            bond_distance,
            angle_degrees,
            dihedral,
            e_mol,
            mapd,
        )
        ### write best structure to xyz file
        print("writing to xyz... (f: %10.8f)" % f_xray_best)
        f_best_str = ("%10.8f" % f_xray_best).zfill(12)
        m.write_xyz(
            "%s/%s_%s.xyz" % (results_dir, run_id, f_best_str),
            header_str,
            atomlist,
            xyz_best,
        )
        ### Final save to files
        # also write final xyz as "result.xyz"
        # m.write_xyz("tmp_/%s_result.xyz" % run_id, "result", atomlist, xyz_best)
        # predicted data
        if ewald_mode:
            predicted_best_r = spherical_rotavg(predicted_best)
            predicted_best = predicted_best_r

        np.savetxt(
            "%s/%s_%s.dat" % (results_dir, run_id, f_best_str),
            np.column_stack((qvector, predicted_best)),
        )
        return  # end function

    #####################################
    #####################################
    #####################################
    #####################################
    #####################################
    #####################################
