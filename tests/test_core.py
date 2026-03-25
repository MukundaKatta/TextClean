"""Tests for the TextClean pipeline."""

from textclean import PipelineConfig, TextClean


class TestTextCleanPipeline:
    """Core pipeline behaviour."""

    def test_lowercase_and_whitespace(self) -> None:
        cleaner = TextClean().lowercase().normalize_whitespace()
        assert cleaner.process("  Hello   WORLD  ") == "hello world"

    def test_strip_html_and_remove_urls(self) -> None:
        cleaner = TextClean().strip_html().remove_urls().normalize_whitespace()
        text = '<p>Visit <a href="https://example.com">https://example.com</a> now</p>'
        result = cleaner.process(text)
        assert "https" not in result
        assert "<" not in result
        assert "now" in result

    def test_remove_punctuation_and_numbers(self) -> None:
        cleaner = TextClean().remove_punctuation().remove_numbers().normalize_whitespace()
        assert cleaner.process("Price: $42.99!") == "Price"

    def test_remove_emails(self) -> None:
        cleaner = TextClean().remove_emails().normalize_whitespace()
        assert cleaner.process("Contact user@example.com for info") == "Contact for info"

    def test_remove_stopwords(self) -> None:
        cleaner = TextClean().lowercase().remove_stopwords().normalize_whitespace()
        result = cleaner.process("This is a simple test of the system")
        assert "this" not in result.split()
        assert "simple" in result.split()
        assert "test" in result.split()
        assert "system" in result.split()

    def test_stemming(self) -> None:
        cleaner = TextClean().lowercase().stem().normalize_whitespace()
        result = cleaner.process("running happiness")
        assert result == "runn happi"

    def test_remove_accents(self) -> None:
        cleaner = TextClean().remove_accents()
        assert cleaner.process("cafe\u0301 re\u0301sume\u0301") == "cafe resume"

    def test_custom_step(self) -> None:
        cleaner = TextClean().add_step(lambda t: t.replace("foo", "bar"), name="foo_to_bar")
        assert cleaner.process("foo baz") == "bar baz"
        assert "foo_to_bar" in cleaner.steps

    def test_process_batch(self) -> None:
        cleaner = TextClean().lowercase()
        results = cleaner.process_batch(["HELLO", "WORLD"])
        assert results == ["hello", "world"]

    def test_from_config(self) -> None:
        cfg = PipelineConfig(lowercase=True, strip_html=True, normalize_whitespace=True)
        cleaner = TextClean.from_config(cfg)
        result = cleaner.process("<b>Hello</b>   World")
        assert result == "hello world"

    def test_clean_alias(self) -> None:
        cleaner = TextClean().lowercase()
        assert cleaner.clean("FOO") == cleaner.process("FOO")

    def test_repr_and_len(self) -> None:
        cleaner = TextClean().lowercase().stem()
        assert len(cleaner) == 2
        assert "lowercase" in repr(cleaner)
