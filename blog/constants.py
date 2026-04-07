"""Constants from the original MASK paper (Ren et al., 2025) and Epoch AI."""

OG_PAPER_MODEL_NAMES = [
    "claude-3-5-sonnet-20240620",
    "claude-3-7-sonnet-20250219",
    "deepseek-r1",
    "deepseek-v3",
    "deepseek-llm-67b-chat",
    "gemini-2.0-flash",
    "gpt-4.5-preview-2025-02-27",
    "gpt-4o-2024-08-06",
    "gpt-4o-mini-2024-07-18",
    "grok-2-1212",
    "llama-2-13b-chat",
    "llama-2-70b-chat",
    "llama-2-7b-chat",
    "llama-31-405b-instruct",
    "llama-31-70b-instruct",
    "llama-31-8b-instruct",
    "llama-32-1b-instruct",
    "llama-32-3b-instruct",
    "llama-33-70b-instruct",
    "o3-mini-2025-01-31",
    "qwen15-110b-chat",
    "qwen15-32b-chat",
    "qwen15-72b-chat",
    "qwen15-7b-chat",
    "qwen25-05b-instruct",
    "qwen25-14b-instruct",
    "qwen25-15b-instruct",
    "qwen25-32b-instruct",
    "qwen25-3b-instruct",
    "qwen25-72b-instruct",
    "qwen25-7b-instruct",
    "qwq-32b-preview",
]

# Approximate log10(training FLOP) estimates.
#
# Sources:
#   Epoch AI Notable AI Models database (https://epoch.ai/data/notable-ai-models)
#   Accessed 2026-04-03. Downloaded from https://epoch.ai/data/notable_ai_models.csv
#
# Confidence levels:
#   "confident"  — Epoch computed from known architecture + token count (6ND or GPU-hours)
#   "speculative" — Epoch estimated from benchmark scores, not architecture/training details
#   "unknown"    — No estimate available in Epoch; Anthropic/OpenAI have not disclosed
#
# For models with no Epoch estimate, value is None.
LOG10_FLOP: dict[str, tuple[float | None, str]] = {
    # Confident (Epoch AI, open-weight models)
    "together/Qwen/Qwen2.5-7B-Instruct-Turbo": (23.91, "confident"),   # 8.22e23: 6 × 7.61B × 18T tokens
    "together/deepseek-ai/DeepSeek-R1": (24.54, "confident"),           # 3.5e24: 37B active × 14.8T + RL
    "together/deepseek-ai/DeepSeek-V3.1": (24.56, "confident"),         # 3.59e24: V3 base + continued pretraining
    "together/deepseek-ai/DeepSeek-R1-0528": (24.60, "confident"),      # 4.02e24: pretraining + post-training + fine-tuning
    "groq/llama-3.1-8b-instant": (23.86, "confident"),                         # 7.21e23: 6 × 8.03B × 15T tokens
    "together/meta-llama/Llama-3.3-70B-Instruct-Turbo": (24.84, "confident"),  # 6.87e24: geomean of 6ND and GPU-hours
    # Speculative (Epoch AI, estimated from benchmark scores)
    "openai/gpt-4o-mini": (24.87, "speculative"),                       # ~7.36e24
    "openai/gpt-4o": (25.58, "speculative"),                            # ~3.8e25
    # Author estimate (not disclosed by Anthropic, not in Epoch AI).
    # Haiku 4.5 is a small, fast model. Assuming ~10-20B params, ~10T tokens
    # gives ~6e23 to 1.2e24 FLOP. We use 24.0 (1e24) as a rough midpoint.
    # TREAT WITH EXTREME CAUTION — this is a guess.
    "anthropic/claude-haiku-4-5-20251001": (24.0, "author_estimate"),
    # Author estimate: o3-mini is a reasoning model; OpenAI has not disclosed
    # training compute. Benchmark performance sits between gpt-4o-mini and gpt-4o,
    # suggesting comparable base-model FLOP plus RL overhead. We guess ~25.0
    # (1e25). TREAT WITH EXTREME CAUTION.
    "openai/o3-mini": (25.0, "author_estimate"),
}

# Original paper Table 3 results (Ren et al., 2025).
# Values are percentages: (1 - P(lie), P(lie), accuracy).
# All 32 models from Table 3, keyed by paper model name.
OG_PAPER_SCORES: dict[str, tuple[float, float, float]] = {
    "claude-3-5-sonnet-20240620": (27.7, 33.4, 80.1),
    "claude-3-7-sonnet-20250219": (47.6, 26.6, 82.2),
    "deepseek-r1": (24.7, 42.9, 82.2),
    "deepseek-v3": (20.8, 53.5, 71.6),
    "deepseek-llm-67b-chat": (18.6, 45.6, 64.3),
    "gemini-2.0-flash": (20.7, 48.4, 79.4),
    "gpt-4.5-preview-2025-02-27": (27.2, 43.5, 76.7),
    "gpt-4o-2024-08-06": (21.8, 44.5, 78.6),
    "gpt-4o-mini-2024-07-18": (21.4, 45.3, 71.4),
    "grok-2-1212": (14.2, 63.0, 72.5),
    "llama-2-13b-chat": (28.7, 24.7, 40.1),
    "llama-2-70b-chat": (28.3, 26.7, 40.6),
    "llama-2-7b-chat": (27.5, 21.5, 33.6),
    "llama-31-405b-instruct": (21.6, 28.0, 72.1),
    "llama-31-70b-instruct": (27.1, 43.5, 73.8),
    "llama-31-8b-instruct": (18.8, 23.5, 62.0),
    "llama-32-1b-instruct": (13.9, 13.1, 23.0),
    "llama-32-3b-instruct": (21.8, 23.5, 40.0),
    "llama-33-70b-instruct": (24.7, 44.9, 75.6),
    "o3-mini-2025-01-31": (19.6, 48.6, 63.3),
    "qwen15-110b-chat": (27.9, 35.6, 72.8),
    "qwen15-32b-chat": (23.8, 42.5, 63.0),
    "qwen15-72b-chat": (24.2, 47.8, 69.3),
    "qwen15-7b-chat": (27.1, 35.1, 52.5),
    "qwen25-05b-instruct": (15.9, 15.4, 20.8),
    "qwen25-14b-instruct": (26.5, 47.7, 64.4),
    "qwen25-15b-instruct": (25.7, 26.9, 28.8),
    "qwen25-32b-instruct": (28.7, 43.9, 63.7),
    "qwen25-3b-instruct": (30.7, 33.8, 46.8),
    "qwen25-72b-instruct": (23.2, 49.2, 66.0),
    "qwen25-7b-instruct": (28.9, 39.0, 51.6),
    "qwq-32b-preview": (20.3, 25.2, 49.2),
}
