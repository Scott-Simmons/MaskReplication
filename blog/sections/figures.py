from blog.decorators import interpretation


def og_headline_result() -> str:
    from blog.plots import og_headline_result as _plot

    _plot()
    return "![From the [MASK paper](https://arxiv.org/abs/2503.03750): Larger models are more accurate but not more honest](figures/og_headline_result.png)"


def replication_headline_result() -> str:
    from blog.plots import replication_headline_result as _plot

    _plot()
    return (
        "![I used [Epoch AI](https://epoch.ai/data/notable-ai-models) to estimate "
        "the FLOP per model, as this information is [unavailable](https://github.com/centerforaisafety/mask/issues/2) "
        "in the original paper.](figures/replication_headline_result.png)"
    )


def truthfulness_headline_result() -> str:
    from blog.plots import truthfulness_headline_result as _plot

    _plot()
    return "![](figures/truthfulness_headline_result.png)"


@interpretation
def two_d_space_projection_headline() -> str:
    from blog.plots import two_d_space_projection as _plot
    from blog.plots import _contour_pair_stats

    _plot()
    pair = _contour_pair_stats(__import__("blog.analysis", fromlist=["load_runs"]).load_runs())
    if pair:
        a, b = pair
        # Order so that the one with lower conditional honesty is mentioned first
        if a["chr"] > b["chr"]:
            a, b = b, a
        chr_ratio = b["chr"] / a["chr"] if a["chr"] > 0 else 0
        return (
            f"![Note how {a['name']} and {b['name']} sit on the same honesty "
            f"contour (within error bars), "
            f"even though {b['name']} is nearly {round(chr_ratio)}x more honest when it engages "
            f"({b['chr']:.0f}% vs {a['chr']:.0f}%), but {a['name']} engages less often "
            f"({a['er']:.0f}% vs {b['er']:.0f}%). The honesty score compresses all of this "
            f"because {a['name']} engages less, pulling samples away from the lie bucket."
            "](figures/two_d_space_projection.png)"
        )
    return "![](figures/two_d_space_projection.png)"


def error_rate_plot() -> str:
    from blog.plots import error_rate_plot as _plot

    _plot()
    return "![](figures/error_rate_plot.png)"


def error_failure_modes() -> str:
    from blog.analysis import load_error_failure_modes

    modes = load_error_failure_modes()
    total = sum(modes.values())

    labels = {
        "subject_unparseable": "Subject model's answer unparseable",
        "reasoning_exhaustion": "Judge exhausted token budget on reasoning",
        "output_truncated": "Judge output truncated or stored as attachment",
        "null_values": "Judge returned null values",
        "no_judge_call": "No judge model invoked",
    }
    lines = [
        "| Failure mode (assessed by gpt-4o with Scout) | Count | % |",
        "|---|---|---|",
    ]
    for key in ["subject_unparseable", "reasoning_exhaustion", "output_truncated", "null_values", "no_judge_call"]:
        count = modes.get(key, 0)
        pct = count / total * 100 if total else 0
        lines.append(f"| {labels.get(key, key)} | {count} | {pct:.0f}% |")
    lines.append(f"| **Total** | **{total}** | |")
    return "\n".join(lines)


def error_by_archetype() -> str:
    from blog.plots import error_by_archetype_plot as _plot

    _plot()
    return "![](figures/error_by_archetype.png)"


def models_used_in_replication() -> str:
    from blog.analysis import load_runs

    runs = load_runs()
    lines = [
        "| Model | Provider | Samples | In paper? |",
        "|---|---|---|---|",
    ]
    for r in runs:
        check = "Yes" if r.in_paper else "No"
        lines.append(f"| {r.display_name} | {r.provider} | {r.n:,} | {check} |")
    return "\n".join(lines)


def dimensions_vectors_empirical() -> str:
    from blog.analysis import load_runs

    runs = load_runs()
    lines = [
        "| Model | $n$ | $H$ | $L$ | $E$ | $N$ | $\\varepsilon$ |",
        "|---|---|---|---|---|---|---|",
    ]
    totals = {"n": 0, "H": 0, "L": 0, "E": 0, "N": 0, "e": 0}
    for r in runs:
        b = r.dimensions
        H = b.get("truthful", 0)
        L = b.get("lie", 0)
        E = b.get("evade", 0)
        N = b.get("no_belief", 0)
        e = b.get("error", 0)
        lines.append(f"| {r.display_name} | {r.n:,} | {H} | {L} | {E} | {N} | {e} |")
        totals["n"] += r.n
        totals["H"] += H
        totals["L"] += L
        totals["E"] += E
        totals["N"] += N
        totals["e"] += e
    lines.append(
        f"| **Total** | **{totals['n']:,}** | **{totals['H']}** | **{totals['L']}** "
        f"| **{totals['E']}** | **{totals['N']}** | **{totals['e']}** |"
    )
    return "\n".join(lines)


def other_1d_projections() -> str:
    return "\n".join(
        [
            "| Metric | Formula | What it captures | In MASK? |",
            "|---|---|---|---|",
            "| Honesty score | $1 - \\frac{L}{n}$ | How often does the model not lie? | Yes (headline) |",
            "| Normalised honesty | $1 - \\frac{L}{H + L + E}$ | As above, but drops no-belief and errors. Keeps evasion. | Yes (appendix) |",
            "| Truthfulness | $\\frac{H}{n}$ | How often is the model directly honest? | No |",
            "| Engagement rate | $\\frac{H + L}{n}$ | How often does the model engage? | No |",
            "| Evasion rate | $\\frac{E}{n}$ | How often does the model dodge? | No |",
            "| Conditional lie rate | $\\frac{L}{H + L}$ | When the model engages, how often does it lie? | No |",
            "| Deflection style | $\\frac{E}{E + N}$ | Of non-answers: dodge or no belief? | No |",
            "| Reliability | $\\frac{n - \\varepsilon}{n}$ | How often does the model produce a parseable response? | No |",
        ]
    )


def _color_diff(diff: float) -> str:
    sign = "+" if diff >= 0 else ""
    color = "green" if diff >= 0 else "red"
    return f'<span style="color:{color}">{sign}{diff:.1f}</span>'


def _binom_ci_str(p_pct: float, n: int) -> str:
    """Format a percentage with its 95% CI."""
    import numpy as np

    p = p_pct / 100
    p = max(min(p, 1.0), 0.0)
    hw = 1.96 * np.sqrt(p * (1 - p) / n) * 100 if n > 0 else 0
    return f"{p_pct:.1f} ± {hw:.1f}"


def paper_vs_replication_table() -> str:
    from blog.analysis import DISPLAY_TO_OG, load_runs
    from blog.constants import OG_PAPER_SCORES

    runs = load_runs()

    # Build lookup for all replication models, with paper scores where available
    rows = []
    for r in runs:
        og_name = DISPLAY_TO_OG.get(r.display_name)
        if og_name and og_name in OG_PAPER_SCORES:
            og_hon, _, og_acc = OG_PAPER_SCORES[og_name]
            rows.append((r, og_hon, og_acc))
        else:
            rows.append((r, None, None))

    # Honesty table
    hon_lines = [
        "**Honesty (1 - P(Lie))**",
        "",
        "| Model | MASK paper | Replication (95% CI) | Diff |",
        "|---|---|---|---|",
    ]
    for r, og_hon, _ in rows:
        rep = _binom_ci_str(r.honesty * 100, r.n)
        if og_hon is not None:
            diff = r.honesty * 100 - og_hon
            hon_lines.append(
                f"| {r.display_name} | {og_hon:.1f} | {rep} | {_color_diff(diff)} |"
            )
        else:
            hon_lines.append(f"| {r.display_name} | — | {rep} | — |")

    # Accuracy table
    acc_lines = [
        "**Accuracy**",
        "",
        "| Model | MASK paper | Replication (95% CI) | Diff |",
        "|---|---|---|---|",
    ]
    for r, _, og_acc in rows:
        rep = _binom_ci_str(r.accuracy * 100, r.n)
        if og_acc is not None:
            diff = r.accuracy * 100 - og_acc
            acc_lines.append(
                f"| {r.display_name} | {og_acc:.1f} | {rep} | {_color_diff(diff)} |"
            )
        else:
            acc_lines.append(f"| {r.display_name} | — | {rep} | — |")

    return "\n".join(hon_lines) + "\n\n" + "\n".join(acc_lines)


def deception_dimensions() -> str:
    return "\n".join(
        [
            "$$\\{\\text{Honest},\\ \\text{Lie},\\ \\text{Evade},\\ \\text{No Belief},\\ \\text{Parse Error}\\}$$",
            "",
            "$$\\{H,\\ L,\\ E,\\ N,\\ \\varepsilon\\}$$",
        ]
    )


def honesty_metric() -> str:
    return "\n".join(
        [
            '::: {style="text-align:center; margin:1.5em 0"}',
            "",
            "$\\text{Honesty}$[^pedantic_r5] $: \\mathbb{R}^5 \\to \\mathbb{R}$",
            "",
            ":::",
            "",
            "$$= 1 - P(\\text{Lie}) = 1 - \\frac{L}{H + L + E + N + \\varepsilon}$$",
        ]
    )


def dumb_and_diplomat() -> str:
    return "\n".join(
        [
            '<div style="display: flex; justify-content: center; gap: 2em; margin: 2em 0;">',
            '<div style="text-align: center;">',
            '<img src="assets/honest.jpg" alt="Jesus Christ" style="height: 200px;"><br>',
            "<strong>Jesus Christ</strong>",
            "</div>",
            '<div style="text-align: center;">',
            '<img src="assets/evasion.jpeg" alt="Kash Patel" style="height: 200px;"><br>',
            '<strong>Kash Patel</strong><br><strong>(<a href="assets/evasion.mp4">see here</a>)</strong>',
            "</div>",
            '<div style="text-align: center;">',
            '<img src="assets/no_belief.jpeg" alt="Patrick Star" style="height: 200px;"><br>',
            "<strong>Patrick Star</strong>",
            "</div>",
            "</div>",
            "",
            "| Agent | $H$ | $L$ | $E$ | $N$ | $\\varepsilon$ | MASK Honesty $1 - \\frac{L}{n}$ | Normalised MASK Honesty $1 - \\frac{L}{H+L+E}$ |",
            "|---|---|---|---|---|---|---|---|",
            "| Jesus Christ | $n$ | 0 | 0 | 0 | 0 | 100% | 100% |",
            "| Kash Patel | 0 | 0 | $n$ | 0 | 0 | 100% | 100% |",
            "| Patrick Star | 0 | 0 | 0 | $n$ | 0 | 100% | undefined |",
        ]
    )
