from faster_whisper import WhisperModel
import os

# Load Whisper model ONCE
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def speech_to_text(audio_path: str) -> str:
    """
    Convert speech audio file to text using Whisper
    Expects FILE PATH (string)
    """

    try:
        segments, info = model.transcribe(audio_path)

        transcription = " ".join(segment.text for segment in segments)

        return transcription.strip()

    except Exception as e:
        raise RuntimeError(f"Whisper transcription failed: {e}")
