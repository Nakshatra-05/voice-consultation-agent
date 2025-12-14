import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

def text_to_speech(text: str):
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")

    if not key or not region:
        print("Azure key/region missing. Check your .env file.")
        return

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    # Indian English female voice, you can change later if you want
    speech_config.speech_synthesis_voice_name = "en-IN-NeerjaNeural"

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ Speech synthesized successfully.")
    else:
        print("❌ TTS failed:", result.reason)

if __name__ == "__main__":
    text_to_speech("Hello, this is a test for the iTechSeed Voice Consultation Agent.")
