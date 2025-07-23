# -*- coding: utf-8 -*-
"""
JSONL persistence for Article-to-JSONL.

* When running from source: writes to <project_root>/data/journal.jsonl
* When running as a PyInstaller EXE: writes to <folder_with_exe>/data/journal.jsonl
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ------------------------------------------------------------
# Resolve a stable directory for saving data
# ------------------------------------------------------------
if getattr(sys, "frozen", False):
    # Running inside a PyInstaller bundle
    BASE_DIR = Path(sys.executable).parent
else:
    # Running from source code
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)  # ensure folder exists

DATA_FILE = DATA_DIR / "journal.jsonl"


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
def save_entry(summary: str, opinion: str, url: str, rating: int) -> None:
    """Append one journal line to data/journal.jsonl."""
    entry = {
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": url,
        "rating": rating,  # -5 … 5
        "summary": summary,
        "opinion_text": opinion,
    }
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
