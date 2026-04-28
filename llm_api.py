import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
API_MODEL = os.getenv("API_MODEL", "GPT-5-mini")

# ============================================
# ✅ TOOL CALL DECIDER (RULE-BASED)
# ============================================

def _determine_tool_call(query: str) -> str | None:
    """
    Trả về TOOL_CALL: fetch_web("<url>")
    """
    q = query.strip().lower()
    if not q:
        return None

    # Nếu user đưa URL → crawl URL đó
    if "http://" in q or "https://" in q or "www." in q:
        url = q if q.startswith("http") else f"https://{q}"
        return f'TOOL_CALL: fetch_web("{url}")'

    # Các câu hỏi kiến thức chung → Wikipedia
    if any(x in q for x in ["what is", "who is", "history", "define", "explain", "info", "information"]):
        wiki_key = q.replace(" ", "_").replace("?", "")
        return f'TOOL_CALL: fetch_web("https://en.wikipedia.org/wiki/{wiki_key}")'

    # Các chủ đề y tế / policy → WHO
    if any(x in q for x in ["law", "policy", "covid", "health", "climate", "regulation", "govern", "legal", "trade", "economy", "security"]):
        search_term = "+".join(q.split())
        return f'TOOL_CALL: fetch_web("https://www.who.int/search?q={search_term}")'

    # fallback Wikipedia search
    search_term = "+".join(q.split())
    return f'TOOL_CALL: fetch_web("https://en.wikipedia.org/w/index.php?search={search_term}")'


# ============================================
# ✅ PARSE TOOL CALL
# ============================================

def _extract_url_from_tool_call(tool_call: str) -> str | None:
    if not tool_call or "fetch_web" not in tool_call:
        return None

    try:
        raw = tool_call.split("fetch_web(", 1)[1].split(")", 1)[0]
        return raw.strip().strip('"').strip("'")
    except Exception:
        return None


# ============================================
# ✅ CALL LLM
# ============================================

def _call_llm(query: str, context: str = "") -> str:
    if not API_URL or not API_KEY:
        return "❌ ERROR: Missing API_URL or API_KEY in .env"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # ✅ PROMPT SỬA LẠI HOÀN CHỈNH
    system_message = f"""
Bạn là AI assistant thông minh.

QUY TẮC:
1) Nếu query yêu cầu kiến thức ngoài context → trả lời bằng TOOL_CALL: fetch_web("<url>").
2) Nếu context có thông tin → dùng context để trả lời.
3) Không được bịa.
4) Nếu cần web nhưng chưa có URL → trả TOOL_CALL để tôi fetch.
"""

    payload = {
        "model": API_MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"}
        ],
        "temperature": 0.4,
        "max_tokens": 500,
    }

    # tuning
    model = API_MODEL.lower()
    if "gpt-5" in model and "mini" in model:
        payload["temperature"] = 1
    if "gpt-5.1" in model:
        payload["reasoning_effort"] = "none"

    # ✅ DEBUG PROMPT (hiện prompt đầy đủ)
    print("\n===== PROMPT SEND TO LLM =====")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("===============================\n")

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # extract content
        text = None
        try:
            text = data["choices"][0]["message"]["content"]
        except:
            pass

        if not text:
            return json.dumps(data, ensure_ascii=False)

        text = text.strip()
        return text

    except Exception as exc:
        return f"❌ LLM request failed: {exc}"


# ============================================
# ✅ FETCH WEB
# ============================================

def fetch_web(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return r.text[:15000]  # trả 15k chars
    except Exception as exc:
        return f"❌ Failed to fetch {url}: {exc}"


# ============================================
# ✅ EMBEDDING (simple version)
# ============================================

class APIEmbedding:
    def __init__(self, dim=128):
        self.dim = dim

    def _text_to_vector(self, text: str):
        """Simple ASCII-based embedding (placeholder)."""
        b = text.encode("utf-8", errors="ignore")
        v = [0.0] * self.dim
        for i, bt in enumerate(b):
            v[i % self.dim] += bt / 255.0

        # normalize
        norm = sum(x*x for x in v) ** 0.5
        if norm > 0:
            v = [x / norm for x in v]
        return v

    def embed(self, texts):
        if not isinstance(texts, list):
            raise ValueError("embed() expects list[str]")
        return [self._text_to_vector(t) for t in texts]


# ============================================
# ✅ MAIN CHAT FUNCTION (FINAL)
# ============================================

def chat_with_ai(query: str, context: str = "") -> str:
    if not query.strip():
        return "❌ Empty query."

    # STEP 1: rule-based tool suggestion
    rule_tool = _determine_tool_call(query)

    if rule_tool:
        url = _extract_url_from_tool_call(rule_tool)
        if url:
            web = fetch_web(url)
            if web.startswith("❌"):
                return web

            # summarize using LLM
            res = _call_llm(query, context=web)

            # tránh vòng lặp tool-call
            if res.upper().startswith("TOOL_CALL:"):
                return f"✅ Fetch result from {url}:\n\n{web[:2000]}"

            return res

    # STEP 2: direct ask LLM
    res = _call_llm(query, context)

    # STEP 3: nếu LLM yêu cầu tool thì thực thi
    if res.upper().startswith("TOOL_CALL:"):
        url = _extract_url_from_tool_call(res)
        if url:
            web = fetch_web(url)
            if web.startswith("❌"):
                return web
            return _call_llm(query, context=web)

    return res