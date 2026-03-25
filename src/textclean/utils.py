"""Utility functions, regex patterns, stopword list, simple stemmer, and accent removal."""

from __future__ import annotations

import re
import unicodedata

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

PATTERN_HTML_TAGS = re.compile(r"<[^>]+>")
PATTERN_URLS = re.compile(
    r"https?://\S+|www\.\S+", re.IGNORECASE
)
PATTERN_EMAILS = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)
PATTERN_NUMBERS = re.compile(r"\d+")
PATTERN_PUNCTUATION = re.compile(r"[^\w\s]", re.UNICODE)
PATTERN_WHITESPACE = re.compile(r"\s+")

# ---------------------------------------------------------------------------
# English stopword list (common subset)
# ---------------------------------------------------------------------------

STOPWORDS: set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "as", "is", "was", "are", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "shall", "can",
    "not", "no", "nor", "so", "too", "very", "just", "about", "above",
    "after", "again", "all", "also", "am", "any", "because", "before",
    "below", "between", "both", "during", "each", "few", "further",
    "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "into", "it", "its", "itself", "me", "more", "most",
    "my", "myself", "now", "off", "once", "only", "other", "our",
    "ours", "ourselves", "out", "over", "own", "same", "she", "some",
    "such", "than", "that", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through",
    "under", "until", "up", "we", "what", "when", "where", "which",
    "while", "who", "whom", "why", "you", "your", "yours", "yourself",
    "yourselves",
}


# ---------------------------------------------------------------------------
# Simple suffix-stripping stemmer
# ---------------------------------------------------------------------------

_SUFFIX_RULES: list[tuple[str, str]] = [
    ("ational", "ate"),
    ("tional", "tion"),
    ("enci", "ence"),
    ("anci", "ance"),
    ("izer", "ize"),
    ("ising", "ise"),
    ("izing", "ize"),
    ("ating", "ate"),
    ("ation", "ate"),
    ("ness", ""),
    ("ment", ""),
    ("ful", ""),
    ("less", ""),
    ("ously", "ous"),
    ("ively", "ive"),
    ("ling", "l"),
    ("ling", ""),
    ("ally", "al"),
    ("ing", ""),
    ("ies", "y"),
    ("sses", "ss"),
    ("ed", ""),
    ("ly", ""),
    ("er", ""),
    ("es", ""),
    ("s", ""),
]


def simple_stem(word: str) -> str:
    """Apply a basic suffix-stripping stemmer to *word*.

    This is intentionally simplistic and language-agnostic enough for
    demonstration / lightweight use-cases.  For production NLP work,
    consider NLTK or spaCy stemmers.
    """
    if len(word) <= 3:
        return word
    lower = word.lower()
    for suffix, replacement in _SUFFIX_RULES:
        if lower.endswith(suffix):
            stem = lower[: -len(suffix)] + replacement
            if len(stem) >= 2:
                return stem
    return lower


# ---------------------------------------------------------------------------
# Accent / diacritic removal
# ---------------------------------------------------------------------------


def remove_accents(text: str) -> str:
    """Remove diacritical marks (accents) from *text* using Unicode NFD decomposition."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


# ---------------------------------------------------------------------------
# Misc helpers
# ---------------------------------------------------------------------------


def strip_html(text: str) -> str:
    """Remove HTML / XML tags from *text*."""
    return PATTERN_HTML_TAGS.sub("", text)


def remove_urls(text: str) -> str:
    """Remove URLs from *text*."""
    return PATTERN_URLS.sub("", text)


def remove_emails(text: str) -> str:
    """Remove email addresses from *text*."""
    return PATTERN_EMAILS.sub("", text)


def remove_numbers(text: str) -> str:
    """Remove digits from *text*."""
    return PATTERN_NUMBERS.sub("", text)


def remove_punctuation(text: str) -> str:
    """Remove punctuation characters from *text*."""
    return PATTERN_PUNCTUATION.sub("", text)


def normalize_whitespace(text: str) -> str:
    """Collapse consecutive whitespace into a single space and strip edges."""
    return PATTERN_WHITESPACE.sub(" ", text).strip()


def remove_stopwords(text: str, stopwords: set[str] | None = None) -> str:
    """Remove stopwords from *text*.

    Uses the built-in ``STOPWORDS`` set unless *stopwords* is provided.
    """
    words = text.split()
    stop = stopwords if stopwords is not None else STOPWORDS
    return " ".join(w for w in words if w.lower() not in stop)


def stem_text(text: str) -> str:
    """Apply :func:`simple_stem` to every token in *text*."""
    return " ".join(simple_stem(w) for w in text.split())
