from fastapi import FastAPI, File, UploadFile
import face_recognition
import shutil
import os
import numpy as np

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

    test_img = face_recognition.load_image_file(test_image)
    test_encodings = face_recognition.face_encodings(test_img)

    if not test_encodings:
        os.remove(test_image)
        return {"status": "DENY", "reason": "No face detected"}

    test_encoding = test_encodings[0]

    authorized_images = [
        os.path.join(AUTHORIZED_DIR, f)
        for f in os.listdir(AUTHORIZED_DIR)
        if os.path.isfile(os.path.join(AUTHORIZED_DIR, f))
    ]

    for img_path in authorized_images:
        known_img = face_recognition.load_image_file(img_path)
        known_encodings = face_recognition.face_encodings(known_img)
        if not known_encodings:
            continue
        results = face_recognition.compare_faces([known_encodings[0]], test_encoding, tolerance=0.5)
        print(f"Comparing with {img_path} → match: {results[0]}")
        if results[0]:
            os.remove(test_image)
            print("✅ ACCEPT")
            return {"status": "ACCEPT"}

    os.remove(test_image)
    print("❌ DENY")
    return {"status": "DENY"}