from groq import Groq
import os
from dotenv import load_dotenv

# Load .env from project root (3 levels up from app/core)
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_path, "..", ".env")
load_dotenv(env_path)

client = Groq()

def call_llm(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
        )
        return completion.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"LLM service unavailable: {str(e)}")
