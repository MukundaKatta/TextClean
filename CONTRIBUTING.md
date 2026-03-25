# Contributing to TextClean

Thank you for your interest in contributing to TextClean! We welcome contributions of all kinds.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/my-feature`
4. Install development dependencies: `make dev`

## Development Workflow

```bash
# Install in editable mode with dev dependencies
make dev

# Run tests
make test

# Run linter
make lint

# Format code
make fmt
```

## Pull Request Process

1. Ensure all tests pass: `make test`
2. Add tests for any new functionality
3. Update documentation if needed
4. Submit your PR with a clear description of changes

## Code Style

- Follow PEP 8 conventions
- Use type hints for all function signatures
- Write docstrings for public methods
- Keep functions focused and composable

## Reporting Issues

- Use GitHub Issues to report bugs
- Include a minimal reproducible example
- Describe expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
