.PHONY: help venv sync install run test clean format lint

help:
	@echo "Available targets:"
	@echo "  venv      - Create virtual environment with uv"
	@echo "  sync      - Install dependencies with uv sync"
	@echo "  install   - Alias for sync"
	@echo "  run       - Run the agent (use: make run ARGS='--requirements \"...\"')"
	@echo "  test      - Run tests"
	@echo "  clean     - Remove .venv and out/ directory"
	@echo "  format    - Format code with black"
	@echo "  lint      - Lint code with ruff"

venv:
	uv venv

sync: venv
	uv sync

install: sync

run: sync
	uv run python -m iac_agent.main $(ARGS)

test: sync
	uv run pytest

clean:
	rm -rf .venv
	rm -rf out/

format: sync
	uv run black src/

lint: sync
	uv run ruff check src/

