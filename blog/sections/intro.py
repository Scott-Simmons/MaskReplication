def tldr() -> str:
    return (
        "**TLDR:** I replicated the MASK benchmark's headline result that scaling improves accuracy "
        "but not honesty. I also show various ways that the honesty score hides "
        "nuance. I show why reporting the full outcome set is useful, and argue for reporting raw counts, "
        "including errors, and error bars as the way forward for deception evaluation, "
        "and evaluations in general."
    )


def toc() -> str:
    return "\n".join(
        [
            "**Contents:** "
            "[1. Introduction](#introduction) | "
            "[2. Replication results](#replication-results) | "
            "[3. Dimensions of deception](#dimensions-of-deception) | "
            "[4. Try it yourself](#try-it-yourself) | "
            "[Appendix](#appendix-paper-vs-replication-differences)",
        ]
    )


def intro() -> str:
    return "---\n\n" + (
        "Truth is often inconvenient. For starters, we cannot be sure that we actually "
        "know it. But even when we think we do know it, many of us lie to "
        "others in public anyway, because it can conflict with what's "
        "socially comfortable. Saying true things in the face of that pressure requires "
        "intelligence and courage (subject to a certain amount of tact). It's also how "
        "things change. Galileo was put under house arrest for the rest of his "
        "life for saying the Earth goes around the Sun. He was right, everyone eventually "
        "agreed, and science moved forward."
    )


def link_to_ai() -> str:
    return (
        "Just like we can hide our underlying beliefs when subject to social "
        "pressure, AI models can hide their 'internal beliefs'[^internal_beliefs] subject to pressure from a "
        "prompt. And while scaling up AI models has made them more "
        "capable, a result from [Ren et al., 2025](https://arxiv.org/abs/2503.03750) suggests that "
        "larger models are not more honest."
    )


def how_i_reacted() -> str:
    return (
        "When I first saw this, it was quite a provocative result. For many reasons. "
        "How is lying defined? How is truth established? Many of these questions are "
        "answered in the paper, and questions remain.[^open_questions] "
        "But two questions I want to address in this blog post are:\n\n"
        "### [1. Does this survive independent replication?](#replication-results)\n\n"
        "### [2. Are there any other measures that can help characterise deception?]"
        "(#dimensions-of-deception)"
    )
