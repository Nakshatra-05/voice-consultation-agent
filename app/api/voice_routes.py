import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.stt_module import transcribe_audio
from app.utils import logger

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}

@router.post("/process")
async def process_voice(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        logger.info(f"Received file: {file.filename}")

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # STT
        transcription = transcribe_audio(file_path)
        logger.info("Transcription successful")

        return {
            "filename": file.filename,
            "transcription": transcription
        }

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process audio"
        )

    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Temporary file removed")
