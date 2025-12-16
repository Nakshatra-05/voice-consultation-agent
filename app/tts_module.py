import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=speech_region
)

# Default voice – we can change later for Hindi, etc.
speech_config.speech_synthesis_voice_name = "en-IN-NeerjaNeural"
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def speak_text(text: str):
    """
    Speaks the given text using Azure TTS.
    """
    result = synthesizer.speak_text_async(text).get()
    return result
