---
sidebar_position: 2
---

# Installation

## Requirements

- Python 3.11 or higher
- Windows 10/11 (for GUI application)

## Installation Methods

### Option 1: Windows Installer (Recommended)

Download the latest installer from the [GitHub Releases](https://github.com/Naruki-Ichihara/vmm-frc/releases) page.

1. Download `VMM-FRC_Setup_x.x.x.exe`
2. Run the installer
3. Follow the installation wizard
4. Launch VMM-FRC from the Start Menu

### Option 2: pip install

```bash
pip install vmm-frc
```

### Option 3: From Source

```bash
git clone https://github.com/Naruki-Ichihara/vmm-frc.git
cd vmm-frc
pip install -e .
```

## Running the Application

### GUI Application

After installation, launch the GUI:

```bash
vmm-frc-gui
```

Or run directly:

```bash
python -m vmm.gui
```

### Python API

```python
import vmm

# Import image sequence
from vmm.io import import_image_sequence
volume = import_image_sequence("path/to/images", "tif")

# Compute fiber orientation
from vmm.analysis import compute_structure_tensor, compute_orientation
st = compute_structure_tensor(volume, noise_scale=2.0, integration_scale=4.0)
orientation = compute_orientation(st)
```

## Dependencies

VMM-FRC requires the following packages (automatically installed):

- numpy
- scipy
- scikit-image
- opencv-python
- pyvista
- pyvistaqt
- PySide6
- matplotlib
- numba
- pandas
- pydicom
