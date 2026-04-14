"""Blog post versioning and changelog."""

VERSION = "2"

# (version, date, [items])
CHANGELOG: list[tuple[str, str, list[str]]] = [
    ("2", "2026-04-13", ["Change the title"]),
    ("1", "2026-04-13", ["Initial blog post publication"]),
]
