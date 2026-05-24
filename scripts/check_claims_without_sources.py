#!/usr/bin/env python3
"""
check_claims_without_sources.py — Hallucination-prone phrase detector for Academic Research OS.

Scans outputs/ and synthesis/ for unsourced-sounding language.
A phrase is HIGH RISK if it appears with no claim ID (C\\d{3}) within 2 lines.
Exits with code 1 if any HIGH RISK phrases are found.

Usage:
  python scripts/check_claims_without_sources.py
  python scripts/check_claims_without_sources.py --strict
  python scripts/check_claims_without_sources.py --dirs outputs synthesis notes
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Tuple


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
MAGENTA = "\033[35m" if _COLOR else ""
BOLD   = "\033[1m"  if _COLOR else ""
RESET  = "\033[0m"  if _COLOR else ""


def header(msg: str) -> str:
    return f"\n{BOLD}{msg}{RESET}"


# ---------------------------------------------------------------------------
# Phrase lists
# ---------------------------------------------------------------------------

# HIGH-RISK phrases: assertive, unsourced-sounding
HIGH_RISK_PHRASES: List[str] = [
    "studies show",
    "research shows",
    "it is well known",
    "it is clear that",
    "research proves",
    "experts agree",
    "many researchers",
    "recent studies",
    "according to experts",
    # additional common hallucination markers
    "it has been widely accepted",
    "it is generally accepted",
    "the literature agrees",
    "consensus is",
    "it is widely known",
    "everyone knows",
    "it is obvious that",
    "clearly,",
]

# MEDIUM-RISK phrases (only flagged in --strict mode)
MEDIUM_RISK_PHRASES: List[str] = [
    "suggests that",
    "appears to",
    "seems to",
    "it seems",
    "it appears",
    "arguably",
    "presumably",
    "one might argue",
    "it could be argued",
    "it is likely that",
    "it is possible that",
]

# Pattern for claim IDs: C followed by 1+ digits (e.g., C001, C42, C1234)
CLAIM_ID_RE = re.compile(r"\bC\d{1,6}\b")

# Evidence comment pattern used in drafts: <!-- Evidence: ... -->
EVIDENCE_COMMENT_RE = re.compile(r"<!--\s*[Ee]vidence\s*:", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    filepath: str
    lineno: int
    phrase: str
    sentence: str
    risk_level: str  # "HIGH" or "MEDIUM"
    reason: str


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def _extract_sentence_containing(line: str, phrase: str) -> str:
    """Return the sentence fragment containing the phrase (trimmed to 200 chars)."""
    line = line.strip()
    phrase_lower = phrase.lower()
    idx = line.lower().find(phrase_lower)
    if idx == -1:
        return line[:200]
    # Walk back to sentence start
    start = max(0, idx)
    for ch in ".!?\n":
        pos = line.rfind(ch, 0, idx)
        if pos != -1:
            start = max(start, pos + 1)
    # Walk forward to sentence end
    end = len(line)
    for ch in ".!?\n":
        pos = line.find(ch, idx + len(phrase))
        if pos != -1:
            end = min(end, pos + 1)
    return line[start:end].strip()[:200]


def _has_claim_id_nearby(lines: List[str], center: int, window: int = 2) -> bool:
    """Return True if any claim ID appears within `window` lines of `center` (0-indexed)."""
    start = max(0, center - window)
    end = min(len(lines), center + window + 1)
    context = " ".join(lines[start:end])
    return bool(CLAIM_ID_RE.search(context))


def _has_evidence_comment_nearby(lines: List[str], center: int, window: int = 2) -> bool:
    """Return True if an evidence HTML comment appears within `window` lines."""
    start = max(0, center - window)
    end = min(len(lines), center + window + 1)
    context = " ".join(lines[start:end])
    return bool(EVIDENCE_COMMENT_RE.search(context))


def scan_file(
    filepath: Path,
    high_risk: List[str],
    medium_risk: Optional[List[str]],
) -> Tuple[List[Finding], bool]:
    """
    Scan one file for flagged phrases.

    Returns (findings, is_clean).
    """
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"{YELLOW}[WARN]{RESET} Cannot read {filepath}: {exc}", file=sys.stderr)
        return [], True

    lines = text.splitlines()
    findings: List[Finding] = []

    all_phrases = [(p, "HIGH") for p in high_risk]
    if medium_risk:
        all_phrases += [(p, "MEDIUM") for p in medium_risk]

    for i, line in enumerate(lines):
        line_lower = line.lower()
        for phrase, base_risk in all_phrases:
            if phrase.lower() not in line_lower:
                continue

            has_claim = _has_claim_id_nearby(lines, i)
            has_evidence = _has_evidence_comment_nearby(lines, i)

            if has_claim or has_evidence:
                # Phrase is present but linked to evidence — not a risk
                continue

            # Phrase present AND no nearby claim ID or evidence comment
            risk = base_risk
            reason = (
                "Flagged phrase found with no claim ID (C\\d+) or <!-- Evidence: --> "
                "within 2 lines."
            )

            findings.append(Finding(
                filepath=str(filepath),
                lineno=i + 1,
                phrase=phrase,
                sentence=_extract_sentence_containing(line, phrase),
                risk_level=risk,
                reason=reason,
            ))
            break  # one finding per line is sufficient

    return findings, len(findings) == 0


def scan_directories(
    dirs: List[str],
    high_risk: List[str],
    medium_risk: Optional[List[str]],
    root: Path,
) -> Tuple[List[Finding], List[str], List[str]]:
    """
    Scan all .md files in the given directories.

    Returns (all_findings, clean_files, skipped_dirs).
    """
    all_findings: List[Finding] = []
    clean_files: List[str] = []
    skipped_dirs: List[str] = []

    for d in dirs:
        scan_path = root / d
        if not scan_path.exists():
            skipped_dirs.append(d)
            continue
        for md_file in sorted(scan_path.rglob("*.md")):
            findings, is_clean = scan_file(md_file, high_risk, medium_risk)
            all_findings.extend(findings)
            if is_clean:
                clean_files.append(str(md_file))

    return all_findings, clean_files, skipped_dirs


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(
    all_findings: List[Finding],
    clean_files: List[str],
    skipped_dirs: List[str],
    strict: bool,
) -> bool:
    """Print structured report. Returns True if any HIGH RISK findings exist."""

    high_risk_findings = [f for f in all_findings if f.risk_level == "HIGH"]
    medium_risk_findings = [f for f in all_findings if f.risk_level == "MEDIUM"]

    print(header("=" * 60))
    print(header("  UNSOURCED CLAIM DETECTION REPORT"))
    print(header("=" * 60))
    if strict:
        print(f"  {YELLOW}Mode: STRICT (medium-risk phrases also flagged){RESET}")

    # ------------------------------------------------------------------
    if all_findings:
        print(header("Flagged Occurrences"))
        # Group by file
        by_file: dict = {}
        for f in all_findings:
            by_file.setdefault(f.filepath, []).append(f)

        for fpath, file_findings in sorted(by_file.items()):
            rel = fpath
            print(f"\n  {BOLD}File:{RESET} {rel}")
            for finding in file_findings:
                risk_color = RED if finding.risk_level == "HIGH" else YELLOW
                print(
                    f"    {risk_color}[{finding.risk_level} RISK]{RESET} "
                    f"Line {finding.lineno} — phrase: {BOLD}{finding.phrase!r}{RESET}"
                )
                print(f"    Sentence: {CYAN}{finding.sentence}{RESET}")
                print(f"    Reason  : {finding.reason}")
    else:
        print(f"\n  {GREEN}No flagged phrases found.{RESET}")

    # ------------------------------------------------------------------
    print(header("Summary"))
    total = len(all_findings)
    hi = len(high_risk_findings)
    med = len(medium_risk_findings)
    clean = len(clean_files)

    print(f"  Total flagged occurrences  : {RED if total else GREEN}{total}{RESET}")
    print(f"  HIGH RISK (exits code 1)   : {RED if hi else GREEN}{hi}{RESET}")
    print(f"  MEDIUM RISK (strict mode)  : {YELLOW if med else GREEN}{med}{RESET}")
    print(f"  Files with no issues       : {GREEN}{clean}{RESET}")

    if skipped_dirs:
        print(f"  Directories not found      : {YELLOW}{', '.join(skipped_dirs)}{RESET}")

    if hi:
        print(f"\n{RED}{BOLD}RESULT: FAIL — {hi} HIGH RISK phrase(s) found without claim IDs. Exits code 1.{RESET}\n")
        print(f"  Fix: Add a claim ID (e.g., C042) within 2 lines of each flagged sentence,")
        print(f"  or add <!-- Evidence: C042 --> as an HTML comment after the sentence.")
    else:
        print(f"\n{GREEN}{BOLD}RESULT: PASS — No HIGH RISK unsourced phrases detected.{RESET}\n")

    return len(high_risk_findings) > 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect hallucination-prone phrases in research draft files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/check_claims_without_sources.py
  python scripts/check_claims_without_sources.py --strict
  python scripts/check_claims_without_sources.py --dirs outputs synthesis notes
  python scripts/check_claims_without_sources.py --root /path/to/project --strict
""",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Project root directory (default: current working directory)",
    )
    parser.add_argument(
        "--dirs",
        nargs="+",
        default=["outputs", "synthesis"],
        help="Subdirectories to scan (default: outputs synthesis)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help=(
            "Also flag medium-risk phrases ('suggests that', 'appears to', 'seems to') "
            "without nearby claim IDs."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()

    medium_phrases = MEDIUM_RISK_PHRASES if args.strict else None

    print(f"{CYAN}[INFO]{RESET} Root    : {root}")
    print(f"{CYAN}[INFO]{RESET} Dirs    : {', '.join(args.dirs)}")
    print(f"{CYAN}[INFO]{RESET} Strict  : {args.strict}")

    all_findings, clean_files, skipped_dirs = scan_directories(
        args.dirs,
        HIGH_RISK_PHRASES,
        medium_phrases,
        root,
    )

    has_high_risk = print_report(all_findings, clean_files, skipped_dirs, args.strict)
    sys.exit(1 if has_high_risk else 0)


if __name__ == "__main__":
    main()
