"""
Run simulated annealing
"""

# run example: python3 run.py ...

from timeit import default_timer

start = default_timer()
import os
import sys
import json
import numpy as np

# my modules
import modules.mol as mol
import modules.wrap as wrap
import modules.read_input as read_input

# create class objects
m = mol.Xyz()
w = wrap.Wrapper()
p = read_input.Input_to_params("input.json")

# Call the run function
w.run(p)

print("Total time: %3.2f s" % float(default_timer() - start))
