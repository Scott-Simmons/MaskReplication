def recap() -> str:
    return "TODO: Insert recap"


def encourage_the_basis_framing() -> str:
    return "\n".join([
        "TODO: Insert encourage_the_basis_framing",
        "",
        "TODO: Work in this point — MASK only reports P(honest) and P(lie) as percentages. "
        "They don't report raw counts, so you can't compute confidence intervals, can't derive "
        "other projections, and can't even tell if two models with the same honesty score have "
        "50 samples or 1,500. Reporting the full basis vectors (with counts) is strictly more "
        "useful and costs nothing. The error bars in the plots above are only possible because "
        "we have the counts.",
        "",
        "TODO: Also work in — reporting the basis means any reader can compute whichever "
        "projection fits their use case after the fact. New metric proposed next year? "
        "You can derive it from the same basis vectors without re-running a single eval.",
    ])
