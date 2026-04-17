"""Blog post versioning and changelog."""

VERSION = "3"

# (version, date, [items])
CHANGELOG: list[tuple[str, str, list[str]]] = [
    (
        "3",
        "2026-04-17",
        [
            "Switch the replication-vs-paper callout to use MASK honesty (1 − P(lie)) rather than P(honest)",
            "Soften the Anthropic-another-league line with a Scale-AI / Haiku-4.5 caveat",
            "Tidy the install parenthetical in the Try-it-yourself section",
            "Add a footer thanks to CAIS, Scale AI, and the MASK authors",
        ],
    ),
    ("2", "2026-04-13", ["Change the title"]),
    ("1", "2026-04-13", ["Initial blog post publication"]),
]
