import whisper

# Load once (CPU-friendly)
model = whisper.load_model("small")

def transcribe_audio(path: str) -> dict:
    """
    Returns:
    {
        "text": "...",
        "language": "en" / "hi"
    }
    """
    result = model.transcribe(path)

    return {
        "text": result.get("text", "").strip(),
        "language": result.get("language", "en")
    }
