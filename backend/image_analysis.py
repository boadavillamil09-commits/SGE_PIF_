import cv2
import numpy as np


def _brightness_label(value: float) -> str:

    if value < 85:
        return "Oscura"

    if value < 170:
        return "Media"

    return "Clara"


def _contrast_label(value: float) -> str:

    if value < 40:
        return "Bajo"

    if value < 80:
        return "Medio"

    return "Alto"


def _sharpness_label(value: float) -> str:

    if value < 100:
        return "Baja"

    if value < 500:
        return "Media"

    return "Alta"


def analyze_image(
    image_bgr: np.ndarray,
) -> dict:

    if image_bgr is None:
        raise ValueError(
            "La imagen no puede ser None."
        )

    height, width = image_bgr.shape[:2]

    gray = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2GRAY,
    )

    hsv = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2HSV,
    )

    brightness = float(
        np.mean(gray)
    )

    contrast = float(
        np.std(gray)
    )

    sharpness = float(
        cv2.Laplacian(
            gray,
            cv2.CV_64F,
        ).var()
    )

    saturation = float(
        np.mean(hsv[:, :, 1])
    )

    aspect_ratio = width / height

    if aspect_ratio > 1.05:
        orientation = "Horizontal"

    elif aspect_ratio < 0.95:
        orientation = "Vertical"

    else:
        orientation = "Cuadrada"

    return {
        "width": width,
        "height": height,
        "megapixels": round(
            width * height / 1_000_000,
            2,
        ),
        "aspect_ratio": round(
            aspect_ratio,
            2,
        ),
        "orientation": orientation,
        "brightness": round(
            brightness,
            2,
        ),
        "brightness_label": _brightness_label(
            brightness
        ),
        "contrast": round(
            contrast,
            2,
        ),
        "contrast_label": _contrast_label(
            contrast
        ),
        "sharpness": round(
            sharpness,
            2,
        ),
        "sharpness_label": _sharpness_label(
            sharpness
        ),
        "saturation": round(
            saturation,
            2,
        ),
    }