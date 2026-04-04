def preamble() -> str:
    return "I wanted to explore the models' deception characteristics in more detail."


def introduce_the_dimensions() -> str:
    return (
        "The categories that a pressured statement, subject to some internally held "
        "belief, can fall into are:"
    )


def empirical_dimensions_intro() -> str:
    return (
        "The outcomes are mutually exclusive and collectively exhaustive, so nothing is double-counted or missed. "
        "Here are the empirical outcome count vectors for my MASK replication:"
    )


def honesty_in_terms_of_dimensions() -> str:
    return 'With this in mind, "honesty" as reported by the paper means:'


def honesty_is_lossy() -> str:
    return "However this reduction compresses a lot of useful information."


def hypothetical_subheader() -> str:
    return "### Hypothetical"


def interp_dumb_and_diplomatic() -> str:
    return "TODO: Insert interp_dumb_and_diplomatic"


def making_this_empirical_subheader() -> str:
    return "### Making this empirical"


def empirical_lossy_demonstration() -> str:
    return (
        "To make these thought experiments concrete, here is the data from my "
        "replication plotted on 2 axes + contours:"
    )


def one_d_projections() -> str:
    return (
        "When all outcome counts are reported, researchers can compute whatever "
        "measures they are interested in[^classification_analogy], or define new ones. Here are some more:"
    )


def truthfulness_argument() -> str:
    return (
        "Of these, I would argue that truthfulness ($H / \\text{n}$) is a more "
        "informative headline metric than the MASK honesty score ($1 - L / \\text{n}$). "
        "Admittedly, this is a subjective assessment, though when the raw counts are reported, the distinction matters less."
    )


def headline_still_holds() -> str:
    return "Interestingly, the headline result still holds even when using truthfulness (H / total) instead of the MASK honesty score (1 - L / total): scaling has not made models more truthful."


def communicating_uncertainty_subheader() -> str:
    return "### Communicating uncertainty"


def more_examples_of_2d_projections() -> str:
    return "Here are three more representations of the same data:"


def more_2d_projections_commentary() -> str:
    return (
        "Note that the middle panel "
        "includes $\\varepsilon$ to show that when an outcome is "
        "rare, the proportion estimate is noisier and error bars inflate relative "
        "to the point estimates. This is exactly why reporting counts matters, "
        "especially for LLM evaluations, where silent errors (unparseable outputs, judge failures, dropped "
        "samples) are common. Making these visible in the dimensions is a step towards better "
        "evaluation science."
    )
