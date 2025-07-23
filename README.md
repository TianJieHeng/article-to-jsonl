# Article‑to‑JSONL – Personal Journal & Fine‑Tuning Data Collector

A lightweight desktop app (Tkinter + OpenAI) that lets you:

1. Paste any article URL  
2. **Fetch & Summarize** – the app downloads the page, cleans out clutter, and asks GPT for a one‑paragraph summary  
3. Write your own opinion  
4. Slide a –5 … +5 rating for how strongly you agree/disagree  
5. **Save Entry** – each record is appended to `data/journal.jsonl`, ready for fine‑tuning or preference‑model training.

---

## Features

| Module | Highlights |
|--------|------------|
| **UI (`Tkinter`)** | Responsive threading; rating slider; simple, single‑window workflow |
| **Fetcher** | `newspaper3k` + an HTML‑tag fallback to guarantee text extraction |
| **Summarizer** | OpenAI Python ≥ 1.0 client; easily swappable for local models |
| **Storage** | JSONL lines with `date`, `url`, `summary`, `opinion_text`, `rating` |
| **Packaging** | PyInstaller instructions for a one‑file `journal_tool.exe` |

## Prerequisites

* **Windows 10/11 x64**  
* **Python 3.11.x** (64‑bit) – <https://python.org/downloads>  
  *Check with `python --version` in a fresh Command Prompt.*

---

## Setup (Windows PowerShell)

```powershell
# 1  Create & activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 2  Install dependencies
pip install -r requirements.txt

# 3  Create your .env from the template
copy .env.example .env
notepad .env        # paste your real OpenAI key

# 4  Launch the GUI
python -m src.app
If you prefer Command Prompt, replace the activation line with
.\.venv\Scripts\activate.bat.

JSONL Output Schema

{
  "date": "2025‑07‑23T15:42:17Z",
  "url": "https://example.com/article",
  "summary": "One‑paragraph Ryoko‑style recap…",
  "opinion_text": "Your reaction here…",
  "rating": 3           // -5 … +5 integer
}

Perfect for supervised or preference‑based fine‑tuning.

Building a Stand‑Alone EXE
powershell
Copy
Edit
pip install pyinstaller
pyinstaller ^
  --onefile ^
  --noconsole ^
  --name journal_tool ^
  --paths src ^
  --add-data "data;data" ^
  src/app.py
The binary appears in dist/journal_tool.exe.



License
MIT © 2025 Tiān Jié Héng
Feel free to fork, and fuck off! :)
