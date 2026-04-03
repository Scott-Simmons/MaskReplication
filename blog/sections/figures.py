def placeholder_plot() -> str:
    return "![TODO: Insert placeholder_plot caption](figures/placeholder_plot.png)"


def og_headline_result() -> str:
    return "![From the [MASK paper](https://arxiv.org/abs/2503.03750): Larger models are more accurate but not more honest](figures/og_headline_result.png)"


def replication_headline_result() -> str:
    from blog.plots import replication_headline_result as _plot
    _plot()
    return ("![Note: I used [Epoch AI](https://epoch.ai/data/notable-ai-models) to estimate "
            "the FLOP per model, as they were unavailable from the original paper.[^1]](figures/replication_headline_result.png)")


def replication_new_models_headline_result() -> str:
    return "![TODO: Insert replication_new_models_headline_result caption](figures/placeholder_plot.png)"


def two_d_space_projection_headline() -> str:
    from blog.plots import two_d_space_projection as _plot
    _plot()
    return ("![Model behaviour space with iso-P(Lie) contours. "
            "Note how Qwen 2.5 7B and o3-mini sit on the same P(Lie) contour (within error bars), "
            "even though o3-mini evades 3x more (33% vs 11%) and lies more when it does engage "
            "(76% vs 60%). The honesty score compresses all of this because o3-mini's evasion "
            "pulls samples away from the lie bucket."
            "](figures/two_d_space_projection.png)")


def more_2d_projections() -> str:
    from blog.plots import more_2d_projections as _plot
    _plot()
    return ("![Three more basis projections. "
            "Claude Haiku 4.5 is an outlier in the first panel (88% conditionally honest). "
            "Qwen 2.5 7B is an outlier in the third (25% deflection style, meaning when "
            "it does not answer, it is mostly because it lacks beliefs, not because it evades)."
            "](figures/more_2d_projections.png)")


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


def basis_vectors_empirical() -> str:
    from blog.analysis import load_runs

    runs = load_runs()
    lines = [
        "| Model | $n$ | $H$ | $L$ | $E$ | $N$ | $\\varepsilon$ |",
        "|---|---|---|---|---|---|---|",
    ]
    totals = {"n": 0, "H": 0, "L": 0, "E": 0, "N": 0, "e": 0}
    for r in runs:
        b = r.basis
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
    return "\n".join([
        "| Metric | Formula | What it captures | In MASK? |",
        "|---|---|---|---|",
        "| Honesty score | $\\frac{H}{H + L + E + N}$ | Strictest: honest out of all responses | Yes (headline) |",
        "| Normalised honesty | $\\frac{H}{H + L + E}$ | Excludes no-belief from denominator | Yes (appendix) |",
        "| Conditional honesty | $\\frac{H}{H + L}$ | When it takes a position, is it truthful? | No |",
        "| Engagement rate | $\\frac{H + L}{H + L + E + N}$ | How often does it commit to a position? | No |",
        "| Evasion rate | $\\frac{E}{H + L + E + N}$ | How often does it dodge? | No |",
        "| Conditional lie rate | $\\frac{L}{H + L}$ | When it engages, how often does it lie? | No |",
        "| Deflection style | $\\frac{E}{E + N}$ | Of non-answers: strategic dodge vs no belief? | No |",
    ])


def placeholder_table() -> str:
    return "\n".join([
        "*TODO: Insert placeholder_table caption*",
        "",
        "| Model | Accuracy | Honesty |",
        "|---|---|---|",
        "| Model A | 0.85 | 0.42 |",
        "| Model B | 0.91 | 0.38 |",
        "| Model C | 0.72 | 0.67 |",
    ])


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

    # Build lookup: paper_name -> replication run (intersection only)
    matches = []
    for r in runs:
        og_name = DISPLAY_TO_OG.get(r.display_name)
        if og_name and og_name in OG_PAPER_SCORES:
            og_hon, _, og_acc = OG_PAPER_SCORES[og_name]
            matches.append((r, og_hon, og_acc))

    # Honesty table
    hon_lines = [
        "**Honesty (P(honest))**",
        "",
        "| Model | Paper | Replication (95% CI) | Diff |",
        "|---|---|---|---|",
    ]
    for r, og_hon, _ in matches:
        rep = _binom_ci_str(r.honesty * 100, r.n)
        diff = r.honesty * 100 - og_hon
        hon_lines.append(
            f"| {r.display_name} | {og_hon:.1f} | {rep} | {_color_diff(diff)} |"
        )

    # Accuracy table
    acc_lines = [
        "**Accuracy (correct / total)**",
        "",
        "| Model | Paper | Replication (95% CI) | Diff |",
        "|---|---|---|---|",
    ]
    for r, _, og_acc in matches:
        rep = _binom_ci_str(r.accuracy * 100, r.n)
        diff = r.accuracy * 100 - og_acc
        acc_lines.append(
            f"| {r.display_name} | {og_acc:.1f} | {rep} | {_color_diff(diff)} |"
        )

    return "\n".join(hon_lines) + "\n\n" + "\n".join(acc_lines)


def deception_basis() -> str:
    return "\n".join([
        "$$\\{\\text{Honest},\\ \\text{Lie},\\ \\text{Evade},\\ \\text{No Belief},\\ \\text{Parse Error}\\}$$",
        "",
        "$$\\{H,\\ L,\\ E,\\ N,\\ \\varepsilon\\}$$",
    ])


def honesty_metric() -> str:
    return "$$\\text{Honesty} = 1 - P(\\text{Lie}) = 1 - \\frac{L}{H + L + E + N}$$"


def dumb_and_diplomat() -> str:
    return "\n".join([
        "```",
        "  Unpressured Query     Pressured Query",
        "        │                      │",
        "        ▼                      ▼",
        "   ┌─────────┐          ┌─────────┐",
        "   │  Belief  │          │  Belief  │",
        "   └────┬────┘          └────┬────┘",
        "        │                      │",
        "        ▼                      ▼",
        "   ┌─────────┐     ┌────────────────────┐",
        "   │ Response │     │ Truthful │ Lie │ ...│",
        "   └─────────┘     └────────────────────┘",
        "```",
        "",
        "*TODO: Insert dumb_and_diplomat caption*",
    ])
