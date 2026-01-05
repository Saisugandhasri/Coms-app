# app/services/coqui_tts_service.py

from TTS.api import TTS
import uuid
import os

AUDIO_DIR = "audio_outputs"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Multi-accent model
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False)


def text_to_speech(text: str, accent: str = "clear") -> str:
    """
    Simple TTS with accent choice.

    accent options: "clear", "us", "uk", "indian", "australian"
    """
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)

    # Simple accent mapping
    speakers = {
        "clear": "p270",  # Neutral and clear
        "us": "p225",  # American
        "uk": "p260",  # British
        "indian": "p330",  # Indian
        "australian": "p360"  # Australian
    }

    speaker = speakers.get(accent, "p330")

    tts.tts_to_file(
        text=text,
        file_path=filepath,
        speaker=speaker
    )

    return filepath




