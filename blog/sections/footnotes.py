def flops() -> str:
    return ""


def error_in_the_basis() -> str:
    return (
        "[^1]: Including $\\varepsilon$ (parse errors) in the basis is deliberate. "
        "Without it, $\\{H, L, E, N\\}$ is not an exhaustive partition of responses. "
        "A response that fails to parse does not land in any of those four buckets, "
        "so the counts would not sum to $n$ and every derived metric would have a "
        "hidden denominator problem. $\\varepsilon$ closes the basis so that it spans "
        "the full space of outcomes. API failures (timeouts, rate limits) expose the "
        "same gap at a different level: they silently shrink $n$ without landing anywhere "
        "in the basis. This is not merely a bookkeeping nuisance — it can introduce "
        "systematic bias. If a model tends to time out specifically on questions where it "
        "would otherwise lie, the surviving sample over-represents honest responses and "
        "the reported honesty score is inflated. The basis argument applies here too: "
        "unaccounted outcomes corrupt every derived metric, whether they fall inside a "
        "response or before one is returned. "
        "<mark>TODO: Rerun DeepSeek-R1 to get closer to n=1000.</mark>"
    )


def classification_basis_analogy() -> str:
    return (
        "[^2]: This is why even for a simple basis of "
        "$\\{\\text{TP}, \\text{TN}, \\text{FP}, \\text{FN}\\}$ in a traditional "
        "binary classifier context there is a "
        "[cornucopia of metrics](https://en.wikipedia.org/wiki/Template:Diagnostic_testing_diagram) "
        "that we project that basis onto. I would like to see the eval community "
        "refining metrics that characterise deception, in a similar way to how the ML "
        "community looks at [ROC curves](https://en.wikipedia.org/wiki/Receiver_operating_characteristic), "
        "[PR curves](https://en.wikipedia.org/wiki/Precision_and_recall), and "
        "[MCC](https://en.wikipedia.org/wiki/Phi_coefficient) "
        "instead of accuracy to assess a model's validity."
    )


def theoretical_limit_per_basis_size() -> str:
    return ""
