"""Simple image comparison utilities for visual regression testing."""

from pathlib import Path

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None  # type: ignore[assignment]


def compare_images(
    baseline: Path,
    actual: Path,
    threshold: float = 0.2,
) -> tuple[bool, float]:
    """Compare two images and return whether they match within threshold.

    Args:
        baseline: Path to reference screenshot.
        actual: Path to current screenshot.
        threshold: Maximum allowed ratio of differing pixels (0-1).

    Returns:
        Tuple of (is_match, diff_ratio).

    Raises:
        RuntimeError: If Pillow is not installed.
    """
    if PILImage is None:
        raise RuntimeError(
            "Pillow is required for visual regression. "
            "Install with: uv pip install Pillow"
        )

    with PILImage.open(baseline) as im1, PILImage.open(actual) as im2:
        # Normalize sizes to the smaller dimensions
        w = min(im1.width, im2.width)
        h = min(im1.height, im2.height)
        resized1 = im1.convert("RGB").resize((w, h))
        resized2 = im2.convert("RGB").resize((w, h))

        diff_pixels = 0
        total_pixels = w * h
        for y in range(h):
            for x in range(w):
                p1 = resized1.getpixel((x, y))
                p2 = resized2.getpixel((x, y))
                if not isinstance(p1, tuple) or not isinstance(p2, tuple):
                    raise RuntimeError("Unexpected pixel format from Pillow")
                # Simple Euclidean distance in RGB space
                dist = sum(
                    (a - b) ** 2
                    for a, b in zip(p1[:3], p2[:3], strict=False)
                ) ** 0.5
                if dist > 30:
                    diff_pixels += 1

        diff_ratio = diff_pixels / total_pixels if total_pixels else 0.0
        return diff_ratio < threshold, diff_ratio
