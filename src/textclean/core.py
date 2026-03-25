"""Core TextClean pipeline with a fluent, chainable API."""

from __future__ import annotations

from collections.abc import Callable
from typing import Self

from textclean.config import PipelineConfig
from textclean.utils import (
    STOPWORDS,
    normalize_whitespace as _normalize_whitespace,
    remove_accents as _remove_accents,
    remove_emails as _remove_emails,
    remove_numbers as _remove_numbers,
    remove_punctuation as _remove_punctuation,
    remove_stopwords as _remove_stopwords,
    remove_urls as _remove_urls,
    stem_text as _stem_text,
    strip_html as _strip_html,
)

# Type alias for a single cleaning step
CleanStep = Callable[[str], str]


class TextClean:
    """Composable text-cleaning pipeline with a fluent builder API.

    Build a pipeline by chaining methods, then call :meth:`process` or
    :meth:`clean` to run the pipeline on text.

    Example::

        cleaner = (
            TextClean()
            .lowercase()
            .strip_html()
            .remove_urls()
            .remove_punctuation()
            .normalize_whitespace()
        )
        result = cleaner.process("Hello <b>World</b>!")
    """

    def __init__(self) -> None:
        self._steps: list[tuple[str, CleanStep]] = []

    # ------------------------------------------------------------------
    # Builder / chainable methods
    # ------------------------------------------------------------------

    def lowercase(self) -> Self:
        """Add a step that converts text to lowercase."""
        self._steps.append(("lowercase", str.lower))
        return self

    def strip_html(self) -> Self:
        """Add a step that removes HTML / XML tags."""
        self._steps.append(("strip_html", _strip_html))
        return self

    def remove_urls(self) -> Self:
        """Add a step that removes URLs."""
        self._steps.append(("remove_urls", _remove_urls))
        return self

    def remove_emails(self) -> Self:
        """Add a step that removes email addresses."""
        self._steps.append(("remove_emails", _remove_emails))
        return self

    def remove_numbers(self) -> Self:
        """Add a step that removes digits."""
        self._steps.append(("remove_numbers", _remove_numbers))
        return self

    def remove_punctuation(self) -> Self:
        """Add a step that removes punctuation characters."""
        self._steps.append(("remove_punctuation", _remove_punctuation))
        return self

    def remove_stopwords(self, stopwords: set[str] | None = None) -> Self:
        """Add a step that removes stopwords.

        Parameters
        ----------
        stopwords:
            Optional custom set of stopwords. Falls back to the built-in
            English stopword list when ``None``.
        """
        sw = stopwords if stopwords is not None else STOPWORDS

        def _step(text: str) -> str:
            return _remove_stopwords(text, sw)

        self._steps.append(("remove_stopwords", _step))
        return self

    def normalize_whitespace(self) -> Self:
        """Add a step that collapses whitespace and strips edges."""
        self._steps.append(("normalize_whitespace", _normalize_whitespace))
        return self

    def remove_accents(self) -> Self:
        """Add a step that strips diacritical marks."""
        self._steps.append(("remove_accents", _remove_accents))
        return self

    def stem(self) -> Self:
        """Add a step that applies a simple suffix-stripping stemmer."""
        self._steps.append(("stem", _stem_text))
        return self

    def add_step(self, fn: CleanStep, *, name: str | None = None) -> Self:
        """Register an arbitrary custom cleaning step.

        Parameters
        ----------
        fn:
            A callable that accepts a string and returns a cleaned string.
        name:
            Optional human-readable label for debugging / repr.
        """
        label = name or getattr(fn, "__name__", "custom")
        self._steps.append((label, fn))
        return self

    # ------------------------------------------------------------------
    # Factory from config
    # ------------------------------------------------------------------

    @classmethod
    def from_config(cls, config: PipelineConfig) -> TextClean:
        """Build a pipeline from a :class:`PipelineConfig` instance.

        Steps are added in a sensible default order.
        """
        pipeline = cls()
        if config.strip_html:
            pipeline.strip_html()
        if config.remove_urls:
            pipeline.remove_urls()
        if config.remove_emails:
            pipeline.remove_emails()
        if config.lowercase:
            pipeline.lowercase()
        if config.remove_accents:
            pipeline.remove_accents()
        if config.remove_numbers:
            pipeline.remove_numbers()
        if config.remove_punctuation:
            pipeline.remove_punctuation()
        if config.remove_stopwords:
            pipeline.remove_stopwords(stopwords=config.custom_stopwords)
        if config.stem:
            pipeline.stem()
        if config.normalize_whitespace:
            pipeline.normalize_whitespace()
        return pipeline

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def process(self, text: str) -> str:
        """Run *text* through every registered pipeline step in order."""
        result = text
        for _name, step in self._steps:
            result = step(result)
        return result

    def clean(self, text: str) -> str:
        """Alias for :meth:`process` (convenience name)."""
        return self.process(text)

    def process_batch(self, texts: list[str]) -> list[str]:
        """Run :meth:`process` on each item in *texts* and return results."""
        return [self.process(t) for t in texts]

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    @property
    def steps(self) -> list[str]:
        """Return the ordered list of step names in this pipeline."""
        return [name for name, _fn in self._steps]

    def __len__(self) -> int:
        return len(self._steps)

    def __repr__(self) -> str:
        step_names = ", ".join(self.steps)
        return f"TextClean(steps=[{step_names}])"
