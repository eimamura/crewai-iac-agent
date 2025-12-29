"""Validator for proposal format and structure."""

from typing import List, Tuple


REQUIRED_HEADINGS = [
    "## Summary",
    "## Assumptions",
    "## Minimal AWS Architecture",
    "## Minimal Terraform Repo Layout",
    "## Modules and Responsibilities",
    "## Required Resources",
    "## Terraform Skeleton (Code)",
    "## Why this design",
    "## Alternatives",
    "## Risks & Mitigations",
    "## Next Questions (Only if truly blocking)",
    "## CrewAI Python Scaffold (uv-managed)",
    "## Git Workflow and Repo Hygiene",
    "## How to Run (Local)",
    "## Notes (Extensibility)",
]


def extract_headings(text: str) -> List[str]:
    """Extract all markdown headings (##) from text."""
    headings = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("## "):
            headings.append(line)
    return headings


def validate_headings(text: str) -> Tuple[bool, List[str]]:
    """
    Validate that all required headings are present in correct order.
    Returns (is_valid, missing_or_out_of_order).
    """
    found_headings = extract_headings(text)
    errors = []

    # Check for missing headings
    for required in REQUIRED_HEADINGS:
        if required not in found_headings:
            errors.append(f"Missing heading: {required}")

    # Check order
    found_indices = []
    for i, found in enumerate(found_headings):
        if found in REQUIRED_HEADINGS:
            found_indices.append((i, REQUIRED_HEADINGS.index(found)))

    # Check if order is correct
    if found_indices:
        prev_index = -1
        for pos, req_index in found_indices:
            if req_index <= prev_index:
                errors.append(
                    f"Heading '{found_headings[pos]}' appears out of order. "
                    f"Expected order: {REQUIRED_HEADINGS}"
                )
                break
            prev_index = req_index

    return len(errors) == 0, errors


def validate_proposal(text: str) -> Tuple[bool, List[str]]:
    """
    Validate proposal format.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    is_valid, heading_errors = validate_headings(text)
    errors.extend(heading_errors)

    # Basic content checks
    if len(text.strip()) < 100:
        errors.append("Proposal content is too short (minimum 100 characters)")

    return len(errors) == 0, errors

