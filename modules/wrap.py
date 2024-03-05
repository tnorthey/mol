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

    def chd_1D(
        self,
        run_id,
        start_xyz_file,
        target_xyz_file,
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        noise=0,
        sa_nsteps=2000,
        ga_nsteps=2000,
        sa_step_size=0.01,
        sa_starting_temp=0.2,
        sa_harmonic_factor=(0.01, 0.01),
        nrestarts=10,
        ntrials=1,
        non_h_modes_only=False,  # only include "non-hydrogen" modes
        hf_energy=True,
        pcd_mode=False,
    ):
        """
        simple fitting to CHD 1D data
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
        twod_mode = False

        # debugging....
        print(sa_harmonic_factor)

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
        #_, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
        _, _, atomlist, target_xyz = m.read_xyz(target_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        compton_array = x.compton_spline(atomic_numbers, qvector)
        starting_iam = xyz2iam(starting_xyz, atomic_numbers, compton_array)
        #reference_iam = xyz2iam(reference_xyz, atomic_numbers, compton_array)
        target_iam = xyz2iam(target_xyz, atomic_numbers, compton_array)

        natoms = starting_xyz.shape[0]
        nmfile = "nm/chd_normalmodes.txt"
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

        #f_save = True

        # hydrogen modes damped
        hydrogen_modes = np.arange(28, nmodes)  # CHD hydrogen modes
        sa_h_mode_modification = np.ones(nmodes)
        for i in hydrogen_modes:
            sa_h_mode_modification[i] = 0.2
        sa_step_size_array = sa_step_size * np.ones(nmodes) * sa_h_mode_modification

        ho_indices1 = np.array([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]])  # chd (C-C bonds)
        # ho_indices = [
        #    [0, 1, 2, 3, 4, 6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
        #    [1, 2, 3, 4, 5, 7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        # ]  # chd (C-C and C-H bonds)

        ho_indices2 = np.array([
            [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ])  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)

        mode_indices = np.arange(0, 28)  # CHD, "non-hydrogen" modes

        #############################
        ### end arguments         ###
        #############################

        ### Rarely edit after this...

        #############################
        ### Initialise some stuff ###
        #############################

        target_function_file = "tmp_/TARGET_FUNCTION_%s.dat" % run_id
        target_iam_file = "tmp_/TARGET_IAM_%s.dat" % run_id
        target_pcd_file = "tmp_/TARGET_PCD_%s.dat" % run_id

        # save target IAM file before noise is added
        print("Saving data to %s ..." % target_iam_file)
        np.savetxt(target_iam_file, np.column_stack((qvector, target_iam)))

        if pcd_mode:
            target_pcd = 100 * (target_iam / reference_iam - 1)
            # Save PCD to file
            print("Saving data to %s ..." % target_pcd_file)
            np.savetxt(target_pcd_file, np.column_stack((qvector, target_pcd)))

        ### ADDITION OF RANDOM NOISE
        noise_bool = True
        if noise_bool:
            mu = 0  # normal distribution with mean of mu
            sigma = noise
            noise_array = sigma * np.random.randn(qlen) + mu
            target_iam += noise_array

        # define target_function
        if os.path.exists(target_function_file):
            print("Loading data from %s ..." % target_function_file)
            target_function = np.loadtxt(target_function_file)[:, 1]
            print(target_function)
        else:
            if pcd_mode:
                target_function = 100 * (target_iam / reference_iam - 1)
            else:
                target_function = target_iam
            print("Saving data to %s ..." % target_function_file)
            np.savetxt(target_function_file, np.column_stack((qvector, target_function)))
        ###
        # calculate target_f_signal for noise data compared to clean data
        if noise != 0:
            if pcd_mode:
                clean_data = target_pcd
            else:
                clean_data = target_iam
            target_f_signal = (
                np.sum((clean_data - target_function) ** 2 / np.abs(target_function))
                / qlen
            )

        # Store values for reinitialising at each trial
        xyz_best = starting_xyz  # initialise
        starting_xyz_ = starting_xyz  # store the starting xyz
        sa_nsteps_ = sa_nsteps
        sa_starting_temp_ = sa_starting_temp
        sa_harmonic_factor_ = sa_harmonic_factor
        mode_indices_ = mode_indices
        #################################
        ### End Initialise some stuff ###
        #################################
        for j in range(ntrials):
            print(f"Trial {j}")
            # reinitialise values for each trial
            xyz_best = starting_xyz_
            sa_nsteps = sa_nsteps_
            sa_starting_temp = sa_starting_temp_
            sa_harmonic_factor = sa_harmonic_factor_
            mode_indices = mode_indices_
            for i in range(nrestarts):
                starting_xyz = xyz_best

                for k in range(1):
                    #if k % 2 == 0:  # annealing mode
                    if i < nrestarts - 1:  # annealing mode
                        print(f"Run {i}: SA")
                        nsteps = sa_nsteps
                        starting_temp = sa_starting_temp
                        harmonic_factor = sa_harmonic_factor
                        mode_indices = np.arange(0, 28)  # CHD, non-hydrogen modes
                    else:  # greedy mode
                        print(f"Run {i}: GA")
                        nsteps = ga_nsteps
                        starting_temp = 0
                        harmonic_factor = (0, 0)
                        mode_indices = np.arange(0, nmodes)  # CHD, all modes
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
                        starting_temp,
                        nsteps,
                        inelastic,
                        harmonic_factor,
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

            ### save f_array
            #if f_save:
            #    print("saving f array...")
            #    fname = "tmp_/f_array_%i.dat" % i
            #    np.savetxt(fname, f_array)

            ### analysis on xyz_best
            # 0145 dihedral that describes the ring-opening
            p0 = np.array(xyz_best[0, :])
            p1 = np.array(xyz_best[1, :])
            p4 = np.array(xyz_best[4, :])
            p5 = np.array(xyz_best[5, :])
            dihedral = m.new_dihedral(np.array([p0, p1, p4, p5]))
            # r05 ring-opening bond-length
            r05 = np.linalg.norm(xyz_best[0, :] - xyz_best[5, :])
            # rmsd compared to target
            non_h_indices = np.array([0, 1, 2, 3, 4, 5])  # chd
            # Kabsch rotation to target
            rmsd, r = m.rmsd_kabsch(xyz_best, target_xyz, non_h_indices)
            # MAPD compared to target
            mapd = m.mapd_function(xyz_best, target_xyz, non_h_indices)
            # f_signal / target_f_signal
            signal_ratio = 0  # define as 0 if noise == 0
            if noise != 0:
                signal_ratio = f_xray_best / target_f_signal
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
            # encode the analysis values into the xyz header
            header_str = "%12.8f %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f" % (
                f_xray_best,
                rmsd,
                r05,
                dihedral,
                e_mol,
                mapd,
                signal_ratio,
            )
            ### write best structure to xyz file
            print("writing to xyz... (f: %10.8f)" % f_xray_best)
            f_best_str = ("%10.8f" % f_xray_best).zfill(12)
            m.write_xyz(
                "tmp_/%s_%s.xyz" % (run_id, f_best_str),
                header_str,
                atomlist,
                xyz_best,
            )
            ### Final save to files
            # also write final xyz as "result.xyz"
            m.write_xyz("tmp_/%s_result.xyz" % run_id, "result", atomlist, xyz_best)
            # target xyz
            m.write_xyz(
                "tmp_/%s_target.xyz" % run_id,
                "run_id: %s" % run_id,
                atomlist,
                target_xyz,
            )
            # predicted data
            if twod_mode:
                np.savetxt("tmp_/%s_%s.dat" % (run_id, f_best_str), predicted_best)
                np.savetxt("tmp_/%s_result.dat" % run_id, predicted_best)
            else:
                np.savetxt(
                    "tmp_/%s_%s.dat" % (run_id, f_best_str),
                    np.column_stack((qvector, predicted_best)),
                )
        return  # end function

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
