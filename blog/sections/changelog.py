"""Changelog section for the blog post."""

from blog.version import VERSION


def changelog() -> str:
    """Full changelog page content in Keep a Changelog format."""
    from blog.version import CHANGELOG

    lines = [
        "## Changelog",
        "",
        f"[← Back to current version (v{VERSION})](index.html)",
        "",
    ]
    for version, date, items in CHANGELOG:
        lines.append(f"### [{version}](versions/{version}/index.html) - {date}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def version_stamp() -> str:
    """Inline version stamp with link to changelog, for the bottom of the post."""
    return f"Version {VERSION} ([changelog](changelog.html))"
