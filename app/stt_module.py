import whisper

model = whisper.load_model("small")

def transcribe_audio(path: str):
    result = model.transcribe(path)

    return {
        "text": result["text"],
        "language": result["language"]
    }
