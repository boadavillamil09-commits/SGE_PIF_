from pathlib import Path

import cv2
import numpy as np

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from image_analysis import analyze_image
from color_analysis import analyze_colors
from object_detection import detect_objects, load_model


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="Analizador Visual",
    description="Sistema de análisis de imágenes mediante visión artificial.",
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
    }

    if file.content_type not in allowed_types:
        return {
            "error": "Formato de imagen no permitido."
        }

    contents = await file.read()

    image_array = np.frombuffer(
        contents,
        dtype=np.uint8,
    )

    image_bgr = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR,
    )

    if image_bgr is None:
        return {
            "error": "No fue posible procesar la imagen."
        }

    image_info = analyze_image(
        image_bgr
    )

    color_info = analyze_colors(
        image_bgr
    )

    model = load_model()

    detections = detect_objects(
        model,
        image_bgr,
    )

    return {
        "image": image_info,
        "colors": color_info,
        "objects": detections,
    }