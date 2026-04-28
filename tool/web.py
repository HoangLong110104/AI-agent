import requests
from bs4 import BeautifulSoup
import urllib.parse


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# --------------------------------------------------
# Wikipedia
# --------------------------------------------------
def fetch_wikipedia(query: str, lang: str = "vi") -> str:
    """
    Fetch summary text from Wikipedia.
    """
    q = urllib.parse.quote(query.replace(" ", "_"))
    url = f"https://{lang}.wikipedia.org/wiki/{q}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return ""

        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = soup.select("p")

        texts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        return "\n".join(texts[:10])

    except Exception as e:
        print("Wikipedia fetch error:", e)
        return ""


# --------------------------------------------------
# Vietnamnet (báo Việt)
# --------------------------------------------------
def fetch_vietnamnet(query: str) -> str:
    """
    Search & fetch content from Vietnamnet.
    """
    q = urllib.parse.quote(query)
    search_url = f"https://vietnamnet.vn/tim-kiem?q={q}"

    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        link = soup.select_one("a[href*='/']")

        if not link:
            return ""

        article_url = link["href"]
        if not article_url.startswith("http"):
            article_url = "https://vietnamnet.vn" + article_url

        article_page = requests.get(article_url, headers=HEADERS, timeout=10)
        article_soup = BeautifulSoup(article_page.text, "html.parser")

        paragraphs = article_soup.select("p")
        texts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

        return "\n".join(texts[:15])

    except Exception as e:
        print("Vietnamnet fetch error:", e)
        return ""


# --------------------------------------------------
# General Web (DuckDuckGo lite)
# --------------------------------------------------
def fetch_general_web(query: str) -> str:
    """
    Lightweight general web search (DuckDuckGo HTML).
    """
    q = urllib.parse.quote(query)
    url = f"https://duckduckgo.com/html/?q={q}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        snippets = soup.select(".result__snippet")
        texts = [s.get_text().strip() for s in snippets if s.get_text().strip()]

        return "\n".join(texts[:10])

    except Exception as e:
        print("General web fetch error:", e)
        return ""
