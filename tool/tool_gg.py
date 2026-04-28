
import os
from pathlib import Path
try:
    from serpapi import GoogleSearch
except ImportError:
    from serpapi.google_search import GoogleSearch
import trafilatura
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


# =========================
# CONFIG
# =========================

SERP_API_KEY = os.getenv("SERP_API_KEY")  # export SERP_API_KEY=xxx


# =========================
# GOOGLE SEARCH
# =========================

def search_google(query: str, num_results: int = 5):
    """
    Tìm Google bằng SerpAPI
    Trả về list URL (organic results)
    """
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": num_results,
        "hl": "vi",
    }

    if not SERP_API_KEY:
        return []

    search = GoogleSearch(params)
    results = search.get_dict()

    error_message = results.get("error")
    if error_message:
        print(f"SerpAPI error: {error_message}")
        return []

    links = []
    for r in results.get("organic_results", []):
        link = r.get("link")
        if link:
            links.append(link)

    return links


# =========================
# CRAWL + EXTRACT MAIN CONTENT
# =========================

def crawl_url(url: str, max_len: int = 2500) -> str:
    """
    Crawl 1 URL và trích nội dung chính
    Đã loại menu / footer / quảng cáo
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return ""

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            favor_recall=True,
        )

        if not text:
            return ""

        return text.strip()[:max_len]

    except Exception:
        return ""


# =========================
# DEDUPLICATE
# =========================

def deduplicate_texts(texts):
    """
    Loại nội dung trùng nhau (fingerprint ngắn)
    """
    seen = set()
    unique = []

    for t in texts:
        key = t[:200]
        if key not in seen:
            unique.append(t)
            seen.add(key)

    return unique


# =========================
# MAIN PIPELINE
# =========================

def get_web_data(query: str, max_total_length: int = 6000) -> str:
    """
    Pipeline hoàn chỉnh:
    query -> google -> crawl -> clean -> gộp context
    """
    links = search_google(query)

    texts = []
    total_len = 0

    for link in links:
        content = crawl_url(link)
        if content:
            texts.append(
                f"[SOURCE] {link}\n{content}"
            )

    texts = deduplicate_texts(texts)

    final_text = ""
    for t in texts:
        if total_len + len(t) > max_total_length:
            break
        final_text += t + "\n\n"
        total_len += len(t)

    return final_text.strip()


# =========================
# TEST MANUAL
# =========================

if __name__ == "__main__":
    q = "Thời tiết Hà Nội hôm nay như nào"

    if not SERP_API_KEY:
        print("Khong tim thay SERP_API_KEY. Hay tao file .env voi dong: SERP_API_KEY=your_key")
        raise SystemExit(1)

    data = get_web_data(q)
    if not data:
        print("Khong lay duoc du lieu web. Kiem tra API key, quota SerpAPI, hoac doi truy van khac.")
    else:
        print(data)