---
sidebar_position: 6
title: Void Analysis
---

# Void Analysis

This document explains how to detect and analyze voids (porosity) in fiber-reinforced composite materials using VMM-FRC.

## Overview

Voids are defects in composite materials that can significantly affect mechanical properties. VMM-FRC provides two methods for void detection:

1. **Otsu Thresholding**: Automatic threshold-based segmentation
2. **InSegt Segmentation**: Interactive machine learning-based segmentation with 3-class labeling

## Methods

### Otsu-based Void Detection

Otsu's method automatically determines the optimal threshold to separate voids (dark regions) from the material:

```python
from vmm.analysis import segment_voids_otsu, compute_void_statistics

# Segment voids using Otsu's method
void_mask, threshold = segment_voids_otsu(
    volume,
    invert=True,      # Voids are darker than material
    min_size=100,     # Remove small noise
    closing_size=2    # Fill small holes
)

# Compute statistics
stats = compute_void_statistics(void_mask)
print(f"Void fraction: {stats['void_fraction_percent']:.2f}%")
print(f"Number of voids: {stats['num_voids']}")
```

### InSegt-based Void Detection

For more accurate void detection, use InSegt's interactive 3-class segmentation:

| Label | Color | Class |
|-------|-------|-------|
| 1 | Cyan | Fiber |
| 2 | Magenta | Matrix |
| 3 | Yellow | Void |

```python
from vmm.analysis import segment_voids_from_insegt

# After InSegt segmentation
void_mask = segment_voids_from_insegt(insegt_result, void_label=3)
```

## Using the GUI

### Step 1: Load Data and Define ROI

1. Load your CT volume
2. Create an ROI around the region of interest
3. Ensure orientation analysis is completed for the ROI

### Step 2: InSegt Labeling

1. Click **Train InSegt** in the Segmentation ribbon group
2. In the labeling tool:
   - **Key 1**: Fiber label (Cyan)
   - **Key 2**: Matrix label (Magenta)
   - **Key 3**: Void label (Yellow)
   - **Key 0**: Eraser
   - **Arrow keys**: Adjust pen size
   - **L**: Toggle live update
3. Draw annotations on fiber, matrix, and void regions
4. Close the window when satisfied with segmentation

### Step 3: Apply to Volume

1. Click **Apply InSegt** to apply the trained model to all slices
2. The void regions will be highlighted in red overlay

### Step 4: Mask Orientation Data

1. Click **Crop Orientation** in the Void ribbon group
2. Set dilation pixels (recommended: 3-5 pixels)
3. Click OK to mask orientation data

The orientation values at void locations (and optionally nearby regions) will be set to NaN, excluding them from subsequent analysis.

## Void Statistics

The `compute_void_statistics` function provides comprehensive analysis:

```python
from vmm.analysis import compute_void_statistics

stats = compute_void_statistics(void_mask, voxel_size=(1.0, 1.0, 1.0))

# Available statistics
print(f"Void fraction: {stats['void_fraction_percent']:.2f}%")
print(f"Number of voids: {stats['num_voids']}")
print(f"Mean void size: {stats['mean_void_size']:.1f} voxels")
print(f"Max void size: {stats['max_void_size']:.1f} voxels")
print(f"Mean sphericity: {stats['mean_sphericity']:.3f}")
```

### Statistics Output

| Metric | Description |
|--------|-------------|
| `void_fraction` | Total void volume fraction (0-1) |
| `void_fraction_percent` | Total void volume fraction (%) |
| `num_voids` | Number of distinct void regions |
| `mean_void_size` | Mean void volume |
| `max_void_size` | Maximum void volume |
| `min_void_size` | Minimum void volume |
| `mean_sphericity` | Mean sphericity (1 = perfect sphere) |
| `slice_void_fractions` | Void fraction per slice |

## Local Void Fraction Mapping

Identify regions with high void concentration:

```python
from vmm.analysis import compute_local_void_fraction

# Compute local void fraction with 30-voxel window
local_vf = compute_local_void_fraction(void_mask, window_size=30)

# Or use Gaussian smoothing
local_vf_smooth = compute_local_void_fraction(void_mask, gaussian_sigma=10.0)

# Find hotspots
hotspots = local_vf > 0.1  # Regions with >10% local void content
```

## Void Size Distribution

Analyze the distribution of void sizes:

```python
from vmm.analysis import analyze_void_distribution
import matplotlib.pyplot as plt

hist, bin_edges, stats = analyze_void_distribution(void_mask, bins=50, log_scale=True)

print(f"Total voids: {stats['count']}")
print(f"Median size: {stats['median_size']:.1f} voxels")

# Plot histogram
plt.figure(figsize=(10, 6))
plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), align='edge')
plt.xscale('log')
plt.xlabel('Void Size (voxels)')
plt.ylabel('Count')
plt.title('Void Size Distribution')
plt.show()
```

## Masking Orientation with Voids

Exclude void regions from orientation analysis:

```python
from vmm.analysis import mask_orientation_with_voids, crop_orientation_to_roi

# Method 1: Direct masking
masked_theta = mask_orientation_with_voids(
    theta,
    void_mask,
    dilation_pixels=5  # Also exclude 5 pixels around voids
)

# Method 2: Crop and mask in one step
cropped_theta = crop_orientation_to_roi(
    theta,
    roi_bounds=[0, 100, 0, 200, 0, 200],
    void_mask=void_mask,
    dilation_pixels=3
)
```

### Why Mask Orientation Data?

Orientation analysis at void locations is unreliable because:
- Voids have no fiber structure to analyze
- Boundary regions near voids have distorted gradients
- Including voids skews statistical analysis

The dilation option extends the mask to exclude regions near voids where orientation may be affected by boundary effects.

## Complete Workflow Example

```python
import numpy as np
from vmm.io import import_image_sequence
from vmm.analysis import (
    compute_structure_tensor,
    compute_orientation,
    segment_voids_otsu,
    compute_void_statistics,
    mask_orientation_with_voids
)

# Load CT data
volume = import_image_sequence("data/ct_scan/slice", 100, 4, "tif")

# Compute orientation
tensor = compute_structure_tensor(volume, noise_scale=2)
theta, phi = compute_orientation(tensor)

# Detect voids
void_mask, threshold = segment_voids_otsu(volume, min_size=50)

# Get void statistics
stats = compute_void_statistics(void_mask)
print(f"Void fraction: {stats['void_fraction_percent']:.2f}%")

# Mask orientation data
masked_theta = mask_orientation_with_voids(theta, void_mask, dilation_pixels=3)
masked_phi = mask_orientation_with_voids(phi, void_mask, dilation_pixels=3)

# Compute statistics excluding voids
valid_theta = masked_theta[~np.isnan(masked_theta)]
print(f"Mean orientation (excluding voids): {np.mean(valid_theta):.2f} degrees")
print(f"Std orientation (excluding voids): {np.std(valid_theta):.2f} degrees")
```

## Best Practices

1. **Use InSegt for complex images**: When voids have similar intensity to matrix regions, InSegt provides more accurate segmentation than Otsu thresholding.

2. **Set appropriate dilation**: Use 3-5 pixels of dilation to exclude boundary effects near voids.

3. **Check void overlay**: Visually verify the void detection using the red overlay in the GUI before applying orientation masking.

4. **Consider minimum size**: Set `min_size` in Otsu segmentation to remove noise-induced false positives.

5. **Validate with statistics**: Compare void fraction with expected manufacturing quality metrics.
