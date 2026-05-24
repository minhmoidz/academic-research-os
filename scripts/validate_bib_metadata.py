#!/usr/bin/env python3
"""
validate_bib_metadata.py — BibTeX metadata quality checker for Academic Research OS.

Offline checks (no network calls):
  HARD FAIL (exits 1):
    - Any entry missing both doi and url fields.
  WARNINGS (printed, never exits 1):
    - Missing author, title, or year field.
    - DOI field present but not matching canonical pattern 10.NNNN/...

Run:
  python scripts/validate_bib_metadata.py
  python scripts/validate_bib_metadata.py --bib library/references.bib
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

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
# Canonical DOI pattern: 10.NNNN/suffix
# Handles: 10.1234/foo, 10.18653/v1/2024.acl-long.211, 10.1002/14651858.MR000077
# ---------------------------------------------------------------------------
DOI_RE = re.compile(r"^10\.\d{4,}/\S+$")

# Pseudo-entry types that should not be validated for metadata
_SKIP_TYPES = {"string", "preamble", "comment"}


# ---------------------------------------------------------------------------
# BibTeX parser
# ---------------------------------------------------------------------------

def parse_bib(path: Path) -> List[Dict[str, str]]:
    """
    Parse a .bib file into a list of entry dicts.

    Each dict contains 'citekey' and 'type', plus any BibTeX field names
    (lowercased) mapped to their values (whitespace-normalised, braces stripped).

    Uses a two-pass strategy:
      1. Locate entry start positions via @type{key, pattern.
      2. Slice the body between consecutive entry starts and extract field=value pairs.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(fail_msg(f"Cannot read {path}: {exc}"))
        sys.exit(1)

    entry_starts = list(re.finditer(
        r"^@(\w+)\s*\{\s*([^,\s]+)\s*,",
        text,
        re.MULTILINE,
    ))

    entries: List[Dict[str, str]] = []
    for i, m in enumerate(entry_starts):
        entry_type = m.group(1).lower()
        citekey    = m.group(2).strip()
        body_start = m.end()
        body_end   = entry_starts[i + 1].start() if i + 1 < len(entry_starts) else len(text)
        body       = text[body_start:body_end]

        fields: Dict[str, str] = {"citekey": citekey, "type": entry_type}

        # Match field = {value} (handles one level of nested braces: {foo {bar} baz})
        for fm in re.finditer(
            r"\b(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}",
            body,
            re.DOTALL,
        ):
            fname = fm.group(1).lower()
            fval  = " ".join(fm.group(2).split())  # normalise whitespace
            fields[fname] = fval

        entries.append(fields)

    return entries


# ---------------------------------------------------------------------------
# Hard check: DOI or URL present
# ---------------------------------------------------------------------------

def check_doi_or_url(
    entries: List[Dict],
) -> Tuple[bool, List[str]]:
    """Returns (passed, messages). HARD FAIL if any entry has neither doi nor url."""
    fails: List[str] = []
    for e in entries:
        if e.get("type") in _SKIP_TYPES:
            continue
        has_doi = bool((e.get("doi") or "").strip())
        has_url = bool((e.get("url") or "").strip())
        if not has_doi and not has_url:
            fails.append(f"  {e['citekey']}: missing both 'doi' and 'url' fields")
    if fails:
        return False, [f"{len(fails)} entry/entries missing both DOI and URL:"] + fails
    return True, [f"All {len(entries)} entries have at least one of: doi, url."]


# ---------------------------------------------------------------------------
# Soft check: required bibliographic fields (author / title / year)
# ---------------------------------------------------------------------------

def check_required_fields(entries: List[Dict]) -> List[str]:
    """Returns list of warning messages (never causes exit 1)."""
    warns: List[str] = []
    for e in entries:
        if e.get("type") in _SKIP_TYPES:
            continue
        for field in ("author", "title", "year"):
            if not (e.get(field) or "").strip():
                warns.append(f"  {e['citekey']}: missing '{field}' field")
    return warns


# ---------------------------------------------------------------------------
# Soft check: DOI format
# ---------------------------------------------------------------------------

def check_doi_format(entries: List[Dict]) -> List[str]:
    """Returns list of warning messages for malformed DOI values."""
    warns: List[str] = []
    for e in entries:
        if e.get("type") in _SKIP_TYPES:
            continue
        doi = (e.get("doi") or "").strip()
        if doi and not DOI_RE.match(doi):
            warns.append(f"  {e['citekey']}: malformed DOI — {doi!r} (expected 10.NNNN/...)")
    return warns


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate BibTeX metadata for Academic Research OS.",
    )
    parser.add_argument(
        "--bib",
        type=str,
        default=None,
        help="Path to references.bib (default: <repo-root>/library/references.bib)",
    )
    args = parser.parse_args()

    root    = Path(__file__).parent.parent.resolve()
    bib_path = Path(args.bib).resolve() if args.bib else root / "library" / "references.bib"

    print(hdr("=" * 60))
    print(hdr("  BIB METADATA VALIDATION REPORT"))
    print(hdr("=" * 60))
    print(info_msg(f"BibTeX file : {bib_path}"))

    if not bib_path.exists():
        print(fail_msg(f"references.bib not found at {bib_path}"))
        sys.exit(1)

    all_entries = parse_bib(bib_path)
    real_entries = [e for e in all_entries if e.get("type") not in _SKIP_TYPES]
    print(info_msg(f"Entries parsed: {len(real_entries)}"))

    all_passed = True

    # ------------------------------------------------------------------
    # Hard checks
    # ------------------------------------------------------------------
    print(hdr("Hard Checks (exits 1 on failure)"))

    passed, msgs = check_doi_or_url(real_entries)
    if passed:
        print(f"\n  {pass_msg('DOI or URL present')}")
        for m in msgs:
            print(f"    {m}")
    else:
        print(f"\n  {fail_msg('DOI or URL present')}")
        for m in msgs:
            print(f"    {m}")
        all_passed = False

    # ------------------------------------------------------------------
    # Soft checks (warnings only)
    # ------------------------------------------------------------------
    print(hdr("Soft Checks (warnings only — never exits 1)"))

    req_warns = check_required_fields(real_entries)
    if req_warns:
        print(f"\n  {warn_msg('Required fields (author / title / year)')}")
        for w in req_warns:
            print(f"    {w}")
    else:
        print(f"\n  {pass_msg('Required fields (author / title / year)')}")
        print(f"    All entries have author, title, and year.")

    doi_warns = check_doi_format(real_entries)
    if doi_warns:
        print(f"\n  {warn_msg('DOI format')}")
        for w in doi_warns:
            print(f"    {w}")
    else:
        print(f"\n  {pass_msg('DOI format')}")
        print(f"    All DOI values match the canonical 10.NNNN/... pattern.")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total_warns = len(req_warns) + len(doi_warns)
    print(hdr("Summary"))
    print(f"  Entries checked : {len(real_entries)}")
    print(f"  Hard failures   : {RED if not all_passed else GREEN}{0 if all_passed else 'see above'}{RESET}")
    print(f"  Warnings        : {YELLOW if total_warns else GREEN}{total_warns}{RESET}")

    if all_passed:
        print(f"\n{GREEN}{BOLD}RESULT: PASS — BibTeX metadata is valid.{RESET}\n")
    else:
        print(f"\n{RED}{BOLD}RESULT: FAIL — fix missing DOI/URL entries. Exits code 1.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
