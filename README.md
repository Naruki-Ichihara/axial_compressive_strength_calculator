# Axial Compressive Strength Calculator (ACSC)

A computational framework for analyzing fiber-reinforced composite materials through 3D imaging. The system processes volumetric image data to extract fiber orientation fields, then calculates axial compressive strength using micromechanical models that account for fiber misalignment effects.

## Features

- **3D Image Processing**: Import and process volumetric image sequences (TIF, PNG, JPG, DICOM)
- **Structure Tensor Analysis**: Compute fiber orientation fields using gradient-based methods
- **Micromechanical Modeling**: Calculate compression strength with power-law plasticity model
- **Interactive GUI**: PySide6-based interface with 2D/3D visualization and analysis tools
- **High Performance**: Numba JIT-compiled computations with parallel execution

## Installation

### Standard Installation

```bash
# Clone the repository
git clone <repository-url>
cd axial_compressive_strength_calculator

# Install in development mode (recommended for development)
pip install -e .

# Or install normally
pip install .

# Install with optional development tools
pip install -e ".[dev]"

# Install with build tools (for creating executables)
pip install -e ".[build]"
```

### Docker Installation (Recommended for Linux/WSL)

```bash
# Start container with X11/GUI support
docker-compose up -d

# Enter container
docker exec -it acsc /bin/bash

# Inside container, run the GUI
python run_gui.py
```

## Requirements

### System Requirements

- **Python**: 3.11, 3.12, or 3.13
- **Display Server**: X11 or Wayland (for GUI)
- **Memory**: 4GB+ recommended for large image volumes

### X11 Configuration

The GUI requires a display server. For headless environments:

**WSL2 Users:**
- WSLg provides built-in X11/Wayland support (Windows 11)
- The provided `docker-compose.yml` is pre-configured for WSL2

**Linux Remote/SSH:**
```bash
# Enable X11 forwarding
ssh -X user@remote-host

# Or set DISPLAY variable
export DISPLAY=:0
```

**Docker Users:**
- Use the provided `docker-compose.yml` which maps `/tmp/.X11-unix` and `/mnt/wslg`
- Ensure host X11 server allows connections: `xhost +local:`

## Usage

### Launching the GUI

```bash
# Using the run_gui.py script
python run_gui.py

# Or using the installed console script (after pip install)
acsc-gui
```

### Programmatic Usage

```python
from acsc.io import import_image_sequence
from acsc.analysis import compute_structure_tensor, compute_orientation, drop_edges_3D
from acsc.simulation import estimate_compression_strength_from_profile, MaterialParams

# Load image sequence
volume = import_image_sequence("data/NTC_S/NTC_", 100, 4, "tif")

# Compute structure tensor and orientation
tensor = compute_structure_tensor(volume, noise_scale=1.0)
orientation = compute_orientation(tensor, reference_vector=[1, 0, 0])
orientation = drop_edges_3D(5, orientation)

# Define material properties
material = MaterialParams(
    longitudinal_modulus=150000,  # E1 (MPa)
    transverse_modulus=10000,     # E2 (MPa)
    poisson_ratio=0.3,            # ν
    shear_modulus=5000,           # G (MPa)
    tau_y=50,                     # Yield stress (MPa)
    K=0.1,                        # Hardening coefficient
    n=2.0                         # Hardening exponent
)

# Calculate compression strength
strength, strain, stress_curve, strain_array = \
    estimate_compression_strength_from_profile(orientation, material)

print(f"Compression Strength: {strength:.2f} MPa")
print(f"Ultimate Strain: {strain:.4f}")
```

## Project Structure

```
/workspace/
├── acsc/                     # Main package
│   ├── io.py                # Image/volume input pipeline
│   ├── analysis.py          # Structure tensor analysis
│   ├── simulation.py        # Compression strength calculation
│   └── gui.py               # PySide6 GUI application
├── data/                    # Sample image sequences
│   ├── NTC_S/               # NTC sample (1,024 TIF files)
│   └── T1C_S/               # T1C sample (1,024 TIF files)
├── run_gui.py               # GUI entry point script
├── pyproject.toml           # Modern Python package configuration (PEP 621)
└── docker-compose.yml       # Docker environment
```

## Dependencies

### Core Analysis
- **numpy**: Numerical computing and array operations
- **numba**: JIT compilation for performance-critical code
- **scipy**: Scientific computing (interpolation, signal processing, statistics)
- **scikit-image**: Image processing and structure tensor computation
- **pandas**: Data analysis

### Image I/O
- **opencv-python**: Image import (TIF, PNG, JPG)
- **pydicom**: DICOM medical image support

### GUI Framework
- **PySide6**: Qt bindings for GUI
- **matplotlib**: Plotting and visualization
- **pyvista**: 3D visualization
- **pyvistaqt**: PyVista integration with Qt

## Data Format

### Image Sequences
- **Supported formats**: TIF, PNG, JPG, DICOM
- **Naming convention**: Zero-padded indices (e.g., `NTC_0000.tif`, `NTC_0001.tif`, ...)
- **Volume convention**: (depth, height, width) = (z, y, x)
- **Sample data**: Included in `data/` directory (1,024 images per dataset)

### Material Parameters
The `MaterialParams` dataclass requires:
- `longitudinal_modulus` (E1): Fiber-direction modulus (MPa)
- `transverse_modulus` (E2): Transverse modulus (MPa)
- `poisson_ratio` (ν): Poisson's ratio
- `shear_modulus` (G): Shear modulus (MPa)
- `tau_y`: Matrix yield stress (MPa)
- `K`: Hardening coefficient
- `n`: Hardening exponent

## Algorithm Overview

### Data Flow Pipeline

```
Image Files → import_image_sequence() → 3D Volume
    ↓
compute_structure_tensor() → Structure Tensor (6 components)
    ↓
compute_orientation() → Fiber Orientation Angles (degrees)
    ↓
Histogram Analysis → Probability Distribution
    ↓
estimate_compression_strength_from_profile() → Strength, Strain, Stress Curve
```

### Micromechanical Model

**Power-law plasticity model:**
- Elastic regime: τ = G × γ
- Plastic regime: γ = (τ/G) + K(τ/τ_y)^n

**Strength calculation:**
1. Discretize shear stress range and compute shear strains
2. For each misalignment angle, compute axial stress-strain relationship
3. Interpolate to create uniform strain arrays
4. Weight contributions by measured probability distribution
5. Superpose weighted stress contributions
6. Detect failure using peak detection on stress-strain curve

## Performance

- **JIT Compilation**: Numba-accelerated orientation calculations with parallel execution
- **Memory Efficiency**: Float32 precision for structure tensors
- **Vectorization**: NumPy operations throughout for optimal performance
- **Lazy Processing**: Optional on-the-fly image transformations

## Development

### Package Configuration

This project uses modern Python packaging with `pyproject.toml` (PEP 621):
- All metadata, dependencies, and build configuration in one file
- No legacy `setup.py` or `setup.cfg` files
- Fully compatible with pip, build, and other modern Python tools

### Running Tests
```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=acsc --cov-report=html
```

### Code Quality Tools
```bash
# Format code with black
black acsc/

# Lint with ruff
ruff check acsc/

# Auto-fix linting issues
ruff check --fix acsc/
```

### Building Executables
```bash
# Install build dependencies
pip install -e ".[build]"

# Build with PyInstaller (configuration in build scripts)
pyinstaller run_gui.py --name ACSC_GUI
```

Cross-platform executables are built via GitHub Actions:
- Windows: `ACSC_GUI_windows.exe`
- Linux: `ACSC_GUI_linux`
- macOS: `ACSC_GUI_macos.app`

## Troubleshooting

### GUI Not Launching

**Error: "Could not connect to display"**
```bash
# Check DISPLAY variable
echo $DISPLAY

# For WSL2, ensure WSLg is working
wslg --version

# For Docker, verify X11 forwarding
xhost +local:
```

**Error: "No module named 'PySide6'"**
```bash
# Reinstall with all dependencies
pip install -e .
```

### Import Errors

**Error: "No module named 'acsc'"**
```bash
# Install in development mode
pip install -e .
```

## License

MIT License

## Author

Naruki Ichihara (ichihara.naruki@nihon-u.ac.jp)

## Citation

If you use this software in your research, please cite:

```
[Add citation information here]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This project uses the following open-source libraries:
- NumPy, SciPy, scikit-image for scientific computing
- PySide6 for GUI framework
- PyVista for 3D visualization
- Numba for JIT compilation
