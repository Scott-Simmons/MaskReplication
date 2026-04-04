def recap() -> str:
    return "\n".join(
        [
            "If this is interesting to you, the eval logs and analysis code are available at "
            "[this repo](https://github.com/Scott-Simmons/MaskReplication). You can add more "
            "models by running the MASK eval from "
            "[inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/mask) and dropping "
            "the `.eval` files into the `eval_logs/` directory. All results in this article will regenerate with "
            "`make clean build`. I would particularly be interested in contributions from "
            "abliterated models and the (current and future) frontier.",
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
        ]
    )


def encourage_the_basis_framing() -> str:
    return ""
