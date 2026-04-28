import requests
from datetime import datetime

def realtime_search(query: str) -> str:
    """
    Simple real-time search via DuckDuckGo HTML (no API key).
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": query}

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    # VERY basic extraction (đủ dùng cho agent)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")

    snippets = soup.select(".result__snippet")
    texts = [s.text.strip() for s in snippets[:5]]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"[LIVE DATA @ {now}]\n" + "\n".join(texts)