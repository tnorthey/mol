import sys
import numpy as np

# Ensure at least one file is provided
if len(sys.argv) < 2:
    print("Usage: python average_columns.py file1.dat file2.dat ...")
    sys.exit(1)

# Load all files into a list of arrays
columns = [np.loadtxt(fname) for fname in sys.argv[1:]]

# Stack columns horizontally and compute row-wise mean
data = np.column_stack(columns)
row_means = np.mean(data, axis=1)

# Print the result
for val in row_means:
    print(val)

