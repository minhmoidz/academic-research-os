#!/usr/bin/env python3
"""
validate_citations.py — Citation consistency checker for Academic Research OS.

Checks:
  1. Reads library/references.bib and extracts all citekeys.
  2. Scans notes/, outputs/, synthesis/ for @citekey and \\cite{citekey} patterns.
  3. Reports orphan citations (used in notes but not in .bib).
  4. Reports unused bib entries (in .bib but never cited in notes).
  5. Reads evidence/evidence_matrix.csv and checks every paper_citekey exists in .bib.
  6. Exits with code 1 if any orphan citations found.
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Terminal colours (no external deps — use raw ANSI)
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


def ok(msg: str) -> str:
    return f"{GREEN}[OK]{RESET} {msg}"


def warn(msg: str) -> str:
    return f"{YELLOW}[WARN]{RESET} {msg}"


def error(msg: str) -> str:
    return f"{RED}[ERROR]{RESET} {msg}"


def info(msg: str) -> str:
    return f"{CYAN}[INFO]{RESET} {msg}"


def header(msg: str) -> str:
    return f"\n{BOLD}{msg}{RESET}"


# ---------------------------------------------------------------------------
# BibTeX parser — extracts citekeys only (no full parse needed)
# ---------------------------------------------------------------------------

# Matches @type{citekey, ...}  (any entry type)
_BIBTEX_ENTRY_RE = re.compile(
    r"@\w+\s*\{\s*([^,\s]+)\s*,",
    re.IGNORECASE | re.MULTILINE,
)


def extract_bib_citekeys(bib_path: Path) -> set:
    """Return the set of all citekeys defined in a .bib file."""
    if not bib_path.exists():
        print(error(f"BibTeX file not found: {bib_path}"))
        sys.exit(2)

    try:
        text = bib_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(error(f"Cannot read {bib_path}: {exc}"))
        sys.exit(2)

    keys = set(_BIBTEX_ENTRY_RE.findall(text))
    return keys


# ---------------------------------------------------------------------------
# Citation scanner — finds @key and \cite{key} patterns in Markdown files
# ---------------------------------------------------------------------------

# @citekey — must not be preceded by another word char (avoid email addresses)
_AT_CITE_RE = re.compile(r"(?<!\w)@([A-Za-z][A-Za-z0-9_:\-]*)")

# \cite{key} and \cite[...]{key}
_LATEX_CITE_RE = re.compile(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}")


def _parse_latex_cite(match_str: str) -> list:
    r"""Split possibly comma-separated cite keys, e.g. \cite{a,b,c}."""
    return [k.strip() for k in match_str.split(",") if k.strip()]


def scan_md_files(directories: list) -> dict:
    """
    Scan .md files in the given directories.

    Returns:
        dict mapping citekey -> list of (filepath, line_number) occurrences.
    """
    citations: dict = {}

    for scan_dir in directories:
        p = Path(scan_dir)
        if not p.exists():
            print(warn(f"Directory does not exist, skipping: {scan_dir}"))
            continue

        for md_file in p.rglob("*.md"):
            try:
                lines = md_file.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError as exc:
                print(warn(f"Cannot read {md_file}: {exc}"))
                continue

            for lineno, line in enumerate(lines, start=1):
                for m in _AT_CITE_RE.finditer(line):
                    key = m.group(1)
                    citations.setdefault(key, []).append((str(md_file), lineno))

                for m in _LATEX_CITE_RE.finditer(line):
                    for key in _parse_latex_cite(m.group(1)):
                        citations.setdefault(key, []).append((str(md_file), lineno))

    return citations


# ---------------------------------------------------------------------------
# Evidence matrix reader
# ---------------------------------------------------------------------------

_MATRIX_CITEKEY_COLUMN = "paper_citekey"


def read_matrix_citekeys(matrix_path: Path) -> dict:
    """
    Read evidence_matrix.csv and return mapping citekey -> list of claim_ids
    that reference it.  Returns empty dict if file does not exist.
    """
    if not matrix_path.exists():
        print(warn(f"Evidence matrix not found: {matrix_path} — skipping matrix check"))
        return {}

    results: dict = {}
    try:
        with matrix_path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None or _MATRIX_CITEKEY_COLUMN not in reader.fieldnames:
                print(warn(
                    f"Column '{_MATRIX_CITEKEY_COLUMN}' not found in {matrix_path} — "
                    "skipping matrix citekey check"
                ))
                return {}
            for row in reader:
                key = (row.get(_MATRIX_CITEKEY_COLUMN) or "").strip()
                claim_id = (row.get("claim_id") or "").strip()
                if key:
                    results.setdefault(key, []).append(claim_id)
    except (OSError, csv.Error) as exc:
        print(warn(f"Cannot read {matrix_path}: {exc}"))
        return {}

    return results


# ---------------------------------------------------------------------------
# Report printer
# ---------------------------------------------------------------------------

def print_report(
    bib_keys: set,
    cited_keys: dict,
    matrix_keys: dict,
    scan_dirs: list,
) -> bool:
    """
    Print the full structured report.

    Returns True if any FATAL issues (orphan citations) found.
    """
    fatal = False

    print(header("=" * 60))
    print(header("  CITATION VALIDATION REPORT"))
    print(header("=" * 60))

    # ------------------------------------------------------------------
    print(header("1. BibTeX Summary"))
    print(info(f"  Total entries in .bib: {len(bib_keys)}"))

    # ------------------------------------------------------------------
    print(header("2. Citation Scan"))
    print(info(f"  Directories scanned: {', '.join(scan_dirs)}"))
    print(info(f"  Unique citekeys found in notes: {len(cited_keys)}"))

    # ------------------------------------------------------------------
    print(header("3. Orphan Citations  (cited in notes but NOT in .bib)"))

    orphans = {k: v for k, v in cited_keys.items() if k not in bib_keys}
    if orphans:
        fatal = True
        print(error(f"  {len(orphans)} orphan citation(s) found:"))
        for key, occurrences in sorted(orphans.items()):
            print(f"    {RED}@{key}{RESET}")
            for fpath, lineno in occurrences[:5]:  # cap display at 5 per key
                print(f"      -> {fpath}:{lineno}")
            if len(occurrences) > 5:
                print(f"      ... and {len(occurrences) - 5} more occurrence(s)")
    else:
        print(ok("  No orphan citations found."))

    # ------------------------------------------------------------------
    print(header("4. Unused BibTeX Entries  (in .bib but never cited in notes)"))

    unused = bib_keys - set(cited_keys.keys())
    # Also exclude entries that appear in the matrix (they may be legitimate)
    truly_unused = unused - set(matrix_keys.keys())
    if truly_unused:
        print(warn(f"  {len(truly_unused)} unused bib entry/entries:"))
        for key in sorted(truly_unused):
            print(f"    {YELLOW}{key}{RESET}")
    else:
        print(ok("  All bib entries are referenced in notes or evidence matrix."))

    # Also show matrix-only entries (not in notes but in matrix)
    matrix_only = unused & set(matrix_keys.keys())
    if matrix_only:
        print(info(f"  {len(matrix_only)} entry/entries used only in evidence matrix (not in notes):"))
        for key in sorted(matrix_only):
            print(f"    {CYAN}{key}{RESET}")

    # ------------------------------------------------------------------
    print(header("5. Evidence Matrix Citekey Check"))

    if not matrix_keys:
        print(warn("  Evidence matrix not checked (file missing or no citekey column)."))
    else:
        matrix_orphans = {k: v for k, v in matrix_keys.items() if k not in bib_keys}
        if matrix_orphans:
            fatal = True
            print(error(f"  {len(matrix_orphans)} matrix citekey(s) NOT in .bib:"))
            for key, claim_ids in sorted(matrix_orphans.items()):
                ids_str = ", ".join(c for c in claim_ids if c) or "(no claim_id)"
                print(f"    {RED}{key}{RESET}  [claims: {ids_str}]")
        else:
            print(ok(f"  All {len(matrix_keys)} matrix citekey(s) found in .bib."))

    # ------------------------------------------------------------------
    print(header("6. Summary"))
    total_cited = len(cited_keys)
    total_bib = len(bib_keys)
    total_orphans = len(orphans)
    total_unused = len(truly_unused)
    total_matrix_orphans = len({k for k in matrix_keys if k not in bib_keys})

    print(f"  Citekeys in .bib              : {total_bib}")
    print(f"  Unique citekeys in notes      : {total_cited}")
    print(f"  Orphan citations (FATAL)      : {RED if total_orphans else GREEN}{total_orphans}{RESET}")
    print(f"  Unused bib entries (warning)  : {YELLOW if total_unused else GREEN}{total_unused}{RESET}")
    print(f"  Matrix citekeys not in .bib   : {RED if total_matrix_orphans else GREEN}{total_matrix_orphans}{RESET}")

    if fatal:
        print(f"\n{RED}{BOLD}RESULT: FAIL — orphan citations detected. Exits with code 1.{RESET}\n")
    else:
        print(f"\n{GREEN}{BOLD}RESULT: PASS — no orphan citations.{RESET}\n")

    return fatal


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate citation consistency across the Academic Research OS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_citations.py
  python scripts/validate_citations.py --root /path/to/project
  python scripts/validate_citations.py --bib library/refs.bib --scan notes outputs
""",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Project root directory (default: current working directory)",
    )
    parser.add_argument(
        "--bib",
        type=str,
        default=None,
        help="Path to .bib file (default: <root>/library/references.bib)",
    )
    parser.add_argument(
        "--scan",
        nargs="+",
        default=None,
        help=(
            "Directories to scan for citations (default: notes/ outputs/ synthesis/). "
            "Paths are resolved relative to --root."
        ),
    )
    parser.add_argument(
        "--matrix",
        type=str,
        default=None,
        help="Path to evidence_matrix.csv (default: <root>/evidence/evidence_matrix.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    root = Path(args.root).resolve()

    bib_path = Path(args.bib).resolve() if args.bib else root / "library" / "references.bib"
    matrix_path = Path(args.matrix).resolve() if args.matrix else root / "evidence" / "evidence_matrix.csv"

    default_scan_dirs = ["notes", "outputs", "synthesis"]
    scan_dir_names = args.scan if args.scan else default_scan_dirs
    scan_dirs = [str(root / d) for d in scan_dir_names]

    print(info(f"Project root : {root}"))
    print(info(f"BibTeX file  : {bib_path}"))
    print(info(f"Matrix file  : {matrix_path}"))
    print(info(f"Scan dirs    : {', '.join(scan_dirs)}"))

    bib_keys = extract_bib_citekeys(bib_path)
    cited_keys = scan_md_files(scan_dirs)
    matrix_keys = read_matrix_citekeys(matrix_path)

    fatal = print_report(bib_keys, cited_keys, matrix_keys, scan_dirs)

    sys.exit(1 if fatal else 0)


if __name__ == "__main__":
    main()
