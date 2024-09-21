# mol

### File tree

<!-- TREEVIEW START -->
```bash
├── data_/
│   ├── nmm/
├── images/
├── mathematica/
├── modules/
│   ├── __pycache__/
├── nm/
├── noise/
├── __pycache__/
├── scripts/
├── shell_scripts/
├── sine_transform/
├── tests/
│   ├── __pycache__/
└── xyz/
    ├── target_traj090/
    ├── target_traj094/
    ├── target_traj099/
```

<!-- TREEVIEW END -->

### setup

create a virtual env. install numpy, scipy

### run tests using pytest
```sh
pytest -v

```

### Example script can be run for CHD with the "go" script

the target xyz files are in the xyz/target\_traj099/ directory
choose which frame to be the target with, e.g. for frame 20,
```sh
./go_1d_chd.sh 20
```

it will run the `run_1d_chd.py` script, which calls files in the modules directory, namely the wrap.py file, which calls the sa.py routines to run simulated annealing.

