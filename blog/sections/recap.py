from blog.decorators import interpretation


@interpretation
def recap() -> str:
    return "\n".join(
        [
            "If this is interesting to you, the eval logs and analysis code are available at "
            "[this repo](https://github.com/Scott-Simmons/MaskReplication). You can add more "
            "models by running the MASK eval from "
            "[inspect_evals](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/) and dropping "
            "the `.eval` files into the `eval_logs/` directory.\n\nAll results in this article will regenerate with "
            "`make clean build`. Raise a PR!",
            "",
            "Here is an invocation to get you started (you will need to install [inspect_evals](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/#installation)):",
            "",
            "```bash",
            "inspect eval inspect_evals/mask \\",
            "    --model <A_NEW_MODEL_TO_ADD> \\",
            "    --log-dir ./eval_logs \\",
            "    --retry-on-error 5 \\",
            '    -T binary_judge_model="openai/gpt-4o-mini"',
            "```",
            "",
            "I am particularly interested in contributions from "
            "[abliterated models](https://huggingface.co/blog/mlabonne/abliteration), (current and future) frontier models, and xAI models, which would be "
            "interesting given their "
            '[stated emphasis](https://x.com/elonmusk/status/1948572708369039542) on building "maximally truth-seeking" AI. '
            "Right now, with respect to honesty, Anthropic models appear to be in [another league](https://labs.scale.com/leaderboard/mask).",
        ]
    )
