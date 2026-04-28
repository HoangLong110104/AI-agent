import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "./chroma_db"
EMBED_BATCH = 64

def _as_bool(name: str, default: bool = False) -> bool:
	value = os.getenv(name)
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")
EMBEDDING_ENABLED = _as_bool("EMBEDDING_ENABLED", False)

CHAT_API_URL = os.getenv("API_URL")
CHAT_API_KEY = os.getenv("API_KEY")
CHAT_MODEL = os.getenv("API_MODEL", "GPT-5-mini")

OLLAMA_API_KEY = os.getenv("OLLAMA_KEY")
OLLAMA_API_URL = os.getenv("OLLAMA_URL")
OLLAMA_API_MODEL = os.getenv("OLLAMA_MODEL")