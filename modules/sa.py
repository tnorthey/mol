import numpy as np
from numpy.random import random_sample as random
from numpy import linalg as LA

# my modules
import modules.mol as mol
import modules.x as xray

# create class objects
m = mol.Xyz()
x = xray.Xray()

#############################
class Annealing:
    """Gradient descent functions"""

    def __init__(self):
        pass

    def read_nm_displacements(self, fname, natoms):
        """read_nm_displacements: Reads displacement vector from file=fname e.g. 'normalmodes.txt'
        Inputs: 	natoms (int), total number of atoms
        Outputs:	displacements, array of displacements, size: (nmodes, natoms, 3)"""
        if natoms == 2:
            nmodes = 1
        elif natoms > 2:
            nmodes = 3 * natoms - 6
        else:
            print("ERROR: natoms. Are there < 2 atoms?")
            return False
        with open(fname, "r") as xyzfile:
            tmp = np.loadtxt(fname)
        displacements = np.zeros((nmodes, natoms, 3))
        for i in range(3 * natoms):
            for j in range(nmodes):
                if i % 3 == 0:  # Indices 0,3,6,...
                    dindex = int(i / 3)
                    displacements[j, dindex, 0] = tmp[i, j]  # x coordinates
                elif (i - 1) % 3 == 0:  # Indices 1,4,7,...
                    displacements[j, dindex, 1] = tmp[i, j]  # y coordinates
                elif (i - 2) % 3 == 0:  # Indices 2,5,8,...
                    displacements[j, dindex, 2] = tmp[i, j]  # z coordinates
        return displacements

    def displacements_from_wavenumbers(self, wavenumbers, step_size, exponential=False):
        nmodes = len(wavenumbers)
        displacement_factors = np.zeros(nmodes)
        for i in range(nmodes):  # initial factors are inv. prop. to wavenumber
            if wavenumbers[i] > 0:
                if exponential:
                    displacement_factors[i] = np.exp(wavenumbers[0] / wavenumbers[i])
                else:
                    displacement_factors[i] = wavenumbers[0] / wavenumbers[i]
            else:
                displacement_factors[i] = 0.0
        displacement_factors *= step_size  # adjust max size of displacement step
        return displacement_factors

    def uniform_factors(self, nmodes, displacement_factors):
        """uniformly random displacement step along each mode"""
        # initialise random number generator (with random seed)
        rng = np.random.default_rng()
        factors = np.zeros(nmodes)
        for j in range(nmodes):
            # random factors in range [-a, a]
            a = displacement_factors[j]
            factors[j] = 2 * a * rng.random() - a
        return factors

    def simulate_trajectory(
        self, starting_xyz, displacements, wavenumbers, nsteps, step_size
    ):
        """creates a simulated trajectory by randomly moving along normal modes"""
        natom = starting_xyz.shape[0]
        nmodes = len(wavenumbers)
        modes = list(range(nmodes))
        displacement_factors = self.displacements_from_wavenumbers(
            wavenumbers, step_size
        )
        xyz = starting_xyz  # start at starting xyz
        xyz_traj = np.zeros((natom, 3, nsteps))
        for i in range(nsteps):
            factors = self.uniform_factors(
                nmodes, displacement_factors
            )  # random factors
            xyz = nm.nm_displacer(xyz, displacements, modes, factors)
            xyz_traj[:, :, i] = xyz
        return xyz_traj

    def atomic_pre_molecular(
        self, atomic_numbers, qvector, aa, bb, cc, electron_mode=False
    ):
        """both parts of IAM equation that don't depend on atom-atom distances"""
        # compton factors for inelastic effect
        compton_array = x.compton_spline(atomic_numbers, qvector)
        natoms = len(atomic_numbers)
        qlen = len(qvector)
        atomic_total = np.zeros(qlen)  # total atomic factor
        atomic_factor_array = np.zeros((natoms, qlen))  # array of atomic factors
        compton = np.zeros(qlen)
        for k in range(natoms):
            compton += compton_array[k, :]
            atomfactor = np.zeros(qlen)
            for j in range(qlen):
                for i in range(4):
                    atomfactor[j] += aa[atomic_numbers[k] - 1, i] * np.exp(
                        -bb[atomic_numbers[k] - 1, i] * (0.25 * qvector[j] / np.pi) ** 2
                    )
            atomfactor += cc[atomic_numbers[k] - 1]
            atomic_factor_array[k, :] = atomfactor
            if electron_mode:
                atomic_total += (atomic_numbers[k] - atomfactor) ** 2
            else:
                atomic_total += atomfactor ** 2
        nij = int(natoms * (natoms - 1) / 2)
        pre_molecular = np.zeros((nij, qlen))
        k = 0
        for i in range(natoms):
            for j in range(i + 1, natoms):
                if electron_mode:
                    pre_molecular[k, :] = np.multiply(
                        (atomic_numbers[i] - atomic_factor_array[i, :]),
                        (atomic_numbers[j] - atomic_factor_array[j, :]),
                    )
                else:
                    pre_molecular[k, :] = np.multiply(
                        atomic_factor_array[i, :], atomic_factor_array[j, :]
                    )

                k += 1
        return compton, atomic_total, pre_molecular

    def simulated_annealing_modes_ho(
        self,
        atomlist,
        starting_xyz,
        reference_xyz,
        displacements,
        mode_indices,
        target_data,
        qvector,
        step_size_array,
        ho_indices1,
        ho_indices2,
        starting_temp=0.2,
        nsteps=10000,
        inelastic=True,
        harmonic_factor=(0.1, 0.1),
        pcd_mode=False,
        electron_mode=False,
        xyz_save=False,
        twod_mode=False,
    ):
        """simulated annealing minimisation to target_data"""
        ##=#=#=# DEFINITIONS #=#=#=##
        # initialise random number generator (with random seed)
        rng = np.random.default_rng()
        ## start.xyz, reference.xyz ##
        atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]
        compton_array = x.compton_spline(atomic_numbers, qvector)
        # reference signal (for percent difference)
        if twod_mode:
            (
                reference_iam,
                atomic_2d,
                molecular_2d,
                atomic_factor_array,
                rotavg,
                qx,
                qy,
                qz,
            ) = x.iam_calc_2d(atomic_numbers, reference_xyz, qvector)
        else:
            reference_iam, _, _, _ = x.iam_calc(
                atomic_numbers,
                reference_xyz,
                qvector,
                electron_mode,
                inelastic,
                compton_array,
            )
        natoms = starting_xyz.shape[0]  # number of atoms
        nmodes = displacements.shape[0]  # number of displacement vectors
        modes = list(range(nmodes))  # all modes
        ## q-vector, atomic, and pre-molecular IAM contributions ##
        qlen = len(qvector)  # length of q-vector
        aa, bb, cc = x.read_iam_coeffs()
        compton, atomic_total, pre_molecular = self.atomic_pre_molecular(
            atomic_numbers,
            qvector,
            aa,
            bb,
            cc,
            electron_mode,
        )
        ##=#=#=# END DEFINITIONS #=#=#=#

        ##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##
        nho_indices1 = len(ho_indices1[0])  # number of HO indices
        nho_indices2 = len(ho_indices2[0])  # number of HO indices
        r0_arr1 = np.zeros(nho_indices1)  # array of starting xyz bond-lengths
        r0_arr2 = np.zeros(nho_indices2)  # array of starting xyz bond-lengths
        for i in range(nho_indices1):
            # print('bond term: %i %i' % (ho_indices[0][i], ho_indices[1][i]))
            r0_arr1[i] = np.linalg.norm(
                starting_xyz[ho_indices1[0][i], :] - starting_xyz[ho_indices1[1][i], :]
            )
        for i in range(nho_indices2):
            # print('bond term: %i %i' % (ho_indices[0][i], ho_indices[1][i]))
            r0_arr2[i] = np.linalg.norm(
                starting_xyz[ho_indices2[0][i], :] - starting_xyz[ho_indices2[1][i], :]
            )

        total_harmonic_contrib = 0
        total_xray_contrib = 0
        print("HO factors: %4.3f %4.3f" % (harmonic_factor[0], harmonic_factor[1]))
        ##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##

        ##=#=#=# INITIATE LOOP VARIABLES #=#=#=#=#
        xyz = starting_xyz
        i, c = 0, 0
        f, f_best = 1e9, 1e10
        f_array = np.zeros(nsteps)
        xyz_array = np.zeros((natoms, 3, nsteps))
        minimum_found = 0  # this counts unaccepted steps and if there is a large amount in a row it terminates
        # mdisp = displacements * step_size  # array of molecular displacements
        mdisp = displacements
        ##=#=#=# END INITIATE LOOP VARIABLES #=#=#
        while i < nsteps:
            i += 1  # count steps
            # print(i)
            minimum_found += 1  # count unaccepted steps
            if minimum_found == 1000:
                print(
                    '%i steps in a row did not improve the fit: terminating "minimum found"'
                    % minimum_found
                )
                nsteps = i
                break  # end while loop

            ##=#=#=#=# TEMPERATURE #=#=#=#=#=#=#=#=##
            tmp = 1 - i / nsteps  # this is prop. to how far the molecule moves
            temp = starting_temp * tmp  # this is the probability of going uphill
            ##=#=#=# END TEMPERATURE #=#=#=#=#=#=#=##

            ##=#=#=# DISPLACE XYZ RANDOMLY ALONG ALL DISPLACEMENT VECTORS #=#=#=##
            summed_displacement = np.zeros(mdisp[0, :, :].shape)
            for n in mode_indices:
                summed_displacement += (
                    mdisp[n, :, :] * step_size_array[n] * tmp * (2 * rng.random() - 1)
                )
            xyz_ = xyz + summed_displacement  # save a temporary displaced xyz: xyz_

            ##=#=#=# END DISPLACE XYZ RANDOMLY ALONG ALL DISPLACEMENT VECTORS #=#=#=##

            ##=#=#=# IAM CALCULATION #=#=#=##
            if twod_mode:  # 2D x-ray signal, q = q(theta, phi)
                molecular = np.zeros((qlen, qlen))  # total molecular factor
                for ii in range(natoms):
                    for jj in range(ii + 1, natoms):  # j > i
                        fij = np.multiply(
                            atomic_factor_array[ii, :, :], atomic_factor_array[jj, :, :]
                        )
                        xij = xyz_[ii, 0] - xyz_[jj, 0]
                        yij = xyz_[ii, 1] - xyz_[jj, 1]
                        zij = xyz_[ii, 2] - xyz_[jj, 2]
                        molecular += fij * np.cos(qx * xij + qy * yij + qz * zij)
                iam_ = atomic_2d + 2 * molecular
            else:  # assumed to be isotropic 1D signal
                molecular = np.zeros(qlen)  # total molecular factor
                k = 0
                for ii in range(natoms):
                    for jj in range(ii + 1, natoms):  # j > i
                        qdij = qvector * LA.norm(xyz_[ii, :] - xyz_[jj, :])
                        molecular += pre_molecular[k, :] * np.sin(qdij) / qdij
                        k += 1
                iam_ = atomic_total + 2 * molecular
                if inelastic:
                    iam_ += compton
            ##=#=#=# END IAM CALCULATION #=#=#=##

            ##=#=#=# PCD & CHI2 CALCULATIONS #=#=#=##
            if pcd_mode:
                predicted_function_ = 100 * (iam_ / reference_iam - 1)
            else:
                predicted_function_ = iam_

            ### x-ray part of f
            #if twod_mode:
            xray_contrib = (
                np.sum(
                    (predicted_function_ - target_data) ** 2 / target_data
                )
                / qlen
            )
            #else:
            #xray_contrib = np.sum((predicted_function_ - target_data) ** 2) / qlen

            ### harmonic oscillator part of f
            harmonic_contrib = 0
            for iho in range(nho_indices1):
                r = LA.norm(xyz_[ho_indices1[0][iho], :] - xyz_[ho_indices1[1][iho], :])
                harmonic_contrib += harmonic_factor[0] * (r - r0_arr1[iho]) ** 2

            for iho in range(nho_indices2):
                r = LA.norm(xyz_[ho_indices2[0][iho], :] - xyz_[ho_indices2[1][iho], :])
                harmonic_contrib += harmonic_factor[1] * (r - r0_arr2[iho]) ** 2

            ### combine x-ray and harmonic contributions
            f_ = xray_contrib + harmonic_contrib
            ##=#=#=# END PCD & CHI2 CALCULATIONS #=#=#=##

            ##=#=#=# ACCEPTANCE CRITERIA #=#=#=##
            if f_ / f < 1 - 1e-9 or temp > rng.random():
                minimum_found = 0
                c += 1  # count acceptances
                f, xyz = f_, xyz_  # update f and xyz
                # save f to graph
                f_array[c - 1] = f
                if f < f_best:
                    # store values corresponding to f_best
                    f_best, xyz_best, predicted_best = f, xyz, predicted_function_
                    f_xray_best = xray_contrib
                total_harmonic_contrib += harmonic_contrib
                total_xray_contrib += xray_contrib
                # optional save xyz to array
                if xyz_save:
                    xyz_array[:, :, c - 1] = xyz_
            ##=#=#=# END ACCEPTANCE CRITERIA #=#=#=##
        # remove ending zeros from arrays
        f_array = f_array[:c]
        xyz_array = xyz_array[:, :, :c] if xyz_save else 0
        # print ratio of contributions to f
        total_contrib = total_xray_contrib + total_harmonic_contrib
        xray_ratio = total_xray_contrib / total_contrib
        harmonic_ratio = total_harmonic_contrib / total_contrib
        print("xray contrib ratio: %f" % xray_ratio)
        print("harmonic contrib ratio: %f" % harmonic_ratio)
        print("Accepted / Total steps: %i/%i" % (c, nsteps))
        # end function
        return f_best, f_xray_best, predicted_best, xyz_best, f_array, xyz_array
