import os
from fastapi import APIRouter, UploadFile, File
from app.stt_module import transcribe_audio

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/process")
async def process_voice(file: UploadFile = File(...)):
    """
    Accepts an audio file, saves it temporarily,
    runs Whisper STT, and returns transcription.
    """

    # 1. Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. Run Speech-to-Text
    transcription = transcribe_audio(file_path)

    # 3. Return response
    return {
        "filename": file.filename,
        "transcription": transcription
    }
