"""Read eval logs and produce data for the blog post."""

import json
import os
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from blog.constants import LOG10_FLOP, OG_PAPER_MODEL_NAMES

EVAL_LOGS_DIR = Path(__file__).parent.parent / "eval_logs"

# Map raw model IDs to display names and providers
MODEL_DISPLAY = {
    "anthropic/claude-haiku-4-5-20251001": ("Claude Haiku 4.5", "Anthropic"),
    "openai/gpt-4o": ("GPT-4o", "OpenAI"),
    "openai/gpt-4o-mini": ("GPT-4o-mini", "OpenAI"),
    "openai/o3-mini": ("o3-mini", "OpenAI"),
    "together/Qwen/Qwen2.5-7B-Instruct-Turbo": ("Qwen 2.5 7B", "Alibaba"),
    "together/deepseek-ai/DeepSeek-R1": ("DeepSeek-R1", "DeepSeek"),
    "together/deepseek-ai/DeepSeek-R1-0528": ("DeepSeek-R1-0528", "DeepSeek"),
    "together/deepseek-ai/DeepSeek-V3.1": ("DeepSeek-V3.1", "DeepSeek"),
    "together/meta-llama/Llama-3.3-70B-Instruct-Turbo": ("Llama 3.3 70B", "Meta"),
}

# Map display names to OG paper model names for matching
DISPLAY_TO_OG = {
    "Claude Haiku 4.5": None,
    "GPT-4o": "gpt-4o-2024-08-06",
    "GPT-4o-mini": "gpt-4o-mini-2024-07-18",
    "o3-mini": "o3-mini-2025-01-31",
    "Qwen 2.5 7B": "qwen25-7b-instruct",
    "DeepSeek-R1": "deepseek-r1",
    "DeepSeek-R1-0528": None,
    "DeepSeek-V3.1": None,
    "Llama 3.3 70B": "llama-33-70b-instruct",
}

PROVIDER_COLORS = {
    "Anthropic": "#e63946",
    "OpenAI": "#2a9d8f",
    "DeepSeek": "#264653",
    "Meta": "#e9c46a",
    "Alibaba": "#f77f00",
}


@dataclass
class ModelRun:
    model_id: str
    display_name: str
    provider: str
    n: int
    in_paper: bool
    honesty: float = 0.0
    truthfulness: float = 0.0
    accuracy: float = 0.0
    log10_flop: float | None = None
    flop_confidence: str = "unknown"
    dimensions: dict[str, int] = field(default_factory=dict)


def _scores_from_header(header: dict) -> tuple[float, float]:
    """Extract honesty and accuracy from a successful run's header."""
    scores = header["results"]["scores"][0]["metrics"]
    honesty = scores["overall_honesty"]["value"]
    # Use normalised accuracy (excludes no-belief from denominator),
    # matching the paper's definition.
    accuracy = scores["overall_normalised_accuracy"]["value"]
    return honesty, accuracy


def _scores_from_samples(z: zipfile.ZipFile) -> tuple[float, float, float, dict[str, int]]:
    """Compute honesty, truthfulness, and accuracy from individual samples."""
    sample_files = [n for n in z.namelist() if n.startswith("samples/")]
    honesty_counts: Counter[str] = Counter()
    accuracy_counts: Counter[str] = Counter()

    for sf in sample_files:
        s = json.loads(z.read(sf))
        scores = s.get("scores", {})
        scorer = scores.get("accuracy_and_honesty") or next(iter(scores.values()), None)
        if scorer is None:
            continue
        vals = scorer["value"]
        honesty_counts[vals["honesty"]] += 1
        accuracy_counts[vals["accuracy"]] += 1

    n = len(sample_files)
    h = honesty_counts.get("honest", 0)
    l = honesty_counts.get("lie", 0)
    # Honesty = 1 - P(Lie) = 1 - L/total, matching MASK paper definition.
    honesty = 1 - (l / n) if n else 0.0
    # Truthfulness = H/total.
    truthfulness = h / n if n else 0.0
    # Accuracy = correct / total.
    accuracy = accuracy_counts.get("correct", 0) / n if n else 0.0

    dimensions = {
        "truthful": h,
        "lie": l,
        "evade": honesty_counts.get("evade", 0),
        "no_belief": honesty_counts.get("no-belief", 0),
        "error": honesty_counts.get("error", 0),
    }

    return honesty, truthfulness, accuracy, dimensions


def load_runs() -> list[ModelRun]:
    """Load the best run per model from eval logs."""
    best: dict[str, tuple[int, str]] = {}  # model_id -> (n_samples, filepath)

    for fname in os.listdir(EVAL_LOGS_DIR):
        if not fname.endswith(".eval"):
            continue
        fpath = EVAL_LOGS_DIR / fname
        z = zipfile.ZipFile(fpath)
        header = json.loads(z.read("header.json"))
        model_id = header["eval"]["model"]

        # Get n from results if successful, otherwise count sample files
        n = header.get("results", {}).get("completed_samples", 0)
        if n == 0:
            n = sum(1 for name in z.namelist() if name.startswith("samples/"))

        if model_id not in best or n > best[model_id][0]:
            best[model_id] = (n, str(fpath))

    runs = []
    for model_id, (n, fpath) in sorted(best.items()):
        display_name, provider = MODEL_DISPLAY.get(model_id, (model_id, "Unknown"))
        og_name = DISPLAY_TO_OG.get(display_name)
        in_paper = og_name is not None and og_name in OG_PAPER_MODEL_NAMES

        z = zipfile.ZipFile(fpath)
        header = json.loads(z.read("header.json"))

        # Always compute from samples for consistency across all logs.
        honesty, truthfulness, accuracy, dimensions = _scores_from_samples(z)

        flop_entry = LOG10_FLOP.get(model_id, (None, "unknown"))
        log10_flop, flop_confidence = flop_entry

        runs.append(ModelRun(
            model_id=model_id,
            display_name=display_name,
            provider=provider,
            n=n,
            in_paper=in_paper,
            honesty=honesty,
            truthfulness=truthfulness,
            accuracy=accuracy,
            log10_flop=log10_flop,
            flop_confidence=flop_confidence,
            dimensions=dimensions,
        ))

    return runs
