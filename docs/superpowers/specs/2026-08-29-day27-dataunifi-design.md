# Track 1 Day 27 DataUnifi Submission Design

**Date:** 2026-08-29
**Project:** DataUnifi
**Team:** Team 42
**Repository:** `https://github.com/UwU-coder-factorial/Track1_Day27_Team42_DataUnifi`

## Goal

Complete the Team 42 Track 1 Day 27 submission package with an evidence-safe README, a source-of-truth assignment file, and one polished four-page PDF named `Day27_AI-Team-Lab_Team42.pdf`.

The package must maximize rubric coverage without inventing facts. Project facts that are present in the repository may be used directly. Missing team decisions, measurements, stakeholder evidence, and personal inputs remain explicitly marked `NEEDS TEAM INPUT` and keep the submission status `PARTIAL` until the team confirms them.

## Evidence baseline

The repository currently provides:

- Project name: DataUnifi.
- Team: Team 42.
- Members and IDs supplied by the task prompt.
- A repository URL supplied by the task prompt.
- No current project goal, public demo URL, validated user feedback, stakeholder evidence, RACI decision, team-health scores, competency commitment, or growth commitment in the repository.

The generator must not convert the last group into facts. It may produce clearly labeled proposals and a single Human Confirmation Gate for the missing decisions.

## Deliverables

The implementation produces these tracked files:

- `README.md` - submission-facing project scope, members, current-goal status, integrator, demo status, and PDF link.
- `Artifact/JOB.md` - owner/reviewer assignment, evidence ledger, gate checklist, and confirmation status.
- `Artifact/generate_submission.py` - deterministic ReportLab source generator and content model for the PDF.
- `Day27_AI-Team-Lab_Team42.pdf` - the only final submission PDF at repository root.
- `docs/superpowers/specs/2026-08-29-day27-dataunifi-design.md` - this design record.
- `docs/superpowers/plans/2026-08-29-day27-dataunifi-implementation.md` - the implementation plan.

Intermediate rendered PNGs and temporary build files stay under `tmp/pdfs/` or another ignored temporary location and are not submission artefacts.

## Content and truth policy

The PDF follows the supplied Day 27 rubric:

- Page 1 covers Stakeholder Map & Strategy.
- Page 2 covers Conclusion-First Pitch, objection handling, and RACI.
- Page 3 covers AI Team Design, roles, capability gaps, resourcing, and squad goal.
- Page 4 covers Team Health, competency, and a measurable 30-day Growth Plan.

Where source evidence is missing, content uses one of these explicit states:

- `NEEDS TEAM INPUT` for facts that only the team can supply.
- `PROPOSED RACI` for an unconfirmed responsibility matrix.
- `INTERNAL PROTOTYPE/DEMO` for an unvalidated artefact, never `validated product`.
- `NOT PUBLICLY AVAILABLE` when no public demo link is present.

The final status is `PARTIAL` or `BLOCKED` when any required human confirmation or remote verification remains incomplete. `PASS` is permitted only after every Gate 0-5 check, visual PDF check, text QA, and remote check has fresh evidence.

## PDF design

The generator uses ReportLab with A4 landscape pages, built-in or locally available fonts, and no external CDN. It defines a small design system:

- dark navy canvas accents, warm off-white page background, and restrained teal/coral status colors;
- consistent page margins, page title, section labels, footer, and page number;
- compact tables with readable font sizes and wrapped paragraphs;
- influence-interest matrix on Page 1;
- visually distinct Champion, Blocker, Supporter, and Bystander badges;
- a single confirmation panel when human input is missing;
- no emoji or decorative clutter.

Each page is drawn by a focused function so page boundaries remain deterministic. Text content is stored in a structured data model near the top of the source file, separate from drawing helpers. All strings use ASCII hyphens where a dash is needed, while Vietnamese text remains UTF-8 and uses a registered local Unicode font when available.

## Verification

The implementation verifies:

1. `python Artifact/generate_submission.py` exits successfully and writes exactly the root PDF.
2. PyMuPDF reports exactly four pages.
3. Every page is rendered to PNG with Poppler or an available fallback and inspected for clipping, overlap, tiny text, broken tables, malformed Vietnamese, or blank content.
4. Extracted PDF text contains the required headings: Stakeholder Map, Pitch, RACI, AI Team, Capability, Team Health, and Growth Plan.
5. Repository search distinguishes intentional truth-state markers from unresolved generic unfinished markers; no unfinished marker remains.
6. `git diff --check` is clean.
7. The rubric audit checks cross-page consistency: Page 1 stakeholder to Page 2 pitch/RACI, Page 3 capability gap to Page 4 issue/growth action, and Page 4 owners to Page 2 RACI.
8. After push or merge, the remote repository is checked for README, `Artifact/JOB.md`, and the final PDF.

## Scope boundaries

This work does not invent product functionality, create a public demo, claim user validation, assign personal health scores, or change unrelated repository files. It does not create multiple final PDFs. Team-provided facts can be incorporated later by editing the content model and rerunning the same verification workflow.
