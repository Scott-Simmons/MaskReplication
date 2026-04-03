def what_i_wanted_to_do() -> str:
    return (
        "I wanted to verify the paper's main claim: larger models are more accurate "
        "but not more honest. I used the following models:"
    )


def differences_to_og() -> str:
    return (
        "*The MASK public dataset contains 1,000 examples. "
        "Shortfalls are due to API failures during evaluation.*\n\n"
        + _differences_to_og_text()
    )


def _differences_to_og_text() -> str:
    from blog.analysis import load_runs

    n_models = len(load_runs())
    return (
        "I used <mark>a different model judge to save on cost (TODO: maybe remove this caveat)</mark> "
        f"and a slightly different set of {n_models} models because TODO: Insert reasons."
    )


def interpretation() -> str:
    return "TODO: Insert interpretation"


def interpretation_new_models() -> str:
    return "TODO: Insert interpretation_new_models"


def flops_note() -> str:
    return "TODO: Insert flops_note[^1]"
