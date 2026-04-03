"""Generate the blog post markdown from structured sections."""

from pathlib import Path

from blog.sections import basis, footnotes, intro, recap, replication, thanks

STRUCTURE = [
    ("# The Basis of Deception", [
        intro.tldr,
        intro.intro,
        intro.link_to_ai,
        intro.how_i_reacted,
        intro.what_i_did,
    ]),
    ("## Replication results", [
        replication.what_i_wanted_to_do,
        replication.differences_to_og,
        replication.interpretation,
        replication.interpretation_new_models,
    ]),
    ("## The limitation of honesty scores", [
        basis.introduce_the_basis,
        basis.honesty_in_terms_of_basis,
        basis.honesty_is_lossy,
        basis.interp_dumb_and_diplomatic,
        basis.empirical_lossy_demonstration,
        basis.more_examples_of_2d_projections,
    ]),
    ("## Conclusion", [
        recap.recap,
        recap.encourage_the_basis_framing,
    ]),
    (None, [
        thanks.shout_out_inspect,
        thanks.shout_out_misc,
    ]),
    ("## Footnotes", [
        footnotes.flops,
        footnotes.error_in_the_basis,
        footnotes.classification_basis_analogy,
        footnotes.theoretical_limit_per_basis_size,
    ]),
]


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


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "blog_post.md"
    output_path.write_text(generate())
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
