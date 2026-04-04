def paper_vs_replication() -> str:
    return "\n".join(
        [
            "While the headline result holds, specific differences between the paper and this replication are likely caused by:",
            "",
            "1. **Different eval harness.** I replicated mask with [Inspect AI](https://inspect.ai), not the original codebase. I used the mask paper as a reference, but there could still be implementation differences w.r.t. the original code.",
            "2. **Model API drift.** Model weights and serving infrastructure change over time. For the non-local models, will not be able to replicate against the exact checkpoint the paper used.",
            "3. **Different eval judges.** My replication uses gpt-4o-mini as the judge for yes/no questions. The original paper used gpt-4o. I did this to save on costs.",
        ]
    )
