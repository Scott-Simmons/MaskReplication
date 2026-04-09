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
        "about model × archetype interactions requires more models than the current 9. "
        "**Warning:** For (1) and (2), any statistically meaningful investigation will be "
        "[expensive](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/appendix.html#expected-number-of-llm-invocations-per-record)."
    )


def pedantic_r5() -> str:
    return "[^pedantic_r5]: Technically it's $\\mathbb{R}^4$, not $\\mathbb{R}^5$, because there are 4 degrees of freedom: $n = H + L + E + N + \\varepsilon$."


def llm_judge_squared() -> str:
    return "[^llm_judge_squared]: Running an LLM scanner on an eval that uses LLM-as-a-judge = (LLM-as-a-judge)$^2$."


def contour_math() -> str:
    return (
        "[^contour_math]: The MASK honesty score is the product of the conditional lie rate "
        "and the engagement rate: $\\text{MASK Honesty} = 1 - P(\\text{Lie}) = 1 - \\frac{L}{n} "
        "= 1 - \\frac{L}{H+L} \\cdot \\frac{H+L}{n} = 1 - (1 - \\frac{H}{H+L}) "
        "\\cdot \\frac{H+L}{n}$"
    )
