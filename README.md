# TextClean

[![CI](https://github.com/officethree/TextClean/actions/workflows/ci.yml/badge.svg)](https://github.com/officethree/TextClean/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python library for cleaning and normalizing text data with composable pipeline steps.

## Architecture

```mermaid
graph LR
    A[Raw Text] --> B[TextClean Pipeline]
    B --> C1[strip_html]
    C1 --> C2[remove_urls]
    C2 --> C3[lowercase]
    C3 --> C4[remove_punctuation]
    C4 --> C5[remove_stopwords]
    C5 --> C6[stem]
    C6 --> C7[normalize_whitespace]
    C7 --> D[Clean Text]
```

```mermaid
classDiagram
    class TextClean {
        -List steps
        +lowercase() Self
        +strip_html() Self
        +remove_urls() Self
        +remove_emails() Self
        +remove_numbers() Self
        +remove_punctuation() Self
        +remove_stopwords() Self
        +normalize_whitespace() Self
        +remove_accents() Self
        +stem() Self
        +add_step(fn) Self
        +process(text) str
        +clean(text) str
        +process_batch(texts) list
        +from_config(cfg) TextClean
    }
    class PipelineConfig {
        +bool lowercase
        +bool strip_html
        +bool remove_urls
        +bool remove_emails
        +bool remove_numbers
        +bool remove_punctuation
        +bool remove_stopwords
        +bool normalize_whitespace
        +bool remove_accents
        +bool stem
    }
    TextClean ..> PipelineConfig : from_config()
```

## Quickstart

### Installation

```bash
pip install -e .
```

### Usage

```python
from textclean import TextClean

# Build a pipeline with chained steps
cleaner = (
    TextClean()
    .lowercase()
    .strip_html()
    .remove_urls()
    .remove_punctuation()
    .remove_stopwords()
    .normalize_whitespace()
)

text = '<p>Visit https://example.com for MORE info!</p>'
print(cleaner.process(text))
# => "visit info"

# Process multiple texts at once
results = cleaner.process_batch(["<b>Hello</b> World!", "Testing 123..."])
```

### Config-driven pipeline

```python
from textclean import TextClean, PipelineConfig

config = PipelineConfig(
    lowercase=True,
    strip_html=True,
    remove_urls=True,
    normalize_whitespace=True,
)
cleaner = TextClean.from_config(config)
print(cleaner.process("<h1>Hello</h1>"))
# => "hello"
```

### Custom steps

```python
from textclean import TextClean

cleaner = (
    TextClean()
    .lowercase()
    .add_step(lambda t: t.replace("foo", "bar"), name="foo_to_bar")
    .normalize_whitespace()
)
```

## Development

```bash
make dev      # install with dev dependencies
make test     # run tests
make lint     # lint with ruff
make fmt      # format with ruff
```

## Inspiration

Inspired by NLP preprocessing and text cleaning trends.

---

Built by [Officethree Technologies](https://officethree.com) | Made with love and AI
