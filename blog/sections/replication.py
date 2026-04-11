from blog.decorators import interpretation as _interpretation_decorator
from blog.decorators import references_numbers


def what_i_wanted_to_do() -> str:
    return (
        "I wanted to verify the paper's main claim: larger models are more accurate "
        "but not more honest. I used the following models:"
    )


@references_numbers
def differences_to_og() -> str:
    return (
        '<p style="text-align:center; color:#c0392b; font-weight:bold; font-size:0.9em; font-style:italic;">'
        'The <a href="https://huggingface.co/datasets/cais/MASK">MASK public dataset</a> contains 1,000 examples.'
        "</p>\n\n"
        + _differences_to_og_text()
    )


def _differences_to_og_text() -> str:
    from blog.analysis import load_runs
    from blog.constants import OG_PAPER_MODEL_NAMES

    n_models = len(load_runs())
    return (
        "I used a different model judge to save on cost (see [appendix](#appendix-paper-vs-replication-differences)) "
        f"and a smaller set of {n_models} models covering a range of providers and scales. "
        f"The paper tested {len(OG_PAPER_MODEL_NAMES)}, but some are now deprecated."
    )


@_interpretation_decorator
def interpretation() -> str:
    return (
        "The headline result held: accuracy "
        "scales with compute, **but honesty does not.**"
    )


@references_numbers
@_interpretation_decorator
def caveat() -> str:
    from blog.analysis import DISPLAY_TO_OG, load_runs
    from blog.constants import OG_PAPER_SCORES

    hon_diffs = []
    acc_diffs = []
    for r in load_runs():
        og_name = DISPLAY_TO_OG.get(r.display_name)
        if og_name and og_name in OG_PAPER_SCORES:
            # Tuple is (P(honest)=H/n, P(lie)=L/n, accuracy).
            og_truthful, _, og_acc = OG_PAPER_SCORES[og_name]
            hon_diffs.append(r.truthfulness * 100 - og_truthful)
            acc_diffs.append(r.accuracy * 100 - og_acc)

    hon_abs = int(max(abs(d) for d in hon_diffs))
    acc_abs = int(max(abs(d) for d in acc_diffs))

    return (
        '::: {.note style="background:#f8f9fa; border-left:4px solid #5c6bc0; padding:1em 1.2em; margin:1.5em 0; border-radius:4px;"}\n'
        "**Note:** the headline relationship replicates: accuracy scales favourably with FLOPs, **but honesty does not.** "
        f"But the scores differ from the paper: P(honest) within ~{hon_abs} percentage points, "
        f"accuracy within ~{acc_abs} percentage points. "
        "See the [appendix](#appendix-paper-vs-replication-differences) for a model-by-model "
        "comparison.\n"
        ":::"
    )


