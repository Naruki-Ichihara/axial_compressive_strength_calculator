---
sidebar_position: 1
title: API Reference
---

# VMM-FRC API Reference

Complete API documentation for VMM-FRC (Virtual Microstructure Modeling for Fiber Reinforced Polymer Composites).

## Core Modules

### Image I/O
- **vmm.io** - Image sequence import/export utilities

### Analysis
- **vmm.analysis** - Structure tensor computation and fiber orientation analysis
- **vmm.segment** - Image segmentation and fiber volume fraction estimation

### Simulation
- **vmm.simulation** - Virtual microstructure generation
- **vmm.fiber_trajectory** - Fiber trajectory modeling and generation

### Visualization
- **vmm.visualize** - 3D visualization utilities

:::info API Documentation Generation
詳細なAPI ドキュメントは `pydoc-markdown` で生成されます。
`docs/` ディレクトリで以下を実行してください：
```bash
pip install pydoc-markdown
python -m pydoc_markdown
```
:::

## Quick Reference

### Import Image Sequence

```python
from vmm.io import import_image_sequence

volume = import_image_sequence(
    directory="path/to/images",
    file_format="tif",
    grayscale=True
)
```

### Compute Fiber Orientation

```python
from vmm.analysis import compute_structure_tensor, compute_orientation

# Compute structure tensor
structure_tensor = compute_structure_tensor(
    volume,
    noise_scale=2.0,
    integration_scale=4.0
)

# Compute orientation relative to reference axis
reference_vector = [0, 0, 1]  # Z-axis
orientation = compute_orientation(structure_tensor, reference_vector)
```

### Estimate Volume Fraction

```python
from vmm.segment import estimate_vf_distribution, threshold_otsu

# Binarize image
threshold = threshold_otsu(volume)
binary = volume > threshold

# Estimate Vf distribution
vf_stats = estimate_vf_distribution(binary)
```

## Browse All

Use the sidebar to explore all classes, functions, and modules in detail.
