# Tips-Endstone Makefile
# Cross-platform build commands using uv

.PHONY: install sync build clean lint test dev help

# Default target
help:
	@echo "Tips-Endstone Build Commands"
	@echo "============================"
	@echo "  make install  - Install uv (if not present)"
	@echo "  make sync     - Sync dependencies"
	@echo "  make dev      - Sync with dev dependencies"
	@echo "  make build    - Build wheel package"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make lint     - Run ruff linter"
	@echo "  make test     - Run tests"
	@echo ""

# Install uv
install:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
	@echo "uv version: $$(uv --version)"

# Sync dependencies
sync:
	uv sync

# Sync with dev dependencies
dev:
	uv sync --group dev

# Build wheel
build: sync
	uv build --wheel
	@echo "Build complete! Check dist/ folder"

# Clean build artifacts
clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned build artifacts"

# Run linter
lint: dev
	uv run ruff check src/

# Run tests
test: dev
	uv run pytest

# Format code
format: dev
	uv run ruff format src/
