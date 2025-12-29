"""Input/output handling for requirements and proposals."""

import json
from pathlib import Path
from typing import Optional


def read_requirements_file(file_path: str) -> str:
    """Read requirements from a markdown file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Requirements file not found: {file_path}")
    return path.read_text(encoding="utf-8")


def read_requirements_string(requirements: str) -> str:
    """Return requirements string as-is."""
    return requirements


def write_proposal(output_dir: Path, proposal: str) -> None:
    """Write proposal to out/proposal.md."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "proposal.md"
    output_path.write_text(proposal, encoding="utf-8")


def ensure_output_dir() -> Path:
    """Ensure output directory exists and return Path."""
    output_dir = Path("out")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Create .gitkeep if it doesn't exist
    gitkeep = output_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("")
    return output_dir

