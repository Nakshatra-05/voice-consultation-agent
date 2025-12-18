import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.stt_module import transcribe_audio
from app.llm_module import generate_response
from app.tts_module import synthesize_to_file
from app.utils import logger

router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# mp4 allowed ONLY for input
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}


@router.post("/process")
async def process_voice(
    file: UploadFile = File(...),
    preferred_language: str | None = None
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, "response.wav")

    try:
        logger.info(f"Received file: {file.filename}")

        # Save input file
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # STT
        stt_result = transcribe_audio(input_path)
        user_text = stt_result["text"]
        detected_language = stt_result["language"]

        language = preferred_language or detected_language

        logger.info(f"STT text: {user_text}")
        logger.info(f"Language: {language}")

        # Agent response
        agent_reply = generate_response(user_text, language)

        # TTS
        synthesize_to_file(agent_reply, language, output_path)

        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="response.wav"
        )

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
