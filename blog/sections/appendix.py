def citation() -> str:
    return "\n".join([
        "<details>",
        "<summary>BibTeX</summary>",
        "",
        "```bibtex",
        "@misc{ren2025maskbenchmarkdisentanglinghonesty,",
        "      title={The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems},",
        "      author={Richard Ren and Arunim Agarwal and Mantas Mazeika and Cristina Menghini and Robert Vacareanu and Brad Kenstler and Mick Yang and Isabelle Barrass and Alice Gatti and Xuwang Yin and Eduardo Trevino and Matias Geralnik and Adam Khoja and Dean Lee and Summer Yue and Dan Hendrycks},",
        "      year={2025},",
        "      eprint={2503.03750},",
        "      archivePrefix={arXiv},",
        "      primaryClass={cs.LG},",
        "      url={https://arxiv.org/abs/2503.03750},",
        "}",
        "```",
        "",
        "</details>",
    ])


def paper_vs_replication() -> str:
    return "\n".join(
        [
            "While the headline result holds, specific differences between the paper and this replication are likely caused by:",
            "",
            "1. **Different eval harness.** I replicated MASK with [Inspect AI](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/), not the original codebase. I used the MASK paper as a reference, but there could still be implementation differences w.r.t. the original code.",
            "2. **Model API drift.** Non-open-weight models may have drifted since the paper's evaluation window.",
            "3. **Different eval judges.** My replication uses gpt-4o-mini as the judge for yes/no questions. The original paper used gpt-4o. I did this to save on costs.",
        ]
    )


def eval_config_intro() -> str:
    return (
        "Here is a configuration summary, generated from the eval log headers. "
        "The inspect_ai and inspect_evals versions differ across some runs, but that is fine. "
        "The [MASK version](https://ukgovernmentbeis.github.io/inspect_evals/contributing/repo/TASK_VERSIONING.html#task-version-structure) "
        "tracks changes that could affect comparability:"
    )
