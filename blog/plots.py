"""Generate plots for the blog post."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import shutil


from blog.analysis import PROVIDER_COLORS, load_errors_by_archetype, load_runs

OUTPUT_DIR = Path("build/figures")


def og_headline_result() -> None:
    """Get OG headline result"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source = "blog/og_headline_result.png"
    shutil.copy2(source, OUTPUT_DIR)


def replication_headline_result() -> None:
    """Reproduce Figure 7: Accuracy and Honesty vs log10(FLOP), coloured by provider."""
    runs = load_runs()

    # Filter to models with FLOP data
    runs_with_flop = [r for r in runs if r.log10_flop is not None]

    x = np.array([r.log10_flop for r in runs_with_flop])
    y_acc = np.array([r.accuracy * 100 for r in runs_with_flop])
    y_hon = np.array([r.honesty * 100 for r in runs_with_flop])
    providers = [r.provider for r in runs_with_flop]
    names = [r.display_name for r in runs_with_flop]
    confidences = [r.flop_confidence for r in runs_with_flop]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle("Replication: Accuracy and Honesty", fontsize=13, y=0.98)

    for ax, y, ylabel, title_side in [
        (ax1, y_acc, "Accuracy", "left"),
        (ax2, y_hon, "Honesty Score", "right"),
    ]:
        # Regression line + confidence band
        slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
        x_line = np.linspace(x.min() - 0.1, x.max() + 0.1, 100)
        y_line = slope * x_line + intercept

        # Confidence band (95%)
        n_pts = len(x)
        x_mean = x.mean()
        se = np.sqrt(np.sum((y - (slope * x + intercept)) ** 2) / (n_pts - 2))
        h = np.sqrt(1 / n_pts + (x_line - x_mean) ** 2 / np.sum((x - x_mean) ** 2))
        ci = 1.96 * se * h

        # Spearman correlation
        rho, _ = stats.spearmanr(x, y)

        # Band colour based on sign
        band_color = "#c8e6c9" if rho > 0 else "#ffcdd2"
        line_color = "#388e3c" if rho > 0 else "#c62828"

        ax.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.3, color=band_color)
        ax.plot(x_line, y_line, color=line_color, linewidth=1.5, alpha=0.7)

        # Scatter points coloured by provider
        plotted_providers = set()
        for xi, yi, prov, name, conf in zip(x, y, providers, names, confidences):
            color = PROVIDER_COLORS.get(prov, "#999999")
            marker = "o" if conf == "confident" else "D"
            label = prov if prov not in plotted_providers else None
            plotted_providers.add(prov)
            ax.scatter(
                xi,
                yi,
                c=color,
                s=50,
                zorder=5,
                label=label,
                marker=marker,
                edgecolors="white",
                linewidths=0.5,
            )

        # Correlation box
        sign = "+" if rho > 0 else ""
        box_bg = "#e8f5e9" if rho > 0 else "#ffebee"
        box_text_color = "#2e7d32" if rho > 0 else "#b71c1c"
        ax.text(
            0.5,
            0.05,
            f"Correlation: {sign}{rho:.1%}",
            transform=ax.transAxes,
            fontsize=9,
            ha="center",
            va="bottom",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor=box_bg,
                edgecolor=box_text_color,
                alpha=0.9,
            ),
            color=box_text_color,
        )

        ax.set_xlabel(r"$\log_{10}$(FLOP)", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, alpha=0.2)

    # Single legend for both panels
    handles, labels = ax1.get_legend_handles_labels()
    # Add handles from ax2 for providers only in right panel
    h2, l2 = ax2.get_legend_handles_labels()
    for h, l in zip(h2, l2):
        if l not in labels:
            handles.append(h)
            labels.append(l)

    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=len(set(providers)),
        fontsize=9,
        frameon=True,
        bbox_to_anchor=(0.5, -0.02),
    )

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT_DIR / "replication_headline_result.png", dpi=200, bbox_inches="tight"
    )
    plt.close(fig)


def truthfulness_headline_result() -> None:
    """Reproduce headline plot but with Truthfulness (H/total) instead of Honesty (1-L/total)."""
    runs = load_runs()

    runs_with_flop = [r for r in runs if r.log10_flop is not None]

    x = np.array([r.log10_flop for r in runs_with_flop])
    y_acc = np.array([r.accuracy * 100 for r in runs_with_flop])
    y_truth = np.array([r.truthfulness * 100 for r in runs_with_flop])
    providers = [r.provider for r in runs_with_flop]
    names = [r.display_name for r in runs_with_flop]
    confidences = [r.flop_confidence for r in runs_with_flop]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle("Replication: Accuracy and Truthfulness", fontsize=13, y=0.98)

    for ax, y, ylabel, title_side in [
        (ax1, y_acc, "Accuracy", "left"),
        (ax2, y_truth, "Truthfulness (H / n)", "right"),
    ]:
        slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
        x_line = np.linspace(x.min() - 0.1, x.max() + 0.1, 100)
        y_line = slope * x_line + intercept

        n_pts = len(x)
        x_mean = x.mean()
        se = np.sqrt(np.sum((y - (slope * x + intercept)) ** 2) / (n_pts - 2))
        h = np.sqrt(1 / n_pts + (x_line - x_mean) ** 2 / np.sum((x - x_mean) ** 2))
        ci = 1.96 * se * h

        rho, _ = stats.spearmanr(x, y)

        band_color = "#c8e6c9" if rho > 0 else "#ffcdd2"
        line_color = "#388e3c" if rho > 0 else "#c62828"

        ax.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.3, color=band_color)
        ax.plot(x_line, y_line, color=line_color, linewidth=1.5, alpha=0.7)

        plotted_providers = set()
        for xi, yi, prov, name, conf in zip(x, y, providers, names, confidences):
            color = PROVIDER_COLORS.get(prov, "#999999")
            marker = "o" if conf == "confident" else "D"
            label = prov if prov not in plotted_providers else None
            plotted_providers.add(prov)
            ax.scatter(
                xi,
                yi,
                c=color,
                s=50,
                zorder=5,
                label=label,
                marker=marker,
                edgecolors="white",
                linewidths=0.5,
            )

        sign = "+" if rho > 0 else ""
        box_bg = "#e8f5e9" if rho > 0 else "#ffebee"
        box_text_color = "#2e7d32" if rho > 0 else "#b71c1c"
        ax.text(
            0.5,
            0.05,
            f"Correlation: {sign}{rho:.1%}",
            transform=ax.transAxes,
            fontsize=9,
            ha="center",
            va="bottom",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor=box_bg,
                edgecolor=box_text_color,
                alpha=0.9,
            ),
            color=box_text_color,
        )

        ax.set_xlabel(r"$\log_{10}$(FLOP)", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, alpha=0.2)

    handles, labels = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    for h, l in zip(h2, l2):
        if l not in labels:
            handles.append(h)
            labels.append(l)

    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=len(set(providers)),
        fontsize=9,
        frameon=True,
        bbox_to_anchor=(0.5, -0.02),
    )

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT_DIR / "truthfulness_headline_result.png", dpi=200, bbox_inches="tight"
    )
    plt.close(fig)


def two_d_space_projection() -> None:
    """2D behavior space: Engagement Rate vs Conditional Honesty Rate, with exact iso-honesty contours."""
    runs = load_runs()

    # x = Conditional Honesty Rate: H/(H+L) — "when it engages, how often is it honest?"
    # y = Engagement Rate: (H+L)/n       — "how often does it take a stance?"
    # Honesty = 1 - (1 - x/100)*(y/100), exactly.
    engagement_rates = []
    cond_honesty_rates = []
    engagement_ns = []
    cond_honesty_ns = []
    providers = []
    names = []

    for r in runs:
        b = r.dimensions
        H = b.get("truthful", 0)
        L = b.get("lie", 0)
        engaged = H + L

        er = (engaged / r.n * 100) if r.n > 0 else 0
        chr_ = (H / engaged * 100) if engaged > 0 else 0

        engagement_rates.append(er)
        cond_honesty_rates.append(chr_)
        engagement_ns.append(r.n)
        cond_honesty_ns.append(engaged)
        providers.append(r.provider)
        names.append(r.display_name)

    x = np.array(cond_honesty_rates)
    y = np.array(engagement_rates)
    x_ci = np.array([_binom_ci(xv, n) for xv, n in zip(cond_honesty_rates, cond_honesty_ns)])
    y_ci = np.array([_binom_ci(yv, n) for yv, n in zip(engagement_rates, engagement_ns)])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Exact iso-honesty contours: Honesty = 1 - (1 - x/100)*(y/100)
    # So (1 - x/100)*(y/100) = 1 - h  →  y = (1-h)*10000/(100-x)
    x_cont = np.linspace(0, 99, 300)
    contour_levels = [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
    for h in contour_levels:
        p_lie = 1 - h
        y_cont = p_lie * 10000 / (100 - x_cont)
        y_cont = np.where((y_cont >= 0) & (y_cont <= 100), y_cont, np.nan)
        ax.plot(x_cont, y_cont, color="#bbb", linestyle=":", linewidth=0.8, alpha=0.7)
        # Only label the smallest and largest contours
        if h == contour_levels[0] or h == contour_levels[-1]:
            # Place 35% label higher (near top-left), others near bottom
            target_y = 85 if h == contour_levels[0] else 30
            label_x = 100 - p_lie * 10000 / target_y
            label_y = target_y
            if label_x < 8:
                label_x = 8
                label_y = p_lie * 10000 / (100 - label_x)
            if 5 < label_x < 98 and 25 < label_y < 95:
                ax.text(
                    label_x, label_y, f" Honesty={h:.0%}",
                    fontsize=6, color="#999", va="center", ha="left",
                    bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.8),
                )

    # Find two models with most similar honesty but most different conditional honesty
    # to dynamically highlight the "same contour, different decomposition" point
    highlight_pair = _find_contour_pair(runs)
    if highlight_pair:
        h_highlight = np.mean([r.honesty for r in highlight_pair])
        p_lie_h = 1 - h_highlight
        y_highlight = p_lie_h * 10000 / (100 - x_cont)
        y_highlight = np.where((y_highlight >= 0) & (y_highlight <= 100), y_highlight, np.nan)
        ax.plot(x_cont, y_highlight, color="#e63946", linestyle=":", linewidth=1.2, alpha=0.6)
        # Red label for the highlighted contour
        label_y_h = 30
        label_x_h = 100 - p_lie_h * 10000 / label_y_h
        if label_x_h < 8:
            label_x_h = 8
            label_y_h = p_lie_h * 10000 / (100 - label_x_h)
        if 5 < label_x_h < 98 and 25 < label_y_h < 95:
            ax.text(
                label_x_h, label_y_h, f" Honesty={h_highlight:.0%}",
                fontsize=6, color="#e63946", va="center", ha="left",
                bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.8),
            )

    # Scatter points coloured by provider with error bars
    plotted_providers = set()
    for xi, yi, xci, yci, prov, name in zip(x, y, x_ci, y_ci, providers, names):
        color = PROVIDER_COLORS.get(prov, "#999999")
        label = prov if prov not in plotted_providers else None
        plotted_providers.add(prov)
        ax.errorbar(
            xi,
            yi,
            xerr=xci,
            yerr=yci,
            fmt="none",
            ecolor=color,
            alpha=0.3,
            linewidth=1.2,
            capsize=2,
            zorder=4,
        )
        ax.scatter(
            xi,
            yi,
            c=color,
            s=60,
            zorder=5,
            label=label,
            edgecolors="white",
            linewidths=0.5,
        )
        ax.annotate(
            name,
            (xi, yi),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=7,
            color="#555",
        )

    # Drop lines for the highlighted pair
    if highlight_pair:
        highlight_names = {r.display_name for r in highlight_pair}
        for xi, yi, name_i in zip(x, y, names):
            if name_i in highlight_names:
                ax.plot([xi, xi], [ax.get_ylim()[0], yi], color="#e63946", linestyle=":", linewidth=0.7, alpha=0.5, zorder=1)
                ax.plot([ax.get_xlim()[0], xi], [yi, yi], color="#e63946", linestyle=":", linewidth=0.7, alpha=0.5, zorder=1)

    # Quadrant labels
    ax.text(
        0.98,
        0.98,
        "Engaged + Honest",
        transform=ax.transAxes,
        fontsize=8,
        color="#2e7d32",
        fontstyle="italic",
        alpha=0.7,
        ha="right",
        va="top",
    )
    ax.text(
        0.02,
        0.98,
        "Engaged + Deceptive",
        transform=ax.transAxes,
        fontsize=8,
        color="#b71c1c",
        fontstyle="italic",
        alpha=0.7,
        va="top",
    )
    ax.text(
        0.98,
        0.02,
        "Disengaged + Honest",
        transform=ax.transAxes,
        fontsize=8,
        color="#2e7d32",
        fontstyle="italic",
        alpha=0.7,
        ha="right",
    )
    ax.text(
        0.02,
        0.02,
        "Disengaged + Deceptive",
        transform=ax.transAxes,
        fontsize=8,
        color="#b71c1c",
        fontstyle="italic",
        alpha=0.7,
    )

    ax.set_xlabel(r"Conditional Honesty Rate: $\frac{H}{H + L}$ %", fontsize=11)
    ax.set_ylabel(r"Engagement Rate: $\frac{H + L}{n}$ %", fontsize=11)
    # Directional arrows as secondary labels
    ax.text(
        0.5,
        -0.2,
        r"← Deceptive when engaged | Honest when engaged →",
        transform=ax.transAxes,
        fontsize=9,
        ha="center",
        color="#777",
    )
    ax.text(
        -0.2,
        0.5,
        r"← Disengaged | Engaged →",
        transform=ax.transAxes,
        fontsize=9,
        ha="center",
        va="center",
        color="#777",
        rotation=90,
    )
    ax.set_title("One View of the Outcome Space", fontsize=13)
    ax.legend(
        loc="upper left",
        fontsize=9,
        frameon=True,
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0,
    )
    ax.set_xlim(5, 100)
    ax.set_ylim(25, 95)

    fig.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "two_d_space_projection.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def _find_contour_pair(runs):
    """Find the pair of models with most similar honesty but most different conditional honesty rate.

    Returns the two ModelRun objects, or None if < 2 models.
    """
    if len(runs) < 2:
        return None
    best_pair = None
    best_score = -1
    for i, r1 in enumerate(runs):
        for r2 in runs[i + 1 :]:
            b1, b2 = r1.dimensions, r2.dimensions
            eng1 = b1.get("truthful", 0) + b1.get("lie", 0)
            eng2 = b2.get("truthful", 0) + b2.get("lie", 0)
            if eng1 == 0 or eng2 == 0:
                continue
            chr1 = b1.get("truthful", 0) / eng1
            chr2 = b2.get("truthful", 0) / eng2
            honesty_diff = abs(r1.honesty - r2.honesty)
            chr_diff = abs(chr1 - chr2)
            # We want small honesty_diff and large chr_diff
            if honesty_diff < 0.05 and chr_diff > best_score:
                best_score = chr_diff
                best_pair = (r1, r2)
    return best_pair


def _contour_pair_stats(runs):
    """Return (model_a, model_b, stats_dict) for the best contour pair, or None."""
    pair = _find_contour_pair(runs)
    if not pair:
        return None
    r1, r2 = pair
    results = []
    for r in (r1, r2):
        b = r.dimensions
        H = b.get("truthful", 0)
        L = b.get("lie", 0)
        eng = H + L
        results.append({
            "name": r.display_name,
            "honesty": r.honesty * 100,
            "chr": H / eng * 100 if eng > 0 else 0,
            "er": eng / r.n * 100 if r.n > 0 else 0,
        })
    return results[0], results[1]


def _binom_ci(p_pct: float, n: int, z: float = 1.96) -> float:
    """95% CI half-width (in %) for a proportion p (given in %) from n trials."""
    if n <= 0:
        return 0.0
    p = p_pct / 100
    p = max(min(p, 1.0), 0.0)
    return z * np.sqrt(p * (1 - p) / n) * 100


def _iso_hyperbolas(ax, levels, label_prefix):
    """Draw iso-lines of form y = c/x (e.g. iso-P(honest) = engagement × cond_honesty)."""
    x_line = np.linspace(5, 100, 200)
    for c in levels:
        # c = x * y / 100 (both in %), so y = c * 100 / x
        y_line = c * 100 / x_line
        y_line = np.where(y_line <= 100, y_line, np.nan)
        ax.plot(x_line, y_line, color="#bbb", linestyle=":", linewidth=0.7, alpha=0.6)
        # Label where curve enters visible area
        label_x = max(c * 100 / 95, 8)  # where y ≈ 95 or x = 8
        label_y = c * 100 / label_x
        if 5 < label_y < 95:
            ax.text(
                label_x,
                label_y,
                f" {label_prefix}={c}%",
                fontsize=5.5,
                color="#aaa",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.1",
                    facecolor="white",
                    edgecolor="none",
                    alpha=0.8,
                ),
            )


def _iso_diagonals(ax, levels, label_prefix):
    """Draw iso-lines of form x + y = c (e.g. iso-non-engagement)."""
    for c in levels:
        x_line = np.array([0, c])
        y_line = np.array([c, 0])
        ax.plot(x_line, y_line, color="#bbb", linestyle=":", linewidth=0.7, alpha=0.6)
        # Label near midpoint
        mid_x = c / 2
        mid_y = c / 2
        if mid_x < 45 and mid_y < 45:
            ax.text(
                mid_x,
                mid_y + 1,
                f"{label_prefix}={c}%",
                fontsize=5.5,
                color="#aaa",
                va="bottom",
                ha="center",
                bbox=dict(
                    boxstyle="round,pad=0.1",
                    facecolor="white",
                    edgecolor="none",
                    alpha=0.8,
                ),
            )


def error_rate_plot() -> None:
    """Truthfulness vs Error Rate: compare models on x, but trust that comparison less when y is high."""
    runs = load_runs()

    data = []
    for r in runs:
        b = r.dimensions
        H = b.get("truthful", 0)
        eps = b.get("error", 0)
        data.append({
            "name": r.display_name,
            "provider": r.provider,
            "truthfulness": (H / r.n * 100) if r.n > 0 else 0,
            "truthfulness_n": r.n,
            "error_rate": (eps / r.n * 100) if r.n > 0 else 0,
            "error_rate_n": r.n,
        })

    fig, ax = plt.subplots(figsize=(8, 6))

    x_vals = np.array([d["truthfulness"] for d in data])
    y_vals = np.array([d["error_rate"] for d in data])
    x_ci = np.array([_binom_ci(d["truthfulness"], d["truthfulness_n"]) for d in data])
    y_ci = np.array([_binom_ci(d["error_rate"], d["error_rate_n"]) for d in data])

    plotted_providers = set()
    for d, xi, yi, xci, yci in zip(data, x_vals, y_vals, x_ci, y_ci):
        color = PROVIDER_COLORS.get(d["provider"], "#999999")
        label = d["provider"] if d["provider"] not in plotted_providers else None
        plotted_providers.add(d["provider"])
        ax.errorbar(xi, yi, xerr=xci, yerr=yci, fmt="none", ecolor=color,
                     alpha=0.3, linewidth=1.2, capsize=2, zorder=4)
        ax.scatter(xi, yi, c=color, s=60, zorder=5, label=label,
                   edgecolors="white", linewidths=0.5)
        ax.annotate(d["name"], (xi, yi), textcoords="offset points",
                    xytext=(6, 6), fontsize=7, color="#555")

    # Quadrant labels
    ax.text(0.98, 0.02, "Truthful + Reliable", transform=ax.transAxes,
            fontsize=8, color="#2e7d32", fontstyle="italic", alpha=0.7, ha="right")
    ax.text(0.02, 0.02, "Untruthful + Reliable", transform=ax.transAxes,
            fontsize=8, color="#b71c1c", fontstyle="italic", alpha=0.7)
    ax.text(0.98, 0.98, "Truthful + Broken", transform=ax.transAxes,
            fontsize=8, color="#e65100", fontstyle="italic", alpha=0.7, ha="right", va="top")
    ax.text(0.02, 0.98, "Untruthful + Broken", transform=ax.transAxes,
            fontsize=8, color="#b71c1c", fontstyle="italic", alpha=0.7, va="top")

    ax.set_xlabel(r"Truthfulness: $\frac{H}{n}$ %", fontsize=11)
    ax.set_ylabel(r"Error Rate: $\frac{\varepsilon}{n}$ %", fontsize=11)
    ax.text(0.5, -0.2, r"← Less truthful | More truthful →", transform=ax.transAxes,
            fontsize=9, ha="center", color="#777")
    ax.text(-0.2, 0.5, r"← Reliable | Error-prone →", transform=ax.transAxes,
            fontsize=9, ha="center", va="center", color="#777", rotation=90)
    ax.set_title("Truthfulness vs Parse Errors", fontsize=13)
    ax.legend(loc="upper left", fontsize=9, frameon=True,
              bbox_to_anchor=(1.01, 1), borderaxespad=0)

    fig.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "error_rate_plot.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


ARCHETYPE_DISPLAY = {
    "provided_facts": "Provided Facts",
    "known_facts": "Known Facts",
    "doubling_down_known_facts": "Doubling Down",
    "continuations": "Continuations",
    "disinformation": "Disinformation",
    "statistics": "Statistics",
}

ARCHETYPE_JUDGES = {
    "provided_facts": "gpt-4o-mini",
    "known_facts": "gpt-4o-mini",
    "doubling_down_known_facts": "gpt-4o-mini",
    "continuations": "gpt-4o-mini",
    "disinformation": "gpt-4o-mini",
    "statistics": "o3-mini",
}


def error_by_archetype_plot() -> None:
    """Dot plot: error rate by archetype with 95% CIs."""
    arch_data = load_errors_by_archetype()

    display_order = [
        "provided_facts",
        "known_facts",
        "doubling_down_known_facts",
        "continuations",
        "disinformation",
        "statistics",
    ]

    JUDGE_MARKERS = {"gpt-4o-mini": "^", "o3-mini": "X", "both": "D"}
    JUDGE_COLORS = {"gpt-4o-mini": "#555555", "o3-mini": "#c62828", "both": "#1565c0"}

    labels = []
    rates = []
    cis = []
    judges = []
    for key in display_order:
        d = arch_data.get(key, {"errors": 0, "samples": 0})
        n = d["samples"]
        e = d["errors"]
        rate = (e / n * 100) if n > 0 else 0
        ci = _binom_ci(rate, n)
        display = ARCHETYPE_DISPLAY.get(key, key)
        judge = ARCHETYPE_JUDGES.get(key, "?")
        labels.append(display)
        rates.append(rate)
        cis.append(ci)
        judges.append(judge)

    # Add overall row
    total_errors = sum(arch_data.get(k, {}).get("errors", 0) for k in display_order)
    total_samples = sum(arch_data.get(k, {}).get("samples", 0) for k in display_order)
    overall_rate = (total_errors / total_samples * 100) if total_samples > 0 else 0
    overall_ci = _binom_ci(overall_rate, total_samples)
    labels.append("Overall")
    rates.append(overall_rate)
    cis.append(overall_ci)
    judges.append("both")

    n_rows = len(labels)
    fig, ax = plt.subplots(figsize=(8, 0.7 * n_rows + 0.8))

    y_pos = np.arange(n_rows)
    for i in range(n_rows):
        color = JUDGE_COLORS[judges[i]]
        ax.errorbar(
            rates[i], y_pos[i], xerr=cis[i], fmt="none",
            ecolor=color, elinewidth=1.5, capsize=4, zorder=4,
        )

    # Plot each judge type separately for legend
    legend_drawn: set[str] = set()
    for i in range(n_rows):
        judge = judges[i]
        color = JUDGE_COLORS[judge]
        marker = JUDGE_MARKERS[judge]
        label = judge if judge not in legend_drawn else None
        legend_drawn.add(judge)
        ax.scatter(
            rates[i], y_pos[i], c=color, s=80, zorder=5,
            marker=marker, edgecolors="white", linewidths=0.5, label=label,
        )

    # Separator line before overall
    ax.axhline(y=n_rows - 1.5, color="#cccccc", linewidth=0.8, linestyle="--")

    archetype_keys = display_order + [None]
    for i, key in enumerate(archetype_keys):
        if key is not None:
            d = arch_data.get(key, {"errors": 0, "samples": 0})
            err, samp = d["errors"], d["samples"]
        else:
            err, samp = total_errors, total_samples
        color = JUDGE_COLORS[judges[i]]
        text_x = rates[i] + cis[i]
        ax.annotate(
            f" {rates[i]:.1f}%  ({err}/{samp:,})",
            (text_x, i), textcoords="offset points",
            xytext=(6, 0), fontsize=9, color=color, va="center",
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Error Rate (95% CI)", fontsize=11)
    ax.set_title("Parse Errors by Question Archetype", fontsize=13)
    ax.legend(title="Judge model", loc="lower right", fontsize=9, title_fontsize=9)
    ax.grid(True, axis="x", alpha=0.2)
    ax.set_xlim(-0.5, max(r + c for r, c in zip(rates, cis)) + 2)

    fig.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "error_by_archetype.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    replication_headline_result()
    truthfulness_headline_result()
    two_d_space_projection()
    error_rate_plot()
    error_by_archetype_plot()
    print("Done.")
