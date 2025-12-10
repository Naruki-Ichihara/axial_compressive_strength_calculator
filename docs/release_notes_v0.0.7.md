# ACSC v0.0.7 Release Notes

## New Features

### VTK Export Functions
- **Fiber Trajectory Export** (Modelling tab): Export fiber trajectories in VTP format for visualization in Paraview. Includes TiltAngle, AzimuthAngle, and FiberID scalar arrays
- **Orientation Data Export** (Analysis tab): Export theta, phi, and reference orientation data in VTI format. Selection dialog allows choosing which fields to include
- **Vf Map Export** (Analysis tab): Export fiber volume fraction map in VTI format
- **CT Volume Export** (Volume tab): Export 3D CT image data in VTI format

### Splash Screen
- Display splash screen during application startup
- Shows software name, version, and logo
- Modern dark theme design with sharp edges

### Vf-based Fiber Spacing
- Added fiber volume fraction (Vf) based spacing option in simulation settings
- Automatically calculates fiber spacing from target Vf value
- Supports both direct spacing input and Vf-based calculation

## Improvements

### Centralized Version Management
- Single source of truth: `__version__` in `acsc/__init__.py`
- Dynamic version reference in `pyproject.toml`
- Automatic version update in `build_installer.bat` for installer

### Analysis Tab Enhancements
- Vf distribution analysis with histogram visualization
- Slice-by-slice Vf estimation
- 3D Vf map computation

## Technical Details

- VTI format: Volumetric data (orientation, Vf map, CT images)
- VTP format: Polyline data (fiber trajectories)
- PyVista-based VTK file output
