# app/services/tts_service.py

from TTS.api import TTS
import uuid
import os

# Directory for generated audio
AUDIO_DIR = "audio_outputs"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Load TTS model once (for performance)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def text_to_speech(text: str) -> str:
    """
    Converts text to a WAV file and returns the file path.
    """
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)

    # Generate speech audio file
    tts.tts_to_file(text=text, file_path=filepath)

    return filepath




