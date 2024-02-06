import numpy as np
from numpy import linalg as LA

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

    def chd_strategy1(
        self,
        run_id,
        start_xyz_file,
        reference_xyz_file,
        target_xyz_file,
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        ic_ninitials=1000,
        ic_nsteps=200,
        ic_step_size=0.1,
        ic_starting_temp=0.2,
        ic_harmonic_factor=0.1,  # a stronger HO factor for IC generation
        sa_nsteps=2000,
        sa_step_size=0.01,
        sa_starting_temp=0.2,
        sa_harmonic_factor=0.01,
        sa_n_trials=1,  # repeats n_trails times, only saves lowest f
        sa_n_restarts=1,  # entire thing repeats n_restarts times
        save_ic_xyzs=False,  # save all ic_.xyz files in tmp_/
    ):
        """
        Strategy 1 (CHD): Generate a lot of initial conditions via short "hot" SA runs,
            start from the best structure from that -> N restarts of longer "cooler" SA runs
            - This should find a reasonably close starting point from the ICs,
            then optimise it further with the subsequent longer runs
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

        def xyz2iam(xyz, atomlist):
            """convert xyz file to IAM signal"""
            atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
            compton_array = x.compton_spline(atomic_numbers, qvector)
            iam, atomic, molecular, compton = x.iam_calc(
                atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
            )
            return iam

        #############################
        ### arguments             ###
        #############################
        _, _, atomlist, starting_xyz = m.read_xyz(start_xyz_file)
        _, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
        _, _, atomlist, target_xyz = m.read_xyz(target_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        starting_iam = xyz2iam(starting_xyz, atomlist)
        reference_iam = xyz2iam(reference_xyz, atomlist)
        target_iam = xyz2iam(target_xyz, atomlist)

        natoms = starting_xyz.shape[0]
        nmfile = "nm/chd_normalmodes.txt"
        displacements = sa.read_nm_displacements(nmfile, natoms)
        nmodes = displacements.shape[0]

        mode_indices = np.arange(0, nmodes)  # CHD, all modes
        print("including modes:")
        print(mode_indices)

        ###############################################
        ### Initial condition generation parameters ###
        ###############################################
        # alternative step-sizes for generating initial conditions
        # hydrogen modes damped
        hydrogen_modes = np.arange(28, nmodes)  # CHD hydrogen modes
        ic_h_mode_modification = np.ones(nmodes)
        sa_h_mode_modification = np.ones(nmodes)
        for i in hydrogen_modes:
            ic_h_mode_modification[i] *= 0.00
            sa_h_mode_modification[i] *= 0.1
        ic_step_size_array = ic_step_size * np.ones(nmodes) * ic_h_mode_modification
        sa_step_size_array = sa_step_size * np.ones(nmodes) * sa_h_mode_modification
        ###############################################
        ###############################################

        pcd_mode = True
        xyz_save = False

        # ho_indices = [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]  # chd (C-C bonds)
        ho_indices = [
            [0, 1, 2, 3, 4, 6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5, 7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ]  # chd (C-C and C-H bonds)

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
        target_function = 100 * (target_iam / reference_iam - 1)

        #################################
        ### End Initialise some stuff ###
        #################################

        # stuff I want to save
        predicted_best_array = np.zeros((qlen, sa_n_restarts))
        xyz_best_array = np.zeros((natoms, 3, sa_n_restarts))
        f_best_array = np.zeros(sa_n_restarts)
        f_xray_best_array = np.zeros(sa_n_restarts)
        dihedral_array = np.zeros(sa_n_restarts)
        r05_array = np.zeros(sa_n_restarts)
        ic_dihedral_array = np.zeros(ic_ninitials)
        ic_r05_array = np.zeros(ic_ninitials)

        # Generate initial conditions...
        f_best_ = 1e9
        for j in range(ic_ninitials):
            # Run simulated annealing
            (
                f_best,
                f_xray_best,
                predicted_best,
                xyz_best,
                f_array,
                xyz_array,
            ) = sa.simulated_annealing_modes_ho(
                atomlist,
                starting_xyz,
                reference_xyz,
                displacements,
                mode_indices,
                target_function,
                qvector,
                ic_step_size_array,
                ho_indices,
                ic_starting_temp,
                ic_nsteps,
                inelastic,
                ic_harmonic_factor,
                pcd_mode,
                electron_mode,
                False,
            )
            print("f_best (SA): %9.8f" % f_best)

            if save_ic_xyzs:
                ### store results as xyz files ###
                print("writing to xyz... (f: %10.8f)" % f_best)
                f_best_str = ("%10.8f" % f_best).zfill(12)
                m.write_xyz(
                    "tmp_/ic_%s_%s.xyz" % (run_id, f_best_str),
                    "run_id: %s" % run_id,
                    atomlist,
                    xyz_best,
                )

            # dihedral(s)
            p0 = np.array(xyz_best[0, :])
            p1 = np.array(xyz_best[1, :])
            p4 = np.array(xyz_best[4, :])
            p5 = np.array(xyz_best[5, :])
            ic_dihedral_array[j] = m.new_dihedral(np.array([p0, p1, p4, p5]))
            # r05 distance
            ic_r05_array[j] = np.linalg.norm(xyz_best[0, :] - xyz_best[5, :])

            # store best value from the n_initials
            if f_best < f_best_:
                f_best_, f_xray_best_, predicted_best_, xyz_best_ = (
                    f_best,
                    f_xray_best,
                    predicted_best,
                    xyz_best,
                )
        # Finally,
        # this will be the starting point for the full run in the next step
        print("IC generation complete.")
        print(
            "starting_xyz chosen: f_best = %9.8f f_xray_best = %9.8f"
            % (f_best_, f_xray_best_)
        )
        ### store final result as xyz file ###
        print("writing to xyz... (f: %10.8f)" % f_best_)
        f_best_str = ("%10.8f" % f_best_).zfill(12)
        m.write_xyz(
            "tmp_/ic_%s_%s.xyz" % (run_id, f_best_str),
            "run_id: %s" % run_id,
            atomlist,
            xyz_best_,
        )
        starting_xyz = xyz_best_
        ic_f_best = f_best_

        for k_restart in range(sa_n_restarts):
            f_best_ = ic_f_best
            for k_trial in range(sa_n_trials):

                # Run simulated annealing
                (
                    f_best,
                    f_xray_best,
                    predicted_best,
                    xyz_best,
                    f_array,
                    xyz_array,
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
                    xyz_save,
                )
                print("f_best (SA): %9.8f" % f_best)
                ### save xyz_array as an xyz trajectory
                if xyz_save:
                    print("saving xyz array...")
                    fname = "tmp_/save_array.xyz"
                    m.write_xyz_traj(fname, atomlist, xyz_array)

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
            np.savetxt(
                "tmp_/%s_%s.dat" % (run_id, f_best_str),
                np.column_stack((qvector, predicted_best_)),
            )

            # store best data from each restart
            predicted_best_array[:, k_restart] = predicted_best
            xyz_best_array[:, :, k_restart] = xyz_best
            # dihedral(s)
            p0 = np.array(xyz_best[0, :])
            p1 = np.array(xyz_best[1, :])
            p4 = np.array(xyz_best[4, :])
            p5 = np.array(xyz_best[5, :])
            dihedral_array[k_restart] = m.new_dihedral(np.array([p0, p1, p4, p5]))
            # r05 distance
            r05_array[k_restart] = np.linalg.norm(xyz_best[0, :] - xyz_best[5, :])

            # calculate raw IAM data
            # iam_best = xyz2iam(xyz_best_, atomlist)

            # save final IAM signal
            # np.savetxt("tmp_/%s_iam_best.dat" % run_id, np.column_stack((qvector, iam_best)))

        # Final save to npz database
        np.savez(
            "tmp_/out.npz",
            predicted_best_array=predicted_best_array,
            xyz_best_array=xyz_best_array,
            dihedral_array=dihedral_array,
            r05_array=r05_array,
            f_best_array=f_best_array,
            f_xray_best_array=f_xray_best_array,
        )

        # I save them to dat files too; for quicker checking
        np.savetxt("tmp_/%s_dihedral_array.dat" % run_id, dihedral_array)
        np.savetxt("tmp_/%s_r05_array.dat" % run_id, r05_array)
        np.savetxt("tmp_/%s_ic_dihedral_array.dat" % run_id, ic_dihedral_array)
        np.savetxt("tmp_/%s_ic_r05_array.dat" % run_id, ic_r05_array)
        m.write_xyz_traj(
            "tmp_/%s_xyz_best_array.xyz" % run_id, atomlist, xyz_best_array
        )

        ### Final save to files
        # target xyz
        m.write_xyz(
            "tmp_/%s_target_xyz.xyz" % run_id,
            "run_id: %s" % run_id,
            atomlist,
            target_xyz,
        )
        # target function
        np.savetxt(
            "tmp_/%s_target_function.dat" % run_id,
            np.column_stack((qvector, target_function)),
        )
        # save raw target data:
        np.savetxt(
            "tmp_/%s_target_iam.dat" % run_id, np.column_stack((qvector, target_iam))
        )
        # save starting IAM signal
        np.savetxt(
            "tmp_/%s_starting_iam.dat" % run_id,
            np.column_stack((qvector, starting_iam)),
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
        xyz_save = False

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
                f_array,
                xyz_array,
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
                xyz_save,
                twod_mode,
            )
            print("f_best (SA): %9.8f" % f_best)
            ### save xyz_array as an xyz trajectory
            if xyz_save:
                print("saving xyz array...")
                fname = "tmp_/save_array.xyz"
                m.write_xyz_traj(fname, atomlist, xyz_array)

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

    def chd_1D(
        self,
        run_id,
        start_xyz_file,
        reference_xyz_file,
        target_xyz_file,
        qvector=np.linspace(1e-9, 8.0, 81, endpoint=True),
        sa_nsteps=2000,
        sa_step_size=0.01,
        sa_starting_temp=0.2,
        sa_harmonic_factor=(0.01, 0.01),
        nrestarts=10,
        non_h_modes_only=False,  # only include "non-hydrogen" modes
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

        def xyz2iam(xyz, atomlist):
            """convert xyz file to IAM signal"""
            atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
            compton_array = x.compton_spline(atomic_numbers, qvector)
            iam, atomic, molecular, compton = x.iam_calc(
                atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
            )
            return iam

        #############################
        ### arguments             ###
        #############################
        _, _, atomlist, starting_xyz = m.read_xyz(start_xyz_file)
        _, _, atomlist, reference_xyz = m.read_xyz(reference_xyz_file)
        _, _, atomlist, target_xyz = m.read_xyz(target_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        starting_iam = xyz2iam(starting_xyz, atomlist)
        reference_iam = xyz2iam(reference_xyz, atomlist)
        target_iam = xyz2iam(target_xyz, atomlist)

        natoms = starting_xyz.shape[0]
        nmfile = "nm/chd_normalmodes.txt"
        displacements = sa.read_nm_displacements(nmfile, natoms)
        nmodes = displacements.shape[0]

        pcd_mode = False
        xyz_save = False
        f_save = True

        # hydrogen modes damped
        hydrogen_modes = np.arange(28, nmodes)  # CHD hydrogen modes
        sa_h_mode_modification = np.ones(nmodes)
        for i in hydrogen_modes:
            sa_h_mode_modification[i] = 0.2
        sa_step_size_array = sa_step_size * np.ones(nmodes) * sa_h_mode_modification

        ho_indices1 = [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]]  # chd (C-C bonds)
        # ho_indices = [
        #    [0, 1, 2, 3, 4, 6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
        #    [1, 2, 3, 4, 5, 7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        # ]  # chd (C-C and C-H bonds)

        ho_indices2 = [
            [6, 12, 5, 5, 0, 0, 1, 2, 3, 4],
            [7, 13, 12, 13, 6, 7, 8, 9, 10, 11],
        ]  # chd (C-H bonds, and H-H "bonds" for the CH2 carbons)

        mode_indices = np.arange(0, 28)  # CHD, "non-hydrogen" modes

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

        xyz_best = starting_xyz # initialise
        #################################
        ### End Initialise some stuff ###
        #################################
        for i in range(nrestarts):
            print('Run %i: SA' % i)
            starting_xyz = xyz_best
            if i == nrestarts - 1:  # last run parameters
                print('Run %i: GA' % i)
                sa_nsteps *= 10
                sa_starting_temp = 0
                sa_harmonic_factor = (0, 0)
                mode_indices = np.arange(0, nmodes)  # CHD, all modes
                # mode_indices = np.arange(28, nmodes)  # CHD, only "hydrogen" modes
            print("including modes:")
            print(mode_indices)

            # Run simulated annealing
            (
                f_best,
                f_xray_best,
                predicted_best,
                xyz_best,
                f_array,
                xyz_array,
            ) = sa.simulated_annealing_modes_ho(
                atomlist,
                starting_xyz,
                reference_xyz,
                displacements,
                mode_indices,
                target_function,
                qvector,
                sa_step_size_array,
                ho_indices1,
                ho_indices2,
                sa_starting_temp,
                sa_nsteps,
                inelastic,
                sa_harmonic_factor,
                pcd_mode,
                electron_mode,
                xyz_save,
                twod_mode,
            )
            print("f_best (SA): %9.8f" % f_best)

            ### save xyz_array as an xyz trajectory
            if xyz_save:
                print("saving xyz array...")
                fname = "tmp_/save_array.xyz"
                m.write_xyz_traj(fname, atomlist, xyz_array)

            ### save f_array
            if f_save:
                print("saving f array...")
                fname = "tmp_/f_array_%i.dat" % i
                np.savetxt(fname, f_array)

        # NB arbitrary multiply by 1000
        f_xray_best *= 1000.0  # I do this just to avoid collisions in the filenames!

        ### analysis on xyz_best
        # 0145 dihedral that describes the ring-opening
        p0 = np.array(xyz_best[0, :])
        p1 = np.array(xyz_best[1, :])
        p4 = np.array(xyz_best[4, :])
        p5 = np.array(xyz_best[5, :])
        dihedral = m.new_dihedral(np.array([p0, p1, p4, p5]))
        # r05 ring-opening bond-length
        r05 = np.linalg.norm(xyz_best[0, :] - xyz_best[5, :])
        # encode the analysis values into the xyz header
        header_str = "%12.8f %12.8f %12.8f" % (f_xray_best, r05, dihedral)
        ### write best structure to xyz file
        print("writing to xyz... (f: %10.8f)" % f_xray_best)
        f_best_str = ("%10.8f" % f_xray_best).zfill(12)
        m.write_xyz(
            "tmp_/%s_%s.xyz" % (run_id, f_best_str),
            header_str,
            atomlist,
            xyz_best,
        )
        # also write final xyz as "result.xyz"
        m.write_xyz("tmp_/%s_result.xyz" % run_id, "result", atomlist, xyz_best)
        m.write_xyz("tmp_/result.xyz", "result", atomlist, xyz_best)
        # predicted data
        if twod_mode:
            np.savetxt("tmp_/%s_%s.dat" % (run_id, f_best_str), predicted_best)
            np.savetxt("tmp_/%s_result.dat" % run_id, predicted_best)
        else:
            np.savetxt(
                "tmp_/%s_%s.dat" % (run_id, f_best_str),
                np.column_stack((qvector, predicted_best)),
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
        np.savetxt(
            "tmp_/%s_target_function.dat" % run_id,
            np.column_stack((qvector, target_function)),
        )
        # save raw target data:
        np.savetxt(
            "tmp_/%s_target_iam.dat" % run_id, np.column_stack((qvector, target_iam))
        )
        # save starting IAM signal
        np.savetxt(
            "tmp_/%s_starting_iam.dat" % run_id,
            np.column_stack((qvector, starting_iam)),
        )

        return  # end function
