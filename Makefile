.PHONY: install dev test lint fmt clean build

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -v --tb=short

test-cov:
	pytest --cov=textclean --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/

fmt:
	ruff format src/ tests/

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	python -m build
