#!/usr/bin/env python3
"""
validate_evidence_matrix.py — Evidence matrix integrity checker for Academic Research OS.

Checks:
  1. All required columns present in evidence_matrix.csv.
  2. No empty claim_id or claim_text.
  3. evidence_type is one of the allowed values.
  4. direction is one of the allowed values.
  5. confidence is one of the allowed values.
  6. claim_ids follow pattern C + digits (e.g. C001).
  7. No duplicate claim_ids.
  8. Every claim_id in the CSV has a corresponding ## CXXX section in claim_registry.md.
  9. Sentences in outputs/draft.md that use unsourced-sounding language lack Evidence comments.
  Exits with code 1 if any check fails.
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Terminal colours
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_COLOR = _supports_color()
RED    = "\033[31m" if _COLOR else ""
GREEN  = "\033[32m" if _COLOR else ""
YELLOW = "\033[33m" if _COLOR else ""
CYAN   = "\033[36m" if _COLOR else ""
BOLD   = "\033[1m"  if _COLOR else ""
RESET  = "\033[0m"  if _COLOR else ""


def pass_msg(label: str) -> str:
    return f"{GREEN}[PASS]{RESET} {label}"


def fail_msg(label: str) -> str:
    return f"{RED}[FAIL]{RESET} {label}"


def warn_msg(label: str) -> str:
    return f"{YELLOW}[WARN]{RESET} {label}"


def info_msg(label: str) -> str:
    return f"{CYAN}[INFO]{RESET} {label}"


def header(msg: str) -> str:
    return f"\n{BOLD}{msg}{RESET}"


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS: List[str] = [
    "claim_id",
    "claim_text",
    "paper_citekey",
    "citation_location",
    "evidence_type",
    "direction",
    "confidence",
]

VALID_EVIDENCE_TYPES: Set[str] = {
    "experiment",
    "survey",
    "meta-analysis",
    "case-study",
    "theory",
    "opinion",
}

VALID_DIRECTIONS: Set[str] = {
    "supports",
    "contradicts",
    "partially-supports",
    "unclear",
}

VALID_CONFIDENCES: Set[str] = {
    "high",
    "medium",
    "low",
}

CLAIM_ID_PATTERN = re.compile(r"^C\d+$")

# Heuristic phrases that suggest unsourced claims in prose
UNSOURCED_PHRASES: List[str] = [
    "studies show",
    "research proves",
    "it is clear that",
    "has been shown",
    "research shows",
    "it is well known",
    "experts agree",
    "many researchers",
    "recent studies",
    "according to experts",
    "it has been demonstrated",
    "evidence shows",
    "literature shows",
    "science shows",
]


# ---------------------------------------------------------------------------
# Matrix reader
# ---------------------------------------------------------------------------

def read_matrix(path: Path) -> Tuple[Optional[List[str]], List[Dict[str, str]]]:
    """
    Read evidence_matrix.csv.

    Returns (fieldnames, rows). Returns (None, []) if file cannot be read.
    """
    if not path.exists():
        return None, []
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fieldnames = list(reader.fieldnames) if reader.fieldnames else []
            rows = list(reader)
        return fieldnames, rows
    except (OSError, csv.Error) as exc:
        print(warn_msg(f"Cannot read {path}: {exc}"))
        return None, []


# ---------------------------------------------------------------------------
# Check functions — each returns (passed: bool, messages: list[str])
# ---------------------------------------------------------------------------

def check_required_columns(fieldnames: Optional[List[str]]) -> Tuple[bool, List[str]]:
    if fieldnames is None:
        return False, ["Matrix file could not be read."]
    missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
    if missing:
        return False, [f"Missing required column(s): {', '.join(missing)}"]
    return True, [f"All {len(REQUIRED_COLUMNS)} required columns present."]


def check_no_empty_ids_or_text(rows: List[Dict]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for i, row in enumerate(rows, start=2):  # row 1 = header
        cid = (row.get("claim_id") or "").strip()
        ctxt = (row.get("claim_text") or "").strip()
        if not cid:
            issues.append(f"  Row {i}: empty claim_id")
        if not ctxt:
            issues.append(f"  Row {i}: empty claim_text (claim_id={row.get('claim_id', '?')!r})")
    if issues:
        return False, [f"{len(issues)} row(s) with empty claim_id or claim_text:"] + issues
    return True, [f"All {len(rows)} rows have non-empty claim_id and claim_text."]


def check_evidence_type(rows: List[Dict]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for i, row in enumerate(rows, start=2):
        val = (row.get("evidence_type") or "").strip().lower()
        cid = row.get("claim_id", f"row {i}")
        if val not in VALID_EVIDENCE_TYPES:
            issues.append(
                f"  {cid}: evidence_type={val!r} — must be one of: {', '.join(sorted(VALID_EVIDENCE_TYPES))}"
            )
    if issues:
        return False, [f"{len(issues)} invalid evidence_type value(s):"] + issues
    return True, ["All evidence_type values are valid."]


def check_direction(rows: List[Dict]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for i, row in enumerate(rows, start=2):
        val = (row.get("direction") or "").strip().lower()
        cid = row.get("claim_id", f"row {i}")
        if val not in VALID_DIRECTIONS:
            issues.append(
                f"  {cid}: direction={val!r} — must be one of: {', '.join(sorted(VALID_DIRECTIONS))}"
            )
    if issues:
        return False, [f"{len(issues)} invalid direction value(s):"] + issues
    return True, ["All direction values are valid."]


def check_confidence(rows: List[Dict]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for i, row in enumerate(rows, start=2):
        val = (row.get("confidence") or "").strip().lower()
        cid = row.get("claim_id", f"row {i}")
        if val not in VALID_CONFIDENCES:
            issues.append(
                f"  {cid}: confidence={val!r} — must be one of: {', '.join(sorted(VALID_CONFIDENCES))}"
            )
    if issues:
        return False, [f"{len(issues)} invalid confidence value(s):"] + issues
    return True, ["All confidence values are valid."]


def check_claim_id_format(rows: List[Dict]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for i, row in enumerate(rows, start=2):
        cid = (row.get("claim_id") or "").strip()
        if cid and not CLAIM_ID_PATTERN.match(cid):
            issues.append(f"  Row {i}: claim_id={cid!r} does not match pattern C<digits> (e.g., C001)")
    if issues:
        return False, [f"{len(issues)} claim_id(s) with invalid format:"] + issues
    return True, ["All claim_ids follow the C<digits> format."]


def check_no_duplicate_ids(rows: List[Dict]) -> Tuple[bool, List[str]]:
    seen: Dict[str, int] = {}
    dupes: List[str] = []
    for i, row in enumerate(rows, start=2):
        cid = (row.get("claim_id") or "").strip()
        if not cid:
            continue
        if cid in seen:
            dupes.append(f"  {cid}: duplicate (rows {seen[cid]} and {i})")
        else:
            seen[cid] = i
    if dupes:
        return False, [f"{len(dupes)} duplicate claim_id(s):"] + dupes
    return True, [f"No duplicate claim_ids among {len(rows)} rows."]


def check_registry_coverage(
    rows: List[Dict],
    registry_path: Path,
) -> Tuple[bool, List[str]]:
    """Every claim_id in the CSV must have a ## CXXX section in claim_registry.md."""
    if not registry_path.exists():
        return False, [f"claim_registry.md not found at {registry_path}"]

    try:
        registry_text = registry_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, [f"Cannot read {registry_path}: {exc}"]

    # Extract section headers: ## C001, ## C042, etc.
    registry_ids: Set[str] = set(re.findall(r"^##\s+(C\d+)", registry_text, re.MULTILINE))

    matrix_ids = {
        (row.get("claim_id") or "").strip()
        for row in rows
        if (row.get("claim_id") or "").strip()
    }

    missing_from_registry = matrix_ids - registry_ids
    if missing_from_registry:
        msgs = [f"{len(missing_from_registry)} claim_id(s) in CSV but no registry section:"]
        for cid in sorted(missing_from_registry):
            msgs.append(f"  {cid}")
        return False, msgs

    return True, [
        f"All {len(matrix_ids)} claim_id(s) have a corresponding section in claim_registry.md."
    ]


def check_draft_evidence_comments(draft_path: Path) -> Tuple[bool, List[str]]:
    """
    Heuristic: scan outputs/draft.md for sentences with unsourced phrases
    that lack an <!-- Evidence: ... --> comment nearby (within 3 lines).
    Returns (True, messages) — this check is a WARNING, not a hard FAIL.
    """
    if not draft_path.exists():
        return True, [f"draft.md not found at {draft_path} — skipping draft check."]

    try:
        lines = draft_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return True, [f"Cannot read {draft_path}: {exc} — skipping draft check."]

    flagged: List[str] = []
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for phrase in UNSOURCED_PHRASES:
            if phrase in line_lower:
                # Check ±3 lines for an evidence comment
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 4)
                context = " ".join(lines[context_start:context_end])
                if "<!-- evidence:" not in context.lower():
                    flagged.append(
                        f"  Line {i + 1}: phrase {phrase!r} found — no <!-- Evidence: --> nearby\n"
                        f"    > {line.strip()[:120]}"
                    )
                break  # one flag per line is enough

    if flagged:
        msgs = [f"{len(flagged)} sentence(s) with unsourced language and no Evidence comment:"]
        msgs.extend(flagged[:20])
        if len(flagged) > 20:
            msgs.append(f"  ... and {len(flagged) - 20} more.")
        return False, msgs  # treated as FAIL so CI can catch it

    return True, ["No unsourced phrases without Evidence comments found in draft.md."]


# ---------------------------------------------------------------------------
# Main report
# ---------------------------------------------------------------------------

def run_all_checks(
    matrix_path: Path,
    registry_path: Path,
    draft_path: Path,
) -> bool:
    """Run all checks. Return True if all pass (no failures)."""

    print(header("=" * 60))
    print(header("  EVIDENCE MATRIX VALIDATION REPORT"))
    print(header("=" * 60))

    print(info_msg(f"Matrix   : {matrix_path}"))
    print(info_msg(f"Registry : {registry_path}"))
    print(info_msg(f"Draft    : {draft_path}"))

    fieldnames, rows = read_matrix(matrix_path)

    if fieldnames is None and not matrix_path.exists():
        print(f"\n{RED}[FATAL]{RESET} evidence_matrix.csv not found at {matrix_path}")
        return False

    all_passed = True

    # Define check suite
    checks = [
        ("Required columns",        lambda: check_required_columns(fieldnames)),
        ("No empty IDs/text",       lambda: check_no_empty_ids_or_text(rows)),
        ("evidence_type values",    lambda: check_evidence_type(rows)),
        ("direction values",        lambda: check_direction(rows)),
        ("confidence values",       lambda: check_confidence(rows)),
        ("claim_id format",         lambda: check_claim_id_format(rows)),
        ("No duplicate claim_ids",  lambda: check_no_duplicate_ids(rows)),
        ("Registry coverage",       lambda: check_registry_coverage(rows, registry_path)),
        ("Draft evidence comments", lambda: check_draft_evidence_comments(draft_path)),
    ]

    print(header("Check Results"))
    results_summary: List[Tuple[str, bool]] = []

    for label, check_fn in checks:
        passed, messages = check_fn()
        status = pass_msg(label) if passed else fail_msg(label)
        print(f"\n  {status}")
        for msg in messages:
            print(f"    {msg}")
        results_summary.append((label, passed))
        if not passed:
            all_passed = False

    # Summary table
    print(header("Summary"))
    passed_count = sum(1 for _, p in results_summary if p)
    failed_count = len(results_summary) - passed_count
    print(f"  Checks run   : {len(results_summary)}")
    print(f"  Passed       : {GREEN}{passed_count}{RESET}")
    print(f"  Failed       : {RED if failed_count else GREEN}{failed_count}{RESET}")
    print(f"  Matrix rows  : {len(rows)}")

    if all_passed:
        print(f"\n{GREEN}{BOLD}RESULT: PASS — evidence matrix is valid.{RESET}\n")
    else:
        print(f"\n{RED}{BOLD}RESULT: FAIL — fix the above issues. Exits with code 1.{RESET}\n")

    return all_passed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the evidence_matrix.csv for Academic Research OS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_evidence_matrix.py
  python scripts/validate_evidence_matrix.py --root /path/to/project
  python scripts/validate_evidence_matrix.py --matrix evidence/matrix.csv
""",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Project root directory (default: current working directory)",
    )
    parser.add_argument(
        "--matrix",
        type=str,
        default=None,
        help="Path to evidence_matrix.csv (default: <root>/evidence/evidence_matrix.csv)",
    )
    parser.add_argument(
        "--registry",
        type=str,
        default=None,
        help="Path to claim_registry.md (default: <root>/evidence/claim_registry.md)",
    )
    parser.add_argument(
        "--draft",
        type=str,
        default=None,
        help="Path to draft.md (default: <root>/outputs/draft.md)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()

    matrix_path = (
        Path(args.matrix).resolve() if args.matrix
        else root / "evidence" / "evidence_matrix.csv"
    )
    registry_path = (
        Path(args.registry).resolve() if args.registry
        else root / "evidence" / "claim_registry.md"
    )
    draft_path = (
        Path(args.draft).resolve() if args.draft
        else root / "outputs" / "draft.md"
    )

    all_passed = run_all_checks(matrix_path, registry_path, draft_path)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
