from fastapi import FastAPI, File, UploadFile
from deepface import DeepFace
import shutil
import os

app = FastAPI()

AUTHORIZED_DIR = "faces_db"

@app.get("/")
def home():
    return {"message": "Face Recognition API is running"}

@app.post("/verify")
async def verify_face(file: UploadFile = File(...)):
    test_image = "temp.jpg"
    with open(test_image, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Flat structure only: faces_db/image.jpg
    authorized_images = [
        os.path.join(AUTHORIZED_DIR, f)
        for f in os.listdir(AUTHORIZED_DIR)
        if os.path.isfile(os.path.join(AUTHORIZED_DIR, f))
    ]

    if not authorized_images:
        os.remove(test_image)
        return {"status": "DENY", "reason": "No authorized faces found"}

    for img in authorized_images:
        result = DeepFace.verify(
            img1_path=img,
            img2_path=test_image,
            model_name="ArcFace",
            detector_backend="retinaface",
            enforce_detection=False
        )
        print(f"Comparing with {img} → distance: {result['distance']}")
        if result["verified"]:
            os.remove(test_image)
            print('ACCEPT')
            return {"status": "ACCEPT"}

    os.remove(test_image)
    print('DENY')
    return {"status": "DENY"}