"""Aggregate scout scan output into scan_logs/error_counts.json."""

import json
from collections import Counter
from pathlib import Path

from inspect_scout import scan_results_df

SCAN_DIR = Path("scan_logs")
OUTPUT = SCAN_DIR / "error_counts.json"


def _latest_scan(scan_dir: Path) -> Path:
    subdirs = sorted(
        [d for d in scan_dir.iterdir() if d.is_dir() and d.name.startswith("scan_id=")],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if not subdirs:
        raise FileNotFoundError(f"No scan_id=* directories found in {scan_dir}")
    return subdirs[0]


def aggregate() -> None:
    scan_path = _latest_scan(SCAN_DIR)
    results = scan_results_df(str(scan_path), scanner="error_scanner")
    df = results.scanners["error_scanner"]
    counts = Counter(df["answer"].dropna())
    OUTPUT.write_text(json.dumps(dict(counts), indent=2) + "\n")
    print(f"Written: {OUTPUT}  ({sum(counts.values())} errors across {len(counts)} categories)")


if __name__ == "__main__":
    aggregate()
