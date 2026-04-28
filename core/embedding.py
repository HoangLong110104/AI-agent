import requests
from chromadb.api.types import EmbeddingFunction
from config import EMBEDDING_API_URL, EMBEDDING_API_KEY, EMBEDDING_MODEL

class APIEmbedding(EmbeddingFunction):
    def __init__(self, retries=3, timeout=30):
        self.retries = retries
        self.timeout = timeout

    def embed(self, texts):
        if not EMBEDDING_API_URL or not EMBEDDING_API_KEY or not EMBEDDING_MODEL:
            raise RuntimeError("Missing EMBEDDING_API_URL, EMBEDDING_API_KEY, or EMBEDDING_MODEL in .env")

        headers = {
            "Authorization": f"Bearer {EMBEDDING_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"model": EMBEDDING_MODEL, "input": texts}

        last = None
        for _ in range(self.retries):
            try:
                r = requests.post(
                    EMBEDDING_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )

                if not r.ok:
                    details = r.text[:500]
                    try:
                        err = r.json()
                        details = (err.get("error") or {}).get("message") or details
                    except ValueError:
                        pass
                    raise RuntimeError(f"Embedding API error {r.status_code}: {details}")

                try:
                    data = r.json()
                except ValueError:
                    raise RuntimeError(
                        f"Embedding API returned non-JSON response (status {r.status_code}): {r.text[:500]}"
                    )

                if "data" not in data or not isinstance(data["data"], list):
                    raise RuntimeError(f"Unexpected embedding response format: {str(data)[:500]}")

                return [x["embedding"] for x in data["data"]]
            except Exception as e:
                last = e
        raise RuntimeError(f"Embedding failed: {last}")