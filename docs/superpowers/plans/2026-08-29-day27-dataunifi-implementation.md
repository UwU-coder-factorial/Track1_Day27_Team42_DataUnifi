# DataUnifi Day 27 Submission Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an evidence-safe Team 42 Day 27 submission package with a README, assignment/evidence record, deterministic four-page PDF generator, and verified final PDF.

**Architecture:** Keep all editable submission content in a structured content model inside `Artifact/generate_submission.py`; keep drawing helpers separate from the content data. Generate one root-level PDF with deterministic ReportLab page functions, then verify it with Python/PyMuPDF and visual page renders. Unknown team facts remain in one explicit Human Confirmation Gate and are never treated as completed evidence.

**Tech Stack:** Python 3, ReportLab, PyMuPDF, Poppler `pdftoppm` when available, PowerShell, Git.

**Spec:** `docs/superpowers/specs/2026-08-29-day27-dataunifi-design.md`

## Global Constraints

- The final submission filename is exactly `Day27_AI-Team-Lab_Team42.pdf` at repository root.
- The PDF has exactly four A4 landscape pages: Stakeholder Map & Strategy; Pitch & RACI; AI Team Design; Team Health & Growth Plan.
- Do not invent DataUnifi goals, public links, validation, stakeholder identities, personal health scores, or team commitments.
- Use `NEEDS TEAM INPUT` for missing facts and `PROPOSED RACI` for an unconfirmed responsibility matrix.
- Keep the only final PDF at repository root; use `tmp/pdfs/` for rendered PNGs and other intermediates.
- Use locally available fonts and no external CDN.
- Run `node container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format pdf` successfully exactly once immediately before the first PDF-generation command.
- Do not claim `STATUS: PASS` unless Gates 0-5, human confirmation, PDF inspection, placeholder QA, and remote verification all have fresh evidence.

---

### Task 1: Record evidence, owners, and submission scope

**Files:**
- Modify: `README.md`
- Create: `Artifact/JOB.md`

**Interfaces:**
- Produces the authoritative project/member/owner/evidence state consumed by the generator in Task 3.
- Uses the fixed Team 42 member data and owner assignment from the approved spec.

- [ ] **Step 1: Replace the minimal README with evidence-safe submission metadata.**

Write a concise README containing the exact project/team/member information from the task prompt, plus:

```md
# Track 1 - Day 27 - AI Team Lab

- Team: Team 42
- Members:
  - Nguyen Quang Huy - 2A202601873
  - Tran Thi Kieu Trang - 2A202601498
  - Nguyen Quy Dung - 2A202601200
- Project: DataUnifi
- Current goal: NEEDS TEAM INPUT - the repository contains no confirmed 1-3 month goal.
- Integrator: Nguyen Quang Huy
- Product/demo link: Chua co link demo cong khai
- Submission: [Day27_AI-Team-Lab_Team42.pdf](./Day27_AI-Team-Lab_Team42.pdf)

The current package is PARTIAL until the team confirms the goal, stakeholder evidence, RACI, health scores, competency, and growth commitments.
```

Keep the Vietnamese spelling if the source file is UTF-8, but do not add a URL that was not supplied.

- [ ] **Step 2: Create `Artifact/JOB.md` as the source-of-truth assignment and evidence ledger.**

Include these exact owner mappings:

| Member | Owner areas | Reviewer/confirmation needed |
| --- | --- | --- |
| Nguyen Quang Huy | Phase 0 Scope, RACI, Integration, README, Final PDF QA, Gates 0/2/5 | Team confirmation for current goal and RACI |
| Tran Thi Kieu Trang | Stakeholder Map, Stakeholder Strategy, Conclusion-First Pitch, objection handling, Page 1, Pitch Page 2, Gate 1 | Team confirmation for stakeholder identities, stance, and evidence |
| Nguyen Quy Dung | AI Team Architecture, Core Roles, Capability Gaps, Priority Resourcing, Team Health, Competency, Growth Plan, Pages 3/4, Gates 3/4 | Team confirmation for architecture, scores, competency, and commitments |

Add an evidence ledger that explicitly records what is available and what is not. Add one Human Confirmation Gate with the four requested items: current goal, proposed RACI, the 4x3 team-health matrix, and competency/growth commitments. Do not create personal scores or stakeholder names.

- [ ] **Step 3: Check the docs for forbidden generic unfinished markers and whitespace.**

Run:

```powershell
$bad = @('TO'+'DO', 'T'+'BD', 'PLACE'+'HOLDER')
rg -n ($bad -join '|') README.md Artifact/JOB.md
git diff --check
```

Expected: the search returns no matches and `git diff --check` exits with code 0.

- [ ] **Step 4: Commit the evidence and ownership record.**

```powershell
git add README.md Artifact/JOB.md
git commit -m "docs: record DataUnifi Day27 evidence and owners"
```

### Task 2: Write the content-model contract tests first

**Files:**
- Create: `Artifact/test_submission.py`

**Interfaces:**
- Consumes: `build_content()`, `validate_raci(rows)`, and `required_headings()` from `Artifact/generate_submission.py`.
- Produces: executable tests that define the minimum content and RACI invariants before the generator exists.

- [ ] **Step 1: Write failing tests for the content contract.**

Create tests that import the planned functions and assert:

```python
def test_content_has_four_page_sections():
    pages = build_content()["pages"]
    assert [page["title"] for page in pages] == [
        "Stakeholder Map & Strategy",
        "Pitch & RACI",
        "AI Team Design",
        "Team Health & Growth Plan",
    ]

def test_unknown_decisions_are_explicitly_gated():
    content = build_content()
    assert content["confirmation_gate"]["title"] == "TEAM CONFIRMATION REQUIRED"
    assert "NEEDS TEAM INPUT" in content["confirmation_gate"]["body"]

def test_proposed_raci_has_one_accountable_per_task():
    errors = validate_raci(build_content()["raci"])
    assert errors == []

def test_required_headings_are_stable():
    assert required_headings() == [
        "Stakeholder Map",
        "Pitch",
        "RACI",
        "AI Team",
        "Capability",
        "Team Health",
        "Growth Plan",
    ]
```

The RACI test must count literal `A` values across Huy, Trang, and Dung and reject rows with zero or multiple `A` values.

- [ ] **Step 2: Run the tests and confirm they fail for the intended missing module.**

Run:

```powershell
python -m pytest Artifact/test_submission.py -q
```

Expected: collection fails because `Artifact/generate_submission.py` has not been created yet. Do not hide the failure or weaken the test.

- [ ] **Step 3: Commit the test contract.**

```powershell
git add Artifact/test_submission.py
git commit -m "test: define DataUnifi submission content contract"
```

### Task 3: Implement the deterministic four-page ReportLab generator

**Files:**
- Create: `Artifact/generate_submission.py`

**Interfaces:**
- `build_content() -> dict[str, object]` returns the complete four-page structured content and one confirmation gate.
- `validate_raci(rows: list[dict[str, object]]) -> list[str]` returns one human-readable error per invalid row and an empty list for the proposed matrix.
- `required_headings() -> list[str]` returns the seven text-QA headings in order.
- `register_fonts() -> tuple[str, str]` returns regular and bold registered font names, using Windows Arial or a locally available DejaVu fallback.
- `build_pdf(output_path: pathlib.Path) -> pathlib.Path` writes the four-page PDF and returns the same path.
- `main() -> None` resolves the repository root and writes `Day27_AI-Team-Lab_Team42.pdf` there.

- [ ] **Step 1: Implement the data model with only known facts plus labeled proposals.**

`build_content()` must include:

- all three member names/IDs;
- six stakeholder candidate rows, each labeled as unconfirmed and carrying `NEEDS TEAM INPUT` for exact identity/evidence rather than invented names;
- Influence x Interest matrix, quadrant, and stance fields as explicit unconfirmed values;
- four concrete action slots that describe the missing confirmation needed and do not claim an executed action;
- a Page 2 pitch with `CONCLUSION`, two or three reasons, evidence labeled as unavailable/internal only, and a small ask for team confirmation;
- one likely objection and a risk-reduction response framed as a proposed limited pilot/acceptance-criteria action, without calling the product validated;
- five proposed RACI rows for actual near-term work, exactly one `A` per row, and a stakeholder column marked `NEEDS TEAM INPUT`;
- one proposed architecture labeled `PROPOSED - NEEDS TEAM INPUT`, with rationale limited to the known three-person team and unknown project stage;
- Core and Extended capability rows, one to three capability-gap rows with Hire/Outsource/Partner alternatives marked as proposals, and one squad-goal sentence marked for confirmation;
- the four team-health dimensions with Huy, Trang, and Dung values all set to `NEEDS TEAM INPUT`, not numeric scores;
- one competency entry and at most three measurable growth-action rows, each explicitly pending team confirmation;
- exactly one confirmation gate object with the required title and all missing decision fields.

Use `PROPOSED RACI` in the page title/subtitle so the matrix is never mistaken for a team-approved decision.

- [ ] **Step 2: Implement font registration and layout primitives.**

Register a local font by checking these paths in order:

```text
C:\Windows\Fonts\arial.ttf
C:\Windows\Fonts\arialbd.ttf
C:\Windows\Fonts\segoeui.ttf
C:\Windows\Fonts\segoeuib.ttf
```

Fall back to ReportLab Helvetica only if no Unicode-capable local font exists, and write the selected font names to stdout for diagnostics. Add helpers for wrapped paragraphs, section labels, cards, tables, status badges, page title/footer, and safe text clipping. Use A4 landscape dimensions, fixed margins, and a minimum body font size of 7.2pt.

- [ ] **Step 3: Implement the four page functions.**

Create `draw_page_1`, `draw_page_2`, `draw_page_3`, and `draw_page_4` with these required visual regions:

1. Page 1: title, influence-interest matrix, six-row stakeholder table, Champion/Blocker/Supporter/Bystander badge legend, leverage/persuade callouts, and four concrete action rows.
2. Page 2: conclusion-first pitch card, reasons/evidence/small ask, objection-response card, and a compact five-row RACI table with one `A` in every row.
3. Page 3: architecture card, Core versus Extended roles, capability-gap/resourcing table, and squad-goal card.
4. Page 4: four-dimension team-health table, priority issue card, competency card, three-row growth plan, and the single confirmation gate panel.

Every page must include a readable footer with `DataUnifi | Team 42`, the page number, and a state indicator such as `PARTIAL - TEAM CONFIRMATION REQUIRED`.

- [ ] **Step 4: Run content tests and fix only implementation defects.**

Run:

```powershell
python -m pytest Artifact/test_submission.py -q
```

Expected: all contract tests pass with zero failures before any PDF is generated.

- [ ] **Step 5: Commit the generator source.**

```powershell
git add Artifact/generate_submission.py
git commit -m "feat: add DataUnifi Day27 PDF generator"
```

### Task 4: Generate, render, and visually verify the PDF

**Files:**
- Create: `Day27_AI-Team-Lab_Team42.pdf`
- Create: `tmp/pdfs/page-1.png` through `tmp/pdfs/page-4.png` as ignored intermediates

**Interfaces:**
- Consumes: `Artifact/generate_submission.py` and the content contract tests.
- Produces: one root-level PDF with exactly four pages and inspected page renders.

- [ ] **Step 1: Start the PDF artifact operation exactly once.**

Run immediately before the first generation command:

```powershell
node container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format pdf
```

Record the command exit code; do not run it a second time during rerenders.

- [ ] **Step 2: Generate the root PDF.**

Run:

```powershell
python Artifact/generate_submission.py
```

Expected: exit code 0, one `Day27_AI-Team-Lab_Team42.pdf` at repo root, and no alternate final PDF names.

- [ ] **Step 3: Verify page count and required extracted text.**

Run:

```powershell
python -c "import fitz; p=fitz.open('Day27_AI-Team-Lab_Team42.pdf'); print('PAGE_COUNT =', len(p)); assert len(p) == 4; text='\\n'.join(page.get_text() for page in p); required=['Stakeholder Map','Pitch','RACI','AI Team','Capability','Team Health','Growth Plan']; missing=[x for x in required if x not in text]; print('MISSING_HEADINGS =', missing); assert not missing"
```

Expected: `PAGE_COUNT = 4`, `MISSING_HEADINGS = []`.

- [ ] **Step 4: Render all pages to PNGs.**

Prefer Poppler:

```powershell
New-Item -ItemType Directory -Force tmp/pdfs | Out-Null
pdftoppm -png -r 144 Day27_AI-Team-Lab_Team42.pdf tmp/pdfs/page
```

If `pdftoppm` is unavailable, render each page with PyMuPDF at 144 DPI into `tmp/pdfs/page-1.png` through `page-4.png` using a short read-only helper command; keep the same output names.

- [ ] **Step 5: Inspect every rendered page visually and fix defects.**

Use the image viewer on all four PNGs. Check for clipped or overlapping text, tiny body copy, malformed Vietnamese glyphs, broken table borders, badges that collide with labels, blank regions, and content outside the page. If any defect appears, patch the generator, rerun the generator, rerender all four pages, and inspect all four again.

- [ ] **Step 6: Run repository text QA and whitespace checks.**

Run:

```powershell
$bad = @('TO'+'DO', 'T'+'BD', 'PLACE'+'HOLDER')
rg -n ($bad -join '|') . -g '!tmp/pdfs/**'
git diff --check
```

Expected: no forbidden generic unfinished markers and a clean whitespace check. `NEEDS TEAM INPUT` and `PROPOSED RACI` are intentional truth-state markers and must remain documented in the final audit.

- [ ] **Step 7: Commit the verified PDF and source state.**

```powershell
git add Day27_AI-Team-Lab_Team42.pdf README.md Artifact/JOB.md Artifact/generate_submission.py Artifact/test_submission.py
git commit -m "feat: complete DataUnifi Day27 submission package"
```

### Task 5: Audit rubric gates, consistency, and remote state

**Files:**
- Modify: `Artifact/JOB.md`

**Interfaces:**
- Consumes: the generated PDF, extracted text, visual inspection results, Git state, and remote refs.
- Produces: an evidence-backed gate result and the final handoff report.

- [ ] **Step 1: Audit every gate against the actual artefacts.**

Update the checklist in `Artifact/JOB.md` with `PASS`, `PARTIAL`, or `FAIL` only when supported by a check. Verify:

```text
Gate 0: project/member/integrator metadata is present; current goal is still team input.
Gate 1: six candidate rows, matrix, quadrants, stance, leverage/persuasion, and four actions are visible; factual stakeholder confirmation is pending.
Gate 2: conclusion-first structure, objection response, proposed RACI, and exactly one A per task are visible; team approval is pending.
Gate 3: one proposed architecture, rationale, core/extended roles, gap/resourcing/timing, and squad goal are visible; confirmation is pending.
Gate 4: four health dimensions, priority issue, competency, and <=3 measurable growth actions are visible; scores and commitments are pending.
Gate 5: README, exactly one root PDF, four pages, clean text/layout QA, and remote availability are checked.
```

- [ ] **Step 2: Run cross-page consistency checks.**

Confirm that the Page 1 priority stakeholder reference is the one used in the Page 2 pitch/RACI context, the Page 3 capability gap is reflected in the Page 4 priority issue and growth plan, and every growth owner is represented in the RACI. If missing team input prevents a factual link, record `PARTIAL` and name the exact missing field.

- [ ] **Step 3: Verify the local commit and final tree.**

Run:

```powershell
git status --short --branch
git diff --check
git ls-tree -r --name-only HEAD | rg '^(README.md|Artifact/JOB.md|Artifact/generate_submission.py|Artifact/test_submission.py|Day27_AI-Team-Lab_Team42.pdf)$'
```

Expected: clean working tree, clean diff check, and exactly the required submission files listed.

- [ ] **Step 4: Push only the current approved branch if credentials and repository policy allow it.**

Because the work was approved on the existing checkout, use the current branch and do not force push:

```powershell
git push origin main
```

If the remote rejects the push, preserve the local commit and report the exact rejection as a remaining blocker instead of retrying destructively.

- [ ] **Step 5: Verify the remote repository after a successful push.**

Run:

```powershell
git fetch origin --prune
git ls-tree -r --name-only origin/main | rg '^(README.md|Artifact/JOB.md|Day27_AI-Team-Lab_Team42.pdf)$'
git rev-parse HEAD
git rev-parse origin/main
```

Expected: all three remote files are present and the local and remote commit IDs match. If a public HTTP check is needed, open the exact GitHub raw/blob URLs and confirm the PDF is downloadable; record `REMOTE MAIN VERIFIED: NO` when access or push is unavailable.

- [ ] **Step 6: Produce the final report using evidence, not aspiration.**

Use the exact requested fields: status, repo, branch, commit, PDF, page count, remote verification, Gate 0-5 results, consistency, visual check, unresolved human input, remaining blockers, and submit link. Use `STATUS: PARTIAL` while the Human Confirmation Gate remains unresolved; use `STATUS: PASS` only after a team confirmation and fresh remote/visual verification.
