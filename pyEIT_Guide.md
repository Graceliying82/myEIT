# pyEIT User Guide for myEIT Project

This guide summarizes the key functionalities of the `pyEIT` library used in this project and explains how to use them for EIT simulation and reconstruction.

## 1. Mesh Generation (`pyeit.mesh`)

The mesh is the foundation of the Finite Element Method (FEM) simulation. It defines the geometry of the conductive body and the electrode placement.

### Key Function: `mesh.create`

```python
import pyeit.mesh as mesh

# Create a 2D circular mesh
mesh_obj = mesh.create(
    n_el=16,        # Number of electrodes
    h0=0.08,        # Mesh refinement (smaller = finer mesh)
    fd=None         # Custom shape function (default is circle)
)
```

**Output:** `mesh_obj` contains:
- `.node`: Array of (x, y) coordinates for all nodes.
- `.element`: Array of triangle indices (connectivity).
- `.el_pos`: Indices of nodes used as electrodes.

---

## 2. Measurement Protocol (`pyeit.eit.protocol`)

Defines how current is injected and voltage is measured. This is crucial for matching the simulation to real-world hardware or standard EIT patterns.

### Key Function: `protocol.create`

```python
import pyeit.eit.protocol as protocol

protocol_obj = protocol.create(
    n_el=16,            # Number of electrodes
    dist_exc=1,         # Excitation distance (1 = adjacent)
    step_meas=1,        # Measurement step (1 = adjacent)
    parser_meas="std"   # Measurement parser ("std" = skip current carrying electrodes)
)
```

**Key Attributes:**
- `.ex_mat`: Excitation matrix (pairs of current injection electrodes).
- `.meas_mat`: Measurement matrix (pairs of voltage measurement electrodes).

---

## 3. Forward Simulation (`pyeit.eit.fem`)

The Forward Problem calculates the potentials (voltages) inside the body given a known conductivity distribution and current injection.

### Key Class: `EITForward`

```python
from pyeit.eit.fem import EITForward

# Initialize Forward Solver
fwd = EITForward(mesh_obj, protocol_obj)

# 1. Solve for homogeneous background (baseline)
# perm=1.0 is standard background conductivity
f0 = fwd.solve_eit(perm=1.0)
v0 = f0.v  # Baseline Frame voltages

# 2. Solve for inhomogeneous distribution (with anomaly)
# 'perm' is an array of conductivity for each mesh element
f1 = fwd.solve_eit(perm=perm)
v1 = f1.v  # Frame voltages with anomaly
```

---

## 4. Inverse Reconstruction (`pyeit.eit`)

The Inverse Problem estimates the internal conductivity distribution (`perm`) given the boundary voltage measurements (`v1`) and the baseline (`v0`).

### 1. JAC (Jacobian / Gauss-Newton)

**What it is:**
A linearized reconstruction method. It approximates the non-linear EIT problem by calculating a Jacobian matrix (sensitivity matrix) that relates small changes in conductivity to changes in voltage.

**Pros:**
- Good for difference imaging (time difference).
- Mathematically rigorous for small perturbations.
- Highly configurable regularization (Tikhonov, NOSER).

**Cons:**
- Susceptible to noise if regularization is not tuned.
- Assumes linearity (valid only for small changes).

**Usage:**
```python
from pyeit.eit.jac import JAC

# 1. Initialize
eit = JAC(mesh_obj, protocol_obj)

# 2. Setup (Tune Parameters)
# p: Power for NOSER regularization
# lamb: Regularization parameter (higher = smoother, lower = sharper but noisier)
eit.setup(p=0.5, lamb=0.01, method="kotre")

# 3. Solve
# v1: Measurement, v0: Baseline
ds = eit.solve(v1, v0, normalize=True)
```

### 2. BP (Back Projection)

**What it is:**
A heuristic method originally derived for X-ray CT but adapted for EIT. It projects the voltage differences back along the equipotential lines.

**Pros:**
- Extremely fast.
- Robust against some types of noise.
- Simple to understand and implement.

**Cons:**
- Low spatial resolution (images look "smeared" or "star-like").
- Not quantitative (values don't represent true conductivity).

**Usage:**
```python
from pyeit.eit.bp import BP

# 1. Initialize
eit = BP(mesh_obj, protocol_obj)
eit.setup(weight="none")

# 2. Solve
ds = eit.solve(v1, v0, normalize=True)
```

### 3. GREIT (Graz consensus Reconstruction Algorithm for EIT)

**What it is:**
A modern algorithm designed to standardize lung EIT. It uses a training dataset to optimize a reconstruction matrix that minimizes error in resolution, shape, and noise.

**Pros:**
- High quality, uniform resolution.
- Optimized for biological shapes (lungs).
- Standard in clinical research.

**Cons:**
- Complex setup (requires training).
- Slower initialization (but fast reconstruction once trained).

**Usage:**
```python
from pyeit.eit.greit import GREIT

# 1. Initialize
eit = GREIT(mesh_obj, protocol_obj)

# 2. Setup (Training)
# This Step generates a training dataset and learns the matrix (takes time)
eit.setup(p=0.50, lamb=0.01)

# 3. Solve
ds = eit.solve(v1, v0, normalize=True)
```

---

## 5. Visualization (`pyeit.eit.interp2d`)

Visualizing the reconstructed data typically involves interpolating the mesh data onto a regular grid (image).

```python
import numpy as np
import matplotlib.pyplot as plt
from pyeit.eit.interp2d import sim2pts

# Interpolate mesh data (ds) to a 2D grid for plotting
# pts is the grid of coordinates
x, y = mesh_obj.node[:, 0], mesh_obj.node[:, 1]
# sim2pts interpolates the element-wise data to node-wise data or grid
# (Note: Usage varies by specific visualization need, often handled internally by plotting utils)
```

## How we use it in myEIT

In this project, we primarily use the **Forward Solver** to *simulate* the physics of a moving catheter.
1.  We move the catheter (Key input).
2.  `EITForward` calculates the resulting voltages (`v`) and we generate the known Permittivity (`perm`).
3.  We visualize the `perm` directly in 3D using `vispy` to show the "Ground Truth" field.

For **Data Replay**, we generate a synthetic dataset of these Forward solutions.
