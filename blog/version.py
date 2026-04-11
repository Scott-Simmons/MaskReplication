"""Blog post versioning and changelog."""

VERSION = "2"

# (version, date, [items])
CHANGELOG: list[tuple[str, str, list[str]]] = [
    ("2", "2026-04-12", [
        "Add P(honest) and P(lie) comparison tables to appendix",
        "Fix changelog back-link",
        "Byline links to sdsimmons.com",
    ]),
    ("1", "2026-04-05", ["Initial blog post publication"]),
]
