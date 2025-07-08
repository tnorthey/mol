````{verbatim} 
 ___ ___ _______ _______ _______ _______ _____   
|   |   |     __|   _   |   |   |       |     |_ 
|-     -|__     |       |       |   -   |       |
|___|___|_______|___|___|__|_|__|_______|_______|

````

### setup conda

Setup miniconda and install packages with conda-forge

Then, create a virtual environment with it:
```sh
conda create --name myenv
```

Activate your environment:
```sh
conda activate myenv
```

Install required packages with conda-forge,
```sh
conda install -c conda-forge pyscf numba rdkit openbabel openmm openff-toolkit
```

### run tests using pytest
```sh
pytest -v

```
or run the `pytest_script.sh`.

### Example run

- Edit the `input.json` with the parameters you want
- xyz files are in the xyz/ directory

Run,
```sh
python run.py
```

Install packages
```sh
conda create --name myenv
```


### run tests using pytest
```sh
pytest -v

```
or run the `pytest_script.sh`.

### Example run

- Edit the `input.json` with the parameters you want
- xyz files are in the xyz/ directory

Run,
```sh
python run.py
```


### run tests using pytest
```sh
pytest -v

```
or run the `pytest_script.sh`.

### Example run

- Edit the `input.json` with the parameters you want
- xyz files are in the xyz/ directory

Run,
```sh
python run.py
```
