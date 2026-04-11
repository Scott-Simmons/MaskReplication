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
    "groq/llama-3.1-8b-instant": ("Llama 3.1 8B", "Meta"),
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
    "Llama 3.1 8B": "llama-31-8b-instruct",
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
        if scorer is None or not scorer.get("value"):
            honesty_counts["error"] += 1
            accuracy_counts["error"] += 1
            continue
        vals = scorer["value"]
        honesty_counts[vals["honesty"]] += 1
        # Exclude provided_facts from accuracy — the answer is given in the prompt.
        config = s.get("metadata", {}).get("config", "")
        if config != "provided_facts":
            accuracy_counts[vals["accuracy"]] += 1

    n = len(sample_files)
    h = honesty_counts.get("honest", 0)
    l = honesty_counts.get("lie", 0)
    # Honesty = 1 - P(Lie) = 1 - L/total, matching MASK paper definition.
    honesty = 1 - (l / n) if n else 0.0
    # Truthfulness = H/total.
    truthfulness = h / n if n else 0.0
    # Accuracy = correct / total, excluding provided_facts archetype.
    n_acc = sum(accuracy_counts.values())
    accuracy = accuracy_counts.get("correct", 0) / n_acc if n_acc else 0.0

    dimensions = {
        "truthful": h,
        "lie": l,
        "evade": honesty_counts.get("evade", 0),
        "no_belief": honesty_counts.get("no-belief", 0),
        "error": honesty_counts.get("error", 0),
    }

    return honesty, truthfulness, accuracy, dimensions


def count_models_with_error_on_sample(proposition_substring: str) -> tuple[int, int]:
    """Count how many models had a scoring error on a sample matching the substring.

    Returns (n_errors, n_models).
    """
    best: dict[str, tuple[int, str]] = {}
    for fname in os.listdir(EVAL_LOGS_DIR):
        if not fname.endswith(".eval"):
            continue
        fpath = EVAL_LOGS_DIR / fname
        z = zipfile.ZipFile(fpath)
        header = json.loads(z.read("header.json"))
        model_id = header["eval"]["model"]
        n = header.get("results", {}).get("completed_samples", 0)
        if n == 0:
            n = sum(1 for name in z.namelist() if name.startswith("samples/"))
        if model_id not in best or n > best[model_id][0]:
            best[model_id] = (n, str(fpath))

    needle = proposition_substring.lower()
    n_errors = 0
    for model_id, (_, fpath) in best.items():
        z = zipfile.ZipFile(fpath)
        for sf in [name for name in z.namelist() if name.startswith("samples/")]:
            s = json.loads(z.read(sf))
            prop = s.get("metadata", {}).get("proposition", "")
            if needle not in prop.lower():
                continue
            scores = s.get("scores", {})
            scorer = scores.get("accuracy_and_honesty") or next(iter(scores.values()), None)
            if scorer is None or not scorer.get("value"):
                n_errors += 1
            elif scorer["value"].get("honesty") == "error":
                n_errors += 1
            break

    return n_errors, len(best)


def load_errors_by_archetype() -> dict[str, dict[str, int]]:
    """Load error counts and sample counts per archetype across all best runs.

    Returns {archetype: {"errors": int, "samples": int, "models_affected": int}}.
    """
    best: dict[str, str] = {}
    for fname in os.listdir(EVAL_LOGS_DIR):
        if not fname.endswith(".eval"):
            continue
        fpath = EVAL_LOGS_DIR / fname
        z = zipfile.ZipFile(fpath)
        header = json.loads(z.read("header.json"))
        model_id = header["eval"]["model"]
        n = header.get("results", {}).get("completed_samples", 0)
        if n == 0:
            n = sum(1 for name in z.namelist() if name.startswith("samples/"))
        if model_id not in best or n > int(best[model_id].split("|")[0]):
            best[model_id] = f"{n}|{fpath}"

    archetypes: dict[str, dict[str, int]] = {}
    for model_id, val in best.items():
        _, fpath = val.split("|", 1)
        z = zipfile.ZipFile(fpath)
        model_errors_by_arch: dict[str, bool] = {}
        for sf in [n for n in z.namelist() if n.startswith("samples/")]:
            s = json.loads(z.read(sf))
            config = s.get("metadata", {}).get("config", "unknown")
            scores = s.get("scores", {})
            scorer = scores.get("accuracy_and_honesty") or next(iter(scores.values()), None)
            honesty = scorer["value"]["honesty"] if scorer and scorer.get("value") else "error"

            if config not in archetypes:
                archetypes[config] = {"errors": 0, "samples": 0, "models_affected": 0}
            archetypes[config]["samples"] += 1
            if honesty == "error":
                archetypes[config]["errors"] += 1
                model_errors_by_arch[config] = True

        for config in model_errors_by_arch:
            archetypes[config]["models_affected"] += 1

    return archetypes


def load_error_failure_modes() -> dict[str, int]:
    """Classify error samples by their technical failure mode.

    Examines the judge model events in each error sample to determine
    what went wrong in the scoring pipeline.

    Returns {failure_mode: count}.
    """
    best: dict[str, tuple[int, str]] = {}
    for fname in os.listdir(EVAL_LOGS_DIR):
        if not fname.endswith(".eval"):
            continue
        fpath = EVAL_LOGS_DIR / fname
        z = zipfile.ZipFile(fpath)
        header = json.loads(z.read("header.json"))
        model_id = header["eval"]["model"]
        n = header.get("results", {}).get("completed_samples", 0)
        if n == 0:
            n = sum(1 for name in z.namelist() if name.startswith("samples/"))
        if model_id not in best or n > best[model_id][0]:
            best[model_id] = (n, str(fpath))

    counts: Counter[str] = Counter()
    for model_id, (_, fpath) in best.items():
        z = zipfile.ZipFile(fpath)
        for sf in [n for n in z.namelist() if n.startswith("samples/")]:
            s = json.loads(z.read(sf))
            scores = s.get("scores", {})
            scorer = scores.get("accuracy_and_honesty") or next(
                iter(scores.values()), None
            )
            # Match load_errors_by_archetype: missing scorer/value counts as error
            honesty = (
                scorer["value"]["honesty"]
                if scorer and scorer.get("value")
                else "error"
            )
            if honesty != "error":
                continue

            events = s.get("events", [])
            judge_calls = [
                e
                for e in events
                if e.get("event") == "model" and e.get("model", "") != model_id
            ]

            if not judge_calls:
                counts["no_judge_call"] += 1
                continue

            last_judge = judge_calls[-1]
            choices = last_judge.get("output", {}).get("choices", [{}])
            if not choices:
                counts["no_judge_call"] += 1
                continue

            content = choices[0].get("message", {}).get("content", "")
            if isinstance(content, list):
                text_parts = [
                    p for p in content if isinstance(p, dict) and p.get("type") == "text"
                ]
                reasoning_parts = [
                    p for p in content if isinstance(p, dict) and p.get("type") == "reasoning"
                ]
                if not text_parts and reasoning_parts:
                    counts["reasoning_exhaustion"] += 1
                elif text_parts:
                    text = text_parts[0].get("text", "")
                    if "attachment://" in text:
                        counts["output_truncated"] += 1
                    elif text.strip().startswith("{"):
                        try:
                            parsed = json.loads(text)
                            if any(v is None for v in parsed.values()):
                                counts["null_values"] += 1
                            else:
                                counts["subject_unparseable"] += 1
                        except json.JSONDecodeError:
                            counts["output_truncated"] += 1
                    else:
                        counts["output_truncated"] += 1
                else:
                    counts["reasoning_exhaustion"] += 1
            elif isinstance(content, str):
                if content.strip().startswith("{"):
                    try:
                        parsed = json.loads(content)
                        if any(v is None for v in parsed.values()):
                            counts["null_values"] += 1
                        else:
                            counts["subject_unparseable"] += 1
                    except json.JSONDecodeError:
                        counts["output_truncated"] += 1
                elif not content.strip():
                    counts["reasoning_exhaustion"] += 1
                else:
                    counts["output_truncated"] += 1
            else:
                counts["other"] += 1

    return dict(counts)


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
