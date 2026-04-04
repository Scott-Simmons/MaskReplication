def internal_beliefs() -> str:
    return (
        "[^internal_beliefs]: Yes, talking about AI models having 'internal beliefs' "
        "sounds anthropomorphising, and it should raise an eyebrow. "
        "For anyone skeptical or interested in what this means and how it is operationalised, "
        "I encourage reading the [MASK paper](https://arxiv.org/abs/2503.03750) "
        "and the references therein."
    )


def flops() -> str:
    return ""


def error_in_the_basis() -> str:
    return "DELETE THIS"


def classification_basis_analogy() -> str:
    return (
        "[^classification_analogy]: This is why even for a simple basis of "
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


def open_questions() -> str:
    return (
        "[^open_questions]: Two extensions I would love to see someone pick up. "
        "First, how robust is a model's internal belief representation? "
        "The MASK paper queried each model 3 times with optional consistency checks, "
        "but I would like to see this varied — ask N times, M times — to see if it "
        "undermines belief convergence. "
        "Second, how sensitive are the results to the choice of model judge? "
        "The paper used a judge model to produce these results. "
        "How does changing the judge affect the outcomes? "
        "Both of these extensions are expensive, but important."
    )


def pedantic_r5() -> str:
    return "[^pedantic_r5]: Technically it's $\\mathbb{R}^4$ (4 degrees of freedom)."


def theoretical_limit_per_basis_size() -> str:
    return ""
