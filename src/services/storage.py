# -*- coding: utf-8 -*-

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "journal.jsonl"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

def save_entry(summary: str, opinion: str, url: str, rating: int) -> None:
    entry = {
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": url,
        "rating": rating,           # ‑5 .. 5 integer
        "summary": summary,
        "opinion_text": opinion,
    }
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")