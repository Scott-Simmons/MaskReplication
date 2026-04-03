def paper_vs_replication() -> str:
    return "\n".join([
        "Systematic differences between the paper and this replication are likely caused by:",
        "",
        "1. **Different eval harness.** This replication uses [Inspect AI](https://inspect.ai), not the original codebase.",
        "2. **Model API drift.** Model weights and serving infrastructure change over time. We will never know the exact checkpoint the paper used.",
        "3. **<mark>TBD: Different eval judges.</mark>** This replication uses gpt-4o-mini as the judge. The original paper's judge may differ. I may re-run with a matching judge if I can confirm which one the paper used.",
    ])
