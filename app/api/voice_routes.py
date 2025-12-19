import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from app.stt_module import transcribe_audio
from app.llm_module import generate_response
from app.tts_module import synthesize_to_file
from app.session_manager import create_session, add_message
from app.utils import logger

router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}


def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


@router.post("/process")
async def process_voice(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session_id: str | None = Form(None),
    preferred_language: str | None = Form(None)
):
    # ---------- Validation ----------
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Use wav, mp3, or m4a."
        )

    # ---------- Session handling ----------
    if not session_id or not session_id.strip():
        session_id = create_session()
        logger.info(f"New session created: {session_id}")
    else:
        logger.info(f"Using existing session: {session_id}")

    # ---------- Unique files (Windows-safe) ----------
    input_filename = f"input_{uuid.uuid4().hex}{ext}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    output_filename = f"response_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        logger.info("Received audio upload")

        # ---------- Save input audio ----------
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # ---------- Speech-to-Text ----------
        stt_result = transcribe_audio(input_path)
        user_text = stt_result.get("text", "")
        detected_language = stt_result.get("language", "en")

        language = preferred_language or detected_language

        logger.info(f"STT text: '{user_text}'")
        logger.info(f"Detected language: {language}")

        # ---------- STT Fallback (CRITICAL FIX) ----------
        if not user_text or not user_text.strip():
            logger.warning("STT returned empty text. Sending fallback response.")

            fallback_text = (
                "Sorry, I could not hear that clearly. Could you please repeat?"
                if language != "hi"
                else "माफ़ कीजिए, मैं स्पष्ट रूप से सुन नहीं पाया। कृपया दोबारा बोलें।"
            )

            add_message(session_id, "agent", fallback_text)

            synthesize_to_file(fallback_text, language, output_path)
            background_tasks.add_task(cleanup_file, output_path)

            return FileResponse(
                output_path,
                media_type="audio/wav",
                filename="response.wav",
                headers={
                    "X-Session-Id": session_id,
                    "X-Detected-Language": language
                }
            )

        # ---------- Store user message ----------
        add_message(session_id, "user", user_text)

        # ---------- Agent logic ----------
        agent_reply = generate_response(user_text, language)
        add_message(session_id, "agent", agent_reply)

        # ---------- Text-to-Speech ----------
        synthesize_to_file(agent_reply, language, output_path)

        # ---------- Cleanup output AFTER response ----------
        background_tasks.add_task(cleanup_file, output_path)

        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="response.wav",
            headers={
                "X-Session-Id": session_id,
                "X-Detected-Language": language
            }
        )

    except Exception as e:
        logger.error(f"Voice pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Voice processing failed")

    finally:
        # ---------- Cleanup input immediately ----------
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except Exception:
                pass
