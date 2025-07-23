# -*- coding: utf-8 -*-
"""
Downloads & cleans article text.  Uses newspaper3k first, then a
BeautifulSoup fallback.  Adds a desktop‑browser User‑Agent to avoid 403s.
"""
from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from newspaper import Article
from newspaper.configuration import Configuration

from .logger import get_logger

log = get_logger(__name__)

# A common Windows‑Chrome UA string (update yearly if you like)
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def _fallback_scrape(url: str) -> str:
    resp = requests.get(url, timeout=15, headers={"User-Agent": UA})
    if resp.status_code == 403:
        raise RuntimeError(f"Site blocked the request (HTTP 403) → {url}")
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    # crude readability—keep <p>, drop nav/aside/script/etc.
    for bad in soup(["nav", "aside", "header", "footer", "script", "style"]):
        bad.decompose()
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return "\n\n".join(paragraphs)


def fetch_article(url: str) -> dict[str, str | None]:
    """
    Returns dict with keys: title, text, authors, publish_date, url.
    Raises on network/parse errors.
    """
    # newspaper3k with custom UA
    cfg = Configuration()
    cfg.browser_user_agent = UA
    article = Article(url, language="en", config=cfg)

    try:
        article.download()
        if article.download_state == 2:  # FAILED
            raise RuntimeError("newspaper3k download failed")

        article.parse()
        text = article.text or ""
        if not text:
            raise ValueError("newspaper3k extracted no text")
    except Exception as exc:  # noqa: BLE001
        log.warning("newspaper3k failed: %s – trying fallback", exc)
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
