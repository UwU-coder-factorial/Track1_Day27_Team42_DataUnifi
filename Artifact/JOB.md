# DataUnifi Day 27 — Team Assignment and Evidence Record

## Source of truth

This file records Team 42's confirmed Day 27 ownership, evidence, process artefacts, rubric gates, and verification results. The project name is **DataUnifi**. Project behaviour is described as documented design unless a separate implementation or validation record is cited.

## Team

| Member | Student ID |
| --- | --- |
| Nguyễn Quang Huy | 2A202601873 |
| Trần Thị Kiều Trang | 2A202601498 |
| Nguyễn Quý Dũng | 2A202601200 |

## Format and process evidence

- Format làm bài: Markdown working artefacts + Python/ReportLab-generated PDF.
- Individual stakeholder inputs: `Artifact/individual/huy-stakeholders.md`, `Artifact/individual/trang-stakeholders.md`, `Artifact/individual/dung-stakeholders.md`.
- Individual pitch rewrites: `Artifact/individual/huy-pitch.md`, `Artifact/individual/trang-pitch.md`, `Artifact/individual/dung-pitch.md`.
- Team health input: `Artifact/individual/team-health-input.md`.
- Final submission: `Day27_AI-Team-Lab_Team42.pdf` at repository root; no other root PDF is used.

## Owner assignment

| Member | Owner areas |
| --- | --- |
| Nguyễn Quang Huy | Phase 0 scope; RACI; integration; README; final PDF QA; Gates 0, 2, and 5 |
| Trần Thị Kiều Trang | Stakeholder Map; stakeholder strategy; conclusion-first pitch; objection handling; Pages 1–2; Gate 1 |
| Nguyễn Quý Dũng | AI Team Architecture; core roles; capability gaps; priority resourcing; Team Health; competency; Growth Plan; Pages 3–4; Gates 3–4 |

## Team confirmation record

| Field | Record |
| --- | --- |
| Team confirmation status | CONFIRMED |
| Confirmed by | Team/user confirmation in the finalization task |
| Date | 2026-08-29 |
| Source | Written confirmation containing APPROVE, 12 health scores, L2 competency, and approvals for goal, stakeholders, RACI, architecture, individual artefacts, and growth plan |

## Confirmed goal

Trong 1–3 tháng tới, Team 42 hoàn thiện MVP DataUnifi có thể demo end-to-end trên dữ liệu mẫu/được phép sử dụng: một tenant upload CSV, AI đề xuất cleaning rules, người dùng review → dry-run → apply/rollback bằng deterministic engine; sau đó chạy một phiên entity matching có consent, masking và audit log, đủ để đánh giá readiness cho một pilot nội bộ có kiểm soát.

## Confirmed stakeholder map and strategy

| Stakeholder | Influence | Interest | Quadrant | Stance |
| --- | --- | --- | --- | --- |
| Thủ trưởng | High | High | Champion | Ủng hộ |
| Trợ lý Thủ trưởng | High | Low | Blocker | Chưa ủng hộ / cần được thuyết phục thêm |
| Phòng AI | Low | High | Supporter | Ủng hộ |
| Phòng Phần mềm | Low | High | Supporter | Trung lập |
| Nguyễn Quang Huy | High | High | Champion | Ủng hộ |
| Trần Thị Kiều Trang | High | High | Champion | Ủng hộ |
| Nguyễn Quý Dũng | High | High | Champion | Ủng hộ |

Priority leverage:

1. Thủ trưởng — send the one-page MVP scope and architecture/risk-control summary and request approval of demo scope and acceptance criteria.
2. Phòng AI — hold a short technical review of cleaning/matching quality and evaluation criteria before the demo milestone.

Priority persuade/de-risk:

1. Trợ lý Thủ trưởng — present the controlled demo/risk-control flow covering human approval, dry-run, rollback, masking, and audit log.
2. Phòng Phần mềm — review API boundaries, tenant isolation, access controls, deployment assumptions, and maintainability before architecture freeze.

## Confirmed pitch

Audience: **Thủ trưởng**.

Conclusion: Team 42 đề xuất tiếp tục DataUnifi tới một MVP/demo nội bộ có kiểm soát, tập trung chứng minh AI Data Cleaning và Entity Matching trước khi cân nhắc mở rộng.

Evidence wording: `PROJECT_SUMMARY.md` documents the project architecture and risk controls; the repository does not claim production validation, measured accuracy, or business impact.

Small ask: approve the controlled MVP/demo scope and acceptance criteria for the next milestone.

## Confirmed project RACI

| Task | Huy | Trang | Dũng | Stakeholder |
| --- | --- | --- | --- | --- |
| Chốt use case, MVP scope và acceptance criteria | A/R | C | C | Thủ trưởng: I |
| Multi-tenant data model, access control và consent flow | C | I | A/R | Phòng Phần mềm: C |
| AI Data Cleaning + deterministic execution workflow | C | I | A/R | Phòng AI: C |
| Entity Matching: mapping, blocking, scoring, review | C | I | A/R | Phòng AI: C |
| Frontend workflow: upload, review, approval, masking | C | A/R | C | Phòng Phần mềm: C |
| Integration, QA, demo/release readiness | A | R | R | Phòng AI: C; Phòng Phần mềm: C; Thủ trưởng: I |

Every task has exactly one accountable team member and at least one responsible team member.

## Confirmed AI Team and capability gaps

Architecture: **Embedded**.

- Nguyễn Quang Huy — Product / Integration / Release ownership.
- Trần Thị Kiều Trang — UX / Frontend / Stakeholder communication.
- Nguyễn Quý Dũng — AI / Data / Backend.
- Shared capability — Evaluation / QA.

Scaling additions: Security / Privacy review; MLOps / observability; Domain/data governance expert.

| Capability gap | Route | Partner or reviewer | Why | Timing |
| --- | --- | --- | --- | --- |
| AI evaluation baseline | Partner + build internally | Phòng AI | Objective quality criteria for cleaning suggestions and entity matching. | Before demo/pilot-readiness. |
| Integration / deployment review | Partner | Phòng Phần mềm | Review API boundaries, deployment assumptions, access controls, and maintainability. | Before MVP architecture freeze. |
| Security / privacy governance at pilot stage | Partner | Organisation-appointed security/privacy reviewer | Multi-tenant and cross-tenant workflows require privacy/security review. | Before real-data pilot. |

Squad goal: Team 42 sở hữu MVP DataUnifi và chịu trách nhiệm đưa workflow AI Data Cleaning + Entity Matching từ thiết kế hiện tại đến một demo end-to-end có human approval, tenant isolation, consent, masking, auditability và acceptance criteria rõ ràng.

## Confirmed Team Health

| Member | AI Quality | Progress | Team Morale | Shipping Speed |
| --- | ---: | ---: | ---: | ---: |
| Nguyễn Quang Huy | 4 | 4 | 4 | 3 |
| Trần Thị Kiều Trang | 4 | 4 | 5 | 3 |
| Nguyễn Quý Dũng | 4 | 3 | 4 | 3 |

| Dimension | Average |
| --- | ---: |
| AI Quality | 4.00/5 |
| Progress | 3.67/5 |
| Team Morale | 4.33/5 |
| Shipping Speed | 3.00/5 |

- Lowest dimension: Shipping Speed.
- Largest disagreement: Progress and Team Morale, both with range 1.
- Priority issue: improve shipping speed by freezing MVP scope and running the end-to-end demo checklist; the evaluation baseline remains the enabling quality action for the next milestone.

## Confirmed competency and Growth Plan

- Role: AI / Data / Backend.
- Owner: Nguyễn Quý Dũng.
- Current/nearest level: L2 — AI Practitioner.
- Next competency: AI evaluation / quality evaluation.
- 30-day practice: build golden cases for cleaning + matching and run regression evaluation before each milestone/release candidate.

| Problem | Action | Owner | Deadline | Completion signal |
| --- | --- | --- | --- | --- |
| AI quality needs a repeatable acceptance baseline. | Build a golden test set and evaluation checklist for cleaning + matching. | Nguyễn Quý Dũng | 14 days after confirmation (2026-09-12) | Golden cases and a reproducible evaluation report are linked to a release candidate. |
| The project design needs a demonstrable vertical slice. | Freeze MVP scope and complete the end-to-end demo script from CSV upload through cleaning, review, matching, masked result, and audit flow. | Nguyễn Quang Huy | 21 days after confirmation (2026-09-19) | The demo checklist runs end-to-end against confirmed acceptance criteria. |
| Stakeholder interest must become actionable feedback. | Prepare a review package and hold a checkpoint with priority stakeholders, recording issues, decisions, and next actions. | Trần Thị Kiều Trang | 30 days after confirmation (2026-09-28) | A review note contains feedback, decisions, and the next action. |

## Gate audit and verification log

The content contract was updated from the pre-confirmation state to the confirmed final state. Local content, PDF, text, and visual checks were refreshed on 2026-08-29; remote fields will be refreshed after merge.

| Gate | Current result | Evidence |
| --- | --- | --- |
| Gate 0 — Scope | PASS | Team 42, members, DataUnifi, confirmed goal, and integrator are present. |
| Gate 1 — Stakeholder | PASS | Seven concrete stakeholders, influence × interest, quadrants, stances, leverage, persuade/de-risk actions, and individual artefacts are present. |
| Gate 2 — Pitch & RACI | PASS | Conclusion-first pitch, evidence boundary, small ask, objection response, six tasks, and one A/task are present. |
| Gate 3 — AI Team | PASS | Embedded architecture, rationale, roles, three capability gaps, routes, partners, timing, and squad goal are present. |
| Gate 4 — Health & Growth | PASS | Twelve scores, derived summary, L2 competency, next competency, practice, and three complete growth actions are present. |
| Gate 5 — Submission | PASS (local) | Required root files, one four-page PDF, local QA, and branch artefact verification are complete; remote main verification is the post-merge step. |

| Check | Result | Evidence |
| --- | --- | --- |
| Content contract tests | PASS | `python -m pytest Artifact/test_submission.py -q` — 15 passed after final source and PDF-contract updates. |
| PDF generation | PASS | `python Artifact/generate_submission.py` exited 0 and wrote the required root PDF. |
| PDF page count | PASS | PyMuPDF reported 4 pages. |
| Required headings | PASS | PyMuPDF extracted all seven required headings. |
| Individual artefacts | PASS | Three stakeholder files with 7 rows each, three pitch files, and one 12-score health file. |
| Placeholder scan | PASS | No unresolved submission markers in README, JOB, PROJECT_SUMMARY, Artifact/individual, generator, or final PDF text. |
| Visual PDF QA | PASS | Four rendered pages inspected for clipping, overlap, glyphs, table collisions, and footer overlap. |
| Cross-page consistency | PASS | Page 1 stakeholders align with Page 2 pitch/RACI; Page 3 evaluation gap aligns with Page 4 priority/growth; owners align with RACI. |
| Remote main verified | PENDING MERGE | Remote verification follows the clean PR merge. |

Overall status: READY FOR MERGE

Artifact operation marker: unavailable because `container_tools/mark_artifact_operation_started.mjs` is not present in the repository; the required command was attempted once and the supported generator was used.
Main SHA: will be recorded after merge.
PR: #1 — https://github.com/UwU-coder-factorial/Track1_Day27_Team42_DataUnifi/pull/1
