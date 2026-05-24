#!/usr/bin/env python3
"""
validate_csv_rows.py — Research OS CSV data-row validator.

Checks:
  1. evidence_matrix.csv has at least 1 data row (beyond header).
  2. search_log.csv has at least 1 data row.
  3. screening_table.csv has at least 1 data row.
  4. papers_manifest.csv: every citekey in the 'citekey' column exists
     in library/references.bib.

Exits with code 1 if any check fails.
Designed to catch the case where a user commits the scaffold but forgets
to populate data, or lets the manifest and BibTeX diverge.

Run:
  python scripts/validate_csv_rows.py
"""

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# Terminal colours
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

_C = _supports_color()
RED    = "\033[31m" if _C else ""
GREEN  = "\033[32m" if _C else ""
YELLOW = "\033[33m" if _C else ""
CYAN   = "\033[36m" if _C else ""
BOLD   = "\033[1m"  if _C else ""
RESET  = "\033[0m"  if _C else ""

def pass_msg(s: str) -> str: return f"{GREEN}[PASS]{RESET} {s}"
def fail_msg(s: str) -> str: return f"{RED}[FAIL]{RESET} {s}"
def warn_msg(s: str) -> str: return f"{YELLOW}[WARN]{RESET} {s}"
def info_msg(s: str) -> str: return f"{CYAN}[INFO]{RESET} {s}"
def hdr(s: str)      -> str: return f"\n{BOLD}{s}{RESET}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv_rows(path: Path) -> Tuple[bool, List[Dict[str, str]], str]:
    """
    Read a CSV. Returns (success, rows, error_message).
    rows does NOT include the header row.
    """
    if not path.exists():
        return False, [], f"File not found: {path}"
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        return True, rows, ""
    except (OSError, csv.Error) as exc:
        return False, [], f"Cannot read {path}: {exc}"


def extract_bib_citekeys(bib_path: Path) -> Tuple[bool, Set[str], str]:
    """Extract all citekeys from a .bib file. Returns (success, keys, error)."""
    if not bib_path.exists():
        return False, set(), f"references.bib not found: {bib_path}"
    try:
        text = bib_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, set(), f"Cannot read {bib_path}: {exc}"

    keys = set(re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,", text, re.MULTILINE))
    return True, keys, ""


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_minimum_rows(
    label: str,
    path: Path,
    minimum: int = 1,
) -> Tuple[bool, List[str]]:
    """Hard fail if the CSV has fewer than `minimum` data rows."""
    ok, rows, err = read_csv_rows(path)
    if not ok:
        return False, [err]
    if len(rows) < minimum:
        return False, [
            f"{path.name} has {len(rows)} data row(s) — minimum required: {minimum}",
            f"  Path: {path}",
            f"  Action: add at least {minimum - len(rows)} row(s) of real data.",
        ]
    return True, [f"{path.name}: {len(rows)} data row(s) — OK (minimum {minimum})."]


def check_manifest_citekeys(
    manifest_path: Path,
    bib_path: Path,
) -> Tuple[bool, List[str]]:
    """
    Every citekey in papers_manifest.csv must exist in references.bib.
    This catches the case where a paper is added to the manifest but
    the BibTeX entry was forgotten.
    """
    ok_m, manifest_rows, err_m = read_csv_rows(manifest_path)
    if not ok_m:
        return False, [err_m]

    ok_b, bib_keys, err_b = extract_bib_citekeys(bib_path)
    if not ok_b:
        return False, [err_b]

    manifest_keys: List[str] = []
    for row in manifest_rows:
        key = (row.get("citekey") or "").strip()
        if key:
            manifest_keys.append(key)

    missing = [k for k in manifest_keys if k not in bib_keys]
    if missing:
        msgs = [
            f"{len(missing)} citekey(s) in papers_manifest.csv not found in references.bib:"
        ]
        for k in sorted(missing):
            msgs.append(f"  {k}")
        msgs.append(
            "  Fix: add the missing @entry{...} blocks to library/references.bib."
        )
        return False, msgs

    return True, [
        f"papers_manifest.csv: all {len(manifest_keys)} citekey(s) found in references.bib."
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main() -> None:
    root = Path(__file__).parent.parent.resolve()

    csv_files: Dict[str, Path] = {
        "evidence_matrix.csv": root / "evidence"  / "evidence_matrix.csv",
        "search_log.csv":      root / "search"     / "search_log.csv",
        "screening_table.csv": root / "screening"  / "screening_table.csv",
        "papers_manifest.csv": root / "library"    / "papers_manifest.csv",
    }
    bib_path = root / "library" / "references.bib"

    print(hdr("=" * 60))
    print(hdr("  CSV DATA-ROW VALIDATION REPORT"))
    print(hdr("=" * 60))
    for label, p in csv_files.items():
        print(info_msg(f"{label:<25}: {p}"))
    print(info_msg(f"{'references.bib':<25}: {bib_path}"))

    all_passed = True
    print(hdr("Check Results"))

    # --- Minimum-row checks ---
    row_checks = [
        ("evidence_matrix.csv",  csv_files["evidence_matrix.csv"],  1),
        ("search_log.csv",       csv_files["search_log.csv"],       1),
        ("screening_table.csv",  csv_files["screening_table.csv"],  1),
    ]
    for label, path, minimum in row_checks:
        passed, msgs = check_minimum_rows(label, path, minimum)
        tag = pass_msg(f"Minimum rows — {label}") if passed else fail_msg(f"Minimum rows — {label}")
        print(f"\n  {tag}")
        for m in msgs:
            print(f"    {m}")
        if not passed:
            all_passed = False

    # --- Manifest citekey alignment ---
    passed, msgs = check_manifest_citekeys(csv_files["papers_manifest.csv"], bib_path)
    tag = pass_msg("papers_manifest.csv citekeys in references.bib") if passed \
          else fail_msg("papers_manifest.csv citekeys in references.bib")
    print(f"\n  {tag}")
    for m in msgs:
        print(f"    {m}")
    if not passed:
        all_passed = False

    # --- Summary ---
    print(hdr("Summary"))
    checks_run = len(row_checks) + 1
    checks_failed = sum([
        not check_minimum_rows(lbl, p, mn)[0]
        for lbl, p, mn in row_checks
    ]) + (0 if passed else 1)
    print(f"  Checks run : {checks_run}")
    print(f"  Passed     : {GREEN}{checks_run - checks_failed}{RESET}")
    print(f"  Failed     : {RED if checks_failed else GREEN}{checks_failed}{RESET}")

    if all_passed:
        print(f"\n{GREEN}{BOLD}RESULT: PASS — all CSV files have data and are consistent.{RESET}\n")
    else:
        print(f"\n{RED}{BOLD}RESULT: FAIL — fix the above issues. Exits code 1.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
