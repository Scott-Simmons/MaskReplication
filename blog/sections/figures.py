def placeholder_plot() -> str:
    return "![TODO: Insert placeholder_plot caption](figures/placeholder_plot.png)"


def og_headline_result() -> str:
    return "![TODO: Insert og_headline_result caption](figures/placeholder_plot.png)"


def replication_headline_result() -> str:
    return "![TODO: Insert replication_headline_result caption](figures/placeholder_plot.png)"


def replication_new_models_headline_result() -> str:
    return "![TODO: Insert replication_new_models_headline_result caption](figures/placeholder_plot.png)"


def two_d_space_projection_headline() -> str:
    return "![TODO: Insert 2d_space_projection_headline caption](figures/placeholder_plot.png)"


def more_2d_projections() -> str:
    return "![TODO: Insert more_2d_projections caption](figures/placeholder_plot.png)"


def models_used_in_replication() -> str:
    return "\n".join([
        "*TODO: Insert models_used_in_replication caption*",
        "",
        "| Model | Accuracy | Honesty |",
        "|---|---|---|",
        "| Model A | 0.85 | 0.42 |",
        "| Model B | 0.91 | 0.38 |",
        "| Model C | 0.72 | 0.67 |",
    ])


def basis_vectors_empirical() -> str:
    return "\n".join([
        "*TODO: Insert basis_vectors_empirical caption*",
        "",
        "| Model | Accuracy | Honesty |",
        "|---|---|---|",
        "| Model A | 0.85 | 0.42 |",
        "| Model B | 0.91 | 0.38 |",
        "| Model C | 0.72 | 0.67 |",
    ])


def other_1d_projections() -> str:
    return "\n".join([
        "*TODO: Insert other_1d_projections caption*",
        "",
        "| Model | Accuracy | Honesty |",
        "|---|---|---|",
        "| Model A | 0.85 | 0.42 |",
        "| Model B | 0.91 | 0.38 |",
        "| Model C | 0.72 | 0.67 |",
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


def deception_basis() -> str:
    return "$$TODO: Insert deception\\_basis$$"


def honesty_metric() -> str:
    return "$$TODO: Insert honesty\\_metric$$"


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
