from __future__ import annotations

import importlib
import sys
from pathlib import Path


ARTIFACT_DIR = Path(__file__).resolve().parent


def _generator():
    """Load the implementation after the RED phase has created it."""
    source_path = ARTIFACT_DIR / "generate_submission.py"
    assert source_path.exists(), "generate_submission.py is required by the content contract"
    sys.path.insert(0, str(ARTIFACT_DIR))
    try:
        return importlib.import_module("generate_submission")
    finally:
        sys.path.remove(str(ARTIFACT_DIR))


def test_content_has_four_page_sections():
    pages = _generator().build_content()["pages"]
    assert [page["title"] for page in pages] == [
        "Stakeholder Map & Strategy",
        "Pitch & RACI",
        "AI Team Design",
        "Team Health & Growth Plan",
    ]


def test_unknown_decisions_are_explicitly_gated():
    content = _generator().build_content()
    assert content["confirmation_gate"]["title"] == "TEAM CONFIRMATION REQUIRED"
    assert "NEEDS TEAM INPUT" in content["confirmation_gate"]["body"]


def test_proposed_raci_has_one_accountable_per_task():
    generator = _generator()
    errors = generator.validate_raci(generator.build_content()["raci"])
    assert errors == []


def test_raci_validator_rejects_multiple_accountable_people():
    generator = _generator()
    invalid_row = {
        "task": "Example task",
        "Huy": "A",
        "Trang": "A",
        "Dung": "R",
    }
    errors = generator.validate_raci([invalid_row])
    assert errors == ["Example task: expected exactly one A, found 2"]


def test_required_headings_are_stable():
    assert _generator().required_headings() == [
        "Stakeholder Map",
        "Pitch",
        "RACI",
        "AI Team",
        "Capability",
        "Team Health",
        "Growth Plan",
    ]
