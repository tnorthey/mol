"""
Run simulated annealing
"""

# run example: python3 run.py

import sys
from timeit import default_timer

start = default_timer()

# my modules
import modules.mol as mol
import modules.wrap as wrap
import modules.read_input as read_input

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()
p = read_input.Input_to_params("input.json")

# command line args

start_xyz_file = sys.argv[1] if len(sys.argv) > 1 else 0
run_id = sys.argv[2] if len(sys.argv) > 2 else 0

# Call the run function
w.run(p, start_xyz_file, run_id)

print("Total time: %3.2f s" % float(default_timer() - start))
