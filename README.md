# TextClean — Text preprocessing pipeline — chainable cleaning steps: HTML, URLs, stopwords, stemming, normalization

Text preprocessing pipeline — chainable cleaning steps: HTML, URLs, stopwords, stemming, normalization. TextClean gives you a focused, inspectable implementation of that idea.

## Why TextClean

TextClean exists to make this workflow practical. Text preprocessing pipeline — chainable cleaning steps: html, urls, stopwords, stemming, normalization. It favours a small, inspectable surface over sprawling configuration.

## Features

- `TextClean` — exported from `src/textclean/core.py`
- Included test suite
- Dedicated documentation folder

## Tech Stack

- **Runtime:** Python
- **Tooling:** Pydantic

## How It Works

The codebase is organised into `docs/`, `src/`, `tests/`. The primary entry points are `src/textclean/core.py`, `src/textclean/__init__.py`. `src/textclean/core.py` exposes `TextClean` — the core types that drive the behaviour.

## Getting Started

```bash
pip install -e .
```

## Usage

```python
from textclean.core import TextClean

instance = TextClean()
# See the source for the full API
```

## Project Structure

```
TextClean/
├── .env.example
├── CONTRIBUTING.md
├── Makefile
├── README.md
├── docs/
├── pyproject.toml
├── src/
├── tests/
```
