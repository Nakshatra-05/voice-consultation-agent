import whisper

def transcribe(path: str):
    print(f"\n--- Transcribing: {path} ---")
    # Load a small model (CPU friendly, decent accuracy)
    model = whisper.load_model("small")
    result = model.transcribe(path)
    print("Text:", result["text"])

if __name__ == "__main__":
    transcribe("sample_en.m4a")  # your English file
    transcribe("sample_hi.m4a")  # your Hindi file
