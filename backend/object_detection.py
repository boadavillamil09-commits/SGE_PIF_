from functools import lru_cache

import numpy as np
from ultralytics import YOLO


@lru_cache(maxsize=1)
def load_model(
    model_name: str = "yolo26n.pt",
):

    return YOLO(model_name)


def detect_objects(
    model,
    image_bgr: np.ndarray,
    confidence: float = 0.25,
) -> list:

    results = model.predict(
        source=image_bgr,
        conf=confidence,
        imgsz=640,
        verbose=False,
    )

    result = results[0]

    detections = []

    if result.boxes is None:
        return detections

    for i in range(
        len(result.boxes)
    ):

        class_id = int(
            result.boxes.cls[i].item()
        )

        confidence_value = float(
            result.boxes.conf[i].item()
        )

        coordinates = (
            result.boxes.xyxy[i]
            .cpu()
            .numpy()
            .astype(int)
            .tolist()
        )

        detections.append(
            {
                "object": result.names[
                    class_id
                ],
                "confidence": round(
                    confidence_value * 100,
                    2,
                ),
                "box": coordinates,
            }
        )

    return detections