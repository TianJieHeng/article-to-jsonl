# -*- coding: utf-8 -*-

from __future__ import annotations
from openai import OpenAI
from ..config import OPENAI_API_KEY, OPENAI_MODEL
from .logger import get_logger

log = get_logger(__name__)


class BaseSummarizer:
    def summarize(self, text: str) -> str:  # noqa: D401
        """Return a concise personality‑flavoured paragraph summary."""


class OpenAISummarizer(BaseSummarizer):
    def __init__(
        self,
        model: str = OPENAI_MODEL,
        api_key: str | None = OPENAI_API_KEY,
    ) -> None:
        # Create a dedicated client.  If api_key is None the env var is used.
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def summarize(self, text: str) -> str:  # noqa: D401
        prompt = (
            "You are JournalSynth, a witty yet insightful assistant. "
            "Write one engaging paragraph (≈120–150 words) that captures the essence "
            "of the article in your own voice:\n\n"
            f"{text}\n\nSummary:"
        )

        log.debug("Requesting OpenAI summary (≈%s tokens)", len(text) // 4)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
        )

        return response.choices[0].message.content.strip()