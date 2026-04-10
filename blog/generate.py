"""Generate the blog post markdown and HTML from structured sections."""

import shutil
import subprocess
import sys
from pathlib import Path

from blog.sections import (
    appendix,
    changelog,
    dimensions,
    figures,
    footnotes,
    intro,
    recap,
    replication,
)

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
            intro.accuracy_vs_honesty,
            figures.elon_tweet,
            intro.mask_contribution,
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
            replication.caveat,
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
            figures.dumb_and_diplomat,
            dimensions.hypothetical_commentary,
            dimensions.making_this_empirical_subheader,
            dimensions.empirical_lossy_demonstration,
            figures.two_d_space_projection_headline,
            dimensions.what_else_subheader,
            dimensions.one_d_projections,
            figures.other_1d_projections,
            dimensions.truthfulness_argument,
            dimensions.headline_still_holds,
            figures.truthfulness_headline_result,
        ],
    ),
    (
        "## 4. Reporting errors and uncertainty",
        [
            dimensions.errors_intro,
            dimensions.transient_errors_subheader,
            dimensions.transient_errors_body,
            dimensions.parse_errors_subheader,
            dimensions.parse_errors_intro,
            dimensions.parse_error_example,
            dimensions.parse_errors_investigation,
            dimensions.parse_errors_scout,
            dimensions.scout_invocation,
            figures.error_failure_modes,
            dimensions.parse_errors_not_random,
            figures.error_by_archetype,
            dimensions.parse_errors_explanation,
            dimensions.sampling_uncertainty_subheader,
            dimensions.sampling_uncertainty_intro,
            dimensions.uncertainty_concrete_example,
            figures.error_rate_plot,
        ],
    ),
    (
        "## 5. Try it yourself",
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
            footnotes.llm_judge_squared,
            footnotes.clustering,
            footnotes.contour_math,
        ],
    ),
]

CSS_FILE = Path(__file__).parent / "style.css"
ASSETS_DIR = Path(__file__).parent / "assets"


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


def check_review() -> None:
    """Fail the build if any decorated sections need review."""
    from blog.review import sections_needing_review

    needs = sections_needing_review()
    if needs:
        print("ERROR: The following sections need review before building:\n")
        for qname, _, dec_names in needs:
            print(f"  - {qname}  [{', '.join(dec_names)}]")
        print("\nRun 'make review' to approve them for the current version.")
        sys.exit(1)


def main() -> None:
    check_review()

    output_dir = Path("build")
    output_dir.mkdir(exist_ok=True)

    md_text = generate()
    (output_dir / "blog_post.md").write_text(md_text)
    html_text = generate_html(md_text)
    # Inject version stamp at the very bottom, after pandoc renders footnotes
    from blog.version import VERSION, CHANGELOG

    version_label = (
        f"{VERSION}+dev" if Path(f"versions/{VERSION}").exists() else VERSION
    )
    # Find the date for the current version
    version_date = next((date for v, date, _ in CHANGELOG if v == VERSION), "")
    paper_bibtex = (
        "@misc{ren2025maskbenchmarkdisentanglinghonesty,\n"
        "      title={The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems},\n"
        "      author={Richard Ren and Arunim Agarwal and Mantas Mazeika and Cristina Menghini and Robert Vacareanu and Brad Kenstler and Mick Yang and Isabelle Barrass and Alice Gatti and Xuwang Yin and Eduardo Trevino and Matias Geralnik and Adam Khoja and Dean Lee and Summer Yue and Dan Hendrycks},\n"
        "      year={2025},\n"
        "      eprint={2503.03750},\n"
        "      archivePrefix={arXiv},\n"
        "      primaryClass={cs.LG},\n"
        "      url={https://arxiv.org/abs/2503.03750},\n"
        "}"
    )
    blog_bibtex = (
        "@misc{simmons2025mappingdeception,\n"
        "      title={Mapping Deception},\n"
        "      author={Scott Simmons},\n"
        "      year={2025},\n"
        "      url={TODO: final hosted URL},\n"
        "      note={Blog post, code, and eval logs available at https://github.com/Scott-Simmons/MaskReplication},\n"
        "}"
    )
    inspect_mask_bibtex = (
        "@misc{simmons2025inspectmask,\n"
        "      title={MASK Eval for Inspect AI},\n"
        "      author={Scott Simmons},\n"
        "      year={2025},\n"
        "      url={https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/},\n"
        "      note={Inspect AI evaluation implementation},\n"
        "}"
    )
    details_style = 'style="margin-top:0.5em;"'
    summary_style = 'style="cursor:pointer;"'
    pre_style = 'style="text-align:left; display:inline-block; margin-top:0.5em; font-size:0.8em; color:#666;"'
    version_html = (
        '<footer style="text-align:center; margin-top:4em; padding-top:1.5em; border-top:1px solid #eee; color:#999; font-size:0.85em;">'
        '<p>Thanks to Nelson Gardner-Challis, Matt Fisher, Celia Waggoner, and Dan Wilhelm for reviewing the <a href="https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/">MASK eval for Inspect AI</a>.</p>'
        f'<p>Version {version_label} · {version_date} · <a href="changelog.html">changelog</a></p>'
        f"<details {details_style}><summary {summary_style}>cite this post</summary>"
        f"<pre {pre_style}>{blog_bibtex}</pre></details>"
        f"<details {details_style}><summary {summary_style}>cite the MASK eval for Inspect AI</summary>"
        f"<pre {pre_style}>{inspect_mask_bibtex}</pre></details>"
        f"<details {details_style}><summary {summary_style}>cite the MASK paper</summary>"
        f"<pre {pre_style}>{paper_bibtex}</pre></details>"
        "</footer>"
    )
    html_text = html_text.replace("</body>", f"{version_html}\n</body>")
    (output_dir / "blog_post.html").write_text(html_text)
    (output_dir / "index.html").write_text(html_text)
    (output_dir / "style.css").write_text(CSS_FILE.read_text())

    changelog_md = changelog.changelog()
    changelog_html = generate_html(changelog_md)
    (output_dir / "changelog.html").write_text(changelog_html)

    assets_dst = output_dir / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(ASSETS_DIR, assets_dst)

    # Copy archived versions into build if they exist
    versions_src = Path("versions")
    if versions_src.exists():
        versions_dst = output_dir / "versions"
        if versions_dst.exists():
            shutil.rmtree(versions_dst)
        shutil.copytree(versions_src, versions_dst)

    print(f"Generated: {output_dir}/blog_post.md")
    print(f"Generated: {output_dir}/blog_post.html")
    print(f"Generated: {output_dir}/changelog.html")


if __name__ == "__main__":
    main()
