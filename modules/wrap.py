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
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        inelastic=True,
        pcd_mode=False,
        noise=0,
        sa_starting_temp=0.2,
        nmfile = "nm/chd_normalmodes.txt",
        hydrogen_modes = np.arange(28, 36),  # CHD hydrogen modes
        sa_mode_indices = np.arange(0, 28),  # CHD, "non-hydrogen" modes
        ga_mode_indices = np.arange(0, 28),  # CHD, "non-hydrogen" modes
        sa_nsteps=8000,
        ga_nsteps=40000,
        ho_indices1 = np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]),  # chd (C-C bonds)
        ho_indices2 = np.array([
            [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ]),  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)
        angular_bool=False,   # use HO terms on the angles
        angular_indices = np.array([[6, 12, 0, 2, 1, 3, 2, 4, 3, 5, 4, 4, 1, 1], 
                                    [0, 5,  1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0, 0], 
                                    [7, 13, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 7, 6]]),  # chd (non-C-C-C angles: C-C-H, H-C-H angles)
        sa_step_size=0.01,
        ga_step_size=0.01,
        sa_harmonic_factor=(0.01, 0.01),
        ga_harmonic_factor=(0.01, 0.01),
        sa_angular_factor=0.1,
        ga_angular_factor=0.1,
        nrestarts=5,
        non_h_modes_only=False,  # only include "non-hydrogen" modes
        hf_energy=True,  # run PySCF HF energy
        results_dir="tmp_",
        rmsd_indices = np.array([0, 1, 2, 3, 4, 5]), # chd non-hydrogen atoms
        bond_indices = np.array([0, 5]),     # e.g. chd ring-opening bond
        angle_indices = np.array([6, 3, 12]), # e.g. NMM methyl group motion angle
        dihedral_indices = np.array([0, 1, 4, 5]), # e.g. chd ring-opening dihedral
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

        qlen = len(qvector)
        electron_mode = False
        twod_mode = False

        def xyz2iam(xyz, atomic_numbers, compton_array):
            """convert xyz file to IAM signal"""
            iam, atomic, molecular, compton = x.iam_calc(
                atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
            )
            return iam

        #############################
        ### arguments             ###
        #############################
        _, _, atomlist, starting_xyz = m.read_xyz(start_xyz_file)
        _, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        compton_array = x.compton_spline(atomic_numbers, qvector)
        starting_iam = xyz2iam(starting_xyz, atomic_numbers, compton_array)
        reference_iam = xyz2iam(reference_xyz, atomic_numbers, compton_array)

        natoms = starting_xyz.shape[0]
        displacements = sa.read_nm_displacements(nmfile, natoms)
        nmodes = displacements.shape[0]
        aa, bb, cc = x.read_iam_coeffs()
        compton, atomic_total, pre_molecular = x.atomic_pre_molecular(
            atomic_numbers,
            qvector,
            aa,
            bb,
            cc,
            electron_mode,
        )

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

        if target_file_ext == '.xyz':
            # read from target xyz file
            _, _, atomlist, target_xyz = m.read_xyz(target_file)
            target_iam = xyz2iam(target_xyz, atomic_numbers, compton_array)

            #target_iam_file = "tmp_/TARGET_IAM_%s.dat" % run_id
            # save target IAM file before noise is added
            #print("Saving data to %s ..." % target_iam_file)
            #np.savetxt(target_iam_file, np.column_stack((qvector, target_iam)))

            ### ADDITION OF RANDOM NOISE
            constant_noise_bool = False
            noise_data_file = "noise/noise.dat"
            if constant_noise_bool and os.path.exists(noise_data_file):
                # read the noise from a file
                print('reading noise data from %s' % noise_data_file)
                noise_array = np.loadtxt(noise_data_file)
                # resize to length of q and scale magnitude
                noise_array = noise * noise_array[0 : qlen]
            else:
                # generate random noise here instead of reading from file
                mu = 0  # normal distribution with mean of mu
                sigma = noise
                print('Randomly generating noise from normal dist... sigma = %3.2f' % sigma)
                noise_array = sigma * np.random.randn(qlen) + mu
            target_function = target_iam + noise_array  # define target_function
        elif target_file_ext == '.dat':
            # if target file is a data file, read as target_function
            target_function = np.loadtxt(target_file)
            excitation_factor = 0.057
            target_function /= excitation_factor
        else:
            print('Error: target_file must be a .xyz or .dat file!')


        # save target function to file if it doesn't exist
        if not os.path.exists(target_function_file):
            print("Saving data to %s ..." % target_function_file)
            np.savetxt(target_function_file, np.column_stack((qvector, target_function)))
        print(target_function)

        # load target function from file
        #if os.path.exists(target_function_file):
        #    print("Loading data from %s ..." % target_function_file)
        #    target_function = np.loadtxt(target_function_file)[:, 1]
        #    print(target_function)
        #else:
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
                atomic_total,
                pre_molecular,
                aa,
                bb,
                cc,
                sa_step_size_array,
                ho_indices1,
                ho_indices2,
                angular_indices,
                starting_temp,
                nsteps,
                inelastic,
                harmonic_factor,
                angular_factor,
                pcd_mode,
                electron_mode,
                twod_mode,
                angular_bool,
            )
            print("f_best (SA): %9.8f" % f_best)

        ### analysis on xyz_best
        analysis_bool = False
        if analysis_bool:
            # bond-length of interest
            bond_distance = np.linalg.norm(xyz_best[bond_indices[0], :] - xyz_best[bond_indices[1], :])
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
            # rmsd compared to target
            # Kabsch rotation to target
            rmsd, r = m.rmsd_kabsch(xyz_best, target_xyz, rmsd_indices)
            # MAPD compared to target
            mapd = m.mapd_function(xyz_best, target_xyz, rmsd_indices)
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
            # save target xyz
            m.write_xyz(
                "%s/%s_target.xyz" % (results_dir, run_id),
                "run_id: %s" % run_id,
                atomlist,
                target_xyz,
            )
        else:
            bond_distance, angle_degrees, dihedral = 0, 0, 0
            rmsd, mapd, e_mol = 0, 0, 0
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
        #m.write_xyz("tmp_/%s_result.xyz" % run_id, "result", atomlist, xyz_best)
        # predicted data
        if twod_mode:
            np.savetxt("%s/%s_%s.dat" % (results_dir, run_id, f_best_str), predicted_best)
            np.savetxt("%s/%s_result.dat" % (results_dir, run_id), predicted_best)
        else:
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

    def chd_2D(
        self,
        run_id,
        start_xyz_file,
        reference_xyz_file,
        target_xyz_file,
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        sa_nsteps=2000,
        sa_step_size=0.01,
        sa_starting_temp=0.2,
        sa_harmonic_factor=0.01,
        sa_n_restarts=1,  # entire thing repeats n_restarts times
        non_h_modes_only=False,  # only include "non-hydrogen" modes
    ):
        """
        simple fitting to CHD 2D data
        """
        #############################
        ######### Inputs ############
        # run_id_ : define a number to label the start of the output filenames
        # start_xyz_file : xyz file containing starting positions of the atoms
        # target_xyz_file : xyz file containing target positions of the atoms
        #############################

        run_id = str(run_id).zfill(2)  # pad with zeros
        qlen = len(qvector)
        inelastic, electron_mode = True, False
        twod_mode = True

        def xyz2iam(xyz, atomlist):
            """convert xyz file to IAM signal"""
            atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
            (
                iam_total,
                atomic,
                molecular,
                atomic_factor_array,
                rotavg,
                qx,
                qy,
                qz,
            ) = x.iam_calc_2d(atomic_numbers, xyz, qvector)
            return iam_total, atomic, qx, qy, qz

        #############################
        ### arguments             ###
        #############################
        _, _, atomlist, starting_xyz = m.read_xyz(start_xyz_file)
        _, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
        _, _, atomlist, target_xyz = m.read_xyz(target_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        starting_iam, atomic, qx, qy, qz = xyz2iam(starting_xyz, atomlist)
        reference_iam, atomic, qx, qy, qz = xyz2iam(reference_xyz, atomlist)
        target_iam, atomic, qx, qy, qz = xyz2iam(target_xyz, atomlist)

        natoms = starting_xyz.shape[0]
        nmfile = "nm/chd_normalmodes.txt"
        displacements = sa.read_nm_displacements(nmfile, natoms)
        nmodes = displacements.shape[0]

        if non_h_modes_only:
            mode_indices = np.arange(0, 28)  # CHD, "non-hydrogen" modes
        else:
            mode_indices = np.arange(0, nmodes)  # CHD, all modes
            # mode_indices = np.arange(28, nmodes)  # CHD, only "hydrogen" modes
        print("including modes:")
        print(mode_indices)

        pcd_mode = False

        # hydrogen modes damped
        hydrogen_modes = np.arange(28, nmodes)  # CHD hydrogen modes
        sa_h_mode_modification = np.ones(nmodes)
        for i in hydrogen_modes:
            sa_h_mode_modification[i] = 0.2
        sa_step_size_array = sa_step_size * np.ones(nmodes) * sa_h_mode_modification

        # ho_indices = [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]  # chd (C-C bonds)
        ho_indices = [
            [0, 1, 2, 3, 4, 6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5, 7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ]  # chd (C-C and C-H bonds)

        ho_indices = [
            [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ]  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)

        #############################
        ### end arguments         ###
        #############################

        ### Rarely edit after this...

        #############################
        ### Initialise some stuff ###
        #############################

        ### ADDITION OF RANDOM NOISE
        noise_bool = False
        noise = 0
        if noise_bool:
            mu = 0  # normal distribution with mean of mu
            sigma = noise
            noise_array = sigma * np.random.randn(qlen) + mu
            target_iam += noise_array
        ###

        # define target_function
        # target_function = 100 * (target_iam / reference_iam - 1)
        target_function = target_iam

        #################################
        ### End Initialise some stuff ###
        #################################

        for k_restart in range(sa_n_restarts):
            f_best_ = 1e9
            # Run simulated annealing
            (
                f_best,
                f_xray_best,
                predicted_best,
                xyz_best,
            ) = sa.simulated_annealing_modes_ho(
                atomlist,
                starting_xyz,
                reference_xyz,
                displacements,
                mode_indices,
                target_function,
                qvector,
                sa_step_size_array,
                ho_indices,
                sa_starting_temp,
                sa_nsteps,
                inelastic,
                sa_harmonic_factor,
                pcd_mode,
                electron_mode,
                twod_mode,
            )
            print("f_best (SA): %9.8f" % f_best)
            ### save xyz_array as an xyz trajectory
            #if xyz_save:
            #    print("saving xyz array...")
            #    fname = "tmp_/save_array.xyz"
            #    m.write_xyz_traj(fname, atomlist, xyz_array)

            # store best values from the n_trials
            if f_best < f_best_:
                f_best_, f_xray_best_, predicted_best_, xyz_best_ = (
                    f_best,
                    f_xray_best,
                    predicted_best,
                    xyz_best,
                )

            print("writing to xyz... (f: %10.8f)" % f_xray_best)
            f_best_str = ("%10.8f" % f_xray_best).zfill(12)
            m.write_xyz(
                "tmp_/%s_%s.xyz" % (run_id, f_best_str),
                "run_id: %s" % run_id,
                atomlist,
                xyz_best,
            )
            # also write final xyz as "result.xyz"
            m.write_xyz("tmp_/%s_result.xyz" % run_id, "result", atomlist, xyz_best)
            m.write_xyz("tmp_/result.xyz", "result", atomlist, xyz_best)
            # predicted data
            if twod_mode:
                np.savetxt("tmp_/%s_%s.dat" % (run_id, f_best_str), predicted_best_)
                np.savetxt("tmp_/%s_result.dat" % run_id, predicted_best_)
            else:
                np.savetxt(
                    "tmp_/%s_%s.dat" % (run_id, f_best_str),
                    np.column_stack((qvector, predicted_best_)),
                )

        ### Final save to files
        # target xyz
        m.write_xyz(
            "tmp_/%s_target.xyz" % run_id,
            "run_id: %s" % run_id,
            atomlist,
            target_xyz,
        )
        # also write target xyz as "target.xyz"
        m.write_xyz("tmp_/target.xyz", "target", atomlist, target_xyz)
        # target function
        np.savetxt("tmp_/%s_target_function.dat" % run_id, target_function)
        # save raw target data:
        np.savetxt("tmp_/%s_target_iam.dat" % run_id, target_iam)
        # save starting IAM signal
        np.savetxt("tmp_/%s_starting_iam.dat" % run_id, starting_iam)

        return  # end function
