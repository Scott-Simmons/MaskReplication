def flops() -> str:
    return ""


def error_in_the_basis() -> str:
    return (
        "[^1]: Including $\\varepsilon$ (parse errors) in the basis is deliberate. "
        "Without it, $\\{H, L, E, N\\}$ is not an exhaustive partition of responses. "
        "A response that fails to parse does not land in any of those four buckets, "
        "so the counts would not sum to $n$ and every derived metric would have a "
        "hidden denominator problem. $\\varepsilon$ closes the basis so that it spans "
        "the full space of outcomes."
    )


def classification_basis_analogy() -> str:
    return (
        "[^2]: This is why even for a simple basis of "
        "$\\{\\text{TP}, \\text{TN}, \\text{FP}, \\text{FN}\\}$ in a traditional "
        "classifier context there is a "
        "[cornucopia of metrics](https://en.wikipedia.org/wiki/Template:Diagnostic_testing_diagram) "
        "that we project that basis onto. I would like to see the eval community "
        "refining metrics that characterise deception, in a similar way to how the ML "
        "community looks at ROC curves, PR curves, and Matthew's correlation coefficient "
        "instead of accuracy to assess a model's validity."
    )


def theoretical_limit_per_basis_size() -> str:
    return ""
