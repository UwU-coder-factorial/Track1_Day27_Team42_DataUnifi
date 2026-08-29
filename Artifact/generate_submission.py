from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle


PAGE_W, PAGE_H = landscape(A4)
MARGIN = 8 * mm
CONTENT_W = PAGE_W - (2 * MARGIN)

NAVY = colors.HexColor("#102A43")
INK = colors.HexColor("#243B53")
MUTED = colors.HexColor("#627D98")
PAPER = colors.HexColor("#F7F9FC")
WHITE = colors.white
TEAL = colors.HexColor("#0F766E")
TEAL_LIGHT = colors.HexColor("#D9F3F0")
CORAL = colors.HexColor("#C2413B")
CORAL_LIGHT = colors.HexColor("#FDE7E5")
GOLD = colors.HexColor("#B7791F")
GOLD_LIGHT = colors.HexColor("#FFF4D6")
BLUE_LIGHT = colors.HexColor("#E6F0FF")
GRID = colors.HexColor("#D9E2EC")
LAVENDER = colors.HexColor("#EEE9FF")

REGULAR_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"


def required_headings() -> list[str]:
    return [
        "Stakeholder Map",
        "Pitch",
        "RACI",
        "AI Team",
        "Capability",
        "Team Health",
        "Growth Plan",
    ]


def summarize_health(scores: dict[str, dict[str, int]]) -> dict[str, Any]:
    dimensions = ("AI Quality", "Progress", "Team Morale", "Shipping Speed")
    averages = {
        dimension: round(sum(row[dimension] for row in scores.values()) / len(scores), 2)
        for dimension in dimensions
    }
    ranges = {
        dimension: max(row[dimension] for row in scores.values()) - min(row[dimension] for row in scores.values())
        for dimension in dimensions
    }
    largest_range = max(ranges.values())
    largest_dimensions = [dimension for dimension in dimensions if ranges[dimension] == largest_range]
    return {
        "averages": averages,
        "lowest_dimension": min(dimensions, key=averages.get),
        "largest_disagreement": " and ".join(largest_dimensions) + f" (range {largest_range})",
    }


def build_content() -> dict[str, Any]:
    stakeholders = [
        {
            "stakeholder": "Thủ trưởng",
            "influence": "High",
            "interest": "High",
            "quadrant": "Champion",
            "stance": "Ủng hộ",
            "evidence": "Confirmed team stakeholder; decides value, feasibility, risk, and approval to proceed.",
        },
        {
            "stakeholder": "Trợ lý Thủ trưởng",
            "influence": "High",
            "interest": "Low",
            "quadrant": "Blocker",
            "stance": "Chưa ủng hộ / cần được thuyết phục thêm",
            "evidence": "Confirmed high-influence stakeholder; needs clarity on benefit, data, scope, and accountability.",
        },
        {
            "stakeholder": "Phòng AI",
            "influence": "Low",
            "interest": "High",
            "quadrant": "Supporter",
            "stance": "Ủng hộ",
            "evidence": "Confirmed technical stakeholder for cleaning quality, matching logic, and evaluation review.",
        },
        {
            "stakeholder": "Phòng Phần mềm",
            "influence": "Low",
            "interest": "High",
            "quadrant": "Supporter",
            "stance": "Trung lập",
            "evidence": "Confirmed technical stakeholder for integration, deployment, access controls, and maintainability review.",
        },
        {
            "stakeholder": "Nguyễn Quang Huy",
            "influence": "High",
            "interest": "High",
            "quadrant": "Champion",
            "stance": "Ủng hộ",
            "evidence": "Confirmed internal core stakeholder; product, integration, and release ownership.",
        },
        {
            "stakeholder": "Trần Thị Kiều Trang",
            "influence": "Execution",
            "interest": "High",
            "quadrant": "Supporter",
            "stance": "Ủng hộ",
            "evidence": "Confirmed internal core stakeholder; UX, frontend, and stakeholder communication ownership.",
        },
        {
            "stakeholder": "Nguyễn Quý Dũng",
            "influence": "Execution",
            "interest": "High",
            "quadrant": "Supporter",
            "stance": "Ủng hộ",
            "evidence": "Confirmed internal core stakeholder; AI, data, and backend ownership.",
        },
    ]

    raci = [
        {
            "task": "Chốt use case, MVP scope và acceptance criteria",
            "Huy": "A/R",
            "Trang": "C",
            "Dũng": "C",
            "Stakeholder": "Thủ trưởng: I",
        },
        {
            "task": "Multi-tenant data model, access control và consent flow",
            "Huy": "C",
            "Trang": "I",
            "Dũng": "A/R",
            "Stakeholder": "Phòng Phần mềm: C",
        },
        {
            "task": "AI Data Cleaning + deterministic execution workflow",
            "Huy": "C",
            "Trang": "I",
            "Dũng": "A/R",
            "Stakeholder": "Phòng AI: C",
        },
        {
            "task": "Entity Matching: mapping, blocking, scoring, review",
            "Huy": "C",
            "Trang": "I",
            "Dũng": "A/R",
            "Stakeholder": "Phòng AI: C",
        },
        {
            "task": "Frontend workflow: upload, review, approval, masking",
            "Huy": "C",
            "Trang": "A/R",
            "Dũng": "C",
            "Stakeholder": "Phòng Phần mềm: C",
        },
        {
            "task": "Integration, QA, demo/release readiness",
            "Huy": "A",
            "Trang": "R",
            "Dũng": "R",
            "Stakeholder": "Phòng AI: C; Phòng Phần mềm: C; Thủ trưởng: I",
        },
    ]

    scores = {
        "Huy": {"AI Quality": 4, "Progress": 4, "Team Morale": 4, "Shipping Speed": 3},
        "Trang": {"AI Quality": 4, "Progress": 4, "Team Morale": 5, "Shipping Speed": 3},
        "Dũng": {"AI Quality": 4, "Progress": 3, "Team Morale": 4, "Shipping Speed": 3},
    }
    health_summary = summarize_health(scores)
    dimensions = tuple(health_summary["averages"])
    health_rows = [
        [dimension, scores["Huy"][dimension], scores["Trang"][dimension], scores["Dũng"][dimension], f"Average {health_summary['averages'][dimension]:.2f}/5"]
        for dimension in dimensions
    ]
    priority = (
        f"Priority for next milestone: {health_summary['lowest_dimension']} is lowest "
        f"(average {health_summary['averages'][health_summary['lowest_dimension']]:.2f}/5). "
        "Freeze MVP scope and run the end-to-end demo checklist to protect release readiness; "
        "the AI evaluation baseline remains the enabling quality action."
    )

    return {
        "project": "DataUnifi",
        "team": "Team 42",
        "members": [
            {"name": "Nguyễn Quang Huy", "short": "Huy", "id": "2A202601873"},
            {"name": "Trần Thị Kiều Trang", "short": "Trang", "id": "2A202601498"},
            {"name": "Nguyễn Quý Dũng", "short": "Dũng", "id": "2A202601200"},
        ],
        "status": "PASS - TEAM CONFIRMED & VERIFIED",
        "stakeholders": stakeholders,
        "raci": raci,
        "pages": [
            {"title": "Stakeholder Map & Strategy", "kicker": "GATE 1 / CONFIRMED"},
            {"title": "Pitch & RACI", "kicker": "GATE 2 / CONCLUSION FIRST"},
            {"title": "AI Team Design", "kicker": "GATE 3 / EMBEDDED"},
            {"title": "Team Health & Growth Plan", "kicker": "GATE 4 / CONFIRMED"},
        ],
        "matrix": {
            "note": "Quadrant and stance are separate fields; all classifications were confirmed by the team.",
            "leverage": [
                "Thủ trưởng: align MVP scope, risk controls, and approval to proceed.",
                "Phòng AI: review cleaning/matching quality and evaluation criteria.",
            ],
            "persuade": [
                "Trợ lý Thủ trưởng: address benefit, data, scope, and accountability concerns.",
                "Phòng Phần mềm: de-risk API boundaries, tenant isolation, and deployment assumptions.",
            ],
            "actions": [
                "Send a one-page MVP scope and architecture/risk-control summary to Thủ trưởng.",
                "Run a short technical review with Phòng AI before the demo milestone.",
                "Present the controlled demo flow to Trợ lý Thủ trưởng and capture concerns.",
                "Share the API/architecture flow with Phòng Phần mềm before architecture freeze.",
            ],
        },
        "pitch": {
            "audience": "Thủ trưởng",
            "conclusion": "Team 42 đề xuất tiếp tục DataUnifi tới một MVP/demo nội bộ có kiểm soát, tập trung chứng minh AI Data Cleaning và Entity Matching trước khi cân nhắc mở rộng.",
            "reasons": [
                "DataUnifi xử lý vấn đề dữ liệu khách hàng phân mảnh và không nhất quán giữa nhiều nguồn.",
                "Human approval, deterministic execution, dry-run/rollback, consent, masking, and audit log reduce operational risk.",
                "MVP giới hạn cho phép đánh giá tính khả thi và chất lượng trước khi mở rộng.",
            ],
            "evidence": "Evidence: PROJECT_SUMMARY.md documents multi-tenant isolation, CSV ingestion, AI cleaning suggestions, deterministic execution, matching, consent, masking, and audit logging. This is documented design evidence; no production validation or business metrics are claimed.",
            "ask": "Small ask: approve the controlled MVP/demo scope and acceptance criteria for the next milestone.",
            "objection": "AI chưa đủ đáng tin để cho phép xử lý hoặc liên kết dữ liệu quan trọng.",
            "response": "DataUnifi chỉ dùng AI để đề xuất cleaning, mapping, and weighting. Người dùng review; thay đổi được dry-run; approved rules chạy bằng deterministic engine; uncertain matches vào vùng review; cross-tenant data dùng consent, masking, and audit.",
            "max_page_fraction": 0.5,
            "plain_text": "Team 42 đề xuất tiếp tục DataUnifi tới một MVP/demo nội bộ có kiểm soát, tập trung chứng minh AI Data Cleaning và Entity Matching trước khi cân nhắc mở rộng. DataUnifi xử lý vấn đề dữ liệu khách hàng phân mảnh và không nhất quán giữa nhiều nguồn. Human approval, deterministic execution, dry-run/rollback, consent, masking, and audit log reduce operational risk. MVP giới hạn cho phép đánh giá tính khả thi và chất lượng trước khi mở rộng. Evidence: PROJECT_SUMMARY.md documents the project design and risk controls; no production validation or business metrics are claimed. Small ask: approve the controlled MVP/demo scope and acceptance criteria for the next milestone.",
        },
        "team_design": {
            "architecture": "Embedded",
            "rationale": "Team hiện có 3 core members và năng lực AI/Data gắn trực tiếp vào DataUnifi. Embedded giúp product, frontend/integration và AI/backend làm việc trong cùng squad thay vì tạo một AI hub riêng không phù hợp quy mô hiện tại.",
            "core": [
                "Nguyễn Quang Huy — Product / Integration / Release ownership",
                "Trần Thị Kiều Trang — UX / Frontend / Stakeholder communication",
                "Nguyễn Quý Dũng — AI / Data / Backend",
                "Shared — Evaluation / QA",
            ],
            "extended": [
                "Security / Privacy review — before real-data pilot",
                "MLOps / observability — when release scale requires it",
                "Domain/data governance expert — when pilot scope requires it",
            ],
            "gaps": [
                {
                    "gap": "AI evaluation baseline",
                    "route": "Partner + build internally",
                    "partner": "Phòng AI",
                    "why": "Team cần tiêu chí chất lượng khách quan cho cleaning suggestions và entity matching.",
                    "when": "Trước milestone demo/pilot-readiness.",
                },
                {
                    "gap": "Integration / deployment review",
                    "route": "Partner",
                    "partner": "Phòng Phần mềm",
                    "why": "Cần review API boundaries, deployment assumptions, access controls, and maintainability.",
                    "when": "Trước khi freeze MVP architecture.",
                },
                {
                    "gap": "Security / privacy governance at pilot stage",
                    "route": "Partner",
                    "partner": "Đơn vị/reviewer security/privacy được tổ chức chỉ định",
                    "why": "Multi-tenant customer data và cross-tenant matching cần review privacy/security trước real-data pilot.",
                    "when": "Trước real-data pilot.",
                },
            ],
            "squad_goal": "Team 42 sở hữu MVP DataUnifi và chịu trách nhiệm đưa workflow AI Data Cleaning + Entity Matching từ thiết kế hiện tại đến một demo end-to-end có human approval, tenant isolation, consent, masking, auditability và acceptance criteria rõ ràng.",
        },
        "health": {
            "scores": scores,
            "rows": health_rows,
            "summary": health_summary,
            "priority": priority,
            "competency": "Role: AI / Data / Backend | Owner: Nguyễn Quý Dũng | Current/nearest level: L2 — AI Practitioner | Next competency: AI evaluation / quality evaluation | 30-day practice: build golden cases for cleaning + matching and run regression evaluation before each milestone/release candidate.",
            "growth": [
                {"problem": "AI quality needs a repeatable acceptance baseline.", "action": "Build a golden test set and evaluation checklist for cleaning + matching.", "owner": "Nguyễn Quý Dũng", "deadline": "14 days after confirmation (2026-09-12)", "completion_signal": "Golden cases are stored in project artefacts and a reproducible evaluation report is linked to a release candidate."},
                {"problem": "The project design needs a demonstrable vertical slice.", "action": "Freeze MVP scope and complete an end-to-end demo script from CSV upload through cleaning, review, matching, masked result, and audit flow.", "owner": "Nguyễn Quang Huy", "deadline": "21 days after confirmation (2026-09-19)", "completion_signal": "The demo checklist runs end-to-end against the confirmed acceptance criteria."},
                {"problem": "Stakeholder interest must become actionable feedback.", "action": "Prepare a review package and hold a checkpoint with priority stakeholders, recording issues, decisions, and next actions.", "owner": "Trần Thị Kiều Trang", "deadline": "30 days after confirmation (2026-09-28)", "completion_signal": "A review note contains feedback, decisions, and the next action."},
            ],
        },
        "confirmation_gate": {
            "title": "TEAM CONFIRMED",
            "body": "All required Day 27 team inputs were confirmed by team/user on 2026-08-29: goal, stakeholder classification, six-task RACI, Embedded architecture, individual evidence artefacts, twelve health scores, L2 competency, and three growth commitments.",
        },
    }


def validate_raci(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    allowed_columns = {"task", "Huy", "Trang", "Dũng", "Stakeholder"}
    for row in rows:
        task = str(row.get("task", "Unnamed task"))
        for column in row:
            if column not in allowed_columns:
                errors.append(f"{task}: unrecognized RACI column '{column}'")
        codes = {
            member: {code.strip() for code in str(row.get(member, "")).split("/")}
            for member in ("Huy", "Trang", "Dũng")
        }
        accountable = sum("A" in codes[member] for member in codes)
        responsible = any("R" in codes[member] for member in codes)
        if accountable != 1:
            errors.append(f"{task}: expected exactly one A, found {accountable}")
        if not responsible:
            errors.append(f"{task}: expected at least one R")
    return errors


def register_fonts() -> tuple[str, str]:
    global REGULAR_FONT, BOLD_FONT
    candidates = [
        (Path(r"C:\Windows\Fonts\arial.ttf"), Path(r"C:\Windows\Fonts\arialbd.ttf"), "Arial"),
        (Path(r"C:\Windows\Fonts\segoeui.ttf"), Path(r"C:\Windows\Fonts\segoeuib.ttf"), "SegoeUI"),
    ]
    for regular_path, bold_path, family in candidates:
        if regular_path.exists() and bold_path.exists():
            pdfmetrics.registerFont(TTFont(f"{family}-Regular", str(regular_path)))
            pdfmetrics.registerFont(TTFont(f"{family}-Bold", str(bold_path)))
            REGULAR_FONT = f"{family}-Regular"
            BOLD_FONT = f"{family}-Bold"
            print(f"FONT_REGULAR={REGULAR_FONT}")
            print(f"FONT_BOLD={BOLD_FONT}")
            return REGULAR_FONT, BOLD_FONT
    print("FONT_REGULAR=Helvetica")
    print("FONT_BOLD=Helvetica-Bold")
    return REGULAR_FONT, BOLD_FONT


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "body": ParagraphStyle("body", fontName=REGULAR_FONT, fontSize=7.5, leading=9.2, textColor=INK, alignment=TA_LEFT),
        "body_white": ParagraphStyle("body_white", fontName=REGULAR_FONT, fontSize=7.5, leading=9.2, textColor=WHITE, alignment=TA_LEFT),
        "small": ParagraphStyle("small", fontName=REGULAR_FONT, fontSize=7.2, leading=8.6, textColor=INK, alignment=TA_LEFT),
        "small_muted": ParagraphStyle("small_muted", fontName=REGULAR_FONT, fontSize=7.2, leading=8.5, textColor=MUTED, alignment=TA_LEFT),
        "tiny": ParagraphStyle("tiny", fontName=REGULAR_FONT, fontSize=6.7, leading=7.9, textColor=INK, alignment=TA_LEFT),
        "label": ParagraphStyle("label", fontName=BOLD_FONT, fontSize=6.8, leading=8, textColor=TEAL, alignment=TA_LEFT),
        "label_white": ParagraphStyle("label_white", fontName=BOLD_FONT, fontSize=6.8, leading=8, textColor=WHITE, alignment=TA_LEFT),
        "table_header": ParagraphStyle("table_header", fontName=BOLD_FONT, fontSize=7.1, leading=8.2, textColor=WHITE, alignment=TA_LEFT),
        "table_cell": ParagraphStyle("table_cell", fontName=REGULAR_FONT, fontSize=7.2, leading=8.5, textColor=INK, alignment=TA_LEFT),
        "table_cell_center": ParagraphStyle("table_cell_center", fontName=REGULAR_FONT, fontSize=7.2, leading=8.5, textColor=INK, alignment=TA_CENTER),
        "card_title": ParagraphStyle("card_title", fontName=BOLD_FONT, fontSize=9, leading=10.6, textColor=NAVY, alignment=TA_LEFT),
        "card_title_white": ParagraphStyle("card_title_white", fontName=BOLD_FONT, fontSize=9, leading=10.6, textColor=WHITE, alignment=TA_LEFT),
        "gate": ParagraphStyle("gate", fontName=REGULAR_FONT, fontSize=7.0, leading=8.1, textColor=INK, alignment=TA_LEFT),
    }


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    safe = html.escape(str(text)).replace("\n", "<br/>")
    return Paragraph(safe, style)


def draw_paragraph(canvas: Canvas, text: str, x: float, top: float, width: float, height: float, style: ParagraphStyle) -> float:
    paragraph = _p(text, style)
    _, paragraph_height = paragraph.wrap(width, height)
    paragraph.drawOn(canvas, x, top - paragraph_height)
    return paragraph_height


def draw_card(canvas: Canvas, x: float, top: float, width: float, height: float, title: str, body: str, styles: dict[str, ParagraphStyle], fill=PAPER, accent=TEAL, body_style="body", title_style="card_title") -> None:
    canvas.setFillColor(fill)
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.7)
    canvas.roundRect(x, top - height, width, height, 5, fill=1, stroke=1)
    canvas.setFillColor(accent)
    canvas.roundRect(x, top - 4, width, 4, 5, fill=1, stroke=0)
    draw_paragraph(canvas, title, x + 10, top - 12, width - 20, 18, styles[title_style])
    draw_paragraph(canvas, body, x + 10, top - 34, width - 20, height - 42, styles[body_style])


def draw_bullets(canvas: Canvas, items: list[str], x: float, top: float, width: float, styles: dict[str, ParagraphStyle], gap: float = 5) -> float:
    current = top
    for item in items:
        canvas.setFillColor(TEAL)
        canvas.circle(x + 2.5, current - 4, 2.2, fill=1, stroke=0)
        used = draw_paragraph(canvas, item, x + 10, current, width - 10, 70, styles["body"])
        current -= used + gap
    return top - current


def draw_table(canvas: Canvas, data: list[list[Any]], x: float, top: float, col_widths: list[float], styles: dict[str, ParagraphStyle], header=True, font_style="table_cell") -> float:
    rendered: list[list[Any]] = []
    for row_index, row in enumerate(data):
        rendered_row = []
        for value in row:
            if row_index == 0 and header:
                rendered_row.append(_p(str(value), styles["table_header"]))
            else:
                style = styles["table_cell_center"] if isinstance(value, str) and value in {"A", "R", "C", "I", "A/R"} else styles[font_style]
                rendered_row.append(_p(str(value), style))
        rendered.append(rendered_row)
    table = Table(rendered, colWidths=col_widths, repeatRows=1 if header else 0, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY) if header else ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [WHITE, PAPER]),
    ]))
    _, table_height = table.wrapOn(canvas, sum(col_widths), PAGE_H)
    table.drawOn(canvas, x, top - table_height)
    return table_height


def draw_page_frame(canvas: Canvas, content: dict[str, Any], page_no: int, styles: dict[str, ParagraphStyle]) -> float:
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 68, PAGE_W, 68, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 68, 7, 68, fill=1, stroke=0)
    page = content["pages"][page_no - 1]
    draw_paragraph(canvas, page["kicker"], MARGIN + 8, PAGE_H - 15, 300, 12, styles["label_white"])
    draw_paragraph(canvas, page["title"], MARGIN + 8, PAGE_H - 29, 560, 27, ParagraphStyle("page_title", fontName=BOLD_FONT, fontSize=20, leading=22, textColor=WHITE, alignment=TA_LEFT))
    draw_paragraph(canvas, "DATAUNIFI / TEAM 42", PAGE_W - MARGIN - 150, PAGE_H - 23, 142, 15, ParagraphStyle("top_right", fontName=BOLD_FONT, fontSize=8, leading=9, textColor=TEAL_LIGHT, alignment=TA_CENTER))
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 29, PAGE_W - MARGIN, 29)
    draw_paragraph(canvas, "DataUnifi | Team 42", MARGIN, 20, 140, 10, styles["small_muted"])
    draw_paragraph(canvas, content["status"], PAGE_W / 2 - 125, 20, 250, 10, ParagraphStyle("footer_status", fontName=BOLD_FONT, fontSize=6.7, leading=8, textColor=TEAL, alignment=TA_CENTER))
    draw_paragraph(canvas, f"{page_no} / 4", PAGE_W - MARGIN - 42, 20, 42, 10, ParagraphStyle("footer_page", fontName=BOLD_FONT, fontSize=7, leading=8, textColor=MUTED, alignment=TA_RIGHT))
    return PAGE_H - 88


def draw_matrix(canvas: Canvas, x: float, top: float, width: float, height: float, styles: dict[str, ParagraphStyle]) -> None:
    draw_paragraph(canvas, "Influence x Interest matrix", x, top, width, 15, styles["card_title"])
    mx, mw, mh = x + 22, width - 40, height - 45
    my = top - 30 - mh
    canvas.setFillColor(TEAL_LIGHT)
    canvas.rect(mx, my, mw / 2, mh / 2, fill=1, stroke=0)
    canvas.setFillColor(CORAL_LIGHT)
    canvas.rect(mx + mw / 2, my, mw / 2, mh / 2, fill=1, stroke=0)
    canvas.setFillColor(BLUE_LIGHT)
    canvas.rect(mx, my + mh / 2, mw / 2, mh / 2, fill=1, stroke=0)
    canvas.setFillColor(GOLD_LIGHT)
    canvas.rect(mx + mw / 2, my + mh / 2, mw / 2, mh / 2, fill=1, stroke=0)
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(0.8)
    canvas.rect(mx, my, mw, mh, fill=0, stroke=1)
    canvas.line(mx + mw / 2, my, mx + mw / 2, my + mh)
    canvas.line(mx, my + mh / 2, mx + mw, my + mh / 2)
    labels = [
        ("Supporter", mx + 6, my + mh - 14, TEAL),
        ("Champion", mx + mw / 2 + 6, my + mh - 14, GOLD),
        ("Bystander", mx + 6, my + 8, MUTED),
        ("Blocker", mx + mw / 2 + 6, my + 8, CORAL),
    ]
    for label, lx, ly, color in labels:
        canvas.setFillColor(color)
        canvas.setFont(BOLD_FONT, 7)
        canvas.drawString(lx, ly, label)
    draw_paragraph(canvas, "HIGH", mx - 21, my + mh - 5, 19, 10, styles["tiny"])
    draw_paragraph(canvas, "LOW", mx - 21, my - 1, 19, 10, styles["tiny"])
    draw_paragraph(canvas, "LOW", mx + 2, my - 15, 25, 10, styles["tiny"])
    draw_paragraph(canvas, "HIGH", mx + mw - 28, my - 15, 28, 10, styles["tiny"])
    draw_paragraph(canvas, "Influence", x + width / 2 - 28, top - height + 2, 56, 10, styles["tiny"])
    canvas.saveState()
    canvas.translate(x + 3, my + mh / 2 - 18)
    canvas.rotate(90)
    draw_paragraph(canvas, "Interest", 0, 0, 38, 10, styles["tiny"])
    canvas.restoreState()


def draw_badge(canvas: Canvas, label: str, x: float, y: float, fill: colors.Color) -> float:
    text_width = pdfmetrics.stringWidth(label, BOLD_FONT, 6.8)
    width = text_width + 14
    canvas.setFillColor(fill)
    canvas.roundRect(x, y, width, 14, 7, fill=1, stroke=0)
    canvas.setFillColor(NAVY if fill != CORAL else WHITE)
    canvas.setFont(BOLD_FONT, 6.8)
    canvas.drawCentredString(x + width / 2, y + 4.2, label)
    return width


def draw_page_1(canvas: Canvas, content: dict[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    top = draw_page_frame(canvas, content, 1, styles)
    draw_matrix(canvas, MARGIN, top, 218, 151, styles)
    x_table = MARGIN + 230
    stakeholder_data = [["Stakeholder", "Influence", "Interest", "Quadrant", "Stance", "Evidence / reason"]]
    for row in content["stakeholders"]:
        stakeholder_data.append([row[key] for key in ("stakeholder", "influence", "interest", "quadrant", "stance", "evidence")])
    table_height = draw_table(canvas, stakeholder_data, x_table, top, [116, 55, 55, 66, 61, CONTENT_W - 230 - 353], styles, font_style="tiny")
    canvas.setFillColor(MUTED)
    canvas.setFont(REGULAR_FONT, 6.9)
    canvas.drawString(MARGIN + 4, top - 165, content["matrix"]["note"])
    badge_x = MARGIN + 4
    for label, fill in [("Champion", GOLD_LIGHT), ("Blocker", CORAL_LIGHT), ("Supporter", TEAL_LIGHT), ("Bystander", BLUE_LIGHT)]:
        badge_x += draw_badge(canvas, label, badge_x, top - 189, fill) + 5
    cards_top = top - max(205, table_height + 22)
    card_gap = 9
    card_w = (CONTENT_W - card_gap) / 2
    leverage = "\n".join(content["matrix"]["leverage"])
    persuade = "\n".join(content["matrix"]["persuade"])
    draw_card(canvas, MARGIN, cards_top, card_w, 56, "Leverage: 2 priority stakeholders", leverage, styles, fill=TEAL_LIGHT, accent=TEAL, body_style="tiny")
    draw_card(canvas, MARGIN + card_w + card_gap, cards_top, card_w, 56, "Persuade / de-risk: 2 priority stakeholders", persuade, styles, fill=CORAL_LIGHT, accent=CORAL, body_style="tiny")
    action_top = cards_top - 67
    canvas.setFillColor(NAVY)
    canvas.roundRect(MARGIN, action_top - 83, CONTENT_W, 83, 5, fill=1, stroke=0)
    draw_paragraph(canvas, "Concrete actions for the next 1-2 weeks", MARGIN + 10, action_top - 12, 300, 13, styles["card_title_white"])
    action_y = action_top - 30
    action_w = (CONTENT_W - 35) / 4
    for index, action in enumerate(content["matrix"]["actions"], start=1):
        ax = MARGIN + 10 + (index - 1) * (action_w + 5)
        canvas.setFillColor(TEAL_LIGHT if index % 2 else BLUE_LIGHT)
        canvas.circle(ax + 7, action_y - 4, 7, fill=1, stroke=0)
        canvas.setFillColor(NAVY)
        canvas.setFont(BOLD_FONT, 7)
        canvas.drawCentredString(ax + 7, action_y - 6.5, str(index))
        draw_paragraph(canvas, action, ax + 19, action_y, action_w - 19, 47, styles["body_white"])


def draw_page_2(canvas: Canvas, content: dict[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    top = draw_page_frame(canvas, content, 2, styles)
    gap = 10
    left_w = 392
    right_w = CONTENT_W - left_w - gap
    pitch = content["pitch"]
    draw_card(canvas, MARGIN, top, left_w, 230, "CONCLUSION FIRST", pitch["conclusion"], styles, fill=WHITE, accent=TEAL, body_style="body")
    draw_paragraph(canvas, "Audience: " + pitch["audience"], MARGIN + 10, top - 61, left_w - 20, 16, styles["label"])
    draw_paragraph(canvas, "2-3 REASONS", MARGIN + 10, top - 86, left_w - 20, 13, styles["label"])
    draw_bullets(canvas, pitch["reasons"], MARGIN + 10, top - 100, left_w - 20, styles, gap=3)
    draw_paragraph(canvas, "EVIDENCE", MARGIN + 10, top - 153, left_w - 20, 13, styles["label"])
    draw_paragraph(canvas, pitch["evidence"], MARGIN + 10, top - 167, left_w - 20, 32, styles["tiny"])
    draw_paragraph(canvas, "SMALL ASK", MARGIN + 10, top - 194, left_w - 20, 13, styles["label"])
    draw_paragraph(canvas, pitch["ask"], MARGIN + 10, top - 206, left_w - 20, 36, styles["tiny"])
    rx = MARGIN + left_w + gap
    draw_card(canvas, rx, top, right_w, 230, "OBJECTION + RESPONSE", pitch["objection"], styles, fill=CORAL_LIGHT, accent=CORAL, body_style="body")
    draw_paragraph(canvas, pitch["response"], rx + 10, top - 66, right_w - 20, 75, styles["body"])
    draw_card(canvas, rx + 10, top - 142, right_w - 20, 68, "Risk-reduction logic", "Controlled scope, named acceptance criteria, documented result, then a deliberate go / revise decision.", styles, fill=WHITE, accent=GOLD, body_style="tiny")
    raci_top = top - 250
    draw_paragraph(canvas, "RACI - one A and at least one R per task", MARGIN, raci_top, CONTENT_W, 17, styles["card_title"])
    raci_data = [["Task", "Huy", "Trang", "Dũng", "Stakeholder"]]
    raci_data.extend([[row[key] for key in ("task", "Huy", "Trang", "Dũng", "Stakeholder")] for row in content["raci"]])
    draw_table(canvas, raci_data, MARGIN, raci_top - 20, [300, 43, 48, 45, CONTENT_W - 436], styles)
    canvas.setFillColor(MUTED)
    canvas.setFont(REGULAR_FONT, 6.8)
    canvas.drawString(MARGIN, 45, "R = Responsible | A = Accountable | C = Consulted | I = Informed")


def draw_page_3(canvas: Canvas, content: dict[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    top = draw_page_frame(canvas, content, 3, styles)
    design = content["team_design"]
    gap = 10
    arch_w = 265
    draw_card(canvas, MARGIN, top, arch_w, 111, "ARCHITECTURE", design["architecture"], styles, fill=TEAL_LIGHT, accent=TEAL, body_style="card_title")
    draw_paragraph(canvas, design["rationale"], MARGIN + 10, top - 57, arch_w - 20, 48, styles["small"])
    role_x = MARGIN + arch_w + gap
    role_w = CONTENT_W - arch_w - gap
    draw_card(canvas, role_x, top, role_w, 111, "CORE ROLES - needed now", "\n".join("- " + item for item in design["core"]), styles, fill=WHITE, accent=TEAL, body_style="small")
    roles_top = top - 121
    draw_card(canvas, role_x, roles_top, role_w, 86, "EXTENDED ROLES - when scaling", "\n".join("- " + item for item in design["extended"]), styles, fill=LAVENDER, accent=GOLD, body_style="small")
    gap_top = roles_top - 96
    draw_paragraph(canvas, "CAPABILITY GAPS + PRIORITY RESOURCING", MARGIN, gap_top, CONTENT_W, 16, styles["card_title"])
    gap_data = [["Capability gap", "Route", "Partner", "Why", "When needed"]]
    gap_data.extend([[row["gap"], row["route"], row["partner"], row["why"], row["when"]] for row in design["gaps"]])
    draw_table(canvas, gap_data, MARGIN, gap_top - 19, [155, 110, 150, 230, CONTENT_W - 645], styles, font_style="tiny")
    squad_top = gap_top - 112
    draw_card(canvas, MARGIN, squad_top, CONTENT_W, 82, "SQUAD GOAL", design["squad_goal"], styles, fill=NAVY, accent=TEAL, body_style="body_white", title_style="card_title_white")


def draw_page_4(canvas: Canvas, content: dict[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    top = draw_page_frame(canvas, content, 4, styles)
    health = content["health"]
    health_data = [["Dimension", "Huy", "Trang", "Dũng", "Team Summary"]] + health["rows"]
    health_height = draw_table(canvas, health_data, MARGIN, top, [150, 100, 100, 100, CONTENT_W - 450], styles)
    priority_top = top - health_height - 12
    draw_card(canvas, MARGIN, priority_top, 365, 78, "PRIORITY ISSUE", health["priority"], styles, fill=CORAL_LIGHT, accent=CORAL, body_style="small")
    draw_card(canvas, MARGIN + 375, priority_top, CONTENT_W - 375, 78, "COMPETENCY", health["competency"], styles, fill=GOLD_LIGHT, accent=GOLD, body_style="small")
    growth_top = priority_top - 89
    draw_paragraph(canvas, "GROWTH PLAN - 30 DAYS", MARGIN, growth_top, CONTENT_W, 16, styles["card_title"])
    growth_data = [["Problem", "30-day action", "Owner", "Deadline", "Completion signal"]]
    growth_data.extend([[row[key] for key in ("problem", "action", "owner", "deadline", "completion_signal")] for row in health["growth"]])
    growth_height = draw_table(canvas, growth_data, MARGIN, growth_top - 18, [145, 245, 90, 100, CONTENT_W - 580], styles, font_style="tiny")
    gate_top = growth_top - growth_height - 18
    gate_h = 96
    canvas.setFillColor(GOLD_LIGHT)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.roundRect(MARGIN, gate_top - gate_h, CONTENT_W, gate_h, 5, fill=1, stroke=1)
    canvas.setFillColor(GOLD)
    canvas.roundRect(MARGIN, gate_top - 5, CONTENT_W, 5, 5, fill=1, stroke=0)
    draw_paragraph(canvas, "CONFIRMATION RECORD", MARGIN + 10, gate_top - 14, CONTENT_W - 20, 16, styles["card_title"])
    draw_paragraph(canvas, content["confirmation_gate"]["body"], MARGIN + 10, gate_top - 35, CONTENT_W - 20, gate_h - 42, styles["gate"])


def build_pdf(output_path: Path) -> Path:
    content = build_content()
    raci_errors = validate_raci(content["raci"])
    if raci_errors:
        raise ValueError("Invalid RACI: " + "; ".join(raci_errors))
    register_fonts()
    styles = _styles()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    canvas.setTitle("Track 1 Day 27 - AI Team Lab - Team 42 - DataUnifi")
    canvas.setAuthor("Team 42")
    draw_page_1(canvas, content, styles)
    canvas.showPage()
    draw_page_2(canvas, content, styles)
    canvas.showPage()
    draw_page_3(canvas, content, styles)
    canvas.showPage()
    draw_page_4(canvas, content, styles)
    canvas.showPage()
    canvas.save()
    return output_path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "Day27_AI-Team-Lab_Team42.pdf"
    build_pdf(output)
    print(f"PDF_OUTPUT={output}")


if __name__ == "__main__":
    main()
