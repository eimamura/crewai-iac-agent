# CrewAI IaC Agent MVP

A CrewAI-based Infrastructure as Code (IaC) agent MVP that generates minimal Terraform baseline proposals for AWS architectures.

## Overview

This agent takes AWS architecture requirements as input and produces:
1. A minimal Terraform baseline proposal (repo layout, modules, resources, skeleton code)
2. A structured proposal document following a strict 15-section format
3. Actionable, copy-pastable Terraform skeletons

## Features

- **Minimal and Opinionated**: Focuses on MVP-level proposals, avoiding feature creep
- **Strict Format**: Enforces exact output structure with 15 required sections
- **Dry-run Mode**: Works without LLM API keys using template-based drafts
- **Format Validation**: Automatically validates proposal structure
- **uv-managed**: Uses `uv` for fast, reliable dependency management

## Prerequisites

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Quick Start

### 1. Install Dependencies

```bash
make venv
make sync
```

Or manually:
```bash
uv venv
uv sync
```

### 2. Run the Agent

**With requirements file:**
```bash
uv run python -m iac_agent.main --requirements-file requirements.md
```

**With inline requirements:**
```bash
uv run python -m iac_agent.main --requirements "
- ALB + ECS Fargate for API
- RDS Postgres
- Separate dev/prod environments
"
```

**Dry-run mode (no LLM key required):**
```bash
uv run python -m iac_agent.main --requirements "..." --dry-run
```

### 3. Output

The agent will:
- Print the proposal to STDOUT
- Write `out/proposal.md`

## Project Structure

```
.
├── src/
│   └── iac_agent/
│       ├── __init__.py
│       ├── main.py          # CLI entrypoint
│       ├── crew.py          # CrewAI agents and tasks
│       ├── prompts.py       # Prompt templates
│       ├── validator.py     # Format validation
│       └── io.py            # File I/O utilities
├── pyproject.toml           # Project dependencies (uv)
├── uv.lock                  # Lock file (committed)
├── Makefile                 # Common commands
└── README.md
```

## Configuration

### LLM API Keys

The agent supports OpenAI (default) and can be extended for other providers.

Set environment variables:
```bash
export OPENAI_API_KEY="your-key-here"
# or
export ANTHROPIC_API_KEY="your-key-here"
```

If no API key is provided, use `--dry-run` mode for template-based drafts.

## Output Format

The proposal follows a strict 15-section format:

1. Summary
2. Assumptions
3. Minimal AWS Architecture
4. Minimal Terraform Repo Layout
5. Modules and Responsibilities
6. Required Resources
7. Terraform Skeleton (Code)
8. Why this design
9. Alternatives
10. Risks & Mitigations
11. Next Questions (Only if truly blocking)
12. CrewAI Python Scaffold (uv-managed)
13. Git Workflow and Repo Hygiene
14. How to Run (Local)
15. Notes (Extensibility)

## Development

### Format Code
```bash
make format
```

### Lint Code
```bash
make lint
```

### Run Tests
```bash
make test
```

## Git Workflow

- Branch: `mvp/crewai-iac-agent`
- Commits: Conventional Commits (feat/fix/chore/docs/test/refactor)
- Tag: `mvp-v0.1` when MVP is complete

## License

MIT

