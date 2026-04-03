def tldr() -> str:
    return (
        "**TLDR:** I replicate the MASK benchmark's headline result: scaling improves accuracy "
        "but not honesty. I also show various ways that the single honesty score hides "
        "nuance. Two models can score identically while behaving completely differently. "
        "I show why reporting the full basis is useful, and argue for reporting raw counts, "
        "including errors, and error bars as the way forward for deception evaluation."
    )


def intro() -> str:
    return "---\n\n" + (
        "Truth is often inconvenient. For starters, we cannot be sure that we actually "
        "know it. But even when deep down, we think we do know it, many of us lie to "
        "ourselves and others in public anyway, because it can conflict with what's "
        "socially comfortable. Saying true things in the face of that pressure requires "
        "intelligence and courage (subject to a certain amount of tact). It's also how "
        "things actually change. Galileo was put under house arrest for the rest of his "
        "life for saying the Earth goes around the Sun. He was right, everyone eventually "
        "agreed, and science moved forward."
    )


def link_to_ai() -> str:
    return (
        "Just like humans can hide their underlying beliefs when subject to social "
        "pressure, AI models hide their internal beliefs subject to pressure from a "
        "prompt too. And while scaling up AI models has made them dramatically more "
        "capable, [Ren et al., 2025](https://arxiv.org/abs/2503.03750) suggests that "
        "larger models are not more honest."
    )


def how_i_reacted() -> str:
    return (
        "When I first saw this, it was quite a provocative result. For many reasons. "
        "How is lying defined? How is truth established? Many of these questions are "
        "answered in the paper. But two questions remained:\n\n"
        "> 1. [Does this survive independent replication?](#replication-results)\n"
        "> 2. [Are there any other measures that can help characterise deception?]"
        "(#the-limitation-of-honesty-scores-actually-most-1d-projections)"
    )


def what_i_did() -> str:
    from blog.analysis import load_runs

    n_models = len(load_runs())
    return (
        "Last year, I implemented the MASK evaluation into the "
        f"[Inspect AI](https://inspect.ai) framework. In this post, I replicate the "
        f"original headline result across {n_models} models, and propose a basis for "
        "deception analysis that I think gives researchers a more complete picture than any single "
        "honesty score."
    )
