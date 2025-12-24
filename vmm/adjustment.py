"""
Image adjustment module for volume data.
Provides interactive adjustment of brightness, contrast, gamma, and sharpness.
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class AdjustmentSettings:
    """Container for all image adjustment settings."""
    brightness: float = 0.0      # Range: -100 to 100
    contrast: float = 1.0        # Range: 0.1 to 3.0
    gamma: float = 1.0           # Range: 0.1 to 3.0
    sharpness: float = 0.0       # Range: 0 to 100
    invert: bool = False         # Invert intensity

    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return {
            'brightness': self.brightness,
            'contrast': self.contrast,
            'gamma': self.gamma,
            'sharpness': self.sharpness,
            'invert': self.invert
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AdjustmentSettings':
        """Create settings from dictionary."""
        return cls(
            brightness=data.get('brightness', 0.0),
            contrast=data.get('contrast', 1.0),
            gamma=data.get('gamma', 1.0),
            sharpness=data.get('sharpness', 0.0),
            invert=data.get('invert', False)
        )

    def is_default(self) -> bool:
        """Check if all settings are at default values."""
        return (self.brightness == 0.0 and
                self.contrast == 1.0 and
                self.gamma == 1.0 and
                self.sharpness == 0.0 and
                not self.invert)

    def reset(self):
        """Reset all settings to default values."""
        self.brightness = 0.0
        self.contrast = 1.0
        self.gamma = 1.0
        self.sharpness = 0.0
        self.invert = False


class ImageAdjuster:
    """Handles image adjustment operations for volume data."""

    def __init__(self):
        self.settings = AdjustmentSettings()
        self._original_volume: Optional[np.ndarray] = None
        self._original_dtype = None
        self._original_min = None
        self._original_max = None

    def set_original_volume(self, volume: np.ndarray):
        """Store the original volume for adjustment reference."""
        self._original_volume = volume.copy()
        self._original_dtype = volume.dtype
        self._original_min = float(volume.min())
        self._original_max = float(volume.max())

    def get_original_volume(self) -> Optional[np.ndarray]:
        """Get the stored original volume."""
        return self._original_volume

    def has_original_volume(self) -> bool:
        """Check if original volume is stored."""
        return self._original_volume is not None

    def apply_brightness(self, image: np.ndarray, brightness: float) -> np.ndarray:
        """
        Apply brightness adjustment.

        Args:
            image: Input image (normalized 0-1)
            brightness: Brightness value (-100 to 100)

        Returns:
            Adjusted image
        """
        if brightness == 0:
            return image

        # Convert brightness to 0-1 scale
        offset = brightness / 100.0
        return np.clip(image + offset, 0, 1)

    def apply_contrast(self, image: np.ndarray, contrast: float) -> np.ndarray:
        """
        Apply contrast adjustment.

        Args:
            image: Input image (normalized 0-1)
            contrast: Contrast factor (0.1 to 3.0, 1.0 = no change)

        Returns:
            Adjusted image
        """
        if contrast == 1.0:
            return image

        # Adjust around the midpoint (0.5)
        return np.clip((image - 0.5) * contrast + 0.5, 0, 1)

    def apply_gamma(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """
        Apply gamma correction.

        Args:
            image: Input image (normalized 0-1)
            gamma: Gamma value (0.1 to 3.0, 1.0 = no change)

        Returns:
            Adjusted image
        """
        if gamma == 1.0:
            return image

        # Gamma correction: output = input ^ (1/gamma)
        return np.power(np.clip(image, 0, 1), 1.0 / gamma)

    def apply_sharpness(self, image: np.ndarray, sharpness: float) -> np.ndarray:
        """
        Apply sharpness enhancement using unsharp masking.

        Args:
            image: Input image (normalized 0-1)
            sharpness: Sharpness amount (0 to 100)

        Returns:
            Sharpened image
        """
        if sharpness == 0:
            return image

        # Amount factor (0-100 mapped to 0-2)
        amount = sharpness / 50.0

        # Create blurred version
        blurred = gaussian_filter(image, sigma=1.0)

        # Unsharp mask: result = original + amount * (original - blurred)
        sharpened = image + amount * (image - blurred)

        return np.clip(sharpened, 0, 1)

    def apply_invert(self, image: np.ndarray, invert: bool) -> np.ndarray:
        """
        Invert image intensity.

        Args:
            image: Input image (normalized 0-1)
            invert: Whether to invert

        Returns:
            Inverted or original image
        """
        if not invert:
            return image
        return 1.0 - image

    def apply_adjustments(self, volume: Optional[np.ndarray] = None,
                          settings: Optional[AdjustmentSettings] = None) -> np.ndarray:
        """
        Apply all adjustments to the volume.

        Args:
            volume: Volume to adjust (uses stored original if None)
            settings: Settings to apply (uses stored settings if None)

        Returns:
            Adjusted volume
        """
        if volume is None:
            if self._original_volume is None:
                raise ValueError("No volume provided and no original volume stored")
            volume = self._original_volume

        if settings is None:
            settings = self.settings

        # Quick return if no adjustments needed
        if settings.is_default():
            return volume.copy()

        # Normalize to 0-1 range
        v_min = self._original_min if self._original_min is not None else float(volume.min())
        v_max = self._original_max if self._original_max is not None else float(volume.max())

        if v_max == v_min:
            normalized = np.zeros_like(volume, dtype=np.float32)
        else:
            normalized = (volume.astype(np.float32) - v_min) / (v_max - v_min)

        # Apply adjustments in order
        result = normalized
        result = self.apply_brightness(result, settings.brightness)
        result = self.apply_contrast(result, settings.contrast)
        result = self.apply_gamma(result, settings.gamma)
        result = self.apply_sharpness(result, settings.sharpness)
        result = self.apply_invert(result, settings.invert)

        # Convert back to original range and dtype
        result = result * (v_max - v_min) + v_min

        # Clip to valid range for dtype
        if self._original_dtype is not None:
            if np.issubdtype(self._original_dtype, np.integer):
                info = np.iinfo(self._original_dtype)
                result = np.clip(result, info.min, info.max)
            result = result.astype(self._original_dtype)

        return result

    def apply_to_slice(self, slice_2d: np.ndarray,
                       settings: Optional[AdjustmentSettings] = None) -> np.ndarray:
        """
        Apply adjustments to a single 2D slice (for real-time preview).

        Args:
            slice_2d: 2D slice to adjust
            settings: Settings to apply (uses stored settings if None)

        Returns:
            Adjusted 2D slice
        """
        if settings is None:
            settings = self.settings

        # Quick return if no adjustments needed
        if settings.is_default():
            return slice_2d.copy()

        # Normalize using original volume range if available
        if self._original_min is not None and self._original_max is not None:
            v_min, v_max = self._original_min, self._original_max
        else:
            v_min, v_max = float(slice_2d.min()), float(slice_2d.max())

        if v_max == v_min:
            normalized = np.zeros_like(slice_2d, dtype=np.float32)
        else:
            normalized = (slice_2d.astype(np.float32) - v_min) / (v_max - v_min)

        # Apply adjustments
        result = normalized
        result = self.apply_brightness(result, settings.brightness)
        result = self.apply_contrast(result, settings.contrast)
        result = self.apply_gamma(result, settings.gamma)
        result = self.apply_sharpness(result, settings.sharpness)
        result = self.apply_invert(result, settings.invert)

        # Convert back to original range
        result = result * (v_max - v_min) + v_min

        return result


def export_adjustment_settings(settings: AdjustmentSettings,
                               filepath: str,
                               volume_info: Optional[dict] = None) -> bool:
    """
    Export adjustment settings to a text file.

    Args:
        settings: AdjustmentSettings to export
        filepath: Path to save the settings file
        volume_info: Optional dictionary with volume metadata

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("VMM-FRC Image Adjustment Settings\n")
            f.write("=" * 60 + "\n\n")

            # Timestamp
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Volume info if provided
            if volume_info:
                f.write("-" * 40 + "\n")
                f.write("Volume Information\n")
                f.write("-" * 40 + "\n")
                for key, value in volume_info.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")

            # Adjustment settings
            f.write("-" * 40 + "\n")
            f.write("Adjustment Parameters\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Brightness:  {settings.brightness:+.1f}\n")
            f.write(f"  Contrast:    {settings.contrast:.2f}\n")
            f.write(f"  Gamma:       {settings.gamma:.2f}\n")
            f.write(f"  Sharpness:   {settings.sharpness:.1f}\n")
            f.write(f"  Invert:      {'Yes' if settings.invert else 'No'}\n")
            f.write("\n")

            # Description
            f.write("-" * 40 + "\n")
            f.write("Parameter Descriptions\n")
            f.write("-" * 40 + "\n")
            f.write("  Brightness:  Shifts all pixel values (-100 to +100)\n")
            f.write("  Contrast:    Multiplier around midpoint (0.1 to 3.0, 1.0 = no change)\n")
            f.write("  Gamma:       Gamma correction (0.1 to 3.0, 1.0 = no change)\n")
            f.write("               Lower values brighten, higher values darken\n")
            f.write("  Sharpness:   Unsharp mask amount (0 to 100)\n")
            f.write("  Invert:      Inverts all pixel intensities\n")

            f.write("\n" + "=" * 60 + "\n")

        return True
    except Exception as e:
        print(f"Error exporting adjustment settings: {e}")
        return False


def load_adjustment_settings(filepath: str) -> Optional[AdjustmentSettings]:
    """
    Load adjustment settings from a text file.

    Args:
        filepath: Path to the settings file

    Returns:
        AdjustmentSettings if successful, None otherwise
    """
    try:
        settings = AdjustmentSettings()

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('Brightness:'):
                    settings.brightness = float(line.split(':')[1].strip())
                elif line.startswith('Contrast:'):
                    settings.contrast = float(line.split(':')[1].strip())
                elif line.startswith('Gamma:'):
                    settings.gamma = float(line.split(':')[1].strip())
                elif line.startswith('Sharpness:'):
                    settings.sharpness = float(line.split(':')[1].strip())
                elif line.startswith('Invert:'):
                    value = line.split(':')[1].strip().lower()
                    settings.invert = value in ('yes', 'true', '1')

        return settings
    except Exception as e:
        print(f"Error loading adjustment settings: {e}")
        return None
