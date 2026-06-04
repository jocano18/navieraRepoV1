"""Trim legal clauses and keep the operational B/L section for parsing."""

import re


def trim_boilerplate(text: str) -> str:
    """Keep text before standard terms & conditions blocks."""
    upper = text.upper()
    cut_markers = (
        "TERMS AND CONDITIONS",
        "IT IS AGREED THAT NO RESPONSIBILITY",
        "IT IS AGREED THAT",
        "UNKNOWN CLAUSE",
        "FOR TRANSHIPMENT INFORMATION",
    )
    end = len(text)
    for marker in cut_markers:
        idx = upper.find(marker)
        if idx > 200:
            end = min(end, idx)
    body = text[:end]
    # Drop very long lines typical of legal paragraphs (> 120 chars)
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if len(stripped) > 120 and " " in stripped and stripped.count(" ") > 15:
            continue
        lines.append(line)
    return "\n".join(lines)
