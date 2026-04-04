"""Generate the blog post markdown and HTML from structured sections."""

import subprocess
from pathlib import Path

from blog.sections import appendix, dimensions, figures, footnotes, intro, recap, replication

STRUCTURE = [
    (
        "# Mapping Deception",
        [
            intro.tldr,
            intro.toc,
        ],
    ),
    (
        "## 1. Introduction",
        [
            intro.intro,
            intro.link_to_ai,
            figures.og_headline_result,
            intro.how_i_reacted,
            intro.what_i_will_do,
        ],
    ),
    (
        "## 2. Replication results",
        [
            replication.what_i_wanted_to_do,
            figures.models_used_in_replication,
            replication.differences_to_og,
            replication.interpretation,
            figures.replication_headline_result,
        ],
    ),
    (
        "## 3. Dimensions of deception",
        [
            dimensions.preamble,
            dimensions.introduce_the_dimensions,
            figures.deception_dimensions,
            dimensions.empirical_dimensions_intro,
            figures.dimensions_vectors_empirical,
            dimensions.honesty_in_terms_of_dimensions,
            figures.honesty_metric,
            dimensions.honesty_is_lossy,
            dimensions.hypothetical_subheader,
            dimensions.interp_dumb_and_diplomatic,
            figures.dumb_and_diplomat,
            dimensions.making_this_empirical_subheader,
            dimensions.empirical_lossy_demonstration,
            figures.two_d_space_projection_headline,
            dimensions.one_d_projections,
            figures.other_1d_projections,
            dimensions.truthfulness_argument,
            dimensions.headline_still_holds,
            figures.truthfulness_headline_result,
            dimensions.communicating_uncertainty_subheader,
            dimensions.more_examples_of_2d_projections,
            figures.more_2d_projections,
            dimensions.more_2d_projections_commentary,
        ],
    ),
    (
        "## 4. Try it yourself",
        [
            recap.recap,
        ],
    ),
    (
        "## Appendix: Paper vs replication differences",
        [
            appendix.paper_vs_replication,
            figures.paper_vs_replication_table,
        ],
    ),
    (
        None,
        [
            footnotes.internal_beliefs,
            footnotes.classification_dimensions_analogy,
            footnotes.open_questions,
            footnotes.pedantic_r5,
        ],
    ),
]

CSS_FILE = Path(__file__).parent / "style.css"


def generate() -> str:
    parts: list[str] = []
    for heading, blocks in STRUCTURE:
        if heading is not None:
            parts.append(heading)
        parts.append("---" if heading and heading.startswith("# ") else "")
        for block in blocks:
            parts.append(block())
        parts.append("---")
    # Remove trailing --- and any empty strings, then rejoin
    while parts and parts[-1] in ("---", ""):
        parts.pop()
    return "\n\n".join(part for part in parts if part) + "\n"


def generate_html(md_text: str) -> str:
    result = subprocess.run(
        [
            "pandoc",
            "--from=markdown",
            "--to=html",
            "--mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
            "--css=style.css",
            "--standalone",
            "--metadata=title:Mapping Deception",
        ],
        input=md_text,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def main() -> None:
    output_dir = Path("build")
    output_dir.mkdir(exist_ok=True)

    md_text = generate()
    (output_dir / "blog_post.md").write_text(md_text)
    (output_dir / "blog_post.html").write_text(generate_html(md_text))
    (output_dir / "style.css").write_text(CSS_FILE.read_text())

    print(f"Generated: {output_dir}/blog_post.md")
    print(f"Generated: {output_dir}/blog_post.html")


if __name__ == "__main__":
    main()
