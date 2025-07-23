from __future__ import annotations
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from .logger import get_logger

log = get_logger(__name__)

def _fallback_scrape(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # crude readability—keep <p>, drop nav/aside/script.
    for bad in soup(["nav", "aside", "header", "footer", "script", "style"]):
        bad.decompose()
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return "\n\n".join(paragraphs)

def fetch_article(url: str) -> dict[str, str | None]:
    """
    Returns dict with keys: title, text, authors, publish_date.
    Raises on hard network errors; returns empty text on failure.
    """
    article = Article(url, language="en")
    try:
        article.download()
        article.parse()
        text = article.text or ""
        if not text:
            raise ValueError("newspaper3k extraction empty")
    except Exception as exc:           # noqa: BLE001
        log.warning("newspaper3k failed: %s - trying fallback", exc)
        text = _fallback_scrape(url)

    return {
        "title": article.title or "",
        "text": text,
        "authors": article.authors or [],
        "publish_date": (
            article.publish_date.isoformat() if article.publish_date else None
        ),
        "url": url,
    }