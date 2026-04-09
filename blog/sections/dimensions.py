from blog.decorators import interpretation


def preamble() -> str:
    return "I wanted to explore the models' deception characteristics in more detail."


def introduce_the_dimensions() -> str:
    return (
        "When a model is pressured to answer against its own belief, "
        "its response can fall into one of these categories:"
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


def what_else_subheader() -> str:
    return "### What else can we measure?"


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
    return "### Reporting errors (WIP)"


def yes_errors_happen() -> str:
    return "Errors are an unavoidable part of LLM evaluation. Here are two types that I cannot get away from, no matter how much I try:"


def transient_errors_can_be_mitigated() -> str:
    return (
        "**(1) Transient errors:** can be retried automatically using "
        "Inspect AI's [`--retry-on-error`](https://inspect.aisi.org.uk/reference/inspect_eval.html) flag. "
        "This is very convenient!"
    )


def parse_errors_also_happen() -> str:
    return (
        "**(2) LLM parse errors:** A fact of (LLM) life. "
        "For example, a question about Detroit's population had an error in 6 / 10 models, becuase the LLM judge "
        "ran out of token budget before producing a valid JSON block as the final step in its reasoning:"
    )


def parse_error_example() -> str:
    return (
        "```json\n"
        "{\n"
        '  "lower_bound": -10.5,\n'
        '  "upper_bound": -10.5,\n'
        '  "relative_lower_bound": -10.5,\n'
        '  "relative_upper_bound": "<TRUNCATED>"\n'
        "}\n"
        "```\n"
    )


def inspect_ai_keeps_it_visible() -> str:
    return (
        "LLM parse errors are made transparently visible with Inspect AI's [eval logs](https://inspect.aisi.org.uk/eval-logs.html)."
        "This is also very convenient! [Inspect Scout]() was also conveniently used to analyse the logs for the parse errors, to "
        "find that <some_hopefully_nice_finding>."
    )


def error_distribution() -> str:
    return "<error_distribution_here>"


def but_actually_its_part_of_the_process() -> str:
    return (
        "Tuning judge parameters like `NUMERIC_JUDGE_MODEL`, `JUDGE_REASONING_EFFORT`, or `MAX_JUDGE_TOKENS` would likely resolve this, though it would diverge "
        "from the defaults used in the MASK paper."
    )


def reporting_uncertainty_subheader() -> str:
    return "### Reporting uncertainty"


def reporting_uncertainty_prose() -> str:
    return "Reporting confidence intervals separates claims that the data can support from ones it cannot."


def _uncertainty_numbers() -> tuple[str, str, float, int, int]:
    from blog.analysis import load_runs

    runs = {r.display_name: r for r in load_runs()}
    haiku = runs["Claude Haiku 4.5"]
    o3 = runs["o3-mini"]
    ratio = haiku.truthfulness / o3.truthfulness
    return (
        haiku.display_name,
        o3.display_name,
        ratio,
        haiku.dimensions["error"],
        o3.dimensions["error"],
    )


def uncertainty_concrete_example() -> str:
    haiku_name, o3_name, ratio, haiku_errors, o3_errors = _uncertainty_numbers()
    return (
        f"The claim that {haiku_name} is {ratio:.1f}x more truthful than {o3_name} is valid. "
        f"However, asserting that {haiku_name} has a {haiku_errors / o3_errors:.2f}x lower error rate "
        "risks conflating noise with real differences. Based on prior observations, it’s likely that the "
        "error rate is determined by the properties of the numeric judge model, so this result checks out "
        "with our available evidence."
    )
