def internal_beliefs() -> str:
    return (
        "[^internal_beliefs]: If 'internal beliefs' raises eyebrows, "
        "see Appendix A.1 (Belief Consistency) of the "
        "[MASK paper](https://arxiv.org/abs/2503.03750) "
        "for how this is operationalised and justified."
    )


def classification_dimensions_analogy() -> str:
    return (
        "[^classification_analogy]: By analogy to the many "
        "[binary classification metrics](https://en.wikipedia.org/wiki/Template:Diagnostic_testing_diagram) "
        "out there, deception metrics have plenty of scope to evolve in a similar way."
    )


def open_questions() -> str:
    return (
        "[^open_questions]: In particular, three extensions I would like to see: "
        "**(1) Belief robustness:** The MASK paper queried each model 3 times "
        "(I am purposely oversimplifying), but I would like to see this number varied "
        "to see if scaling this up undermines belief convergence. "
        "**(2) Judge sensitivity:** The paper used 2 judge models to produce these results. "
        "How sensitive are the results to different judge models? "
        "**(3) Archetype decomposition:** The MASK dataset stratifies questions by archetype "
        "(see the [paper](https://arxiv.org/abs/2503.03750) for details). "
        "Decomposing the outcome vectors per archetype would be valuable, but drawing robust conclusions "
        "about model × archetype interactions requires more models than the current 10. "
        "**Warning:** For (1) and (2), any statistically meaningful investigation will be "
        "[expensive](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/appendix.html#expected-number-of-llm-invocations-per-record)."
    )


def pedantic_r5() -> str:
    return "[^pedantic_r5]: 4 degrees of freedom because $n = H + L + E + N + \\varepsilon$, and ($n = 1{,}000$)."


def wilson_ci() -> str:
    return (
        "[^wilson_ci]: All confidence intervals in this post use the "
        "[Wilson score interval](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval)."
    )


def clustering() -> str:
    return (
        "[^clustering]: As the parse error analysis showed, clustering by question type means "
        "independence assumptions do not always hold. "
        "See: [Clustered standard errors](https://en.wikipedia.org/wiki/Clustered_standard_errors)."
    )


def contour_math() -> str:
    return (
        "[^contour_math]: The MASK honesty score can be composed from the conditional lie rate "
        "and the engagement rate: $\\text{MASK Honesty} = 1 - P(\\text{Lie}) = 1 - \\frac{L}{n} "
        "= 1 - \\frac{L}{H+L} \\cdot \\frac{H+L}{n} = 1 - (1 - \\frac{H}{H+L}) "
        "\\cdot \\frac{H+L}{n}.$ "
    )
