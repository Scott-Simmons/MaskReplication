"""Generate the blog post markdown and HTML from structured sections."""

import subprocess
from pathlib import Path

from blog.sections import appendix, basis, figures, footnotes, intro, recap, replication, thanks

STRUCTURE = [
    ("# The Basis of Deception", [
        intro.tldr,
        intro.intro,
        intro.link_to_ai,
        figures.og_headline_result,
        intro.how_i_reacted,
        intro.what_i_did,
    ]),
    ("## Replication results", [
        replication.what_i_wanted_to_do,
        figures.models_used_in_replication,
        replication.differences_to_og,
        replication.interpretation,
        figures.replication_headline_result,
        replication.interpretation_new_models,
        replication.flops_note,
    ]),
    ("## The limitation of honesty scores (actually, most 1D projections!)", [
        basis.introduce_the_basis,
        figures.deception_basis,
        figures.basis_vectors_empirical,
        basis.honesty_in_terms_of_basis,
        figures.honesty_metric,
        basis.honesty_is_lossy,
        basis.interp_dumb_and_diplomatic,
        figures.dumb_and_diplomat,
        basis.empirical_lossy_demonstration,
        figures.two_d_space_projection_headline,
        basis.one_d_projections,
        figures.other_1d_projections,
        basis.more_examples_of_2d_projections,
        figures.more_2d_projections,
    ]),
    ("## Conclusion", [
        recap.recap,
        recap.encourage_the_basis_framing,
    ]),
    ("## Appendix: Paper vs replication differences", [
        appendix.paper_vs_replication,
        figures.paper_vs_replication_table,
    ]),
    (None, [
        thanks.shout_out_inspect,
        thanks.shout_out_misc,
    ]),
    (None, [
        footnotes.flops,
        footnotes.error_in_the_basis,
        footnotes.classification_basis_analogy,
        footnotes.theoretical_limit_per_basis_size,
    ]),
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
            "--metadata=title:The Basis of Deception",
        ],
        input=md_text,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    md_text = generate()
    (output_dir / "blog_post.md").write_text(md_text)
    (output_dir / "blog_post.html").write_text(generate_html(md_text))
    (output_dir / "style.css").write_text(CSS_FILE.read_text())

    print(f"Generated: {output_dir}/blog_post.md")
    print(f"Generated: {output_dir}/blog_post.html")


if __name__ == "__main__":
    main()
