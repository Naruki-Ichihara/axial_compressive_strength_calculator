---
sidebar_position: 3
title: vmm.analysis
---

# vmm.analysis

Structure tensor computation and fiber orientation analysis.

## Functions

### drop_edges_3D

```python
def drop_edges_3D(width: int, volume: np.ndarray) -> np.ndarray
```

Remove edge pixels from all sides of a 3D volume to eliminate boundary artifacts.

**Args:**
- `width` (int): Number of pixels to remove from each edge.
- `volume` (np.ndarray): Input 3D array with shape (depth, height, width).

**Returns:**
- `np.ndarray`: Cropped 3D volume with shape (depth-2*width, height-2*width, width-2*width).

**Example:**

```python
import numpy as np
from vmm.analysis import drop_edges_3D

vol = np.random.rand(100, 200, 200)
cropped = drop_edges_3D(10, vol)
print(cropped.shape)  # (80, 180, 180)
```

---

### compute_structure_tensor

```python
def compute_structure_tensor(volume: np.ndarray, noise_scale: int, mode: str = 'nearest') -> np.ndarray
```

Compute 3D structure tensor for fiber orientation analysis using gradient-based methods.

The structure tensor is a symmetric 3x3 matrix field that captures local orientation information in 3D volumes. Each voxel gets a tensor describing the predominant direction of intensity gradients in its neighborhood.

**Args:**
- `volume` (np.ndarray): Input 3D grayscale volume (depth, height, width).
- `noise_scale` (int): Gaussian smoothing sigma for noise reduction before gradient computation. Larger values provide more smoothing but reduce spatial resolution.
- `mode` (str, optional): Boundary condition for Gaussian filtering. Options: 'constant', 'edge', 'wrap', 'reflect', 'mirror', 'nearest'. Default is 'nearest'.

**Returns:**
- `np.ndarray`: Structure tensor array with shape (6, depth, height, width). Components represent the upper triangular part of the symmetric 3x3 tensor: [T_xx, T_xy, T_xz, T_yy, T_yz, T_zz].

**Raises:**
- `ValueError`: If the input volume is not exactly 3D.

**Example:**

```python
from vmm.analysis import compute_structure_tensor

tensor = compute_structure_tensor(volume, noise_scale=2)
print(tensor.shape)  # (6, depth, height, width)
```

---

### compute_orientation

```python
def compute_orientation(
    structure_tensor: np.ndarray,
    reference_vector: Optional[List[float]] = None
) -> Union[Tuple[np.ndarray, np.ndarray], np.ndarray]
```

Extract fiber orientation angles from structure tensor using eigenvalue decomposition.

Computes orientation angles by finding the eigenvector corresponding to the smallest eigenvalue of each structure tensor, which represents the direction of minimal intensity variation (i.e., the fiber direction).

**Args:**
- `structure_tensor` (np.ndarray): 4D array with shape (6, depth, height, width) containing the symmetric structure tensor components.
- `reference_vector` (List[float], optional): 3D reference direction vector [x, y, z]. If provided, returns only the angle relative to this reference. If None, returns both theta and phi spherical angles.

**Returns:**
- If `reference_vector` is None: Tuple of (theta, phi) arrays with shape (depth, height, width).
  - `theta`: Azimuthal angle in degrees (-180 to 180).
  - `phi`: Elevation angle in degrees (-90 to 90).
- If `reference_vector` is provided: Single array of angles in degrees (0 to 180) relative to reference.

**Example:**

```python
from vmm.analysis import compute_structure_tensor, compute_orientation

# Compute structure tensor
tensor = compute_structure_tensor(volume, noise_scale=2)

# Get orientation relative to Z-axis
reference_vector = [0, 0, 1]
orientation = compute_orientation(tensor, reference_vector)
print(f"Mean orientation: {orientation.mean():.2f} degrees")
```

---

## Void Analysis Functions

### segment_voids_otsu

```python
def segment_voids_otsu(
    volume: np.ndarray,
    invert: bool = True,
    min_size: int = 0,
    closing_size: int = 0
) -> Tuple[np.ndarray, float]
```

Segment voids in a 3D volume using Otsu's thresholding method.

**Args:**
- `volume` (np.ndarray): Input 3D grayscale volume (depth, height, width).
- `invert` (bool): If True (default), assumes voids are darker than material.
- `min_size` (int): Minimum void size in voxels. Smaller regions are removed.
- `closing_size` (int): Morphological closing kernel size for filling small holes.

**Returns:**
- `Tuple[np.ndarray, float]`: Binary mask (True = void) and computed threshold value.

**Example:**

```python
from vmm.analysis import segment_voids_otsu

void_mask, threshold = segment_voids_otsu(volume, min_size=100)
void_fraction = np.mean(void_mask) * 100
print(f"Void fraction: {void_fraction:.2f}%")
```

---

### segment_voids_from_insegt

```python
def segment_voids_from_insegt(
    segmentation: np.ndarray,
    void_label: int = 3
) -> np.ndarray
```

Extract void regions from InSegt segmentation results.

InSegt uses: Label 1 = Fiber (Cyan), Label 2 = Matrix (Magenta), Label 3 = Void (Yellow).

**Args:**
- `segmentation` (np.ndarray): 3D array of InSegt segmentation labels.
- `void_label` (int): Label value for void regions (default: 3).

**Returns:**
- `np.ndarray`: Boolean 3D array where True indicates void regions.

**Example:**

```python
from vmm.analysis import segment_voids_from_insegt

void_mask = segment_voids_from_insegt(insegt_result)
```

---

### compute_void_statistics

```python
def compute_void_statistics(
    void_mask: np.ndarray,
    voxel_size: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    min_void_size: int = 1
) -> Dict
```

Compute comprehensive statistics for void regions.

**Args:**
- `void_mask` (np.ndarray): Boolean 3D array where True indicates void regions.
- `voxel_size` (Tuple[float, float, float]): Physical size of each voxel as (z, y, x).
- `min_void_size` (int): Minimum void size in voxels to include.

**Returns:**
- `Dict`: Dictionary containing:
  - `void_fraction`: Total void volume fraction (0-1)
  - `void_fraction_percent`: Total void volume fraction (%)
  - `num_voids`: Number of distinct void regions
  - `mean_void_size`, `max_void_size`, `min_void_size`: Size statistics
  - `mean_sphericity`: Mean sphericity of voids (0-1)
  - `slice_void_fractions`: Void fraction per slice

**Example:**

```python
from vmm.analysis import compute_void_statistics

stats = compute_void_statistics(void_mask, voxel_size=(0.5, 0.5, 0.5))
print(f"Void fraction: {stats['void_fraction_percent']:.2f}%")
print(f"Number of voids: {stats['num_voids']}")
```

---

### compute_local_void_fraction

```python
def compute_local_void_fraction(
    void_mask: np.ndarray,
    window_size: int = 50,
    gaussian_sigma: Optional[float] = None
) -> np.ndarray
```

Compute local void fraction map using sliding window or Gaussian averaging.

**Args:**
- `void_mask` (np.ndarray): Boolean 3D array where True indicates void regions.
- `window_size` (int): Size of the averaging window in voxels.
- `gaussian_sigma` (float, optional): Use Gaussian-weighted averaging if provided.

**Returns:**
- `np.ndarray`: 3D array of local void fractions (0-1).

**Example:**

```python
from vmm.analysis import compute_local_void_fraction

local_vf = compute_local_void_fraction(void_mask, window_size=30)
hot_spots = local_vf > 0.1  # Regions with >10% local void content
```

---

### analyze_void_distribution

```python
def analyze_void_distribution(
    void_mask: np.ndarray,
    bins: int = 50,
    log_scale: bool = True
) -> Tuple[np.ndarray, np.ndarray, Dict]
```

Analyze the size distribution of voids.

**Args:**
- `void_mask` (np.ndarray): Boolean 3D array where True indicates void regions.
- `bins` (int): Number of histogram bins.
- `log_scale` (bool): Use logarithmic binning if True.

**Returns:**
- `Tuple`: (histogram counts, bin edges, statistics dict)

---

## Orientation Masking Functions

### mask_orientation_with_voids

```python
def mask_orientation_with_voids(
    theta: np.ndarray,
    void_mask: np.ndarray,
    dilation_pixels: int = 0,
    phi: Optional[np.ndarray] = None
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]
```

Mask orientation data using void regions.

Sets orientation values to NaN where voids are present, optionally dilating the void mask to exclude regions near voids.

**Args:**
- `theta` (np.ndarray): 3D array of theta orientation angles.
- `void_mask` (np.ndarray): Boolean 3D array where True indicates void regions.
- `dilation_pixels` (int): Number of pixels to dilate the void mask.
- `phi` (np.ndarray, optional): 3D array of phi orientation angles.

**Returns:**
- Masked theta array (or tuple of masked theta and phi if phi provided).

**Example:**

```python
from vmm.analysis import mask_orientation_with_voids

masked_theta = mask_orientation_with_voids(theta, void_mask, dilation_pixels=5)
# Orientation values at and near voids are now NaN
```

---

### crop_orientation_to_roi

```python
def crop_orientation_to_roi(
    theta: np.ndarray,
    roi_bounds: List[int],
    void_mask: Optional[np.ndarray] = None,
    void_roi_bounds: Optional[List[int]] = None,
    dilation_pixels: int = 0,
    phi: Optional[np.ndarray] = None
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]
```

Crop orientation data to ROI and optionally mask with voids.

**Args:**
- `theta` (np.ndarray): 3D array of theta orientation angles.
- `roi_bounds` (List[int]): ROI bounds as [z_min, z_max, y_min, y_max, x_min, x_max].
- `void_mask` (np.ndarray, optional): Boolean 3D array of void regions.
- `void_roi_bounds` (List[int], optional): ROI bounds for void mask if different.
- `dilation_pixels` (int): Number of pixels to dilate void mask.
- `phi` (np.ndarray, optional): 3D array of phi orientation angles.

**Returns:**
- Cropped (and optionally masked) orientation data.

**Example:**

```python
from vmm.analysis import crop_orientation_to_roi

cropped_theta = crop_orientation_to_roi(
    theta, [0, 100, 0, 200, 0, 200],
    void_mask=void_mask, dilation_pixels=3
)
```
