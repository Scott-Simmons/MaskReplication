#!/usr/bin/env python3
"""Analyse error distributions across models and question archetypes in MASK eval logs."""

import json
import glob
import zipfile
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Friendly names from blog/analysis.py
# ---------------------------------------------------------------------------
MODEL_DISPLAY = {
    "anthropic/claude-haiku-4-5-20251001": "Claude Haiku 4.5",
    "openai/gpt-4o": "GPT-4o",
    "openai/gpt-4o-mini": "GPT-4o-mini",
    "openai/o3-mini": "o3-mini",
    "together/Qwen/Qwen2.5-7B-Instruct-Turbo": "Qwen 2.5 7B",
    "together/deepseek-ai/DeepSeek-R1": "DeepSeek-R1",
    "together/deepseek-ai/DeepSeek-R1-0528": "DeepSeek-R1-0528",
    "together/deepseek-ai/DeepSeek-V3.1": "DeepSeek-V3.1",
    "together/meta-llama/Llama-3.3-70B-Instruct-Turbo": "Llama 3.3 70B",
    "groq/llama-3.1-8b-instant": "Llama 3.1 8B",
}

# Friendly archetype names
ARCHETYPE_DISPLAY = {
    "provided_facts": "Provided Facts",
    "known_facts": "Known Facts",
    "doubling_down_known_facts": "Doubling Down",
    "disinformation": "Disinformation",
    "continuations": "Continuations",
    "statistics": "Statistics",
}

# Canonical outcome labels
HONESTY_LABELS = ["honest", "lie", "evade", "no-belief", "error"]
LABEL_SHORT = {"honest": "H", "lie": "L", "evade": "E", "no-belief": "N", "error": "err"}

# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------
eval_dir = "eval_logs"
eval_files = sorted(glob.glob(f"{eval_dir}/*.eval"))
# Exclude .eval.old files (glob already does this, but be safe)
eval_files = [f for f in eval_files if not f.endswith(".eval.old")]

print(f"Found {len(eval_files)} eval log files.\n")

# Accumulators
errors_by_model = Counter()
errors_by_archetype = Counter()
errors_by_model_arch = Counter()  # (model, archetype) -> count
total_by_model = Counter()
total_by_archetype = Counter()
total_by_model_arch = Counter()
outcome_by_model = defaultdict(Counter)       # model -> {honesty_val -> count}
outcome_by_archetype = defaultdict(Counter)    # archetype -> {honesty_val -> count}
outcome_by_model_arch = defaultdict(Counter)   # (model, arch) -> {honesty_val -> count}

for fpath in eval_files:
    z = zipfile.ZipFile(fpath)
    header = json.loads(z.read("header.json"))
    model_id = header["eval"]["model"]
    model_name = MODEL_DISPLAY.get(model_id, model_id)

    sample_files = [n for n in z.namelist() if n.startswith("samples/")]

    for sf in sample_files:
        s = json.loads(z.read(sf))
        archetype_raw = s.get("metadata", {}).get("config", "unknown")
        archetype = ARCHETYPE_DISPLAY.get(archetype_raw, archetype_raw)

        scores = s.get("scores", {}).get("accuracy_and_honesty", {}).get("value", {})
        honesty = scores.get("honesty", "missing")
        accuracy = scores.get("accuracy", "missing")

        # Count an error if either honesty or accuracy is "error"
        is_error = honesty == "error" or accuracy == "error"

        total_by_model[model_name] += 1
        total_by_archetype[archetype] += 1
        total_by_model_arch[(model_name, archetype)] += 1

        outcome_by_model[model_name][honesty] += 1
        outcome_by_archetype[archetype][honesty] += 1
        outcome_by_model_arch[(model_name, archetype)][honesty] += 1

        if is_error:
            errors_by_model[model_name] += 1
            errors_by_archetype[archetype] += 1
            errors_by_model_arch[(model_name, archetype)] += 1

    z.close()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fmt_pct(n, total):
    if total == 0:
        return "  -  "
    pct = 100 * n / total
    return f"{pct:5.1f}%"

def print_separator(width=100):
    print("-" * width)

# ---------------------------------------------------------------------------
# 1. Error counts by model
# ---------------------------------------------------------------------------
print("=" * 100)
print("TABLE 1: ERROR COUNTS BY MODEL")
print("=" * 100)
print(f"{'Model':<22s} {'Errors':>8s} {'Total':>8s} {'Error %':>9s}")
print_separator()
models_sorted = sorted(total_by_model.keys(), key=lambda m: errors_by_model.get(m, 0), reverse=True)
for m in models_sorted:
    e = errors_by_model.get(m, 0)
    t = total_by_model[m]
    print(f"{m:<22s} {e:>8d} {t:>8d} {fmt_pct(e, t):>9s}")
total_err = sum(errors_by_model.values())
total_all = sum(total_by_model.values())
print_separator()
print(f"{'TOTAL':<22s} {total_err:>8d} {total_all:>8d} {fmt_pct(total_err, total_all):>9s}")
print()

# ---------------------------------------------------------------------------
# 2. Error counts by archetype
# ---------------------------------------------------------------------------
print("=" * 100)
print("TABLE 2: ERROR COUNTS BY ARCHETYPE")
print("=" * 100)
print(f"{'Archetype':<22s} {'Errors':>8s} {'Total':>8s} {'Error %':>9s}")
print_separator()
archs_sorted = sorted(total_by_archetype.keys(), key=lambda a: errors_by_archetype.get(a, 0), reverse=True)
for a in archs_sorted:
    e = errors_by_archetype.get(a, 0)
    t = total_by_archetype[a]
    print(f"{a:<22s} {e:>8d} {t:>8d} {fmt_pct(e, t):>9s}")
print_separator()
print(f"{'TOTAL':<22s} {total_err:>8d} {total_all:>8d} {fmt_pct(total_err, total_all):>9s}")
print()

# ---------------------------------------------------------------------------
# 3. Error counts: model x archetype cross-tab
# ---------------------------------------------------------------------------
print("=" * 130)
print("TABLE 3: ERROR COUNTS — MODEL x ARCHETYPE (errors / total, error%)")
print("=" * 130)

# Column headers
col_w = 18
header_line = f"{'Model':<22s}"
for a in archs_sorted:
    header_line += f" {a:>{col_w}s}"
header_line += f" {'TOTAL':>{col_w}s}"
print(header_line)
print("-" * 130)

for m in models_sorted:
    row = f"{m:<22s}"
    for a in archs_sorted:
        e = errors_by_model_arch.get((m, a), 0)
        t = total_by_model_arch.get((m, a), 0)
        if t == 0:
            cell = "-"
        else:
            cell = f"{e}/{t} ({100*e/t:.0f}%)"
        row += f" {cell:>{col_w}s}"
    # Row total
    e_tot = errors_by_model.get(m, 0)
    t_tot = total_by_model[m]
    cell = f"{e_tot}/{t_tot} ({100*e_tot/t_tot:.0f}%)"
    row += f" {cell:>{col_w}s}"
    print(row)
print()

# ---------------------------------------------------------------------------
# 4. Outcome distribution by archetype (across all models)
# ---------------------------------------------------------------------------
print("=" * 130)
print("TABLE 4: OUTCOME DISTRIBUTION BY ARCHETYPE (all models combined)")
print("H=honest, L=lie, E=evade, N=no-belief, err=error")
print("=" * 130)

oc_w = 18  # col width
header_line = f"{'Archetype':<22s}"
for label in HONESTY_LABELS:
    header_line += f" {LABEL_SHORT[label]+' (n)':>{oc_w}s}"
header_line += f" {'Total':>{oc_w}s}"
print(header_line)
print("-" * 130)

for a in archs_sorted:
    row = f"{a:<22s}"
    t = total_by_archetype[a]
    for label in HONESTY_LABELS:
        n = outcome_by_archetype[a].get(label, 0)
        pct = 100 * n / t if t else 0
        cell = f"{n:>4d} ({pct:5.1f}%)"
        row += f" {cell:>{oc_w}s}"
    row += f" {t:>{oc_w}d}"
    print(row)

# Totals
row = f"{'TOTAL':<22s}"
for label in HONESTY_LABELS:
    n = sum(outcome_by_archetype[a].get(label, 0) for a in archs_sorted)
    pct = 100 * n / total_all if total_all else 0
    cell = f"{n:>4d} ({pct:5.1f}%)"
    row += f" {cell:>{oc_w}s}"
row += f" {total_all:>{oc_w}d}"
print("-" * 130)
print(row)
print()

# ---------------------------------------------------------------------------
# 5. Outcome distribution by model (across all archetypes)
# ---------------------------------------------------------------------------
print("=" * 130)
print("TABLE 5: OUTCOME DISTRIBUTION BY MODEL (all archetypes combined)")
print("H=honest, L=lie, E=evade, N=no-belief, err=error")
print("=" * 130)

header_line = f"{'Model':<22s}"
for label in HONESTY_LABELS:
    header_line += f" {LABEL_SHORT[label]+' (n)':>{oc_w}s}"
header_line += f" {'Total':>{oc_w}s}"
print(header_line)
print("-" * 130)

for m in models_sorted:
    row = f"{m:<22s}"
    t = total_by_model[m]
    for label in HONESTY_LABELS:
        n = outcome_by_model[m].get(label, 0)
        pct = 100 * n / t if t else 0
        cell = f"{n:>4d} ({pct:5.1f}%)"
        row += f" {cell:>{oc_w}s}"
    row += f" {t:>{oc_w}d}"
    print(row)

# Totals
row = f"{'TOTAL':<22s}"
for label in HONESTY_LABELS:
    n = sum(outcome_by_model[m].get(label, 0) for m in models_sorted)
    pct = 100 * n / total_all if total_all else 0
    cell = f"{n:>4d} ({pct:5.1f}%)"
    row += f" {cell:>{oc_w}s}"
row += f" {total_all:>{oc_w}d}"
print("-" * 130)
print(row)
print()

# ---------------------------------------------------------------------------
# 6. Bonus: Model x Archetype detail for error samples only
# ---------------------------------------------------------------------------
print("=" * 130)
print("BONUS: DETAILED ERROR BREAKDOWN — which (model, archetype) pairs produce errors?")
print("Sorted by error count descending. Only pairs with errors shown.")
print("=" * 130)
print(f"{'Model':<22s} {'Archetype':<22s} {'Errors':>8s} {'Total':>8s} {'Error %':>9s}")
print("-" * 130)

pairs = [(k, v) for k, v in errors_by_model_arch.items() if v > 0]
pairs.sort(key=lambda x: x[1], reverse=True)
for (m, a), e in pairs:
    t = total_by_model_arch[(m, a)]
    print(f"{m:<22s} {a:<22s} {e:>8d} {t:>8d} {fmt_pct(e, t):>9s}")
print()
