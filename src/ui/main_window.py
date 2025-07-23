# -*- coding: utf-8 -*-

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from ..services.fetcher import fetch_article
from ..services.summarizer import OpenAISummarizer
from ..services.storage import save_entry

_SUMMARIZER = OpenAISummarizer()


class JournalApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding="10")
        self.pack(fill="both", expand=True)

        self._work_q: queue.Queue = queue.Queue()

        # ---------------- URL field ----------------
        ttk.Label(self, text="Article URL:").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        ttk.Entry(self, width=80, textvariable=self.url_var).grid(
            row=0, column=1, sticky="ew", padx=4
        )
        ttk.Button(self, text="Fetch & Summarize", command=self._on_fetch).grid(
            row=0, column=2, sticky="e"
        )

        # ---------------- Summary text ----------------
        ttk.Label(self, text="Summary:").grid(row=1, column=0, sticky="nw", pady=(8, 0))
        self.summary_txt = scrolledtext.ScrolledText(
            self, width=100, height=10, wrap="word"
        )
        self.summary_txt.grid(row=1, column=1, columnspan=2, sticky="nsew")

        # ---------------- Opinion text ----------------
        ttk.Label(self, text="Your Thoughts:").grid(
            row=2, column=0, sticky="nw", pady=(8, 0)
        )
        self.opinion_txt = scrolledtext.ScrolledText(
            self, width=100, height=6, wrap="word"
        )
        self.opinion_txt.grid(row=2, column=1, columnspan=2, sticky="nsew")

        # ---------------- Rating slider ----------------
        ttk.Label(
            self,
            text="Your Rating (‑5 = strongly dislike, 5 = strongly like):",
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))
        self.rating_var = tk.IntVar(value=0)
        ttk.Scale(
            self,
            from_=-5,
            to=5,
            orient="horizontal",
            variable=self.rating_var,
            length=300,
        ).grid(row=3, column=1, sticky="w")

        # ---------------- Save button ----------------
        ttk.Button(self, text="Save Entry", command=self._on_save).grid(
            row=4, column=2, sticky="e", pady=(8, 0)
        )

        # Configure grid weights for resizing
        for col in range(3):
            self.columnconfigure(col, weight=1)
        self.rowconfigure(1, weight=3)  # summary box grows most
        self.rowconfigure(2, weight=2)  # opinion box

        # Poll queue for worker results
        self.after(100, self._process_queue)

    # ------------------------------------------------------------------ UI callbacks

    def _on_fetch(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Input Error", "Please enter a URL.")
            return
        threading.Thread(
            target=self._worker_fetch_summarize, args=(url,), daemon=True
        ).start()

    def _on_save(self) -> None:
        summary = self.summary_txt.get("1.0", tk.END).strip()
        opinion = self.opinion_txt.get("1.0", tk.END).strip()
        rating = int(self.rating_var.get())
        url = self.url_var.get().strip()

        if not summary or not opinion:
            messagebox.showerror(
                "Input Error", "Both summary and opinion are required."
            )
            return

        save_entry(summary, opinion, url, rating)
        messagebox.showinfo("Saved", "Journal entry appended to journal.jsonl")

        # Reset opinion field and rating slider
        self.opinion_txt.delete("1.0", tk.END)
        self.rating_var.set(0)

    # ------------------------------------------------------------------ worker thread

    def _worker_fetch_summarize(self, url: str) -> None:
        try:
            article = fetch_article(url)
            summary = _SUMMARIZER.summarize(article["text"])
            self._work_q.put(("summary_done", summary))
        except Exception as exc:  # noqa: BLE001
            self._work_q.put(("error", str(exc)))

    def _process_queue(self) -> None:
        try:
            while True:
                tag, payload = self._work_q.get_nowait()
                if tag == "summary_done":
                    self.summary_txt.delete("1.0", tk.END)
                    self.summary_txt.insert(tk.END, payload)
                elif tag == "error":
                    messagebox.showerror("Error", payload)
        except queue.Empty:
            pass
        finally:
            self.after(100, self._process_queue)