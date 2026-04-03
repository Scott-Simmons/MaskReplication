def recap() -> str:
    return "\n".join([
        "If this is interesting to you, the eval logs and analysis code are available at "
        "[this repo](https://github.com/Scott-Simmons/MaskReplication). You can add more "
        "models by running the MASK eval from "
        "[inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) and dropping "
        "the `.eval` files into the `eval_logs/` directory. Everything regenerates with "
        "`make blog-post`. I would particularly be interested in contributions from "
        "abliterated models and whatever the frontier looks like next month.",
        "",
        "Here is the invocation I used:",
        "",
        "```bash",
        "# inspect_evals 0.6.1.dev4, inspect_ai 0.3.190.dev29, mask version 3-C",
        "inspect eval inspect_evals/mask \\",
        "    --model <YOUR_MODEL> \\",
        "    --log-dir ./eval_logs \\",
        '    -T binary_judge_model="openai/gpt-4o-mini"',
        "```",
    ])


def encourage_the_basis_framing() -> str:
    return ""
