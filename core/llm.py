import requests
from config import OLLAMA_API_KEY, OLLAMA_API_MODEL, OLLAMA_API_URL

def chat_with_ai(question, context=""):
    if not OLLAMA_API_URL or not OLLAMA_API_KEY or not OLLAMA_API_MODEL:
        raise RuntimeError("Missing OLLAMA_URL, OLLAMA_KEY, or OLLAMA_MODEL in .env")

    payload = {
        "model": OLLAMA_API_MODEL,
        "messages": [
            {"role": "system", "content": "Trả lời dựa trên context nếu có."},
            {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"}
        ]
    }
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    r = requests.post(OLLAMA_API_URL, headers=headers, json=payload, timeout=60)

    if not r.ok:
        details = r.text[:500]
        try:
            err = r.json()
            details = (err.get("error") or {}).get("message") or details
        except ValueError:
            pass
        raise RuntimeError(f"LLM API error {r.status_code}: {details}")

    try:
        data = r.json()
    except ValueError:
        raise RuntimeError(
            f"LLM API returned non-JSON response (status {r.status_code}): {r.text[:500]}"
        )

    # OpenAI-compatible shape
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        pass

    # Some providers return {"message": {"content": ...}}
    try:
        return data["message"]["content"]
    except Exception:
        pass

    raise RuntimeError(f"Unexpected LLM response format: {str(data)[:500]}")