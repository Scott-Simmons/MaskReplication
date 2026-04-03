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
        "I used <mark>a different model judge to save on cost (TODO: may remove this "
        "caveat if we rerun with the same judge, it is just expensive)</mark> "
        f"and a slightly different set of {n_models} models. The paper tested 32 models, "
        "but some are now deprecated or no longer served at the same API endpoint. "
        "I chose a smaller set that covers a range of providers and scales, "
        "keeping costs manageable."
    )


def interpretation() -> str:
    return (
        "The headline result held. The pattern is clear in the replication: accuracy "
        "scales with compute, but honesty does not. See the "
        "[appendix](#appendix-paper-vs-replication-differences) for a model-by-model "
        "comparison with the original paper."
    )


def interpretation_new_models() -> str:
    return "TODO: Insert interpretation_new_models"


def flops_note() -> str:
    return "TODO: Insert flops_note[^1]"
