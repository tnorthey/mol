import numpy as np
import sys

# my modules
import modules.mol as mol
import modules.x as xray

# create class objects
m = mol.Xyz()
x = xray.Xray()

xyz_file1 = str(sys.argv[1])
xyz_file2 = str(sys.argv[2])
timestep = str(sys.argv[3])  # time-step 20, 35, 40, etc.
run_id = f"{timestep}_1d"
header, comment, atomlist, xyz1 = m.read_xyz(xyz_file1)
header, comment, atomlist, xyz2 = m.read_xyz(xyz_file2)
atomic_numbers = [m.periodic_table(symbol) for symbol in atomlist]

# TARGET_FUNCTION_20_1d.dat
target_function_file = "results_/tmp_noise0p001_qmax8_traj094_backsteps_final/TARGET_FUNCTION_20_1d.dat"
target_function = np.loadtxt(target_function_file)[:, 1]
qvector = np.loadtxt(target_function_file)[:, 0]
qlen = len(qvector)
target_data = target_function

compton_array = x.compton_spline(atomic_numbers, qvector)
def xyz2iam(xyz, atomic_numbers, compton_array):
    """convert xyz file to IAM signal"""
    electron_mode = False
    inelastic = True
    iam, atomic, molecular, compton = x.iam_calc(
        atomic_numbers, xyz, qvector, electron_mode, inelastic, compton_array
    )
    return iam

npoints = 10
for n in range(npoints + 1):
    #ratio = n / npoints + 0.5 / npoints
    ratio = n / npoints
    xyz_midpoint = ratio * xyz1 + (1 - ratio) * xyz2

    # calculate IAM
    predicted_function_ = xyz2iam(xyz_midpoint, atomic_numbers, compton_array)
    
    # calculate f_signal
    f_signal = (
        np.sum(
            (predicted_function_ - target_data) ** 2 / np.abs(target_data)
        )
        / qlen
    )

    ### write best structure to xyz file
    print("writing to xyz... (f: %10.8f)" % f_signal)
    f_best_str = ("%10.8f" % f_signal).zfill(12)
    header_str = ""
    m.write_xyz(
        "%s_%s.xyz" % (run_id, f_best_str),
        header_str,
        atomlist,
        xyz_midpoint,
    )
 
    np.savetxt(
        "%s_%s.dat" % (run_id, f_best_str),
        np.column_stack((qvector, predicted_function_)),
    )

