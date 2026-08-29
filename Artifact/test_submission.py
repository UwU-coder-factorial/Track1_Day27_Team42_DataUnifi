from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path(__file__).resolve().parent
INDIVIDUAL_DIR = ARTIFACT_DIR / "individual"
UNRESOLVED_MARKERS = (
    "NEEDS " + "TEAM INPUT",
    "PRO" + "POSED",
    "T" + "BD",
    "TO" + "DO",
    "TEAM " + "CONFIRMATION REQUIRED",
    "AWAITING " + "MEMBER CONFIRMATION",
)


def _generator():
    source_path = ARTIFACT_DIR / "generate_submission.py"
    assert source_path.exists(), "generate_submission.py is required by the content contract"
    sys.path.insert(0, str(ARTIFACT_DIR))
    try:
        return importlib.import_module("generate_submission")
    finally:
        sys.path.remove(str(ARTIFACT_DIR))


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _table_rows(path: Path) -> list[str]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped and not stripped.lower().startswith("| stakeholder"):
            rows.append(stripped)
    return rows


def test_content_has_four_page_sections():
    pages = _generator().build_content()["pages"]
    assert [page["title"] for page in pages] == [
        "Stakeholder Map & Strategy",
        "Pitch & RACI",
        "AI Team Design",
        "Team Health & Growth Plan",
    ]


def test_final_submission_has_no_unresolved_markers():
    content = _generator().build_content()
    text = "\n".join(_strings(content))
    assert not [marker for marker in UNRESOLVED_MARKERS if marker in text]
    assert content["status"] == "PASS - TEAM CONFIRMED & VERIFIED"


def test_final_stakeholders_are_concrete_and_complete():
    stakeholders = _generator().build_content()["stakeholders"]
    assert len(stakeholders) >= 6
    for row in stakeholders:
        assert all(row.get(field) for field in ("stakeholder", "influence", "interest", "quadrant", "stance", "evidence"))
        assert not any(marker in row["stakeholder"] for marker in ("Proposed", "candidate", "unknown"))


def test_individual_stakeholder_artefacts_have_at_least_six_rows():
    for filename in ("huy-stakeholders.md", "trang-stakeholders.md", "dung-stakeholders.md"):
        path = INDIVIDUAL_DIR / filename
        assert path.exists(), filename
        assert len(_table_rows(path)) >= 6


def test_individual_pitch_artefacts_are_present_and_structured():
    for filename in ("huy-pitch.md", "trang-pitch.md", "dung-pitch.md"):
        path = INDIVIDUAL_DIR / filename
        assert path.exists(), filename
        text = path.read_text(encoding="utf-8")
        for heading in ("Conclusion First", "Reasons", "Evidence", "Small Ask"):
            assert heading in text
        assert not any(marker in text for marker in UNRESOLVED_MARKERS)


def test_confirmed_team_health_scores_are_integers_from_one_to_five():
    scores = _generator().build_content()["health"]["scores"]
    assert set(scores) == {"Huy", "Trang", "Dũng"}
    assert all(set(row) == {"AI Quality", "Progress", "Team Morale", "Shipping Speed"} for row in scores.values())
    assert all(isinstance(score, int) and 1 <= score <= 5 for row in scores.values() for score in row.values())


def test_team_health_summary_is_derived_from_confirmed_scores():
    summary = _generator().build_content()["health"]["summary"]
    assert summary["averages"] == {
        "AI Quality": 4.0,
        "Progress": 3.67,
        "Team Morale": 4.33,
        "Shipping Speed": 3.0,
    }
    assert summary["lowest_dimension"] == "Shipping Speed"
    assert summary["largest_disagreement"] == "Progress and Team Morale (range 1)"


def test_raci_has_one_accountable_and_at_least_one_responsible_per_task():
    generator = _generator()
    content = generator.build_content()
    assert 4 <= len(content["raci"]) <= 6
    assert generator.validate_raci(content["raci"]) == []


def test_raci_validator_rejects_multiple_accountable_people_and_unknown_columns():
    generator = _generator()
    invalid_row = {
        "task": "Example task",
        "Huy": "A/R",
        "Trang": "A",
        "Dũng": "R",
        "Eve": "C",
    }
    errors = generator.validate_raci([invalid_row])
    assert "Example task: expected exactly one A, found 2" in errors
    assert "Example task: unrecognized RACI column 'Eve'" in errors


def test_growth_plan_has_at_most_three_complete_actions():
    growth = _generator().build_content()["health"]["growth"]
    assert 1 <= len(growth) <= 3
    required = {"problem", "action", "owner", "deadline", "completion_signal"}
    assert all(required <= set(item) and all(item[key] for key in required) for item in growth)


def test_final_pitch_is_conclusion_first_and_within_half_page_scope():
    pitch = _generator().build_content()["pitch"]
    assert pitch["audience"] == "Thủ trưởng"
    assert pitch["conclusion"]
    assert len(pitch["reasons"]) in (2, 3)
    assert pitch["max_page_fraction"] <= 0.5
    assert len(pitch["plain_text"]) <= 900


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


def test_pdf_builder_writes_the_requested_output():
    generator = _generator()
    output = ARTIFACT_DIR / ".test_submission_output.pdf"
    try:
        assert generator.build_pdf(output) == output
        assert output.exists()
    finally:
        output.unlink(missing_ok=True)
