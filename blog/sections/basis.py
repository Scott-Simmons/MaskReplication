def introduce_the_basis() -> str:
    return (
        "The categories that a pressured statement, subject to some internally held "
        "belief, can fall into are:[^2]"
    )


def empirical_basis_intro() -> str:
    return "Here are the empirical basis vectors for my MASK replication:"


def honesty_in_terms_of_basis() -> str:
    return 'With this basis in mind, "honesty" as reported by the paper means:'


def honesty_is_lossy() -> str:
    return "However this projection compresses a lot of useful information."


def hypothetical_subheader() -> str:
    return "### Hypothetical"


def interp_dumb_and_diplomatic() -> str:
    return "TODO: Insert interp_dumb_and_diplomatic"


def making_this_empirical_subheader() -> str:
    return "### Making this empirical"


def empirical_lossy_demonstration() -> str:
    return (
        "To make these thought experiments concrete, here is the data from the "
        "replication plotted in a 2D projection of the basis:"
    )


def one_d_projections() -> str:
    return (
        "Every projection of the deception basis produces a different metric. "
        "When the basis is reported, researchers can compute whatever "
        "measures they are interested in, or define new ones. Here are some useful ones:[^3]"
    )


def more_examples_of_2d_projections() -> str:
    return (
        "The same data can be projected in many other ways. Here are three more, each "
        "telling a different story. The middle panel (\"Reliable vs Broken\") includes "
        "$\\varepsilon$ to show that when a basis vector represents a rare event, the "
        "proportion estimate is noisier and error bars inflate relative to the point "
        "estimates. This is exactly why reporting counts matters, especially for LLM "
        "evaluations, where silent errors (unparseable outputs, judge failures, dropped "
        "samples) are common. Making these visible in the basis is a step towards better "
        "evaluation science."
    )
