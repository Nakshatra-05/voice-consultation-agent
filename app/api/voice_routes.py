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

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}


@router.post("/process")
async def process_voice(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Upload wav, mp3, or m4a."
        )

    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, "response.wav")

    try:
        logger.info(f"Received file: {file.filename}")

        # 1️⃣ Save uploaded audio
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # 2️⃣ Speech-to-Text + language detection
        stt_result = transcribe_audio(input_path)
        user_text = stt_result["text"]
        language = stt_result["language"]

        logger.info(f"Detected language: {language}")
        logger.info(f"User text: {user_text}")

        # 3️⃣ Agent response (language-aware)
        agent_reply = generate_response(user_text, language)
        logger.info(f"Agent reply: {agent_reply}")

        # 4️⃣ Text-to-Speech (dynamic voice)
        synthesize_to_file(agent_reply, language, output_path)
        logger.info("TTS audio generated successfully")

        # 5️⃣ Return audio response
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="response.wav"
        )

    except Exception as e:
        logger.error(f"Voice processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Voice processing failed"
        )

    finally:
        # 6️⃣ Cleanup input audio
        if os.path.exists(input_path):
            os.remove(input_path)
            logger.info("Temporary input file removed")
