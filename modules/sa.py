import random
import numba
import numpy as np
from numpy import linalg as LA
from numpy.typing import NDArray, DTypeLike

from timeit import default_timer

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

    def read_nm_displacements(self, fname: str, natoms: int) -> NDArray:
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

    def simulated_annealing_modes_ho(
        self,
        atomic_numbers: NDArray,
        starting_xyz: NDArray,
        displacements: NDArray,
        mode_indices: NDArray,
        target_data: NDArray,
        qvector: NDArray,
        compton: NDArray,
        atomic_total: NDArray,
        pre_molecular: NDArray,
        aa: NDArray,
        bb: NDArray,
        cc: NDArray,
        step_size_array: NDArray,
        ho_indices1: NDArray,
        ho_indices2: NDArray,
        starting_temp=0.2,
        nsteps=10000,
        inelastic=True,
        harmonic_factor=(0.1, 0.1),
        pcd_mode=False,
        electron_mode=False,
        twod_mode=False,
    ):
        """simulated annealing minimisation to target_data"""
        ##=#=#=# DEFINITIONS #=#=#=##
        natoms = starting_xyz.shape[0]  # number of atoms
        nmodes = displacements.shape[0]  # number of displacement vectors
        nmode_indices = len(mode_indices)
        #print((nmodes, nmode_indices))
        modes = list(range(nmodes))  # all modes
        ## q-vector, atomic, and pre-molecular IAM contributions ##
        #print(qvector)
        qlen = len(qvector)  # length of q-vector
        ##=#=#=# END DEFINITIONS #=#=#=#

        ##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##
        nho_indices1 = len(ho_indices1[0])  # number of HO indices
        nho_indices2 = len(ho_indices2[0])  # number of HO indices
        # Calculate distance arrays for starting_xyz
        diff = starting_xyz[ho_indices1[0]] - starting_xyz[ho_indices1[1]]
        r0_arr1 = LA.norm(diff, axis=1)
        diff = starting_xyz[ho_indices2[0]] - starting_xyz[ho_indices2[1]]
        r0_arr2 = LA.norm(diff, axis=1)
        #print("HO factors: %4.3f %4.3f" % (harmonic_factor[0], harmonic_factor[1]))
        ##=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=##

        @numba.njit
        def run_annealing(nsteps):

            ##=#=#=# INITIATE LOOP VARIABLES #=#=#=#=#
            xyz = starting_xyz
            i, c = 0, 0
            f, f_best = 1e9, 1e10
            f_array = np.zeros(nsteps)
            #xyz_array = np.zeros((natoms, 3, nsteps))
            # mdisp = displacements * step_size  # array of molecular displacements
            mdisp = displacements
            total_harmonic_contrib = 0
            total_xray_contrib = 0
            ##=#=#=# END INITIATE LOOP VARIABLES #=#=#

            for i in range(nsteps):

                ##=#=#=#=# TEMPERATURE #=#=#=#=#=#=#=#=##
                tmp = 1 - i / nsteps  # this is prop. to how far the molecule moves
                temp = starting_temp * tmp  # this is the probability of going uphill
                ##=#=#=# END TEMPERATURE #=#=#=#=#=#=#=##

                ##=#=#=# DISPLACE XYZ RANDOMLY ALONG ALL DISPLACEMENT VECTORS #=#=#=##
                xyz_ = xyz + np.sum(
                    mdisp[mode_indices, :, :]
                    * step_size_array[mode_indices, np.newaxis, np.newaxis]
                    * tmp
                    * (
                        2
                        * np.random.random_sample(nmode_indices)[
                            :, np.newaxis, np.newaxis
                        ]
                        - 1
                    ),
                    axis=0,
                )  # save a temporary displaced xyz: xyz_
                ##=#=#=# END DISPLACE XYZ RANDOMLY ALONG ALL DISPLACEMENT VECTORS #=#=#=##

                ##=#=#=# IAM CALCULATION #=#=#=##
                #if twod_mode:  # 2D x-ray signal, q = q(theta, phi)
                #    molecular = np.zeros((qlen, qlen))  # total molecular factor
                #    for ii in range(natoms):
                #        for jj in range(ii + 1, natoms):  # j > i
                #            fij = np.multiply(
                #                atomic_factor_array[ii, :, :],
                #                atomic_factor_array[jj, :, :],
                #            )
                #            xij = xyz_[ii, 0] - xyz_[jj, 0]
                #            yij = xyz_[ii, 1] - xyz_[jj, 1]
                #            zij = xyz_[ii, 2] - xyz_[jj, 2]
                #            molecular += fij * np.cos(qx * xij + qy * yij + qz * zij)
                #    iam_ = atomic_2d + 2 * molecular
                #else:  # assumed to be isotropic 1D signal
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
                #if pcd_mode:
                #    predicted_function_ = 100 * (iam_ / reference_iam - 1)
                #else:
                predicted_function_ = iam_

                ### x-ray part of f
                xray_contrib = (
                    np.sum(
                        (predicted_function_ - target_data) ** 2 / np.abs(target_data)
                    )
                    / qlen
                )
                # xray_contrib = np.sum((predicted_function_ - target_data) ** 2) / qlen

                ### harmonic oscillator part of f
                # somehow this is faster in numba than the vectorised version
                harmonic_contrib = 0
                for iho in range(nho_indices1):
                    r = LA.norm(
                        xyz_[ho_indices1[0][iho], :] - xyz_[ho_indices1[1][iho], :]
                    )
                    harmonic_contrib += harmonic_factor[0] * (r - r0_arr1[iho]) ** 2
                for iho in range(nho_indices2):
                    r = LA.norm(
                        xyz_[ho_indices2[0][iho], :] - xyz_[ho_indices2[1][iho], :]
                    )
                    harmonic_contrib += harmonic_factor[1] * (r - r0_arr2[iho]) ** 2

                ### combine x-ray and harmonic contributions
                f_ = xray_contrib + harmonic_contrib
                ##=#=#=# END PCD & CHI2 CALCULATIONS #=#=#=##

                ##=#=#=# ACCEPTANCE CRITERIA #=#=#=##
                if f_ / f < 1 - 1e-9 or temp > random.random():
                    # if f_ / f < 1 - 1e-9 or temp > 0.5:
                    minimum_found = 0
                    c += 1  # count acceptances
                    f, xyz = f_, xyz_  # update f and xyz
                    # save f to graph
                    if f < f_best:
                        # store values corresponding to f_best
                        f_best, xyz_best, predicted_best = f, xyz, predicted_function_
                        f_xray_best = xray_contrib
                    total_harmonic_contrib += harmonic_contrib
                    total_xray_contrib += xray_contrib
                    # optional save xyz to array
                    #if xyz_save:
                    #    xyz_array[:, :, c - 1] = xyz_
                ##=#=#=# END ACCEPTANCE CRITERIA #=#=#=##
            # print ratio of contributions to f
            total_contrib = total_xray_contrib + total_harmonic_contrib
            xray_ratio = total_xray_contrib / total_contrib
            harmonic_ratio = total_harmonic_contrib / total_contrib
            return (
                f_best,
                f_xray_best,
                predicted_best,
                xyz_best,
                xray_ratio,
                harmonic_ratio,
                c,
            )
        ### END run_annealing() function ###

        ### Call the run_annealing() function...
        start = default_timer()
        (
            f_best,
            f_xray_best,
            predicted_best,
            xyz_best,
            xray_ratio,
            harmonic_ratio,
            c,
        ) = run_annealing(nsteps)
        print("run_annealing() time: %3.2f s" % float(default_timer() - start))
        ###
        print("xray contrib ratio: %f" % xray_ratio)
        print("harmonic contrib ratio: %f" % harmonic_ratio)
        print("Accepted / Total steps: %i/%i" % (c, nsteps))
        # remove ending zeros from arrays
        #xyz_array = xyz_array[:, :, :c] if xyz_save else 0
        # end function
        return f_best, f_xray_best, predicted_best, xyz_best
