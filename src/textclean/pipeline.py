"""Chainable pipeline for text preprocessing.

Lets callers compose cleaning steps declaratively::

    pipe = (
        Pipeline()
        .strip_html()
        .remove_urls()
        .lowercase()
        .remove_stopwords()
        .stem()
    )
    cleaned = pipe.run(raw_text)

Each step is a pure ``str -> str`` function, which keeps ordering
explicit and makes the pipeline trivial to unit-test step-by-step.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable
import html
import re
import unicodedata


Step = Callable[[str], str]


_HTML_TAG_RE = re.compile(r"<[^>]+>")
_URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_WS_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]")
_NUM_RE = re.compile(r"\b\d+\b")


DEFAULT_STOPWORDS = frozenset(
    """a an the and or but if of in on for with to from by at as is are was were be been being
    this that these those i you he she it we they me him her us them my your his its our their""".split()
)


@dataclass
class Pipeline:
    steps: list[Step] = field(default_factory=list)

    def then(self, step: Step) -> "Pipeline":
        self.steps.append(step)
        return self

    def run(self, text: str) -> str:
        for s in self.steps:
            text = s(text)
        return text

    def run_many(self, texts: Iterable[str]) -> list[str]:
        return [self.run(t) for t in texts]

    # Built-in step builders -------------------------------------------------

    def strip_html(self) -> "Pipeline":
        return self.then(lambda t: html.unescape(_HTML_TAG_RE.sub(" ", t)))

    def remove_urls(self) -> "Pipeline":
        return self.then(lambda t: _URL_RE.sub(" ", t))

    def remove_emails(self) -> "Pipeline":
        return self.then(lambda t: _EMAIL_RE.sub(" ", t))

    def lowercase(self) -> "Pipeline":
        return self.then(str.lower)

    def normalize_unicode(self, form: str = "NFKC") -> "Pipeline":
        return self.then(lambda t: unicodedata.normalize(form, t))

    def strip_accents(self) -> "Pipeline":
        def _strip(t: str) -> str:
            n = unicodedata.normalize("NFKD", t)
            return "".join(c for c in n if not unicodedata.combining(c))
        return self.then(_strip)

    def remove_punctuation(self) -> "Pipeline":
        return self.then(lambda t: _PUNCT_RE.sub(" ", t))

    def remove_numbers(self) -> "Pipeline":
        return self.then(lambda t: _NUM_RE.sub(" ", t))

    def collapse_whitespace(self) -> "Pipeline":
        return self.then(lambda t: _WS_RE.sub(" ", t).strip())

    def remove_stopwords(self, words: Iterable[str] = DEFAULT_STOPWORDS) -> "Pipeline":
        stop = frozenset(w.lower() for w in words)
        def _rm(t: str) -> str:
            return " ".join(tok for tok in t.split() if tok.lower() not in stop)
        return self.then(_rm)

    def stem(self) -> "Pipeline":
        """Porter-lite stemmer — strips the common English suffixes."""
        return self.then(_stem_text)

    def min_token_length(self, n: int) -> "Pipeline":
        return self.then(lambda t: " ".join(w for w in t.split() if len(w) >= n))


# --- A deliberately-tiny Porter-style stemmer --------------------------------
_SUFFIXES = (
    "ational", "tional", "ization", "ational", "fulness", "ousness",
    "iveness", "ement", "ation", "ingly", "edly",
    "ness", "ment", "tion", "sion", "ance", "ence", "able", "ible",
    "ing", "ied", "ies", "ly", "ed", "es", "s",
)


def _stem_word(w: str) -> str:
    wl = w.lower()
    for suf in _SUFFIXES:
        if len(wl) > len(suf) + 2 and wl.endswith(suf):
            return wl[: -len(suf)]
    return wl


def _stem_text(t: str) -> str:
    return " ".join(_stem_word(w) for w in t.split())
