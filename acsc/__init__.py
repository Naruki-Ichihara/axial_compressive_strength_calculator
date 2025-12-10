"""
ACSC - Axial Compressive Strength Calculator

A toolkit for analyzing fiber-reinforced composite materials.
"""

__version__ = "0.0.7"

from acsc.segment import (
    estimate_local_vf,
    estimate_vf_distribution,
    estimate_vf_slice_by_slice,
    compute_vf_map_3d,
    threshold_otsu,
    threshold_percentile,
    apply_morphological_cleaning,
)
