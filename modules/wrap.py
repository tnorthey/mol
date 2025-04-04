import os
import pprint
import numpy as np
from numpy import linalg as LA
try:
    # Handle the case when PySCF isn't there
    from pyscf import gto, scf
    HAVE_PYSCF = True
except ImportError:
    HAVE_PYSCF = False

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

    def run(
        self,
        p,
        run_id='RUN_ID',
        start_xyz_file='START_XYZ_FILE',
        target_file='TARGET_FILE',
    ):
        """
        wrapper function that handles restarts, xyz/dat modes, output files,
        and some analysis e.g. PySCF energy calculations, bond-distance and angle calculations.
        """
        #############################
        ######### Inputs ############
        # p: the parameters object from read_input
        ### Optional inputs:
        # start_xyz_file: the starting xyz file (if given it overrides the one in p)
        # run_id: the run ID (if given it overrides the one in p)
        #############################

        electron_mode = False

        if run_id == "RUN_ID" or run_id == 0:
            run_id = p.run_id
        else:
            print(f"VALUE OVERWRITTEN BY COMMAND LINE ARG: 'run_id' = {run_id}")
        if start_xyz_file == "START_XYZ_FILE" or start_xyz_file == 0:
            start_xyz_file = p.start_xyz_file
        else:
            print(f"VALUE OVERWRITTEN BY COMMAND LINE ARG: 'start_xyz_file' = {start_xyz_file}")
        if target_file == "TARGET_FILE" or target_file == 0:
            target_file = p.target_file
        else:
            print(f"VALUE OVERWRITTEN BY COMMAND LINE ARG: 'target_file' = {target_file}")

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
                    p.qvector,
                    p.th,
                    p.ph,
                    p.inelastic,
                    compton_array,
                )
            else:
                iam, atomic, molecular, compton, pre_molecular = x.iam_calc(
                    atomic_numbers,
                    xyz,
                    p.qvector,
                    electron_mode,
                    p.inelastic,
                    compton_array,
                )
            return iam, atomic, compton, pre_molecular

        #############################
        ### arguments             ###
        #############################
        _, _, atomlist, xyz_start = m.read_xyz(start_xyz_file)
        _, _, atomlist, reference_xyz = m.read_xyz(p.reference_xyz_file)
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        compton_array = x.compton_spline(atomic_numbers, p.qvector)
        starting_iam, atomic, compton, pre_molecular = xyz2iam(
            xyz_start, atomic_numbers, compton_array, p.ewald_mode
        )
        reference_iam, atomic, compton, pre_molecular = xyz2iam(
            reference_xyz, atomic_numbers, compton_array, p.ewald_mode
        )

        save_starting_reference_iams = False  # for debugging
        if save_starting_reference_iams:
            np.savetxt('starting_iam.dat', np.column_stack((p.qvector, starting_iam)))
            np.savetxt('reference_iam.dat', np.column_stack((p.qvector, reference_iam)))

        natoms = xyz_start.shape[0]
        displacements = sa.read_nm_displacements(p.nmfile, natoms)
        nmodes = displacements.shape[0]

        # hydrogen modes damped
        sa_h_mode_modification = np.ones(nmodes)
        for i in p.hydrogen_mode_indices:
            sa_h_mode_modification[i] = 0.2
        p.sa_step_size_array = p.sa_step_size * np.ones(nmodes) * sa_h_mode_modification

        #############################
        ### end arguments         ###
        #############################

        ### Rarely edit after this...

        #############################
        ### Initialise some stuff ###
        #############################

        print(f"Target: {target_file}")
        filename, target_file_ext = os.path.splitext(target_file)
        target_function_file = "%s/TARGET_FUNCTION_%s.dat" % (p.results_dir, run_id)

        ###########################################################
        ###########################################################
        ### Section: xyz or dat mode handling                   ###
        ###########################################################
        ###########################################################
        if p.mode == "xyz":
            # read from target xyz file
            _, _, atomlist, target_xyz = m.read_xyz(target_file)
            target_iam, atomic, compton, pre_molecular = xyz2iam(
                target_xyz, atomic_numbers, compton_array, p.ewald_mode
            )

            # target_iam_file = "tmp_/TARGET_IAM_%s.dat" % run_id
            # save target IAM file before noise is added
            # print("Saving data to %s ..." % target_iam_file)
            # np.savetxt(target_iam_file, np.column_stack((p.qvector, target_iam)))

            ### ADDITION OF RANDOM NOISE
            noise_file_bool = True
            # p.noise_data_file = "noise/noise.dat"
            print(f"checking if {p.noise_data_file} exists...")
            if noise_file_bool and os.path.exists(p.noise_data_file):
                # read the noise from a file
                print(f"Yes. Reading noise data from {p.noise_data_file}")
                noise_array = np.loadtxt(p.noise_data_file)
                # resize to length of q and scale magnitude
                noise_array = p.noise_value * noise_array[0 : p.qlen]
            else:
                print(f"{p.noise_data_file} does not exist.")
                # generate random noise here instead of reading from file
                mu = 0  # normal distribution with mean of mu
                sigma = p.noise_value
                print(
                    "Randomly generating noise from normal dist... sigma = %3.2f"
                    % sigma
                )
                noise_array = sigma * np.random.randn(p.qlen) + mu
            # if Ewald mode the noise_array has to be 3D
            if p.ewald_mode:
                noise_array_3d = np.zeros((p.qlen, p.tlen, p.plen))
                for i in range(p.plen):
                    for j in range(p.tlen):
                        noise_array_3d[:, j, i] = noise_array
                noise_array = noise_array_3d  # redefine as the 3D array
            target_function = target_iam + noise_array  # define target_function
        elif p.mode == "dat":
            # if target file is a data file, read as target_function
            target_function = np.loadtxt(target_file)
            excitation_factor = 0.057
            target_function /= excitation_factor
            target_xyz = xyz_start  # added simply to run the rmsd analysis later compared to this
        else:
            print('Error: mode value must be "xyz" or "dat"!')
        ###########################################################
        ###########################################################
        ### End Section: xyz or dat mode handling               ###
        ###########################################################
        ###########################################################

        # save target function to file if it doesn't exist
        # if not os.path.exists(target_function_file):
        print("Saving data to %s ..." % target_function_file)
        if p.ewald_mode:
            target_function_r = x.spherical_rotavg(target_function, p.th, p.ph)
            np.savetxt(
                target_function_file, np.column_stack((p.qvector, target_function_r))
            )
            ### also save to npy file to results_dir
            npy_save = True
            if npy_save:
                np.save('%s/target_function.npy' % p.results_dir, target_function)
        else:
            np.savetxt(
                target_function_file, np.column_stack((p.qvector, target_function))
            )
        # print(target_function)

        # load target function from file
        # if os.path.exists(target_function_file):
        #    print("Loading data from %s ..." % target_function_file)
        #    target_function = np.loadtxt(target_function_file)[:, 1]
        #    print(target_function)
        # else:
        #    target_function = target_iam
        #    print("Saving data to %s ..." % target_function_file)
        #    np.savetxt(target_function_file, np.column_stack((p.qvector, target_function)))

        #################################
        ### End Initialise some stuff ###
        #################################
        # initialise starting "best" values
        xyz_best = xyz_start
        f_best, f_xray_best = 1e10, 1e10
        if p.ewald_mode: 
            psize = (p.qlen, p.tlen, p.plen)
        else: 
            psize = p.qlen
        predicted_best = np.zeros(psize)
        for i in range(p.nrestarts):
            ### each restart starts at the previous xyz_best
            xyz_start = xyz_best  
            f_start = f_best
            f_xray_start = f_xray_best
            predicted_start = predicted_best
            ###
            if i < p.nrestarts - 1:  # annealing mode
                print(f"Run {i}: SA")
                nsteps = p.sa_nsteps
                starting_temp = p.sa_starting_temp
                harmonic_factor = p.sa_harmonic_factor
                angular_factor = p.sa_angular_factor
                mode_indices = p.sa_mode_indices
            else:  # greedy algorithm mode
                print(f"Run {i}: GA")
                nsteps = p.ga_nsteps
                starting_temp = 0
                harmonic_factor = p.ga_harmonic_factor
                angular_factor = p.ga_angular_factor
                mode_indices = p.ga_mode_indices
            # Run simulated annealing
            (
                f_best,
                f_xray_best,
                predicted_best,
                xyz_best,
            ) = sa.simulated_annealing_modes_ho(
                xyz_start,
                displacements,
                mode_indices,
                target_function,
                reference_iam,
                p.qvector,
                p.th,
                p.ph,
                compton,
                atomic,
                pre_molecular,
                p.sa_step_size_array,
                p.ho_indices1,
                p.ho_indices2,
                p.angular_indices1,
                p.angular_indices2,
                starting_temp,
                nsteps,
                p.inelastic,
                harmonic_factor,
                angular_factor,
                p.pcd_mode,
                p.ewald_mode,
                p.bonds_bool,
                p.angles_bool,
                f_start,
                f_xray_start,
                predicted_start,
            )
            print("f_best (SA): %9.8f" % f_best)

        ### analysis on xyz_best
        # bond-length of interest
        bond_distance = np.linalg.norm(
            xyz_best[p.bond_indices[0], :] - xyz_best[p.bond_indices[1], :]
        )
        # angle of interest
        p0 = np.array(xyz_best[p.angle_indices[0], :])
        p1 = np.array(xyz_best[p.angle_indices[1], :])  # central point
        p2 = np.array(xyz_best[p.angle_indices[2], :])
        angle_degrees = m.angle_2p_3d(p0, p1, p2)
        # dihedral of interest
        p0 = np.array(xyz_best[p.dihedral_indices[0], :])
        p1 = np.array(xyz_best[p.dihedral_indices[1], :])
        p2 = np.array(xyz_best[p.dihedral_indices[2], :])
        p3 = np.array(xyz_best[p.dihedral_indices[3], :])
        dihedral = m.new_dihedral(np.array([p0, p1, p2, p3]))
        rmsd_target_bool = True
        if rmsd_target_bool:
            # rmsd compared to target
            # Kabsch rotation to target
            rmsd, r = m.rmsd_kabsch(xyz_best, target_xyz, p.rmsd_indices)
            # MAPD compared to target
            mapd = m.mapd_function(xyz_best, target_xyz, p.rmsd_indices)
            # save target xyz
            m.write_xyz(
                "%s/%s_target.xyz" % (p.results_dir, run_id),
                ".dat file case: xyz_start (not target_xyz)",
                atomlist,
                target_xyz,
            )
        else:
            bond_distance, angle_degrees, dihedral = 0, 0, 0
            rmsd, mapd, e_mol = 0, 0, 0
        # HF energy with PySCF
        if p.hf_energy and HAVE_PYSCF:
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
            "%s/%s_%s.xyz" % (p.results_dir, run_id, f_best_str),
            header_str,
            atomlist,
            xyz_best,
        )
        ### analysis values dictionary for final print out
        A = {
        'f_xray_best' : '%10.8f' % f_xray_best,
        'rmsd' : '%10.8f' % rmsd ,
        'bond_distance' : '%10.8f' % bond_distance,
        'angle_degrees' : '%10.8f' % angle_degrees,
        'dihedral_degrees' : '%10.8f' % dihedral,
        'energy_hf' : '%10.8f' % e_mol,
        'mapd' : '%10.8f' % mapd,
        }
        ### print analysis values
        print('################')
        print('Analysis values:')
        print('################')
        pprint.pprint(A)
        print('################')
        # also write final xyz as "result.xyz"
        # m.write_xyz("tmp_/%s_result.xyz" % run_id, "result", atomlist, xyz_best)
        # predicted data
        if p.ewald_mode:
            if npy_save:
                np.save('%s/predicted_function.npy' % p.results_dir, predicted_best)
            predicted_best_r = x.spherical_rotavg(predicted_best, p.th, p.ph)
            predicted_best = predicted_best_r
        ### write predicted data to file
        np.savetxt(
            "%s/%s_%s.dat" % (p.results_dir, run_id, f_best_str),
            np.column_stack((p.qvector, predicted_best)),
        )
        return  # end function

    #####################################
    #####################################
    #####################################
    #####################################
    #####################################
    #####################################

