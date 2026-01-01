import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = "../uploads"
AUDIO_DIR = "../uploads/audio"
IMAGE_DIR = "../uploads/images"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llava:7b"
