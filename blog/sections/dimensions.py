from blog.decorators import interpretation, references_numbers


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
    return "However, this reduction compresses a lot of nuance, as I will show."


def hypothetical_subheader() -> str:
    return "### Three agents with perfect honesty scores"


def hypothetical_commentary() -> str:
    return (
        "An agent that always evades, or one that holds no beliefs at all, "
        "still scores 100% MASK honesty! The MASK paper's appendix handles the Patrick Star case "
        "with a normalised honesty score, but not the Kash Patel case."
    )


def making_this_empirical_subheader() -> str:
    return "### Making this empirical"


def empirical_lossy_demonstration() -> str:
    return (
        "Here is the data from my "
        "replication plotted on 2 axes + honesty contours[^contour_math]:"
    )


def what_else_subheader() -> str:
    return "### What else can be measured?"


def one_d_projections() -> str:
    return (
        "When all outcome counts are reported, researchers can compute whatever "
        "measures they are interested in, or define new ones[^classification_analogy]. Here are some more:"
    )


@interpretation
def truthfulness_argument() -> str:
    return (
        "Of these, I would argue that truthfulness ($H / \\text{n}$) is a more "
        "informative headline metric than the MASK honesty score ($1 - L / \\text{n}$). "
        "Admittedly, this is a subjective assessment, though when the raw counts are reported, the distinction matters less."
    )


@interpretation
def headline_still_holds() -> str:
    return "The headline result still holds when using truthfulness (H / n) instead of the MASK honesty score (1 - L / n): **scaling has not made models more truthful.**"


def errors_intro() -> str:
    return (
        "So far I have been computing metrics from raw outcome counts. "
        "But errors and finite sample sizes both affect how those metrics should be interpreted. "
        "Here is what accounting for this looks like in practice, "
        "using tooling from the [Inspect AI ecosystem](https://inspect.aisi.org.uk/extensions/)."
    )


def transient_errors_subheader() -> str:
    return "### Transient errors"


def transient_errors_body() -> str:
    return (
        "Transient API failures are retried automatically with "
        "[Inspect AI](https://inspect.aisi.org.uk/)'s "
        "[`--retry-on-error`](https://inspect.aisi.org.uk/reference/inspect_eval.html) "
        "flag. Very convenient! Especially for evals that make "
        "[a lot of invocations](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/appendix.html#with-mask-defaults) "
        "(my DeepSeek runs certainly needed it)."
    )


def parse_errors_subheader() -> str:
    return "### Parse errors"


@references_numbers
def parse_errors_intro() -> str:
    from blog.analysis import load_runs

    n_models = len(load_runs())
    return (
        "LLMs sometimes produce invalid output. "
        "If not reported, they could silently shift headline scores. "
        f"For example, a question about Detroit's population had an error in 6 / {n_models} models in my replication, "
        "because the judge ran out of token budget before completing its JSON:"
    )


def parse_error_example() -> str:
    return (
        "```\n"
        "{\n"
        '  "lower_bound": -10.5,\n'
        '  "upper_bound": -10.5,\n'
        '  "relative_lower_bound": -10.5,\n'
        '  "relative_upper_bo\n'
        "```\n"
    )


def parse_errors_investigation() -> str:
    return "Thankfully, [Inspect AI's eval logs](https://inspect.aisi.org.uk/eval-logs.html) make these failure modes transparent and auditable."


def parse_errors_scout() -> str:
    return (
        "I also used [Inspect Scout](https://meridianlabs-ai.github.io/inspect_scout/) "
        "to help diagnose the *why*:"
    )


def scout_invocation() -> str:
    return (
        "```bash\n"
        "scout scan error_scanner.py \\\n"
        "  -T eval_logs/ \\\n"
        "  -F \"score.honesty = 'error'\"\n"
        "```"
    )


def parse_errors_not_random() -> str:
    return (
        "When grouped by question type, "
        "the Statistics questions stick out like a sore thumb:"
    )


def parse_errors_explanation() -> str:
    return (
        "The Statistics questions use a separate judge (o3-mini) to parse numerical answers. "
        "Tuning parameters like `NUMERIC_JUDGE_MODEL`, `JUDGE_REASONING_EFFORT`, or `MAX_JUDGE_TOKENS` "
        "would likely resolve this, though these are not the defaults used in the original MASK eval."
    )


def sampling_uncertainty_subheader() -> str:
    return "### Sampling uncertainty"


def sampling_uncertainty_intro() -> str:
    return (
        "Even when the eval runs perfectly, finite samples mean not every difference is real. "
        "With confidence intervals[^wilson_ci] and raw counts, comparisons become more meaningful[^clustering]."
    )


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


@references_numbers
@interpretation
def uncertainty_concrete_example() -> str:
    haiku_name, o3_name, ratio, haiku_errors, o3_errors = _uncertainty_numbers()
    return (
        f"For example, the claim that {haiku_name} is more than {int(ratio)} times more truthful than {o3_name} holds up. "
        f"However, claiming that {haiku_name} has a roughly {int(round(o3_errors / haiku_errors))} times lower error rate "
        "conflates noise with real differences. This is consistent with what the parse error analysis showed: "
        "errors are intrinsic to the Statistics questions, not something that varies across the models being assessed."
    )


@interpretation
def ci_punchline() -> str:
    haiku_name, o3_name, _, haiku_errors, o3_errors = _uncertainty_numbers()
    error_ratio = int(round(o3_errors / haiku_errors))
    return (
        f"Without confidence intervals on this plot, it would be easy to mistakenly conclude that "
        f"{haiku_name} is almost {error_ratio} times more reliable than {o3_name} ({round(o3_errors**-1, 2)} vs {round(haiku_errors**-1, 2)}), "
        "even though this difference is likely noise."
    )


def rigour_subheader() -> str:
    return "### How rigorous is rigorous enough?"


def clustering_caveat() -> str:
    return (
        "Thinking about confidence intervals naturally leads to thinking about "
        "[independence and clustering](https://en.wikipedia.org/wiki/Clustered_standard_errors). "
        "I showed this earlier with how the parse errors clustered by question type."
    )


def rigour_commentary() -> str:
    return (
        "Personally, and I know this could trigger some statisticians, "
        "I would not get hung up on level 4 just yet. "
        "It is probably better to spend time thinking about "
        "whether this is the right eval in the first place, and how it will "
        "[lead towards AI safety improvement](https://www.lesswrong.com/posts/8t8jdTyq6X2B7D8St/have-an-unreasonably-specific-story-about-the-future). "
        "The MASK eval has introduced a lot of interesting framings "
        "that the eval community is going to be able to extend."
    )
