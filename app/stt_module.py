import whisper

# Load model once (expensive), reuse for all calls
model = whisper.load_model("small")

def transcribe_audio(path: str) -> str:
    """
    Transcribes an audio file using Whisper and returns the text.
    """
    result = model.transcribe(path)
    return result["text"]
