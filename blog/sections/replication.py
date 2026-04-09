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
        "scales with compute, **but honesty does not.**"
    )


def caveat() -> str:
    from blog.analysis import DISPLAY_TO_OG, load_runs
    from blog.constants import OG_PAPER_SCORES

    hon_diffs = []
    acc_diffs = []
    for r in load_runs():
        og_name = DISPLAY_TO_OG.get(r.display_name)
        if og_name and og_name in OG_PAPER_SCORES:
            og_hon, _, og_acc = OG_PAPER_SCORES[og_name]
            hon_diffs.append(r.honesty * 100 - og_hon)
            acc_diffs.append(r.accuracy * 100 - og_acc)

    hon_lo, hon_hi = int(min(hon_diffs)), int(max(hon_diffs))
    acc_lo, acc_hi = int(min(acc_diffs)), int(max(acc_diffs))

    return (
        '::: {.note style="background:#f8f9fa; border-left:4px solid #5c6bc0; padding:1em 1.2em; margin:1.5em 0; border-radius:4px;"}\n'
        "**Note:** the headline relationship replicates: accuracy scales favourably with FLOPs, honesty does not. "
        f"The scores differ from the paper: honesty runs higher by ~{hon_lo}-{hon_hi} percentage points, "
        f"accuracy lower by ~{abs(acc_hi)}-{abs(acc_lo)} percentage points. "
        "See the [appendix](#appendix-paper-vs-replication-differences) for a model-by-model "
        "comparison.\n"
        ":::"
    )


