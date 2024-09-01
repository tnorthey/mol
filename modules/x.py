import numpy as np
from scipy import interpolate
from numpy.typing import NDArray, DTypeLike


class Xray:
    def __init__(self):
        pass

    def read_iam_coeffs(self) -> (NDArray, NDArray, NDArray):
        """returns the IAM coefficient arrays"""
        aa = np.array(
            [
                [0.489918, 0.262003, 0.196767, 0.049879],  # hydrogen
                [0.8734, 0.6309, 0.3112, 0.1780],  # helium
                [1.1282, 0.7508, 0.6175, 0.4653],  # lithium
                [1.5919, 1.1278, 0.5391, 0.7029],  # berylium
                [2.0545, 1.3326, 1.0979, 0.7068],  # boron
                [2.3100, 1.0200, 1.5886, 0.8650],  # carbon
                [12.2126, 3.1322, 2.0125, 1.1663],  # nitrogen
                [3.0485, 2.2868, 1.5463, 0.8670],  # oxygen
                [3.5392, 2.6412, 1.5170, 1.0243],  # fluorine
                [3.9553, 3.1125, 1.4546, 1.1251],  # neon
                [4.7626, 3.1736, 1.2674, 1.1128],  # sodium
                [5.4204, 2.1735, 1.2269, 2.3073],  # magnesium
                [6.4202, 1.9002, 1.5936, 1.9646],  # aluminium
                [6.2915, 3.0353, 1.9891, 1.5410],  # Siv
                [6.4345, 4.1791, 1.7800, 1.4908],  # phosphorus
                [6.9053, 5.2034, 1.4379, 1.5863],  # sulphur
                [11.4604, 7.1964, 6.2556, 1.6455],  # chlorine
            ]
        )

        bb = np.array(
            [
                [20.6593, 7.74039, 49.5519, 2.20159],  # hydrogen
                [9.1037, 3.3568, 22.9276, 0.9821],  # helium
                [3.9546, 1.0524, 85.3905, 168.261],  # lithium
                [43.6427, 1.8623, 103.483, 0.5420],  # berylium
                [23.2185, 1.0210, 60.3498, 0.1403],  # boron
                [20.8439, 10.2075, 0.5687, 51.6512],  # carbon
                [0.00570, 9.8933, 28.9975, 0.5826],  # nitrogen
                [13.2771, 5.7011, 0.3239, 32.9089],  # oxygen
                [10.2825, 4.2944, 0.2615, 26.1476],  # fluorine
                [8.4042, 3.4262, 0.2306, 21.7184],  # Ne
                [3.2850, 8.8422, 0.3136, 129.424],  # Na
                [2.8275, 79.2611, 0.3808, 7.1937],  # Mg
                [3.0387, 0.7426, 31.5472, 85.0886],  # Al
                [2.4386, 32.3337, 0.6785, 81.6937],  # Siv
                [1.9067, 27.1570, 0.5260, 68.1645],  # P
                [1.4679, 22.2151, 0.2536, 56.1720],  # S
                [0.0104, 1.1662, 18.5194, 47.7784],  # Cl
            ]
        )

        cc = np.array(
            [
                0.001305,  # hydrogen
                0.0064,  # helium
                0.0377,  # lithium
                0.0385,  # berylium
                -0.1932,  # boron
                0.2156,  # carbon
                -11.529,  # nitrogen
                0.2508,  # oxygen
                0.2776,  # fluorine
                0.3515,  # Ne
                0.6760,  # Na
                0.8584,  # Mg
                1.1151,  # Al
                1.1407,  # Si
                1.1149,  # P
                0.8669,  # S
                -9.5574,  # Cl
            ]
        )
        return aa, bb, cc

    def atomic_factor(self, atom_number, qvector):
        """returns atomic x-ray scattering factor for atom_number, and qvector"""
        aa, bb, cc = self.read_iam_coeffs()
        if isinstance(qvector, float):
            qvector = np.array([qvector])
        qlen = len(qvector)
        atomfactor = np.zeros(qlen)
        for j in range(qlen):
            for i in range(4):
                atomfactor[j] += aa[atom_number - 1, i] * np.exp(
                    -bb[atom_number - 1, i] * (0.25 * qvector[j] / np.pi) ** 2
                )
        atomfactor += cc[atom_number - 1]
        return atomfactor

    def compton_spline(self, atomic_numbers, qvector):
        """spline the compton factors to correct qvector, outputs array (atoms, qvector)"""
        natom = len(atomic_numbers)
        compton_array = np.zeros(
            (natom, len(qvector))
        )  # inelastic component for each atom
        tmp = np.load("data_/Compton_Scattering_Intensities.npz")  # compton factors
        q_compton, arr = tmp["q_compton"], tmp["compton"]
        for i in range(natom):
            tck = interpolate.splrep(q_compton, arr[atomic_numbers[i] - 1, :], s=0)
            compton_array[i, :] = interpolate.splev(qvector, tck, der=0)
        return compton_array

    def atomic_pre_molecular(
        self, atomic_numbers, qvector: NDArray, aa, bb, cc, electron_mode=False
    ):
        """both parts of IAM equation that don't depend on atom-atom distances"""
        # compton factors for inelastic effect
        compton_array = self.compton_spline(atomic_numbers, qvector)
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
                atomic_total += atomfactor**2
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

    def iam_calc(
        self,
        atomic_numbers,
        xyz,
        qvector,
        electron_mode=False,
        inelastic=False,
        compton_array=np.zeros(0),
    ):
        """calculate IAM molecular scattering curve for atoms, xyz, qvector"""
        natom = len(atomic_numbers)
        qlen = len(qvector)
        atomic = np.zeros(qlen)  # total atomic factor
        molecular = np.zeros(qlen)  # total molecular factor
        compton = np.zeros(qlen)  # total compton factor
        atomic_factor_array = np.zeros((natom, qlen))  # array of atomic factors
        if electron_mode:  # electron mode
            zfactor = atomic_numbers
            e_mode_int = 1
        else:  # assume x-ray mode
            zfactor = np.multiply(0.0, atomic_numbers)
            e_mode_int = -1
        for i in range(natom):
            tmp = self.atomic_factor(atomic_numbers[i], qvector)
            atomic_factor_array[i, :] = tmp
            atomic += (zfactor[i] - tmp) ** 2
            if inelastic:
                compton += compton_array[i, :]
        for i in range(natom):
            for j in range(i + 1, natom):  # j > i
                molecular += np.multiply(
                    (zfactor[i] - e_mode_int * atomic_factor_array[i, :]),
                    (zfactor[j] - e_mode_int * atomic_factor_array[j, :]),
                ) * np.sinc(qvector * np.linalg.norm(xyz[i, :] - xyz[j, :]) / np.pi)
        iam = atomic + 2 * molecular
        if inelastic:
            iam += compton
        return iam, atomic, molecular, compton

    def iam_calc_ewald(self, atomic_numbers, xyz, qvector):
        """
        calculate IAM function in the Ewald sphere
        """
        natom = len(atomic_numbers)
        qlen = len(qvector)
        qmin = qvector[0]
        qmax = qvector[-1]
        theta_min = 2 * np.arcsin(qmin / qmax)
        theta_max = 1 * np.pi
        phi_min = 0
        phi_max = 2 * np.pi
        th = np.linspace(theta_min, theta_max, qlen, endpoint=True)
        ph = np.linspace(phi_min, phi_max, qlen, endpoint=True)
        qx = np.zeros((qlen, qlen, qlen))
        qy = np.zeros((qlen, qlen, qlen))
        qz = np.zeros((qlen, qlen, qlen))
        for k in range(1, qlen):       # loop through spheres of non-zero radius r(kk)    
            for i in range(qlen):      # phi loop, note: skips 2*pi as f(0)=f(2*pi)
                for j in range(qlen):  # theta loop           
                    # Create x, y, z as a function of spherical coords...           
                    qx[k, j, i] = qvector[k] * np.sin(th[j]) * np.cos(ph[i])
                    qy[k, j, i] = qvector[k] * np.sin(th[j]) * np.sin(ph[i])
                    qz[k, j, i] = qvector[k] * np.cos(th[j])

        atomic = np.zeros((qlen, qlen, qlen))  # total atomic factor
        molecular = np.zeros((qlen, qlen, qlen))  # total molecular factor
        atomic_factor_array = np.zeros((natom, qlen, qlen, qlen))  # array of atomic factors
        # atomic
        for n in range(natom):
            for i in range(qlen):
                for j in range(qlen):
                    atomic_factor_array[n, :, j, i] = self.atomic_factor(
                        atomic_numbers[n], qvector
                    )
            atomic += np.power(atomic_factor_array[n, :, :, :], 2)
        # molecular
        for n in range(natom):
            for m in range(i + 1, natom):  # j > i
                fnm = np.multiply(
                    atomic_factor_array[n, :, :, :], atomic_factor_array[m, :, :, :]
                )
                xnm = xyz[n, 0] - xyz[m, 0]
                ynm = xyz[n, 1] - xyz[m, 1]
                znm = xyz[n, 2] - xyz[m, 2]
                #### do the maths again.. add to paper...
                molecular += fnm * np.cos(qx * xnm + qy * ynm + qz * znm)
        iam_total = atomic + 2 * molecular
        # the rotational average tends towards the exact sinc function solution of Debye
        # with increasing grid points (useful check!)
        ## write a test to check!
        rotavg = np.sum(iam_total, axis=(1, 2)) / qlen ** 2  # double check this double sum!
        return iam_total, rotavg


    def iam_calc_2d(self, atomic_numbers, xyz, qvector):
        """
        calculate IAM molecular scattering curve for atoms, xyz, qvector
        q on a 2d grid in radial scattering angle theta [0, pi] and azimuthal phi [0, 2*pi]
        """
        natom = len(atomic_numbers)
        qlen = len(qvector)
        # print('q')
        # print(qvector)
        qmin = qvector[0]
        qmax = qvector[-1]
        theta_min = 2 * np.arcsin(qmin / qmax)
        # print("theta_min")
        # print(theta_min)
        theta = np.linspace(theta_min, 1 * np.pi, qlen, endpoint=True)
        phi = np.linspace(0, 2 * np.pi, qlen, endpoint=True)
        print(theta)
        print(phi)
        # qx etc. must be a 2D grid...
        # hmmmm, this works but there might be a better way.
        qx = np.zeros((qlen, qlen))
        qy = np.zeros((qlen, qlen))
        qz = np.zeros((qlen, qlen))
        # why is au2ang involved? might be wrong
        # au2ang = 0.52918
        # k0 = au2ang * qmax / 2
        k0 = qmax / 2
        for i in range(qlen):
            for j in range(qlen):
                qx[i, j] = (
                    -2
                    * k0
                    * np.sin(theta[i] / 2)
                    * np.cos(theta[i] / 2)
                    * np.cos(phi[j])
                )
                qy[i, j] = (
                    -2
                    * k0
                    * np.sin(theta[i] / 2)
                    * np.cos(theta[i] / 2)
                    * np.sin(phi[j])
                )
                qz[i, j] = 2 * k0 * np.sin(theta[i] / 2) * np.sin(theta[i] / 2)
                # qx[i, j] = -k0 * np.sin(theta[i]) * np.cos(phi[j])
                # qy[i, j] = -k0 * np.sin(theta[i]) * np.sin(phi[j])
                # qz[i, j] = k0 * (1 - np.cos(theta[i]))
        atomic = np.zeros((qlen, qlen))  # total atomic factor
        molecular = np.zeros((qlen, qlen))  # total molecular factor
        atomic_factor_array = np.zeros((natom, qlen, qlen))  # array of atomic factors
        # check qmin
        # q_check = (qx ** 2 + qy ** 2 + qz ** 2) ** 0.5
        # print("qmin (check)")
        # print(q_check[0, 0])
        # atomic
        for i in range(natom):
            for j in range(qlen):
                atomic_factor_array[i, :, j] = self.atomic_factor(
                    atomic_numbers[i], qvector
                )
            atomic += np.power(atomic_factor_array[i, :, :], 2)
        # molecular
        for i in range(natom):
            for j in range(i + 1, natom):  # j > i
                fij = np.multiply(
                    atomic_factor_array[i, :, :], atomic_factor_array[j, :, :]
                )
                xij = xyz[i, 0] - xyz[j, 0]
                yij = xyz[i, 1] - xyz[j, 1]
                zij = xyz[i, 2] - xyz[j, 2]
                molecular += fij * np.cos(qx * xij + qy * yij + qz * zij)
        molecular *= 2
        iam_total = atomic + molecular
        rotavg = np.sum(iam_total, axis=1) / qlen  # phi average.. I think is correct
        return iam_total, atomic, molecular, atomic_factor_array, rotavg, qx, qy, qz

    ### other functions ... that may be called by the Gradient descent.
    ###

    def jq_atomic_factors_calc(self, atomic_numbers, qvector):
        """Calculate the atomic term of IAM x-ray scattering, J(q)
        and the array of atomic factors, [f(q)]"""
        natoms = len(atomic_numbers)
        qlen = len(qvector)
        atomic_factor_arr = np.zeros((natoms, qlen))  # array of atomic factors
        jq = np.zeros(qlen)  # total atomic factor
        for i in range(natoms):
            tmp = self.atomic_factor(atomic_numbers[i], qvector)
            atomic_factor_arr[i, :] = tmp
            jq += tmp**2
        return jq, atomic_factor_arr

    def compton_spline_calc(self, atomic_numbers, qvector):
        """spline the compton factors to correct qvector, outputs array (atoms, qvector)"""
        natoms = len(atomic_numbers)
        compton_array = np.zeros(
            (natoms, len(qvector))
        )  # inelastic component for each atom
        tmp = np.load("data_/Compton_Scattering_Intensities.npz")  # compton factors
        q_compton, arr = tmp["q_compton"], tmp["compton"]
        for i in range(natoms):
            tck = interpolate.splrep(q_compton, arr[atomic_numbers[i] - 1, :], s=0)
            compton_array[i, :] = interpolate.splev(qvector, tck, der=0)
        compton_total = np.sum(compton_array, axis=0)
        return compton_total, compton_array

    def Imol_calc(self, atomic_factor_arr, xyz, qvector):
        """Calculate the molecular term of IAM x-ray scattering, Imol(q)"""
        natoms = xyz.shape[0]
        Imol = np.zeros(len(qvector))  # total molecular factor, Imol(q)
        for i in range(natoms):
            for j in range(i + 1, natoms):  # j > i
                Imol += (
                    2
                    * np.multiply(atomic_factor_arr[i, :], atomic_factor_arr[j, :])
                    * np.sinc(qvector * np.linalg.norm(xyz[i, :] - xyz[j, :]) / np.pi)
                )
        return Imol


### End Xray class section
