#!/usr/bin/env python3
"""
import_zotero_bib.py

Import / merge a Zotero-exported .bib file into library/references.bib.

Features:
- Merges new entries without overwriting existing ones
- Reports: new entries added, duplicate keys, key conflicts
- Normalizes citekeys to authorYYYYkeyword format (optional, with --normalize)
- Validates required fields per entry type

Usage:
    python scripts/import_zotero_bib.py zotero_export.bib
    python scripts/import_zotero_bib.py zotero_export.bib --normalize
    python scripts/import_zotero_bib.py zotero_export.bib --dry-run
    python scripts/import_zotero_bib.py zotero_export.bib --report
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
REFERENCES_BIB = ROOT / "library" / "references.bib"

REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "misc": ["author", "title", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "book": ["author", "title", "publisher", "year"],
}

# Regex for parsing .bib entries
ENTRY_PATTERN = re.compile(
    r'@(\w+)\s*\{\s*([^,\s]+)\s*,([^@]*)',
    re.DOTALL
)
FIELD_PATTERN = re.compile(
    r'\b(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)")',
    re.DOTALL
)


def parse_bib(bib_text: str) -> dict[str, dict]:
    """Parse .bib text into {citekey: {type, fields}} dict."""
    entries = {}
    for m in ENTRY_PATTERN.finditer(bib_text):
        entry_type = m.group(1).lower()
        citekey = m.group(2).strip()
        body = m.group(3)
        fields = {}
        for fm in FIELD_PATTERN.finditer(body):
            fname = fm.group(1).lower()
            fval = (fm.group(2) or fm.group(3) or "").strip()
            fields[fname] = fval
        entries[citekey] = {"type": entry_type, "fields": fields}
    return entries


def normalize_citekey(entry: dict, citekey: str) -> str:
    """
    Generate authorYYYYkeyword citekey from entry fields.
    Format: firstauthorlastnameYYYYfirstwordoftitle
    Example: smith2024agents
    """
    fields = entry["fields"]

    # Extract first author last name
    author_raw = fields.get("author", "")
    author_last = ""
    if author_raw:
        first_author = author_raw.split(" and ")[0].strip()
        if "," in first_author:
            author_last = first_author.split(",")[0].strip()
        else:
            parts = first_author.split()
            author_last = parts[-1] if parts else first_author
        author_last = re.sub(r"[^a-zA-Z]", "", author_last).lower()

    # Extract year
    year = fields.get("year", "0000")[:4]

    # Extract first meaningful word of title
    title = fields.get("title", "")
    title_words = re.sub(r"[^a-zA-Z\s]", "", title).lower().split()
    stop_words = {"a", "an", "the", "of", "in", "on", "for", "and", "or", "to", "with"}
    title_kw = next((w for w in title_words if w not in stop_words), "paper")

    if author_last and year and title_kw:
        return f"{author_last}{year}{title_kw}"
    return citekey  # fallback


def validate_entry(citekey: str, entry: dict) -> list[str]:
    """Return list of missing required fields."""
    entry_type = entry["type"]
    required = REQUIRED_FIELDS.get(entry_type, ["author", "title", "year"])
    missing = [f for f in required if not entry["fields"].get(f)]
    return missing


def format_entry(citekey: str, entry: dict) -> str:
    """Format a single .bib entry as a string."""
    entry_type = entry["type"]
    fields = entry["fields"]
    lines = [f"@{entry_type}{{{citekey},"]
    for k, v in fields.items():
        lines.append(f"  {k} = {{{v}}},")
    lines.append("}\n")
    return "\n".join(lines)


def load_bib(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return parse_bib(path.read_text(encoding="utf-8"))


def write_bib(path: Path, entries: dict[str, dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("% references.bib — Academic Research OS\n")
        f.write("% Citekey convention: authorYYYYkeyword (e.g., smith2024agents)\n")
        f.write("% Generated/merged by scripts/import_zotero_bib.py\n\n")
        for citekey, entry in sorted(entries.items()):
            f.write(format_entry(citekey, entry))
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Import Zotero .bib export into library/references.bib")
    parser.add_argument("input_bib", type=Path, help="Path to Zotero-exported .bib file")
    parser.add_argument("--normalize", action="store_true", help="Normalize citekeys to authorYYYYkeyword format")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--report", action="store_true", help="Print detailed report of all entries")
    args = parser.parse_args()

    print("=" * 60)
    print("Zotero BibTeX Importer")
    print("=" * 60)

    if not args.input_bib.exists():
        print(f"ERROR: Input file not found: {args.input_bib}")
        sys.exit(1)

    # Load both files
    existing = load_bib(REFERENCES_BIB)
    incoming = parse_bib(args.input_bib.read_text(encoding="utf-8"))

    print(f"\n[LOAD]")
    print(f"  Existing entries: {len(existing)}")
    print(f"  Incoming entries: {len(incoming)}")

    # Optionally normalize citekeys
    if args.normalize:
        normalized = {}
        key_map = {}
        for key, entry in incoming.items():
            new_key = normalize_citekey(entry, key)
            if new_key != key:
                key_map[key] = new_key
            normalized[new_key] = entry
        incoming = normalized
        if key_map:
            print(f"\n[NORMALIZE] {len(key_map)} key(s) renamed:")
            for old, new in key_map.items():
                print(f"  {old} → {new}")

    # Classify entries
    new_entries = {k: v for k, v in incoming.items() if k not in existing}
    duplicates = {k: v for k, v in incoming.items() if k in existing}
    conflicts = {k for k in duplicates if incoming[k] != existing[k]}

    print(f"\n[MERGE ANALYSIS]")
    print(f"  New (to add):     {len(new_entries)}")
    print(f"  Duplicates:       {len(duplicates)}")
    print(f"  Conflicts:        {len(conflicts)}  ← same key, different content")

    # Validate new entries
    validation_errors = {}
    for key, entry in new_entries.items():
        missing = validate_entry(key, entry)
        if missing:
            validation_errors[key] = missing

    if validation_errors:
        print(f"\n[VALIDATE] {len(validation_errors)} entry(ies) with missing required fields:")
        for key, missing in validation_errors.items():
            print(f"  {key}: missing {missing}")

    # Conflicts detail
    if conflicts:
        print(f"\n[CONFLICTS] (existing entry kept, incoming ignored):")
        for key in sorted(conflicts):
            print(f"  {key}")
            print(f"    existing title: {existing[key]['fields'].get('title', '?')[:60]}")
            print(f"    incoming title: {incoming[key]['fields'].get('title', '?')[:60]}")

    # Detailed report
    if args.report:
        print(f"\n[REPORT] All incoming entries:")
        for key, entry in sorted(incoming.items()):
            title = entry["fields"].get("title", "?")[:60]
            year = entry["fields"].get("year", "?")
            status = "NEW" if key in new_entries else ("CONFLICT" if key in conflicts else "DUP")
            print(f"  [{status}] {key} ({year}) — {title}")

    # Write
    if not args.dry_run:
        merged = {**existing, **new_entries}  # existing takes priority for duplicates
        write_bib(REFERENCES_BIB, merged)
        print(f"\n[WRITE] {REFERENCES_BIB}")
        print(f"  Total entries now: {len(merged)}")
        print(f"  New entries added: {len(new_entries)}")
    else:
        print(f"\n[DRY RUN] No changes written.")
        if new_entries:
            print(f"  Would add {len(new_entries)} new entry(ies):")
            for key in sorted(new_entries):
                print(f"    {key}")


if __name__ == "__main__":
    main()
