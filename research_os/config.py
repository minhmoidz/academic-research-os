"""
research_os.config — Load and resolve research.toml configuration.
"""

import tomllib
from pathlib import Path
from typing import Any, Dict

_DEFAULTS: Dict[str, Any] = {
    "paths": {
        "references":      "library/references.bib",
        "evidence_matrix": "evidence/evidence_matrix.csv",
        "search_log":      "search/search_log.csv",
        "screening_table": "screening/screening_table.csv",
        "papers_manifest": "library/papers_manifest.csv",
        "draft":           "outputs/draft.md",
        "reports_dir":     "reports",
    },
    "scripts": {
        "validate_citations":    "scripts/validate_citations.py",
        "validate_evidence":     "scripts/validate_evidence_matrix.py",
        "check_hallucination":   "scripts/check_claims_without_sources.py",
        "validate_bib_metadata": "scripts/validate_bib_metadata.py",
        "validate_csv_rows":     "scripts/validate_csv_rows.py",
    },
}

# Script display labels (ordered — printed in this order by `validate`)
SCRIPT_LABELS = {
    "validate_citations":    "validate_citations.py",
    "validate_evidence":     "validate_evidence_matrix.py",
    "check_hallucination":   "check_claims_without_sources.py",
    "validate_bib_metadata": "validate_bib_metadata.py",
    "validate_csv_rows":     "validate_csv_rows.py",
}


def find_root() -> Path:
    """
    Locate the project root.

    Primary strategy: the package lives at <root>/research_os/, so
    the root is always <this file's directory's parent>.

    This is reliable for both `pip install -e .` and direct invocation
    via `python -m research_os` from the repo root.
    """
    return Path(__file__).resolve().parent.parent


def load_config(root: Path) -> Dict[str, Any]:
    """Read research.toml from root, merging with defaults for any missing keys."""
    config_path = root / "research.toml"
    if not config_path.exists():
        return _DEFAULTS.copy()

    with config_path.open("rb") as fh:
        user = tomllib.load(fh)

    merged: Dict[str, Any] = {}
    for section, defaults in _DEFAULTS.items():
        merged[section] = {**defaults, **user.get(section, {})}
    return merged


def resolve_paths(root: Path, config: Dict[str, Any]) -> Dict[str, Path]:
    """Return absolute Path objects for every configured path."""
    return {k: root / v for k, v in config["paths"].items()}


def resolve_scripts(root: Path, config: Dict[str, Any]) -> Dict[str, Path]:
    """Return absolute Path objects for every configured script, in order."""
    return {k: root / v for k, v in config["scripts"].items()}
