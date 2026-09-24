import cv2
import numpy as np
from sklearn.cluster import KMeans


def rgb_to_hex(
    rgb: tuple[int, int, int],
) -> str:

    r, g, b = rgb

    return f"#{r:02X}{g:02X}{b:02X}"


def name_color(
    r: int,
    g: int,
    b: int,
) -> str:

    rgb = np.uint8(
        [[[r, g, b]]]
    )

    hsv = cv2.cvtColor(
        rgb,
        cv2.COLOR_RGB2HSV,
    )[0, 0]

    h = float(hsv[0]) * 2
    s = float(hsv[1]) / 255
    v = float(hsv[2]) / 255

    if v < 0.15:
        return "Negro"

    if s < 0.12:

        if v > 0.85:
            return "Blanco"

        if v > 0.55:
            return "Gris claro"

        return "Gris oscuro"

    if s < 0.25:

        if v > 0.75:
            return "Beige grisáceo"

        return "Grisáceo"

    if v < 0.35:

        if h < 30 or h >= 330:
            return "Rojo oscuro"

        if h < 90:
            return "Verde oscuro"

        if h < 210:
            return "Azul oscuro"

        if h < 270:
            return "Morado oscuro"

        return "Rojo oscuro"

    if h < 15 or h >= 345:
        return "Rojo"

    if h < 45:
        return "Naranja"

    if h < 70:
        return "Amarillo"

    if h < 160:
        return "Verde"

    if h < 210:
        return "Cian"

    if h < 260:
        return "Azul"

    if h < 290:
        return "Violeta"

    if h < 330:
        return "Magenta"

    return "Rojo"


def analyze_colors(
    image_bgr: np.ndarray,
) -> dict:

    height, width = image_bgr.shape[:2]

    scale = min(
        1.0,
        400 / max(height, width),
    )

    if scale < 1:

        image = cv2.resize(
            image_bgr,
            (
                int(width * scale),
                int(height * scale),
            ),
            interpolation=cv2.INTER_AREA,
        )

    else:

        image = image_bgr

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB,
    )

    pixels = rgb.reshape(
        -1,
        3,
    ).astype(np.float32)

    max_pixels = 15000

    if len(pixels) > max_pixels:

        rng = np.random.default_rng(42)

        indexes = rng.choice(
            len(pixels),
            size=max_pixels,
            replace=False,
        )

        pixels = pixels[indexes]

    # Número inicial de grupos.
    # Posteriormente lo sustituiremos por
    # una selección automática.
    n_colors = min(
        12,
        len(np.unique(
            pixels.astype(np.uint8),
            axis=0,
        )),
    )

    model = KMeans(
        n_clusters=n_colors,
        random_state=42,
        n_init=10,
    )

    labels = model.fit_predict(
        pixels
    )

    centers = np.clip(
        model.cluster_centers_,
        0,
        255,
    ).astype(np.uint8)

    counts = np.bincount(
        labels
    )

    order = np.argsort(
        counts
    )[::-1]

    palette = []

    total = len(labels)

    for index in order:

        r, g, b = map(
            int,
            centers[index],
        )

        percentage = (
            counts[index] / total
        ) * 100

        palette.append(
            {
                "name": name_color(
                    r,
                    g,
                    b,
                ),
                "rgb": [r, g, b],
                "hex": rgb_to_hex(
                    (r, g, b)
                ),
                "percentage": round(
                    percentage,
                    2,
                ),
            }
        )

    average = np.mean(
        pixels,
        axis=0,
    ).astype(int)

    avg_r, avg_g, avg_b = map(
        int,
        average,
    )

    temperature_index = (
        (avg_r - avg_b)
        /
        (avg_r + avg_b + 1)
    )

    if temperature_index > 0.08:
        temperature = "Cálida"

    elif temperature_index < -0.08:
        temperature = "Fría"

    else:
        temperature = "Neutra"

    return {
        "palette": palette,
        "average_rgb": [
            avg_r,
            avg_g,
            avg_b,
        ],
        "average_hex": rgb_to_hex(
            (
                avg_r,
                avg_g,
                avg_b,
            )
        ),
        "temperature": temperature,
    }