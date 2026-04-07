from blog.decorators import interpretation as _interpretation_decorator


def what_i_wanted_to_do() -> str:
    return (
        "I wanted to verify the paper's main claim: larger models are more accurate "
        "but not more honest. I used the following models:"
    )


def differences_to_og() -> str:
    return (
        "*The [MASK public dataset](https://huggingface.co/datasets/cais/MASK) contains 1,000 examples.*\n\n"
        + _differences_to_og_text()
    )


def _differences_to_og_text() -> str:
    from blog.analysis import load_runs

    n_models = len(load_runs())
    return (
        "I used a different model judge to save on cost (see [appendix](#appendix-paper-vs-replication-differences)) "
        f"and a smaller set of {n_models} models covering a range of providers and scales. "
        "The paper tested 32, but some are now deprecated."
    )


@_interpretation_decorator
def interpretation() -> str:
    return (
        "The headline result held: accuracy "
        "scales with compute, **but honesty does not.** See the "
        "[appendix](#appendix-paper-vs-replication-differences) for a model-by-model "
        "comparison with the original paper."
    )


