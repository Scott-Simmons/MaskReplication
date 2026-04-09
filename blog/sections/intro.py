from blog.decorators import interpretation


@interpretation
def tldr() -> str:
    return (
        "**TLDR:** I replicated an AI honesty benchmark's headline result: that scaling improves accuracy "
        "but not honesty. I also show various ways that the honesty score hides "
        "nuance, and why reporting the full outcome set, error reporting, and uncertainty analysis "
        "is the way forward for deception evaluation, and evaluation science in general."
    )


def toc() -> str:
    return "\n".join(
        [
            "**Contents:**\n\n"
            "1. [Introduction](#introduction)\n"
            "2. [Replication results](#replication-results)\n"
            "3. [Dimensions of deception](#dimensions-of-deception)\n"
            "4. [Reporting errors and uncertainty](#reporting-errors-and-uncertainty)\n"
            "5. [Try it yourself](#try-it-yourself)\n"
            "6. [Appendix](#appendix-paper-vs-replication-differences)",
        ]
    )


def intro() -> str:
    return "---\n\n" + (
        "Truth is tricky. For starters, we cannot be sure that we actually "
        "know it. But even when we think we do know it, many of us lie "
        "in public anyway, because it can conflict with what's "
        "socially comfortable. Saying true things in the face of that pressure requires "
        "intelligence and courage (subject to a certain amount of tact). It's also how "
        "things progress. Galileo was put under house arrest for the rest of his "
        "life for saying the Earth goes around the Sun. He was right, everyone eventually "
        "agreed, and science moved forward."
    )


def link_to_ai() -> str:
    return (
        "Just like we can hide our underlying beliefs when subject to social "
        "pressure, AI models can hide their 'internal beliefs'[^internal_beliefs] when subject to pressure from a "
        "prompt. And while scaling up AI models has made them more "
        "capable, a result from [Ren et al., 2025](https://arxiv.org/abs/2503.03750) suggests that "
        "larger models are not more honest."
    )


def how_i_reacted() -> str:
    return (
        "When I first saw this result, I was provoked. "
        "How is lying defined? How is truth established? "
        "The paper addresses many of these questions, and while some questions "
        "remain,[^open_questions] two questions I want to address in this post are:\n\n"
    )


def what_i_will_do() -> str:
    return (
        "### [1. Does this result survive independent replication?](#replication-results)\n\n"
        "### [2. Are there any other measures that can help us to characterise deception?]"
        "(#dimensions-of-deception)"
    )
