import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")

def synthesize_to_file(text: str, language: str, output_path: str):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )

    # Dynamic voice selection
    if language == "hi":
        speech_config.speech_synthesis_voice_name = "hi-IN-SwaraNeural"
    else:
        speech_config.speech_synthesis_voice_name = "en-IN-NeerjaNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    synthesizer.speak_text_async(text).get()
