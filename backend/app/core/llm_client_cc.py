from dotenv import load_dotenv
from groq import Groq
import os

# ---------------------------
# LOAD API KEY FROM .env
# ---------------------------

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
env_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment")

# Model can be llama3.3:70b or any Grok-supported model
MODEL_NAME = "llama-3.3-70b-versatile"

def call_groq_api(prompt: str, model: str = MODEL_NAME, temperature: float = 0.7):
    """
    Calls Groq SDK chat completions and returns the text output.
    """
    client = Groq(api_key=GROQ_API_KEY)
    messages = [{"role": "user", "content": prompt}]

    resp = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=500
    )

    return resp.choices[0].message.content.strip()