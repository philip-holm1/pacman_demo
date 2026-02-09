"""Spec/Plan Consistency Check (T091)

Usage:
  python scripts/check_spec_plan_consistency.py

Purpose:
  Lightweight verifier that the feature specification (`spec.md`) and
  implementation plan (`plan.md`) both contain expected anchor sections
  and that key functional requirement identifiers (FR-###) and success
  criteria (SC-###) appear in each where appropriate.

Behavior:
  - Parses spec and plan files as plain text.
  - Extracts identifiers matching FR-### and SC-### from spec.
  - Ensures all FR ids appear at least once in plan (for traceability).
  - Checks presence of required section headers: Summary, Technical Context,
    Project Structure, Phase Breakdown in plan; Functional Requirements,
    Success Criteria in spec.
  - Emits a report and exits with code 0 if all checks pass; else non‑zero.

Exit Codes:
  0: All consistency checks passed.
  1: Missing sections.
  2: Missing FR ids in plan.
  3: Missing SC ids in plan (optional warning promoted to failure).

Designed to be simple and dependency‑free; extend as needed for richer tracing.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

SPEC_PATH = Path("specs/001-modern-powerups-pacman/spec.md")
PLAN_PATH = Path("specs/001-modern-powerups-pacman/plan.md")

PLAN_REQUIRED_SECTIONS = [
    "Summary",
    "Technical Context",
    "Project Structure",
    "Phase Breakdown",
    "Implementation Tasks",  # from plan extended description
]

SPEC_REQUIRED_SECTIONS = [
    "Functional Requirements",
    "Success Criteria",
]

FR_PATTERN = re.compile(r"\bFR-(\d{3})\b")
SC_PATTERN = re.compile(r"\bSC-(\d{3})\b")


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:  # pragma: no cover - defensive
        print(f"ERROR: Unable to read {path}: {e}")
        sys.exit(1)


def extract_ids(text: str, pattern: re.Pattern) -> list[str]:
    return sorted(set(pattern.findall(text)))


def has_section(text: str, section_name: str) -> bool:
    # Accept variations like '## Summary' or '### Summary'
    return re.search(rf"^#+\s*{re.escape(section_name)}\b", text, re.MULTILINE) is not None


def main() -> int:
    spec_text = read(SPEC_PATH)
    plan_text = read(PLAN_PATH)

    missing_spec_sections = [s for s in SPEC_REQUIRED_SECTIONS if not has_section(spec_text, s)]
    missing_plan_sections = [s for s in PLAN_REQUIRED_SECTIONS if not has_section(plan_text, s)]

    spec_fr = extract_ids(spec_text, FR_PATTERN)
    spec_sc = extract_ids(spec_text, SC_PATTERN)

    plan_fr_present = [fr for fr in spec_fr if re.search(rf"\bFR-{fr}\b", plan_text)]
    plan_fr_missing = [fr for fr in spec_fr if fr not in plan_fr_present]

    plan_sc_present = [sc for sc in spec_sc if re.search(rf"\bSC-{sc}\b", plan_text)]
    plan_sc_missing = [sc for sc in spec_sc if sc not in plan_sc_present]

    status_lines = []
    code = 0

    if missing_spec_sections or missing_plan_sections:
        code = 1
        if missing_spec_sections:
            status_lines.append(f"Missing spec sections: {', '.join(missing_spec_sections)}")
        if missing_plan_sections:
            status_lines.append(f"Missing plan sections: {', '.join(missing_plan_sections)}")

    if plan_fr_missing:
        # Functional requirements absent in plan constitutes failure
        code = max(code, 2)
        status_lines.append("FR IDs missing in plan: " + ", ".join(f"FR-{m}" for m in plan_fr_missing))

    if plan_sc_missing:
        # Promote to failure for visibility
        code = max(code, 3)
        status_lines.append("SC IDs missing in plan: " + ", ".join(f"SC-{m}" for m in plan_sc_missing))

    if code == 0:
        status_lines.append("Consistency PASS: all required sections and IDs present.")

    print("Spec/Plan Consistency Report")
    print("=============================")
    print(f"Spec FR count: {len(spec_fr)} | Plan FR present: {len(plan_fr_present)}")
    print(f"Spec SC count: {len(spec_sc)} | Plan SC present: {len(plan_sc_present)}")
    for line in status_lines:
        print(line)

    return code


if __name__ == "__main__":
    sys.exit(main())
