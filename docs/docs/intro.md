---
sidebar_position: 1
---

# Introduction to VMM-FRC

**VMM-FRC** (Virtual Microstructure Modeling for Fiber Reinforced Polymer Composites) is a computational framework for analyzing fiber-reinforced composite materials through 3D imaging.

## Key Features

- **3D Image Analysis**: Process volumetric CT/micro-CT image data to extract fiber microstructure
- **Fiber Orientation Analysis**: Compute fiber orientation fields using structure tensor analysis
- **Volume Fraction Estimation**: Calculate fiber volume fraction (Vf) distribution
- **Virtual Microstructure Generation**: Generate virtual fiber microstructures for simulation
- **VTK Export**: Export data for visualization in Paraview and other tools

## Getting Started

New to VMM-FRC? Start here:

1. **[Installation](getting-started/installation.md)** - Install VMM-FRC and its dependencies
2. **[API Reference](api/index.md)** - Explore the API documentation

## Core Modules

### Image I/O
- **vmm.io** - Image sequence import/export utilities

### Analysis
- **vmm.analysis** - Structure tensor and orientation analysis
- **vmm.segment** - Segmentation and Vf estimation

### Simulation
- **vmm.simulation** - Virtual microstructure generation
- **vmm.fiber_trajectory** - Fiber trajectory modeling

### Visualization
- **vmm.visualize** - 3D visualization utilities

## License

VMM-FRC is licensed under the MIT License.

## Acknowledgments

VMM-FRC builds upon:
- [NumPy](https://numpy.org/) for numerical computing
- [scikit-image](https://scikit-image.org/) for image processing
- [PyVista](https://pyvista.org/) for 3D visualization
- [PySide6](https://doc.qt.io/qtforpython-6/) for GUI framework
