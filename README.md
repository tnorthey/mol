# Simulated Annealing for Molecular Geometry Retrieval

This repository contains the Python implementation of the **simulated annealing (SA) framework** described in:

> **Retrieval of molecular geometries from ultrafast x-ray scattering by simulated annealing**  
> Thomas Northey, Peter M. Weber, and Adam Kirrander  
> (2025)

The code enables the retrieval of molecular geometries from **ultrafast x-ray scattering data** using simulated annealing with chemically informed constraints, as presented in the paper.

---

## 📦 Installation (via Conda)

We recommend using **[Miniconda](https://docs.conda.io/en/latest/miniconda.html)** or **Anaconda** for environment setup.

1. Create a new conda environment:
   ```sh
   conda create --name sa_geom python=3.10
   conda activate sa_geom
   ```

2. Install the required packages from `conda-forge`:
   ```sh
   conda install -c conda-forge pyscf numba rdkit openbabel openmm openff-toolkit openff-forcefields
   ```

This ensures reproducibility and avoids version conflicts across platforms.

---

## 🧪 Running Tests

To verify the installation:
```sh
pytest -v
```
or run:
```sh
./pytest_script.sh
```

---

## 🚀 Example Usage

1. Edit the configuration in `input.json` (set simulation parameters).  
2. Place any required molecular `.xyz` files in the `xyz/` directory.  
3. Run the main script:
   ```sh
   python run.py
   ```

---

## ⚙️ Key Parameters (from the Paper)

The default simulated annealing (SA) and greedy algorithm (GA) parameters used in the study are:

| Parameter   | Value  | Description |
|-------------|--------|-------------|
| `T0`        | 1      | Initial temperature (maximises conformational search space) |
| `Δs`        | 0.012  | Step size for random displacements |
| `NSA`       | 4000   | Iterations per SA run |
| `NGA`       | 20000  | Iterations for greedy (downhill-only) refinement |
| `nrestarts` | 5      | Number of SA restarts before greedy refinement |

Additional details:
- Hydrogen normal modes (>3000 cm⁻¹) are damped (factor = 0.2).  
- Bond-length and angular constraints are taken from **OpenFF force fields** to guide optimisation.  
- The final optimisation is performed with the **greedy algorithm** (`P_uphill = 0`) for local refinement.  

These parameters can be adjusted in the input configuration files for different systems.

---

## 📖 Reference

If you use this code in your work, please cite:

> Northey, T., Weber, P. M., & Kirrander, A. *Retrieval of molecular geometries from ultrafast x-ray scattering by simulated annealing*. (2025).  

---
