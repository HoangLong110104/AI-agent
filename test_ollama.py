import os
from dotenv import load_dotenv

load_dotenv()
from ollama import Client
api_key = os.getenv("ollama_api_key")

if not api_key:
    raise RuntimeError("Missing ollama_api_key in .env")

client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {api_key}"}
)

messages = [
    {
        'role': 'user',
        'content': 'World Cup 2026',
    },
]

try:
    for part in client.chat('gpt-oss:120b-cloud', messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)
except Exception as exc:
    print(f"Ollama request failed: {exc}")