def recap() -> str:
    return "\n".join(
        [
            "If this is interesting to you, the eval logs and analysis code are available at "
            "[this repo](https://github.com/Scott-Simmons/MaskReplication). You can add more "
            "models by running the MASK eval from "
            "[inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/mask) and dropping "
            "the `.eval` files into the `eval_logs/` directory. All results in this article will regenerate with "
            "`make clean build`.",
            "",
            "Here is an invocation to get you started:",
            "",
            "```bash",
            "# inspect_evals 0.6.1.dev4, inspect_ai 0.3.190.dev29, mask version 3-C",
            "inspect eval inspect_evals/mask \\",
            "    --model <YOUR_MODEL> \\",
            "    --log-dir ./eval_logs \\",
            "    --retry-on-error 5 \\",
            '    -T binary_judge_model="openai/gpt-4o-mini"',
            "```",
            "",
            "I would particularly be interested in contributions from "
            "abliterated models, (current and future) frontier models, and xAI models, which would be "
            "interesting given the "
            '[stated emphasis](https://x.com/elonmusk/status/1948572708369039542) on building "maximally truth-seeking" AI. '
            "Right now, with respect to honesty, Anthropic models appear to be in another league.",
        ]
    )
