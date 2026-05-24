#!/usr/bin/env python3
"""
build_evidence_matrix.py

Aggregate all paper notes into a consolidated evidence_matrix.csv.
Scans notes/paper_notes/*.md for claim tables and appends to evidence/evidence_matrix.csv.

Usage:
    python scripts/build_evidence_matrix.py                  # dry-run, print only
    python scripts/build_evidence_matrix.py --write          # write to evidence_matrix.csv
    python scripts/build_evidence_matrix.py --check          # validate existing matrix (CI mode)
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
NOTES_DIR = ROOT / "notes" / "paper_notes"
EVIDENCE_FILE = ROOT / "evidence" / "evidence_matrix.csv"

REQUIRED_COLUMNS = [
    "claim_id", "claim_text", "paper_citekey", "citation_location",
    "evidence_type", "direction", "confidence", "used_in_draft",
    "draft_section", "notes"
]

VALID_EVIDENCE_TYPES = {"experiment", "survey", "meta-analysis", "case-study", "theory", "opinion"}
VALID_DIRECTIONS = {"supports", "contradicts", "partially-supports", "unclear"}
VALID_CONFIDENCE = {"high", "medium", "low"}

# Regex to match claim table rows in paper notes:
# | C001 | claim text | evidence | Sec X | high | notes |
CLAIM_ROW_PATTERN = re.compile(
    r'^\|\s*(C\d{3,})\s*\|'        # claim_id
    r'\s*(.+?)\s*\|'               # claim_text
    r'\s*(.+?)\s*\|'               # evidence
    r'\s*(.+?)\s*\|'               # section/page → citation_location
    r'\s*(high|medium|low)\s*\|'  # confidence
    r'(.*)$',                       # notes (optional)
    re.IGNORECASE
)

CITEKEY_PATTERN = re.compile(r'^#\s*@(\w+)', re.MULTILINE)


def extract_citekey(note_path: Path) -> str:
    """Extract citekey from first line of paper note (# @citekey)."""
    text = note_path.read_text(encoding="utf-8")
    m = CITEKEY_PATTERN.search(text)
    if m:
        return m.group(1)
    return note_path.stem  # fallback: filename without extension


def extract_claims_from_note(note_path: Path) -> list[dict]:
    """Parse claim table rows from a paper note file."""
    citekey = extract_citekey(note_path)
    claims = []
    in_table = False
    lines = note_path.read_text(encoding="utf-8").splitlines()

    for i, line in enumerate(lines):
        # Detect claim table header
        if "| Claim ID |" in line or "| claim_id |" in line.lower():
            in_table = True
            continue
        if in_table and line.strip().startswith("|---"):
            continue  # separator row
        if in_table:
            if not line.strip().startswith("|"):
                in_table = False
                continue
            m = CLAIM_ROW_PATTERN.match(line.strip())
            if m:
                claim_id, claim_text, evidence, citation_loc, confidence, notes = m.groups()
                if claim_id.strip() == "Claim ID" or "---" in claim_id:
                    continue
                claims.append({
                    "claim_id": claim_id.strip(),
                    "claim_text": claim_text.strip(),
                    "paper_citekey": citekey,
                    "citation_location": citation_loc.strip(),
                    "evidence_type": "experiment",  # default; user should override
                    "direction": "supports",          # default; user should override
                    "confidence": confidence.strip().lower(),
                    "used_in_draft": "no",
                    "draft_section": "none",
                    "notes": notes.strip().strip("|").strip() if notes else "",
                })
    return claims


def load_existing_matrix() -> tuple[list[dict], set[str]]:
    """Load existing evidence_matrix.csv. Returns (rows, claim_id_set)."""
    if not EVIDENCE_FILE.exists():
        return [], set()
    rows = []
    ids = set()
    with open(EVIDENCE_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            ids.add(row.get("claim_id", "").strip())
    return rows, ids


def validate_matrix(rows: list[dict]) -> list[str]:
    """Validate all rows in the matrix. Returns list of error messages."""
    errors = []
    seen_ids = {}

    for i, row in enumerate(rows, start=2):  # row 1 = header
        cid = row.get("claim_id", "").strip()
        lineno = f"Row {i}"

        # claim_id format
        if not re.fullmatch(r"C\d{3,}", cid):
            errors.append(f"{lineno}: claim_id '{cid}' does not match pattern C### (e.g. C001)")

        # duplicate check
        if cid in seen_ids:
            errors.append(f"{lineno}: duplicate claim_id '{cid}' (first at row {seen_ids[cid]})")
        else:
            seen_ids[cid] = i

        # claim_text not empty
        if not row.get("claim_text", "").strip():
            errors.append(f"{lineno}: claim_text is empty")

        # paper_citekey not empty
        if not row.get("paper_citekey", "").strip():
            errors.append(f"{lineno}: paper_citekey is empty")

        # controlled vocabulary
        et = row.get("evidence_type", "").strip().lower()
        if et not in VALID_EVIDENCE_TYPES:
            errors.append(f"{lineno}: evidence_type '{et}' invalid. Must be one of: {sorted(VALID_EVIDENCE_TYPES)}")

        d = row.get("direction", "").strip().lower()
        if d not in VALID_DIRECTIONS:
            errors.append(f"{lineno}: direction '{d}' invalid. Must be one of: {sorted(VALID_DIRECTIONS)}")

        c = row.get("confidence", "").strip().lower()
        if c not in VALID_CONFIDENCE:
            errors.append(f"{lineno}: confidence '{c}' invalid. Must be one of: {sorted(VALID_CONFIDENCE)}")

    return errors


def write_matrix(rows: list[dict]):
    """Write rows to evidence_matrix.csv."""
    EVIDENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVIDENCE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        for row in rows:
            # Only write known columns, fill missing with empty string
            writer.writerow({col: row.get(col, "") for col in REQUIRED_COLUMNS})


def main():
    parser = argparse.ArgumentParser(description="Build and validate evidence_matrix.csv from paper notes.")
    parser.add_argument("--write", action="store_true", help="Write new claims to evidence_matrix.csv")
    parser.add_argument("--check", action="store_true", help="Validate existing matrix (CI mode, exits 1 on error)")
    parser.add_argument("--notes-dir", type=Path, default=NOTES_DIR, help="Path to paper notes directory")
    args = parser.parse_args()

    print("=" * 60)
    print("Evidence Matrix Builder")
    print("=" * 60)

    # --- CHECK MODE ---
    if args.check:
        print(f"\n[CHECK] Validating {EVIDENCE_FILE} ...")
        if not EVIDENCE_FILE.exists():
            print("  ERROR: evidence_matrix.csv not found.")
            sys.exit(1)
        rows, _ = load_existing_matrix()
        errors = validate_matrix(rows)
        if errors:
            print(f"  FAIL — {len(errors)} error(s):")
            for e in errors:
                print(f"    ✗ {e}")
            sys.exit(1)
        else:
            print(f"  PASS — {len(rows)} rows, no errors.")
        return

    # --- SCAN NOTES ---
    notes_dir = args.notes_dir
    if not notes_dir.exists():
        print(f"Notes directory not found: {notes_dir}")
        sys.exit(1)

    note_files = list(notes_dir.glob("*.md"))
    note_files = [f for f in note_files if "template" not in f.name.lower()]
    print(f"\n[SCAN] Found {len(note_files)} note file(s) in {notes_dir}")

    all_new_claims = []
    for note_path in sorted(note_files):
        claims = extract_claims_from_note(note_path)
        if claims:
            print(f"  {note_path.name}: {len(claims)} claim(s) extracted")
            all_new_claims.extend(claims)
        else:
            print(f"  {note_path.name}: no claim table found")

    # --- MERGE ---
    existing_rows, existing_ids = load_existing_matrix()
    new_claims = [c for c in all_new_claims if c["claim_id"] not in existing_ids]
    duplicate_claims = [c for c in all_new_claims if c["claim_id"] in existing_ids]

    print(f"\n[MERGE]")
    print(f"  Existing rows:    {len(existing_rows)}")
    print(f"  New claims found: {len(all_new_claims)}")
    print(f"  Duplicates (skip): {len(duplicate_claims)}")
    print(f"  To add:           {len(new_claims)}")

    if new_claims:
        print("\n  New claims to add:")
        for c in new_claims:
            print(f"    {c['claim_id']} | {c['paper_citekey']} | {c['claim_text'][:60]}...")

    # --- VALIDATE MERGED ---
    all_rows = existing_rows + new_claims
    errors = validate_matrix(all_rows)
    if errors:
        print(f"\n[VALIDATE] {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        if not args.write:
            print("\nFix errors before writing. Run with --write to force-write anyway (not recommended).")
            sys.exit(1)

    # --- WRITE ---
    if args.write:
        write_matrix(all_rows)
        print(f"\n[WRITE] evidence_matrix.csv updated: {len(all_rows)} total rows.")
    else:
        print(f"\n[DRY RUN] No changes written. Use --write to apply.")
        if new_claims:
            print("         Use --write to add the new claims above.")


if __name__ == "__main__":
    main()
