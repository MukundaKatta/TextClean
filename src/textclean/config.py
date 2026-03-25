"""Configuration models for TextClean pipelines."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    """Declarative configuration for a TextClean pipeline.

    Each boolean flag corresponds to a built-in cleaning step.
    Steps execute in the order listed here when using ``TextClean.from_config()``.
    """

    lowercase: bool = Field(default=False, description="Convert text to lowercase")
    strip_html: bool = Field(default=False, description="Remove HTML/XML tags")
    remove_urls: bool = Field(default=False, description="Remove URLs")
    remove_emails: bool = Field(default=False, description="Remove email addresses")
    remove_numbers: bool = Field(default=False, description="Remove digits")
    remove_punctuation: bool = Field(default=False, description="Remove punctuation")
    remove_stopwords: bool = Field(default=False, description="Remove common English stopwords")
    normalize_whitespace: bool = Field(default=True, description="Collapse whitespace")
    remove_accents: bool = Field(default=False, description="Strip diacritical marks")
    stem: bool = Field(default=False, description="Apply suffix-stripping stemmer")

    custom_stopwords: set[str] | None = Field(
        default=None,
        description="Optional custom stopword set (overrides built-in list)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "lowercase": True,
                "strip_html": True,
                "remove_urls": True,
                "normalize_whitespace": True,
            }
        }
