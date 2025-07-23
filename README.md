## Setup

```PowerShell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env        # paste your OpenAI key
python -m src.app   # run the GUI
