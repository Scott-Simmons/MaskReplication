def what_i_wanted_to_do() -> str:
    return (
        "I wanted to verify the paper's main claim: larger models are more accurate "
        "but not more honest. I used the following models:"
    )


def differences_to_og() -> str:
    return (
        "*The MASK public dataset contains 1,000 examples.*\n\n"
        + _differences_to_og_text()
    )


def _differences_to_og_text() -> str:
    from blog.analysis import load_runs

    n_models = len(load_runs())
    return (
        "I used a different model judge (see [appendix](#appendix-paper-vs-replication-differences)) to save on cost "
        f"and a slightly different set of {n_models} models. The paper tested 32 models, "
        "but some are now deprecated. "
        "I chose a smaller set that covers a range of providers and scales, "
        "while still keeping costs manageable."
    )


def interpretation() -> str:
    return (
        "The headline result held: accuracy "
        "scales with compute, **but honesty does not.** See the "
        "[appendix](#appendix-paper-vs-replication-differences) for a model-by-model "
        "comparison with the original paper."
    )


def interpretation_new_models() -> str:
    return "TODO: Insert interpretation_new_models"


def flops_note() -> str:
    return (
        "**Note:** I used [Epoch AI](https://epoch.ai/data/notable-ai-models) to "
        "estimate the FLOP per model; the per-model FLOP estimates appear missing from the original paper and [original repo](https://github.com/centerforaisafety/mask).[^flops]"
    )
