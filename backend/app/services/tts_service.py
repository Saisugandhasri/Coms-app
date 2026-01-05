import uuid
from pathlib import Path
from gtts import gTTS

AUDIO_DIR = Path("generated_audio")
AUDIO_DIR.mkdir(exist_ok=True)

def generate_audio(text: str) -> str:
    audio_id = f"{uuid.uuid4()}.mp3"
    audio_path = AUDIO_DIR / audio_id

    tts = gTTS(text=text, lang="en",tld="co.in")
    tts.save(audio_path)

    return audio_id
