# Initial offline end-to-end voice pipeline test

from app.stt_module import transcribe_audio
from app.tts_module import speak_text
from app.llm_module import generate_response

def run_voice_pipeline(audio_path: str):
    print("\n--- Voice Consultation Agent Test ---")
    print(f"Input audio file: {audio_path}")

    # 1) Speech-to-Text
    user_text = transcribe_audio(audio_path)
    print("User (transcribed):", user_text)

    # 2) AI Response (placeholder)
    agent_reply = generate_response(user_text)
    print("Agent (text):", agent_reply)

    # 3) Text-to-Speech
    print("Speaking response...")
    speak_text(agent_reply)
    print("✅ Done.")

if __name__ == "__main__":
    # Start with your English/Hindi test file
    run_voice_pipeline("sample_en.m4a")
    # You can also try Hindi:
    # run_voice_pipeline("sample_hi.m4a")