# VMM-FRC v0.0.11 Release Notes

## New Features

### Void Analysis System (InSegt Integration)
- **3-Class Segmentation**: InSegt annotator now supports 3 classes:
  - Cyan (Label 1): Fiber
  - Magenta (Label 2): Matrix
  - Yellow (Label 3): Void
- **Void Overlay Visualization**: Void regions detected by InSegt are displayed as red overlay on all slice views (XY, XZ, YZ)
- **Void Statistics**: Comprehensive void analysis including:
  - Void fraction (%)
  - Number of voids
  - Mean/max/min void sizes
  - Sphericity analysis
  - Slice-by-slice void distribution

### Orientation Masking with Void Regions
- **Crop Orientation with Void**: New button to mask orientation data using InSegt void results
- **Dilation Support**: Configurable pixel dilation around void regions to exclude unreliable orientation data near voids
- **Automatic Alignment**: Void mask automatically aligned to orientation data considering trim width differences

### Reset All Analysis
- **Reset Button**: New "Reset All" button in the ribbon toolbar to clear all analysis results:
  - Orientation data (theta, phi, reference)
  - Vf maps and overlays
  - Void analysis results
  - Fiber detection results
  - InSegt models

## Improvements

### InSegt Labeling Tool UI
- **Improved Status Bar**: Two-line status bar with clear separation
  - First line: Panel labels ("Annotation Panel", "Segmentation Result")
  - Second line: Current label (color-coded), pen size, live update status
- **Color-Coded Labels**: Current label displayed in its actual color (Cyan/Magenta/Yellow)
- **Keyboard Hints**: Quick reference for shortcuts displayed on the right side
- **Fixed Text Overlap**: Resolved garbled text issue in the status area

### Analysis Module Enhancements
New `analysis.py` functions:
- `segment_voids_otsu()`: Otsu-based void segmentation
- `segment_voids_from_insegt()`: Extract voids from InSegt results
- `compute_void_statistics()`: Comprehensive void analysis
- `compute_local_void_fraction()`: Local void fraction mapping
- `analyze_void_distribution()`: Void size distribution analysis
- `mask_orientation_with_voids()`: Mask orientation with void regions
- `crop_orientation_to_roi()`: Crop and mask orientation data

## Bug Fixes
- Fixed `TypeError: 'NoneType' object does not support item assignment` when computing orientation after Reset All
- Fixed void mask alignment issue when void_mask shape doesn't match orientation theta shape due to trim_width differences
- Fixed "No void regions found" warning appearing despite voids being visible
- Fixed colormap/histogram not updating after applying void mask

## Technical Changes
- Removed old threshold-based void analysis from Viewer2D
- Added proper initialization check for `orientation_data` dictionary
- Improved void overlay rendering with correct coordinate transformations
