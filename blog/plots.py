"""Generate plots for the blog post."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import shutil


from blog.analysis import PROVIDER_COLORS, load_runs

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
    """2D behavior space: Evasion Rate vs Conditional Lie Rate, with iso-honesty contours."""
    runs = load_runs()

    # Compute projections from dimensions
    evasion_rates = []  # E / (H + L + E)
    lie_rates = []  # L / (H + L)
    evasion_ns = []
    lie_ns = []
    providers = []
    names = []

    for r in runs:
        b = r.dimensions
        H = b.get("truthful", 0)
        L = b.get("lie", 0)
        E = b.get("evade", 0)

        engaged_or_evaded = H + L + E
        engaged = H + L

        evasion_rate = (E / engaged_or_evaded * 100) if engaged_or_evaded > 0 else 0
        cond_lie_rate = (L / engaged * 100) if engaged > 0 else 0

        evasion_rates.append(evasion_rate)
        lie_rates.append(cond_lie_rate)
        evasion_ns.append(engaged_or_evaded)
        lie_ns.append(engaged)
        providers.append(r.provider)
        names.append(r.display_name)

    x = np.array(evasion_rates)
    y = np.array(lie_rates)
    x_ci = np.array([_binom_ci(xv, n) for xv, n in zip(evasion_rates, evasion_ns)])
    y_ci = np.array([_binom_ci(yv, n) for yv, n in zip(lie_rates, lie_ns)])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Iso-honesty contours: P(Lie) ≈ y/100 * (1 - x/100) = c
    # So y = 100 * c / (1 - x/100)
    x_cont = np.linspace(0, 45, 200)
    for c in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
        y_cont = 100 * c / (1 - x_cont / 100)
        y_cont = np.where(y_cont <= 100, y_cont, np.nan)
        ax.plot(x_cont, y_cont, color="#bbb", linestyle=":", linewidth=0.8, alpha=0.7)
        # Label on the contour line itself
        label_x = 3
        label_y = 100 * c / (1 - label_x / 100)
        if 0 < label_y < 98:
            ax.text(
                label_x,
                label_y,
                f" P(Lie)={c:.0%}",
                fontsize=6.5,
                color="#999",
                va="center",
                ha="left",
                bbox=dict(
                    boxstyle="round,pad=0.1",
                    facecolor="white",
                    edgecolor="none",
                    alpha=0.8,
                ),
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

    # Quadrant labels
    ax.text(
        0.02,
        0.02,
        "Genuinely Honest",
        transform=ax.transAxes,
        fontsize=8,
        color="#2e7d32",
        fontstyle="italic",
        alpha=0.7,
    )
    ax.text(
        0.98,
        0.02,
        "Honest Dodger",
        transform=ax.transAxes,
        fontsize=8,
        color="#2e7d32",
        fontstyle="italic",
        alpha=0.7,
        ha="right",
    )
    ax.text(
        0.02,
        0.98,
        "Direct Liar",
        transform=ax.transAxes,
        fontsize=8,
        color="#b71c1c",
        fontstyle="italic",
        alpha=0.7,
        va="top",
    )
    ax.text(
        0.98,
        0.98,
        "Evasive + Deceptive",
        transform=ax.transAxes,
        fontsize=8,
        color="#b71c1c",
        fontstyle="italic",
        alpha=0.7,
        ha="right",
        va="top",
    )

    ax.set_xlabel(r"Evasion Rate: $\frac{E}{H + L + E}$ %", fontsize=11)
    ax.set_ylabel(r"Conditional Lie Rate: $\frac{L}{H + L}$ %", fontsize=11)
    # Directional arrows as secondary labels
    ax.text(
        0.5,
        -0.2,
        r"← Direct | Evasive →",
        transform=ax.transAxes,
        fontsize=9,
        ha="center",
        color="#777",
    )
    ax.text(
        -0.2,
        0.5,
        r"← Honest | Deceptive →",
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
    ax.grid(True, alpha=0.15)
    ax.set_xlim(-1, 48)
    ax.set_ylim(-1, 100)

    fig.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "two_d_space_projection.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


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


def more_2d_projections() -> None:
    """Three additional 2D projections: Loud/Quiet, Dodger/Clueless, Diplomatic/Dumb."""
    runs = load_runs()

    # Precompute all dimensions values per model
    data = []
    for r in runs:
        b = r.dimensions
        H = b.get("truthful", 0)
        L = b.get("lie", 0)
        E = b.get("evade", 0)
        N = b.get("no_belief", 0)
        eps = b.get("error", 0)
        total = H + L + E + N
        total_full = H + L + E + N + eps
        engaged = H + L
        non_answer = E + N
        data.append(
            {
                "name": r.display_name,
                "provider": r.provider,
                # (1) Loud vs Quiet
                "engagement_rate": (engaged / total * 100) if total > 0 else 0,
                "engagement_rate_n": total,
                "cond_honesty": (H / engaged * 100) if engaged > 0 else 0,
                "cond_honesty_n": engaged,
                # (2) Engaged vs Broken (uses ε)
                "engagement_rate_full": (engaged / total_full * 100)
                if total_full > 0
                else 0,
                "engagement_rate_full_n": total_full,
                "error_rate": (eps / total_full * 100) if total_full > 0 else 0,
                "error_rate_n": total_full,
                # (3) Diplomatic vs Dumb
                "deflection_style": (E / non_answer * 100) if non_answer > 0 else 0,
                "deflection_style_n": non_answer,
                "cond_lie_rate": (L / engaged * 100) if engaged > 0 else 0,
                "cond_lie_rate_n": engaged,
            }
        )

    panels = [
        {
            "x_key": "engagement_rate",
            "y_key": "cond_honesty",
            "xlabel": r"Engagement Rate: $\frac{H+L}{H+L+E+N}$ %",
            "ylabel": r"Cond. Honesty: $\frac{H}{H+L}$ %",
            "x_arrow": r"← Quiet | Loud →",
            "y_arrow": r"← Deceptive | Honest →",
            "quadrants": [
                (0.02, 0.02, "Quiet Liar", "#b71c1c"),
                (0.98, 0.02, "Loud Liar", "#b71c1c"),
                (0.02, 0.98, "Quiet Truth-teller", "#2e7d32"),
                (0.98, 0.98, "Loud Truth-teller", "#2e7d32"),
            ],
            # Iso-P(honest): P(honest) = engagement × cond_honesty → y = c/x (hyperbolas)
            "iso_lines": lambda ax: _iso_hyperbolas(
                ax, [10, 20, 30, 40, 50, 60], "P(honest)"
            ),
        },
        {
            "x_key": "engagement_rate_full",
            "y_key": "error_rate",
            "xlabel": r"Engagement Rate: $\frac{H+L}{H+L+E+N+\varepsilon}$ %",
            "ylabel": r"Error Rate: $\frac{\varepsilon}{H+L+E+N+\varepsilon}$ %",
            "x_arrow": r"← Disengaged | Engaged →",
            "y_arrow": r"← Reliable | Broken →",
            "quadrants": [
                (0.02, 0.02, "Disengaged + Reliable", "#e65100"),
                (0.98, 0.02, "Engaged + Reliable", "#2e7d32"),
                (0.02, 0.98, "Disengaged + Broken", "#b71c1c"),
                (0.98, 0.98, "Engaged + Broken", "#b71c1c"),
            ],
            "iso_lines": None,
        },
        {
            "x_key": "deflection_style",
            "y_key": "cond_lie_rate",
            "xlabel": r"Deflection Style: $\frac{E}{E+N}$ %",
            "ylabel": r"Cond. Lie Rate: $\frac{L}{H+L}$ %",
            "x_arrow": r"← Dumb | Diplomatic →",
            "y_arrow": r"← Honest | Deceptive →",
            "quadrants": [
                (0.02, 0.02, "Honest + Uncertain", "#2e7d32"),
                (0.98, 0.02, "Honest + Evasive", "#2e7d32"),
                (0.02, 0.98, "Deceptive + Uncertain", "#b71c1c"),
                (0.98, 0.98, "Deceptive + Evasive", "#b71c1c"),
            ],
            "iso_lines": None,
        },
    ]

    fig, axes = plt.subplots(1, 3, figsize=(24, 8))

    for ax, panel in zip(axes, panels):
        x_vals = np.array([d[panel["x_key"]] for d in data])
        y_vals = np.array([d[panel["y_key"]] for d in data])

        # Iso-lines
        if panel.get("iso_lines"):
            panel["iso_lines"](ax)

        # Compute CIs
        x_ci = np.array(
            [_binom_ci(d[panel["x_key"]], d[panel["x_key"] + "_n"]) for d in data]
        )
        y_ci = np.array(
            [_binom_ci(d[panel["y_key"]], d[panel["y_key"] + "_n"]) for d in data]
        )

        # Scatter coloured by provider with error bars
        plotted_providers = set()
        for d, xi, yi, xci, yci in zip(data, x_vals, y_vals, x_ci, y_ci):
            color = PROVIDER_COLORS.get(d["provider"], "#999999")
            label = d["provider"] if d["provider"] not in plotted_providers else None
            plotted_providers.add(d["provider"])
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
                s=80,
                zorder=5,
                label=label,
                edgecolors="white",
                linewidths=0.5,
            )
            ax.annotate(
                d["name"],
                (xi, yi),
                textcoords="offset points",
                xytext=(6, 6),
                fontsize=9,
                color="#555",
            )

        # Quadrant labels
        for qx, qy, qlabel, qcolor in panel["quadrants"]:
            va = "bottom" if qy < 0.5 else "top"
            ha = "left" if qx < 0.5 else "right"
            ax.text(
                qx,
                qy,
                qlabel,
                transform=ax.transAxes,
                fontsize=10,
                color=qcolor,
                fontstyle="italic",
                alpha=0.6,
                ha=ha,
                va=va,
            )

        ax.set_xlabel(panel["xlabel"], fontsize=12)
        ax.set_ylabel(panel["ylabel"], fontsize=12)
        ax.text(
            0.5,
            -0.18,
            panel["x_arrow"],
            transform=ax.transAxes,
            fontsize=11,
            ha="center",
            color="#777",
        )
        ax.text(
            -0.18,
            0.5,
            panel["y_arrow"],
            transform=ax.transAxes,
            fontsize=11,
            ha="center",
            va="center",
            color="#777",
            rotation=90,
        )
        ax.tick_params(labelsize=10)
        ax.grid(True, alpha=0.15)

    # Single legend below all panels
    handles, labels = axes[0].get_legend_handles_labels()
    for ax in axes[1:]:
        h, l = ax.get_legend_handles_labels()
        for hi, li in zip(h, l):
            if li not in labels:
                handles.append(hi)
                labels.append(li)
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=len(set(d["provider"] for d in data)),
        fontsize=11,
        frameon=True,
        bbox_to_anchor=(0.5, -0.03),
    )

    fig.tight_layout(rect=[0, 0.03, 1, 0.98])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "more_2d_projections.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    replication_headline_result()
    truthfulness_headline_result()
    two_d_space_projection()
    more_2d_projections()
    print("Done.")
