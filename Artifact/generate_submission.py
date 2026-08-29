from __future__ import annotations

import html
import sys
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


def build_content() -> dict[str, Any]:
    stakeholders = [
        {
            "stakeholder": "Proposed sponsor / decision maker",
            "influence": "NEEDS TEAM INPUT",
            "interest": "NEEDS TEAM INPUT",
            "quadrant": "NEEDS TEAM INPUT",
            "stance": "NEEDS TEAM INPUT",
            "evidence": "Exact identity and relationship are not recorded.",
        },
        {
            "stakeholder": "Proposed intended-user representative",
            "influence": "NEEDS TEAM INPUT",
            "interest": "NEEDS TEAM INPUT",
            "quadrant": "NEEDS TEAM INPUT",
            "stance": "NEEDS TEAM INPUT",
            "evidence": "Use case and user evidence are not recorded.",
        },
        {
            "stakeholder": "Proposed data owner / provider",
            "influence": "NEEDS TEAM INPUT",
            "interest": "NEEDS TEAM INPUT",
            "quadrant": "NEEDS TEAM INPUT",
            "stance": "NEEDS TEAM INPUT",
            "evidence": "Dataset ownership and access evidence are not recorded.",
        },
        {
            "stakeholder": "Proposed engineering / integration owner",
            "influence": "NEEDS TEAM INPUT",
            "interest": "NEEDS TEAM INPUT",
            "quadrant": "NEEDS TEAM INPUT",
            "stance": "NEEDS TEAM INPUT",
            "evidence": "Integration context is not recorded.",
        },
        {
            "stakeholder": "Proposed AI quality reviewer",
            "influence": "NEEDS TEAM INPUT",
            "interest": "NEEDS TEAM INPUT",
            "quadrant": "NEEDS TEAM INPUT",
            "stance": "NEEDS TEAM INPUT",
            "evidence": "Evaluation owner and evidence are not recorded.",
        },
        {
            "stakeholder": "Proposed privacy / security reviewer",
            "influence": "NEEDS TEAM INPUT",
            "interest": "NEEDS TEAM INPUT",
            "quadrant": "NEEDS TEAM INPUT",
            "stance": "NEEDS TEAM INPUT",
            "evidence": "Risk owner and review evidence are not recorded.",
        },
    ]

    raci = [
        {
            "task": "Confirm use case and success criteria",
            "Huy": "A",
            "Trang": "C",
            "Dung": "R",
            "Stakeholder": "NEEDS TEAM INPUT",
        },
        {
            "task": "Prepare source data and schema",
            "Huy": "R",
            "Trang": "I",
            "Dung": "A",
            "Stakeholder": "NEEDS TEAM INPUT",
        },
        {
            "task": "Build AI and data pipeline prototype",
            "Huy": "R",
            "Trang": "C",
            "Dung": "A",
            "Stakeholder": "NEEDS TEAM INPUT",
        },
        {
            "task": "Define test set and evaluation plan",
            "Huy": "A",
            "Trang": "C",
            "Dung": "R",
            "Stakeholder": "NEEDS TEAM INPUT",
        },
        {
            "task": "Review demo or limited pilot readiness",
            "Huy": "A",
            "Trang": "R",
            "Dung": "C",
            "Stakeholder": "NEEDS TEAM INPUT",
        },
    ]

    return {
        "project": "DataUnifi",
        "team": "Team 42",
        "members": [
            {"name": "Nguyễn Quang Huy", "short": "Huy", "id": "2A202601873"},
            {"name": "Trần Thị Kiều Trang", "short": "Trang", "id": "2A202601498"},
            {"name": "Nguyễn Quý Dũng", "short": "Dung", "id": "2A202601200"},
        ],
        "status": "PARTIAL - TEAM CONFIRMATION REQUIRED",
        "stakeholders": stakeholders,
        "raci": raci,
        "pages": [
            {"title": "Stakeholder Map & Strategy", "kicker": "GATE 1 / PROPOSED INPUT"},
            {"title": "Pitch & RACI", "kicker": "GATE 2 / CONCLUSION FIRST"},
            {"title": "AI Team Design", "kicker": "GATE 3 / PROPOSED DESIGN"},
            {"title": "Team Health & Growth Plan", "kicker": "GATE 4 / INPUT REQUIRED"},
        ],
        "matrix": {
            "note": "Quadrant and stance are separate fields; both need team evidence.",
            "leverage": [
                "Champion candidate: NEEDS TEAM INPUT - identify the strong supporter.",
                "Supporter candidate: NEEDS TEAM INPUT - identify the practical enabler.",
            ],
            "persuade": [
                "Persuasion candidate: NEEDS TEAM INPUT - identify the highest-risk voice.",
                "Risk-reduction candidate: NEEDS TEAM INPUT - identify the approver.",
            ],
            "actions": [
                "Confirm the six stakeholder identities and evidence source.",
                "Classify influence, interest, quadrant, and stance separately.",
                "Send the internal prototype/demo to the selected user representative for feedback.",
                "Record one concrete response or decision before the next checkpoint.",
            ],
        },
        "pitch": {
            "audience": "Priority stakeholder: NEEDS TEAM INPUT",
            "conclusion": "NEEDS TEAM INPUT - confirm the DataUnifi goal before approving a rollout recommendation.",
            "reasons": [
                "No confirmed use case or 1-3 month outcome is recorded.",
                "No validated user or stakeholder evidence is recorded.",
                "A limited evidence-gathering checkpoint reduces decision risk while facts are confirmed.",
            ],
            "evidence": "Repository evidence: project/team identity only. Any current artefact must be described as an internal prototype/demo until the team supplies validation evidence.",
            "ask": "Small ask: confirm the target use case, decision audience, and acceptance criteria for one limited checkpoint.",
            "objection": "\"Chất lượng AI chưa đủ ổn định để triển khai.\"",
            "response": "Proposed response: use a limited internal prototype/pilot with a named acceptance set, review results, and expand only if the agreed criteria are met.",
        },
        "team_design": {
            "architecture": "PROPOSED - HYBRID / NEEDS TEAM INPUT",
            "rationale": "The known team has three members. A hybrid shape can keep ownership close to the project while adding targeted review or domain help; project stage and resource limits still need confirmation.",
            "core": [
                "AI / Product - define outcome and user value",
                "AI Engineering - prototype model and workflow",
                "Data / Backend - prepare data and integration",
                "Eval / MLOps - define checks and release evidence",
            ],
            "extended": [
                "UX - only when user workflow is confirmed",
                "Domain - partner before a domain-sensitive pilot",
                "Governance - add for privacy, risk, or scale review",
            ],
            "gaps": [
                {
                    "gap": "Confirmed use case and domain context",
                    "route": "Partner",
                    "why": "External context is safer to validate than to assume.",
                    "when": "Before a pilot or stakeholder decision.",
                },
                {
                    "gap": "Evaluation baseline and acceptance criteria",
                    "route": "Build internally",
                    "why": "The team needs a repeatable test set for each release.",
                    "when": "Before any rollout recommendation.",
                },
            ],
            "squad_goal": "Team/Squad của chúng tôi sở hữu NEEDS TEAM INPUT - the confirmed DataUnifi use case và chịu trách nhiệm đưa NEEDS TEAM INPUT - prototype outcome từ hiện trạng NEEDS TEAM INPUT đến NEEDS TEAM INPUT - agreed pilot readiness.",
        },
        "health": {
            "rows": [
                ["AI Quality", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT"],
                ["Progress", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT"],
                ["Team Morale", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT"],
                ["Shipping Speed", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT", "NEEDS TEAM INPUT"],
            ],
            "priority": "NEEDS TEAM INPUT - confirm the lowest dimension, largest disagreement, reason, and milestone impact.",
            "competency": "Role: NEEDS TEAM INPUT | Current/nearest level: NEEDS TEAM INPUT | Next competency: evaluation/evals is a proposal pending role confirmation.",
            "growth": [
                ["No agreed evaluation baseline", "Confirm a golden test set and run it before each release", "NEEDS TEAM INPUT", "30 days after confirmation", "Saved eval result linked to a release"],
                ["Current goal is not shared", "Write one measurable 1-3 month goal and acceptance signal", "NEEDS TEAM INPUT", "Within 7 days of confirmation", "Goal appears in JOB.md and README"],
                ["Stakeholder feedback path is unknown", "Run one documented feedback checkpoint with the selected representative", "NEEDS TEAM INPUT", "Within 30 days of confirmation", "Feedback note and decision are recorded"],
            ],
        },
        "confirmation_gate": {
            "title": "TEAM CONFIRMATION REQUIRED",
            "body": "1. DataUnifi current goal: NEEDS TEAM INPUT\n\n2. Proposed RACI: confirm or edit the proposed matrix.\n\n3. Team Health: Huy: NEEDS TEAM INPUT | Trang: NEEDS TEAM INPUT | Dũng: NEEDS TEAM INPUT\n\n4. Competency / Growth commitments: NEEDS TEAM INPUT\n\nReply: YES or edit the lines that need to change.",
        },
    }


def validate_raci(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        accountable = sum(1 for member in ("Huy", "Trang", "Dung") if row.get(member) == "A")
        responsible = any("R" in str(row.get(member, "")) for member in ("Huy", "Trang", "Dung"))
        task = str(row.get("task", "Unnamed task"))
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
        "callout": ParagraphStyle("callout", fontName=REGULAR_FONT, fontSize=7.3, leading=8.8, textColor=INK, alignment=TA_LEFT),
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


def draw_card(canvas: Canvas, x: float, top: float, width: float, height: float, title: str, body: str, styles: dict[str, ParagraphStyle], fill=PAPER, accent=TEAL, body_style="body") -> None:
    canvas.setFillColor(fill)
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.7)
    canvas.roundRect(x, top - height, width, height, 5, fill=1, stroke=1)
    canvas.setFillColor(accent)
    canvas.roundRect(x, top - 4, width, 4, 5, fill=1, stroke=0)
    draw_paragraph(canvas, title, x + 10, top - 12, width - 20, 18, styles["card_title"])
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
    draw_paragraph(canvas, content["status"], PAGE_W / 2 - 125, 20, 250, 10, ParagraphStyle("footer_status", fontName=BOLD_FONT, fontSize=6.7, leading=8, textColor=CORAL, alignment=TA_CENTER))
    draw_paragraph(canvas, f"{page_no} / 4", PAGE_W - MARGIN - 42, 20, 42, 10, ParagraphStyle("footer_page", fontName=BOLD_FONT, fontSize=7, leading=8, textColor=MUTED, alignment=TA_RIGHT))
    return PAGE_H - 88


def draw_matrix(canvas: Canvas, x: float, top: float, width: float, height: float, styles: dict[str, ParagraphStyle]) -> None:
    draw_paragraph(canvas, "Influence x Interest matrix", x, top, width, 15, styles["card_title"])
    mx, my, mw, mh = x + 22, top - 30, width - 40, height - 45
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
    stakeholder_data = [["Stakeholder candidate", "Influence", "Interest", "Quadrant", "Stance", "Evidence / reason"]]
    for row in content["stakeholders"]:
        stakeholder_data.append([row[key] for key in ("stakeholder", "influence", "interest", "quadrant", "stance", "evidence")])
    table_height = draw_table(canvas, stakeholder_data, x_table, top, [116, 55, 55, 66, 61, CONTENT_W - 230 - 353], styles, font_style="tiny")
    canvas.setFillColor(MUTED)
    canvas.setFont(REGULAR_FONT, 6.9)
    canvas.drawString(MARGIN + 4, top - 165, "Quadrant labels and stance are not interchangeable. Every row is unconfirmed.")
    badge_x = MARGIN + 4
    for label, fill in [("Champion", GOLD_LIGHT), ("Blocker", CORAL_LIGHT), ("Supporter", TEAL_LIGHT), ("Bystander", BLUE_LIGHT)]:
        badge_x += draw_badge(canvas, label, badge_x, top - 189, fill) + 5
    cards_top = top - max(205, table_height + 22)
    card_gap = 9
    card_w = (CONTENT_W - card_gap) / 2
    leverage = "\n".join(content["matrix"]["leverage"])
    persuade = "\n".join(content["matrix"]["persuade"])
    draw_card(canvas, MARGIN, cards_top, card_w, 56, "Leverage: 2 strong-support candidates", leverage, styles, fill=TEAL_LIGHT, accent=TEAL, body_style="tiny")
    draw_card(canvas, MARGIN + card_w + card_gap, cards_top, card_w, 56, "Persuade / risk-reduce: 2 candidates", persuade, styles, fill=CORAL_LIGHT, accent=CORAL, body_style="tiny")
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
        draw_paragraph(canvas, action, ax + 19, action_y, action_w - 19, 47, styles["tiny"])


def draw_page_2(canvas: Canvas, content: dict[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    top = draw_page_frame(canvas, content, 2, styles)
    gap = 10
    left_w = 392
    right_w = CONTENT_W - left_w - gap
    pitch = content["pitch"]
    draw_card(canvas, MARGIN, top, left_w, 202, "CONCLUSION", pitch["conclusion"], styles, fill=WHITE, accent=TEAL, body_style="body")
    draw_paragraph(canvas, "Audience: " + pitch["audience"], MARGIN + 10, top - 61, left_w - 20, 16, styles["label"])
    draw_paragraph(canvas, "2-3 REASONS", MARGIN + 10, top - 86, left_w - 20, 13, styles["label"])
    draw_bullets(canvas, pitch["reasons"], MARGIN + 10, top - 100, left_w - 20, styles, gap=3)
    draw_paragraph(canvas, "EVIDENCE", MARGIN + 10, top - 153, left_w - 20, 13, styles["label"])
    draw_paragraph(canvas, pitch["evidence"], MARGIN + 10, top - 167, left_w - 20, 32, styles["tiny"])
    draw_paragraph(canvas, "SMALL ASK", MARGIN + 10, top - 194, left_w - 20, 13, styles["label"])
    draw_paragraph(canvas, pitch["ask"], MARGIN + 10, top - 206, left_w - 20, 36, styles["tiny"])
    rx = MARGIN + left_w + gap
    draw_card(canvas, rx, top, right_w, 202, "OBJECTION + RESPONSE", pitch["objection"], styles, fill=CORAL_LIGHT, accent=CORAL, body_style="body")
    draw_paragraph(canvas, pitch["response"], rx + 10, top - 66, right_w - 20, 75, styles["body"])
    draw_card(canvas, rx + 10, top - 123, right_w - 20, 60, "Risk-reduction logic", "Proposed limited checkpoint: named acceptance criteria, documented result, then a deliberate go / revise decision.", styles, fill=WHITE, accent=GOLD, body_style="tiny")
    raci_top = top - 220
    draw_paragraph(canvas, "PROPOSED RACI - exactly one A per task; team confirmation required", MARGIN, raci_top, CONTENT_W, 17, styles["card_title"])
    raci_data = [["Task", "Huy", "Trang", "Dung", "Stakeholder"]]
    raci_data.extend([[row[key] for key in ("task", "Huy", "Trang", "Dung", "Stakeholder")] for row in content["raci"]])
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
    draw_card(canvas, role_x, roles_top, role_w, 86, "EXTENDED ROLES - only when scale requires", "\n".join("- " + item for item in design["extended"]), styles, fill=LAVENDER, accent=GOLD, body_style="small")
    gap_top = roles_top - 96
    draw_paragraph(canvas, "CAPABILITY GAPS + PRIORITY RESOURCING", MARGIN, gap_top, CONTENT_W, 16, styles["card_title"])
    gap_data = [["Capability gap", "Hire / Outsource / Partner", "Why", "When needed"]]
    gap_data.extend([[row["gap"], row["route"], row["why"], row["when"]] for row in design["gaps"]])
    draw_table(canvas, gap_data, MARGIN, gap_top - 19, [210, 125, 248, CONTENT_W - 583], styles)
    squad_top = gap_top - 103
    draw_card(canvas, MARGIN, squad_top, CONTENT_W, 82, "SQUAD GOAL", design["squad_goal"], styles, fill=NAVY, accent=TEAL, body_style="body_white")
    canvas.setFillColor(TEAL_LIGHT)
    canvas.setFont(BOLD_FONT, 7)
    canvas.drawString(MARGIN + 10, squad_top - 66, "The sentence is a proposal until the team confirms the use case and target state.")


def draw_page_4(canvas: Canvas, content: dict[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    top = draw_page_frame(canvas, content, 4, styles)
    health = content["health"]
    health_data = [["Dimension", "Huy", "Trang", "Dũng", "Team Summary"]] + health["rows"]
    health_height = draw_table(canvas, health_data, MARGIN, top, [150, 100, 100, 100, CONTENT_W - 450], styles)
    priority_top = top - health_height - 12
    draw_card(canvas, MARGIN, priority_top, 365, 78, "PRIORITY ISSUE", health["priority"], styles, fill=CORAL_LIGHT, accent=CORAL, body_style="small")
    draw_card(canvas, MARGIN + 375, priority_top, CONTENT_W - 375, 78, "COMPETENCY", health["competency"], styles, fill=GOLD_LIGHT, accent=GOLD, body_style="small")
    growth_top = priority_top - 89
    draw_paragraph(canvas, "GROWTH PLAN - 30 DAYS / PROPOSED", MARGIN, growth_top, CONTENT_W, 16, styles["card_title"])
    growth_data = [["Problem", "30-day action", "Owner", "Deadline", "Completion signal"]] + health["growth"]
    growth_height = draw_table(canvas, growth_data, MARGIN, growth_top - 18, [145, 255, 80, 93, CONTENT_W - 573], styles, font_style="tiny")
    gate_top = growth_top - growth_height - 12
    gate_h = 124
    canvas.setFillColor(GOLD_LIGHT)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.roundRect(MARGIN, gate_top - gate_h, CONTENT_W, gate_h, 5, fill=1, stroke=1)
    canvas.setFillColor(GOLD)
    canvas.roundRect(MARGIN, gate_top - 5, CONTENT_W, 5, 5, fill=1, stroke=0)
    draw_paragraph(canvas, content["confirmation_gate"]["title"], MARGIN + 10, gate_top - 14, CONTENT_W - 20, 16, styles["card_title"])
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
