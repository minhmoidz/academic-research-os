#!/usr/bin/env python3
"""
research_os.cli — Command-line interface for Academic Research OS.

Commands:
  python -m research_os validate   Run all validators (wraps existing scripts)
  python -m research_os status     Print project statistics
  python -m research_os report     Write reports/research_status.md

Entry point (after pip install -e .):
  research-os validate
  research-os status
  research-os report
"""

import argparse
import csv
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from research_os.config import (
    SCRIPT_LABELS,
    find_root,
    load_config,
    resolve_paths,
    resolve_scripts,
)

# ---------------------------------------------------------------------------
# Terminal colours (auto-disabled when not a TTY)
# ---------------------------------------------------------------------------

def _tty() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

_C = _tty()
RED    = "\033[31m" if _C else ""
GREEN  = "\033[32m" if _C else ""
YELLOW = "\033[33m" if _C else ""
CYAN   = "\033[36m" if _C else ""
BOLD   = "\033[1m"  if _C else ""
RESET  = "\033[0m"  if _C else ""

PASS = f"{GREEN}PASS{RESET}"
FAIL = f"{RED}FAIL{RESET}"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _count_bib_entries(bib_path: Path) -> int:
    if not bib_path.exists():
        return 0
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r"^@\w+\s*\{", text, re.MULTILINE))


def _csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def _confidence_breakdown(matrix_rows: List[Dict]) -> Dict[str, int]:
    counts: Dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    for row in matrix_rows:
        c = (row.get("confidence") or "").strip().lower()
        if c in counts:
            counts[c] += 1
    return counts


def _gather_stats(paths: Dict[str, Path]) -> Dict:
    matrix_rows = _csv_rows(paths["evidence_matrix"])
    return {
        "bib_entries":      _count_bib_entries(paths["references"]),
        "manifest_rows":    len(_csv_rows(paths["papers_manifest"])),
        "matrix_rows":      len(matrix_rows),
        "confidence":       _confidence_breakdown(matrix_rows),
        "search_rows":      len(_csv_rows(paths["search_log"])),
        "screening_rows":   len(_csv_rows(paths["screening_table"])),
        "bib_path":         paths["references"],
        "matrix_path":      paths["evidence_matrix"],
    }


# ---------------------------------------------------------------------------
# Command: validate
# ---------------------------------------------------------------------------

def cmd_validate(root: Path, config: Dict) -> int:
    """
    Run each configured validator script as a subprocess.
    Streams each script's output on failure; shows a compact summary table.
    Returns 0 if all pass, 1 if any fail.
    """
    scripts = resolve_scripts(root, config)
    labels  = SCRIPT_LABELS

    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  RESEARCH OS — VALIDATE{RESET}")
    print(f"{BOLD}{'─' * 56}{RESET}\n")

    results: List[Tuple[str, bool, str]] = []

    for key, script_path in scripts.items():
        label = labels.get(key, script_path.name)
        if not script_path.exists():
            results.append((label, False, f"Script not found: {script_path}"))
            continue

        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
        )
        passed = proc.returncode == 0
        output = (proc.stdout + proc.stderr).strip()
        results.append((label, passed, output))

        # Live feedback
        status = PASS if passed else FAIL
        print(f"  [{status}] {label}")
        if not passed:
            for line in output.splitlines():
                if line.strip():
                    print(f"         {line}")

    # Summary line
    n_pass = sum(1 for _, p, _ in results if p)
    n_fail = len(results) - n_pass
    print(f"\n{'─' * 56}")
    color = GREEN if n_fail == 0 else RED
    print(
        f"  {color}{BOLD}{n_pass}/{len(results)} scripts passed"
        f"{'  —  ' + str(n_fail) + ' failed' if n_fail else ''}{RESET}"
    )
    print()

    return 0 if n_fail == 0 else 1


# ---------------------------------------------------------------------------
# Command: status
# ---------------------------------------------------------------------------

def cmd_status(root: Path, config: Dict) -> int:
    paths = resolve_paths(root, config)
    s     = _gather_stats(paths)
    conf  = s["confidence"]

    w = 28  # label column width

    print(f"\n{BOLD}{'─' * 48}{RESET}")
    print(f"{BOLD}  RESEARCH OS — PROJECT STATUS{RESET}")
    print(f"{BOLD}{'─' * 48}{RESET}\n")

    print(f"  {'Bibliography':<{w}}")
    print(f"    {'BibTeX entries':<{w - 2}}: {CYAN}{s['bib_entries']}{RESET}")
    print(f"    {'Papers in manifest':<{w - 2}}: {CYAN}{s['manifest_rows']}{RESET}")

    print(f"\n  {'Evidence Matrix':<{w}}")
    print(f"    {'Total claims':<{w - 2}}: {CYAN}{s['matrix_rows']}{RESET}")
    print(f"    {'├─ high confidence':<{w - 2}}: {GREEN}{conf['high']}{RESET}")
    print(f"    {'├─ medium confidence':<{w - 2}}: {YELLOW}{conf['medium']}{RESET}")
    print(f"    {'└─ low confidence':<{w - 2}}: {RED}{conf['low']}{RESET}")

    print(f"\n  {'Search & Screening':<{w}}")
    print(f"    {'Search log entries':<{w - 2}}: {CYAN}{s['search_rows']}{RESET}")
    print(f"    {'Screened papers':<{w - 2}}: {CYAN}{s['screening_rows']}{RESET}")

    print(f"\n  {'Project root':<{w}}: {root}")
    cfg_path = root / "research.toml"
    print(f"  {'Config':<{w}}: {'research.toml' if cfg_path.exists() else '(defaults)'}")
    print()

    return 0


# ---------------------------------------------------------------------------
# Command: report
# ---------------------------------------------------------------------------

def cmd_report(root: Path, config: Dict) -> int:
    paths       = resolve_paths(root, config)
    reports_dir = paths["reports_dir"]
    reports_dir.mkdir(parents=True, exist_ok=True)

    s    = _gather_stats(paths)
    conf = s["confidence"]
    now  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines: List[str] = [
        "# Research OS — Project Status Report",
        "",
        f"Generated: {now}  ",
        f"Project root: `{root}`  ",
        f"Config: `{'research.toml' if (root / 'research.toml').exists() else 'defaults'}`",
        "",
        "---",
        "",
        "## Bibliography",
        "",
        f"| Item | Count |",
        f"|---|---|",
        f"| BibTeX entries | {s['bib_entries']} |",
        f"| Papers in manifest | {s['manifest_rows']} |",
        "",
        "---",
        "",
        "## Evidence Matrix",
        "",
        f"| Metric | Count |",
        f"|---|---|",
        f"| Total claims | {s['matrix_rows']} |",
        f"| High confidence | {conf['high']} |",
        f"| Medium confidence | {conf['medium']} |",
        f"| Low confidence | {conf['low']} |",
        "",
        "---",
        "",
        "## Search & Screening",
        "",
        f"| Item | Count |",
        f"|---|---|",
        f"| Search log entries | {s['search_rows']} |",
        f"| Screened papers | {s['screening_rows']} |",
        "",
        "---",
        "",
        "## Validator Status",
        "",
        "Run `python -m research_os validate` to check current pass/fail status.",
        "All validators must pass before declaring a review complete.",
        "",
        "_This report was generated automatically by `python -m research_os report`._",
    ]

    report_path = reports_dir / "research_status.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report written to: {report_path}\n")
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-os",
        description="Academic Research OS — evidence-first literature review toolkit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
commands:
  validate    Run all validators and exit 1 on any failure
  status      Print project statistics (claims, papers, searches)
  report      Write reports/research_status.md

examples:
  python -m research_os validate
  python -m research_os status
  python -m research_os report
  research-os validate           # after pip install -e .
""",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Override project root directory (default: auto-detected)",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.add_parser("validate", help="Run all validators")
    sub.add_parser("status",   help="Print project statistics")
    sub.add_parser("report",   help="Write reports/research_status.md")
    return parser


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    root   = Path(args.root).resolve() if args.root else find_root()
    config = load_config(root)

    dispatch = {
        "validate": cmd_validate,
        "status":   cmd_status,
        "report":   cmd_report,
    }
    exit_code = dispatch[args.command](root, config)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
