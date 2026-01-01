import uuid
import tempfile
import whisper

model = whisper.load_model("base")


def transcribe_audio_from_bytes(audio_bytes: bytes):
    audio_id = str(uuid.uuid4())

    # Save to temp file (auto-deleted)
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        temp_path = tmp.name

    # Whisper will internally call ffmpeg properly
    result = model.transcribe(temp_path)

    return result["text"], audio_id
