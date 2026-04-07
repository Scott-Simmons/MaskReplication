from blog.decorators import interpretation


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
    return "With this parameterisation in mind, honesty as defined in the paper means:"


def honesty_is_lossy() -> str:
    return "However, this reduction compresses a lot of nuance."


def hypothetical_subheader() -> str:
    return "### Three agents with perfect honesty scores"


def hypothetical_commentary() -> str:
    return ""


def making_this_empirical_subheader() -> str:
    return "### Making this empirical"


def empirical_lossy_demonstration() -> str:
    return (
        "To make this concrete, here is the data from my "
        "replication plotted on 2 axes + honesty contours[^contour_math]:"
    )


def one_d_projections() -> str:
    return (
        "When all outcome counts are reported, researchers can compute whatever "
        "measures they are interested in, or define new ones[^classification_analogy]. Here are some more:"
    )


def truthfulness_argument() -> str:
    return (
        "Of these, I would argue that truthfulness ($H / \\text{n}$) is a more "
        "informative headline metric than the MASK honesty score ($1 - L / \\text{n}$). "
        "Admittedly, this is a subjective assessment, though when the raw counts are reported, the distinction matters less."
    )


@interpretation
def headline_still_holds() -> str:
    return "The headline result still holds when using truthfulness (H / n) instead of the MASK honesty score (1 - L / n): **scaling has not made models more truthful.**"


def reporting_errors_subheader() -> str:
    return "### Reporting errors"


def reporting_errors_prose() -> str:
    return (
        "*[AI slop — needs rewrite]*\n\n"
        "When I ran this eval, I noticed that transient errors happen all the time — "
        "network timeouts, rate limits, API hiccups — stopping samples from fully completing. "
        "[Inspect AI](https://inspect.aisi.org.uk) provides "
        "[eval-retry functionality](https://inspect.aisi.org.uk/errors-and-limits.html) "
        "to help with this, but transient failures are only half the story. "
        "LLMs can also produce unparseable outputs — going off the rails in unexpected ways "
        "that no retry will fix. These are not edge cases; they are routine in LLM evaluations.\n\n"
        "Another advantage of reporting the full outcome counts is to provide visibility into this:"
    )


def reporting_uncertainty_subheader() -> str:
    return "### Reporting uncertainty"


def reporting_uncertainty_prose() -> str:
    # TODO: AI slop — needs rewrite
    return (
        "*[AI slop — needs rewrite]*\n\n"
        "When an outcome is rare, the proportion estimate is noisier and "
        "error bars inflate relative to the point estimates. "
        "This also applies across models: a score computed from 80 samples "
        "is a much weaker claim than one computed from 1,000. "
        "Right now, DeepSeek-R1 has fewer samples in my replication, so its "
        "error bars are wider — that is information, not noise.\n\n"
        "Even if researchers choose not to report confidence intervals, "
        "reporting the raw counts lets readers derive them. "
        "A percentage without a sample size is unverifiable. "
        "A count is all you need to reconstruct the uncertainty."
    )
