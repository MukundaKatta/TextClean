# Architecture

## Overview

TextClean is a composable text preprocessing pipeline built around a simple builder pattern. Each cleaning operation is a standalone function that can be chained together to form a pipeline.

## Module Structure

```
src/textclean/
  __init__.py      Public API surface (TextClean, PipelineConfig)
  core.py          TextClean class — the pipeline builder and executor
  config.py        Pydantic-based PipelineConfig for declarative setup
  utils.py         Pure-function utilities: regex patterns, stopwords, stemmer
```

## Key Design Decisions

### Fluent / Chainable API

Every builder method on `TextClean` returns `self`, enabling concise pipeline construction:

```python
cleaner = TextClean().lowercase().strip_html().normalize_whitespace()
```

### Steps as Named Tuples

Internally, steps are stored as `(name, callable)` pairs. This gives us free introspection (`cleaner.steps`) while keeping execution fast.

### Config-Driven Construction

`PipelineConfig` (Pydantic model) allows pipelines to be defined declaratively via JSON, YAML, or environment variables and instantiated with `TextClean.from_config(cfg)`.

### Extensibility

`add_step(fn)` lets users inject arbitrary transformations without subclassing.

## Data Flow

```
Input text
  -> step 1 (e.g. strip_html)
  -> step 2 (e.g. lowercase)
  -> ...
  -> step N (e.g. normalize_whitespace)
  -> Cleaned text
```

Each step receives the output of the previous step. All steps are pure `str -> str` functions.
