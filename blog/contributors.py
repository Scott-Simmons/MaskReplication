"""Fetch MASK eval contributors from GitHub issues."""

import json
import subprocess
from pathlib import Path

CACHE_FILE = Path(__file__).parent.parent / "contributors_cache.json"

REPO = "UKGovernmentBEIS/inspect_evals"
LABEL = "eval:MASK"

# Eval reviewers (thanked separately in the footer).
REVIEWERS = [
    {"name": "Nelson Gardner-Challis", "login": "NelsonG-C"},
    {"name": "Matt Fisher", "login": "mattfisher"},
    {"name": "Celia Waggoner", "login": "celiawaggoner"},
    {"name": "Dan Wilhelm", "login": "danwilhelm"},
    {"name": "Jay Bailey", "login": "Jay-Bailey"},
]

# Exclude: the blog author and anyone already thanked as a reviewer.
EXCLUDE_LOGINS = {"Scott-Simmons"} | {r["login"] for r in REVIEWERS}


def _fetch_from_gh() -> list[dict[str, str]]:
    """Fetch issue authors from GitHub CLI, return [{"login": ..., "name": ...}]."""
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--repo", REPO,
            "--label", LABEL,
            "--state", "all",
            "--json", "author",
            "--limit", "100",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    issues = json.loads(result.stdout)
    seen = set()
    contributors = []
    for issue in issues:
        author = issue.get("author", {})
        login = author.get("login", "")
        if login and login not in seen and login not in EXCLUDE_LOGINS and not author.get("is_bot"):
            seen.add(login)
            contributors.append({"login": login, "name": author.get("name", "")})
    return contributors


def get_contributors() -> list[dict[str, str]]:
    """Get contributors, trying GitHub first then falling back to cache."""
    contributors = _fetch_from_gh()
    if contributors:
        CACHE_FILE.write_text(json.dumps(contributors, indent=2))
        return contributors
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return []


def _format_names(people: list[dict[str, str]]) -> str:
    """Format a list of {"name": ..., "login": ...} as linked names."""
    parts = [f'<a href="https://github.com/{p["login"]}">{p["name"] or p["login"]}</a>' for p in people]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def reviewers_thanks_html() -> str:
    """Generate a thanks <p> tag for eval reviewers."""
    names = _format_names(REVIEWERS)
    return (
        f'<p>Thanks to {names} for reviewing the '
        f'<a href="https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/">MASK eval for Inspect AI</a>.</p>'
    )


def contributors_thanks_html() -> str:
    """Generate a thanks <p> tag for issue contributors, or empty string if none."""
    contributors = get_contributors()
    if not contributors:
        return ""
    names = _format_names(contributors)
    return (
        f"<p>Thanks to {names} for raising issues that improved the "
        f'<a href="https://github.com/{REPO}/labels/{LABEL.replace(":", "%3A")}">MASK eval</a>.</p>'
    )
