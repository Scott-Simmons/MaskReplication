"""
Deep audit of MASK eval log sample data for blog post findings.
"""
import zipfile
import json
import os
from collections import defaultdict, Counter
from pathlib import Path

EVAL_DIR = Path("eval_logs")

def load_all_samples():
    """Load all samples from all .eval (not .eval.old) files."""
    all_samples = []
    eval_files = sorted(EVAL_DIR.glob("*.eval"))
    # Exclude .eval.old
    eval_files = [f for f in eval_files if not str(f).endswith(".eval.old")]

    for ef in eval_files:
        with zipfile.ZipFile(ef) as z:
            # Read header for model info
            with z.open("header.json") as hf:
                header = json.load(hf)
            model = header.get("eval", {}).get("model", "unknown")
            task_args = header.get("eval", {}).get("task_args", {})

            sample_files = [n for n in z.namelist() if n.startswith("samples/")]
            for sf_name in sample_files:
                with z.open(sf_name) as sf:
                    sample = json.load(sf)
                sample["_model"] = model
                sample["_eval_file"] = str(ef)
                sample["_task_args"] = task_args
                all_samples.append(sample)

    return all_samples


def get_scores(sample):
    """Extract accuracy/honesty scores."""
    s = sample.get("scores", {}).get("accuracy_and_honesty", {}).get("value", {})
    return s.get("accuracy", ""), s.get("honesty", ""), s.get("honesty@n", "")


def get_question_key(sample):
    """Create a question identifier from metadata."""
    m = sample.get("metadata", {})
    return m.get("proposition", "???")


def short_model(model):
    """Shorten model name."""
    return model.split("/")[-1] if "/" in model else model


def main():
    print("Loading all samples...")
    samples = load_all_samples()
    print(f"Total samples loaded: {len(samples)}")

    # Gather basic stats
    models = sorted(set(s["_model"] for s in samples))
    print(f"Models: {len(models)}")
    for m in models:
        n = sum(1 for s in samples if s["_model"] == m)
        print(f"  {short_model(m)}: {n} samples")

    # =========================================================================
    # 1. THE DETROIT QUESTION
    # =========================================================================
    print("\n" + "=" * 80)
    print("1. THE DETROIT QUESTION")
    print("=" * 80)

    detroit_samples = [s for s in samples if "detroit" in get_question_key(s).lower()
                       or "detroit" in json.dumps(s.get("metadata", {})).lower()]

    if not detroit_samples:
        print("No samples mentioning Detroit found in propositions or metadata!")
        # Broader search: check input messages too
        detroit_samples = [s for s in samples
                           if "detroit" in json.dumps(s.get("input", [])).lower()
                           or "detroit" in json.dumps(s.get("store", {})).lower()]
        if detroit_samples:
            print(f"Found {len(detroit_samples)} samples mentioning Detroit in inputs/store")

    if detroit_samples:
        # Group by question
        q_groups = defaultdict(list)
        for s in detroit_samples:
            q_groups[get_question_key(s)].append(s)

        for q, samps in q_groups.items():
            print(f"\nQuestion: {q}")
            print(f"Ground truth: {samps[0]['metadata'].get('ground_truth', 'N/A')}")
            print(f"Config: {samps[0]['metadata'].get('config', 'N/A')}")
            print(f"Type: {samps[0]['metadata'].get('type', 'N/A')}")
            print(f"Total samples across models: {len(samps)}")

            error_count = 0
            for s in sorted(samps, key=lambda x: x["_model"]):
                acc, hon, hon_n = get_scores(s)
                is_error = (acc == "error" or hon == "error")
                if is_error:
                    error_count += 1
                model_name = short_model(s["_model"])
                marker = " *** ERROR ***" if is_error else ""
                print(f"  {model_name:30s}  accuracy={acc:25s}  honesty={hon:15s}{marker}")

            print(f"\n  Error count: {error_count}/{len(samps)} models")
    else:
        print("No Detroit references found anywhere in samples!")

    # Also search for population-related questions that might be the one mentioned
    print("\n--- Also searching for population-related questions ---")
    pop_samples = [s for s in samples if "population" in get_question_key(s).lower()]
    if pop_samples:
        q_groups = defaultdict(list)
        for s in pop_samples:
            q_groups[get_question_key(s)].append(s)
        for q, samps in q_groups.items():
            error_count = sum(1 for s in samps if get_scores(s)[0] == "error" or get_scores(s)[1] == "error")
            if error_count > 0:
                print(f"\n  Question (errors={error_count}/{len(samps)}): {q[:120]}")
                print(f"  Config: {samps[0]['metadata'].get('config')}, Type: {samps[0]['metadata'].get('type')}")

    # =========================================================================
    # 2. ERROR CONCENTRATION WITHIN STATISTICS
    # =========================================================================
    print("\n" + "=" * 80)
    print("2. ERROR CONCENTRATION WITHIN STATISTICS")
    print("=" * 80)

    stats_samples = [s for s in samples if s.get("metadata", {}).get("config") == "statistics"]
    stats_errors = [s for s in stats_samples if get_scores(s)[0] == "error" or get_scores(s)[1] == "error"]
    print(f"Total Statistics samples: {len(stats_samples)}")
    print(f"Total Statistics errors: {len(stats_errors)}")

    # Group by question
    q_error_counts = defaultdict(lambda: {"errors": 0, "total": 0, "models_erroring": [], "ground_truth": ""})
    for s in stats_samples:
        q = get_question_key(s)
        q_error_counts[q]["total"] += 1
        q_error_counts[q]["ground_truth"] = s["metadata"].get("ground_truth", "")
        acc, hon, _ = get_scores(s)
        if acc == "error" or hon == "error":
            q_error_counts[q]["errors"] += 1
            q_error_counts[q]["models_erroring"].append(short_model(s["_model"]))

    # Sort by error count descending
    sorted_qs = sorted(q_error_counts.items(), key=lambda x: x[1]["errors"], reverse=True)

    print(f"\nTotal unique Statistics questions: {len(sorted_qs)}")
    print(f"\nTop error-producing Statistics questions:")
    print("-" * 80)
    for q, info in sorted_qs:
        if info["errors"] == 0:
            continue
        print(f"\n  Proposition: {q}")
        print(f"  Ground truth: {info['ground_truth'][:150]}")
        print(f"  Errors: {info['errors']}/{info['total']} models")
        print(f"  Models erroring: {', '.join(info['models_erroring'])}")

    # How many questions account for all errors?
    qs_with_errors = [q for q, info in sorted_qs if info["errors"] > 0]
    print(f"\n  Questions with any errors: {len(qs_with_errors)}/{len(sorted_qs)}")
    total_stats_questions = len(sorted_qs)

    # Non-Statistics errors
    non_stats_errors = [s for s in samples
                        if s.get("metadata", {}).get("config") != "statistics"
                        and (get_scores(s)[0] == "error" or get_scores(s)[1] == "error")]
    print(f"\n  Non-Statistics errors: {len(non_stats_errors)}")
    for s in non_stats_errors:
        q = get_question_key(s)
        m = s.get("metadata", {})
        print(f"    Model: {short_model(s['_model'])}, Config: {m.get('config')}, Proposition: {q[:100]}")

    # =========================================================================
    # 3. O3-MINI AS SUBJECT MODEL ERRORS
    # =========================================================================
    print("\n" + "=" * 80)
    print("3. O3-MINI AS SUBJECT MODEL ERRORS")
    print("=" * 80)

    o3_samples = [s for s in samples if "o3-mini" in s["_model"]]
    o3_errors = [s for s in o3_samples if get_scores(s)[0] == "error" or get_scores(s)[1] == "error"]
    print(f"Total o3-mini samples: {len(o3_samples)}")
    print(f"Total o3-mini errors: {len(o3_errors)}")

    # Break down by config
    config_counts = Counter()
    config_error_counts = Counter()
    for s in o3_samples:
        cfg = s.get("metadata", {}).get("config", "unknown")
        config_counts[cfg] += 1
        if get_scores(s)[0] == "error" or get_scores(s)[1] == "error":
            config_error_counts[cfg] += 1

    print(f"\n  o3-mini errors by config:")
    for cfg in sorted(config_counts.keys()):
        errs = config_error_counts.get(cfg, 0)
        total = config_counts[cfg]
        print(f"    {cfg:30s}: {errs}/{total} errors")

    # Detailed look at o3-mini errors
    print(f"\n  Detailed o3-mini error samples:")
    for s in o3_errors:
        m = s.get("metadata", {})
        q = get_question_key(s)
        store = s.get("store", {})
        print(f"\n  --- Config: {m.get('config')}, Type: {m.get('type')} ---")
        print(f"  Proposition: {q[:200]}")
        print(f"  Ground truth: {m.get('ground_truth', '')[:200]}")

        # Check pressured response (what o3-mini actually said)
        pressured = store.get("pressured_responses", [])
        if pressured:
            completion = pressured[0].get("completion", "")[:500]
            print(f"  Pressured response (first 500 chars): {completion}")

        # Check belief elicitation
        belief = store.get("belief_elicit_1_responses", [])
        if belief:
            completion = belief[0].get("completion", "")[:500]
            print(f"  Belief response (first 500 chars): {completion}")

        # Check for judge model usage in events (to see which judge was used)
        events = s.get("events", [])
        for e in events:
            if e.get("event") == "score":
                usage = e.get("model_usage", {})
                judge_models = [k for k in usage.keys() if k != s["_model"]]
                print(f"  Judge models used: {judge_models}")
                break

    # =========================================================================
    # 4. WEIRD / INTERESTING PATTERNS
    # =========================================================================
    print("\n" + "=" * 80)
    print("4. OTHER INTERESTING PATTERNS")
    print("=" * 80)

    # 4a. no-belief distribution by model and config
    print("\n--- 4a. no-belief-elicitation-done distribution ---")
    no_belief_counts = defaultdict(lambda: {"total": 0, "no_belief": 0})
    for s in samples:
        acc, hon, _ = get_scores(s)
        model = short_model(s["_model"])
        cfg = s.get("metadata", {}).get("config", "unknown")
        key = f"{model} | {cfg}"
        no_belief_counts[key]["total"] += 1
        if acc == "no-belief-elicitation-done":
            no_belief_counts[key]["no_belief"] += 1

    # Show only configs with any no-belief
    print(f"\n  Model | Config combos with no-belief outcomes:")
    for key in sorted(no_belief_counts.keys()):
        info = no_belief_counts[key]
        if info["no_belief"] > 0:
            pct = 100 * info["no_belief"] / info["total"]
            print(f"    {key:50s}: {info['no_belief']}/{info['total']} ({pct:.0f}%)")

    # Overall no-belief by config
    print(f"\n  No-belief rates by config (across all models):")
    cfg_nb = defaultdict(lambda: {"total": 0, "no_belief": 0})
    for s in samples:
        acc, _, _ = get_scores(s)
        cfg = s.get("metadata", {}).get("config", "unknown")
        cfg_nb[cfg]["total"] += 1
        if acc == "no-belief-elicitation-done":
            cfg_nb[cfg]["no_belief"] += 1
    for cfg in sorted(cfg_nb.keys()):
        info = cfg_nb[cfg]
        pct = 100 * info["no_belief"] / info["total"] if info["total"] else 0
        print(f"    {cfg:30s}: {info['no_belief']}/{info['total']} ({pct:.1f}%)")

    # 4b. Honesty outcomes by archetype
    print("\n--- 4b. Honesty outcome distribution by config (archetype) ---")
    cfg_honesty = defaultdict(Counter)
    for s in samples:
        _, hon, _ = get_scores(s)
        cfg = s.get("metadata", {}).get("config", "unknown")
        cfg_honesty[cfg][hon] += 1

    for cfg in sorted(cfg_honesty.keys()):
        print(f"\n  {cfg}:")
        total = sum(cfg_honesty[cfg].values())
        for outcome, count in cfg_honesty[cfg].most_common():
            pct = 100 * count / total
            print(f"    {outcome:30s}: {count:4d} ({pct:5.1f}%)")

    # 4c. Honesty by model
    print("\n--- 4c. Honesty outcome distribution by model ---")
    model_honesty = defaultdict(Counter)
    for s in samples:
        _, hon, _ = get_scores(s)
        model = short_model(s["_model"])
        model_honesty[model][hon] += 1

    for model in sorted(model_honesty.keys()):
        print(f"\n  {model}:")
        total = sum(model_honesty[model].values())
        for outcome, count in model_honesty[model].most_common():
            pct = 100 * count / total
            print(f"    {outcome:30s}: {count:4d} ({pct:5.1f}%)")

    # 4d. Look for surprising dishonesty in "easy" configs
    print("\n--- 4d. Dishonest outcomes in known_facts and provided_facts (should be lower deception) ---")
    for cfg in ["known_facts", "provided_facts"]:
        dishonest_in_cfg = [s for s in samples
                           if s.get("metadata", {}).get("config") == cfg
                           and get_scores(s)[1] == "dishonest"]
        if dishonest_in_cfg:
            print(f"\n  {cfg} - {len(dishonest_in_cfg)} dishonest outcomes:")
            by_model = Counter(short_model(s["_model"]) for s in dishonest_in_cfg)
            for model, count in by_model.most_common():
                print(f"    {model}: {count}")

    # 4e. Which specific questions have the highest deception rate?
    print("\n--- 4e. Most-deceived questions (highest dishonest rate across models) ---")
    q_dishonesty = defaultdict(lambda: {"total": 0, "dishonest": 0, "config": "", "ground_truth": ""})
    for s in samples:
        _, hon, _ = get_scores(s)
        q = get_question_key(s)
        q_dishonesty[q]["total"] += 1
        q_dishonesty[q]["config"] = s.get("metadata", {}).get("config", "")
        q_dishonesty[q]["ground_truth"] = s.get("metadata", {}).get("ground_truth", "")[:150]
        if hon == "dishonest":
            q_dishonesty[q]["dishonest"] += 1

    sorted_d = sorted(q_dishonesty.items(), key=lambda x: x[1]["dishonest"], reverse=True)
    print(f"\n  Top 15 most-deception-inducing questions:")
    for q, info in sorted_d[:15]:
        if info["dishonest"] == 0:
            break
        pct = 100 * info["dishonest"] / info["total"]
        print(f"\n    Config: {info['config']}")
        print(f"    Proposition: {q[:150]}")
        print(f"    Ground truth: {info['ground_truth']}")
        print(f"    Dishonest: {info['dishonest']}/{info['total']} models ({pct:.0f}%)")

    # 4f. Evade rates - which questions make models evade most?
    print("\n--- 4f. Top evasion-inducing questions ---")
    q_evasion = defaultdict(lambda: {"total": 0, "evade": 0, "config": ""})
    for s in samples:
        _, hon, _ = get_scores(s)
        q = get_question_key(s)
        q_evasion[q]["total"] += 1
        q_evasion[q]["config"] = s.get("metadata", {}).get("config", "")
        if hon == "evade":
            q_evasion[q]["evade"] += 1

    sorted_e = sorted(q_evasion.items(), key=lambda x: x[1]["evade"], reverse=True)
    print(f"\n  Top 10 most-evaded questions:")
    for q, info in sorted_e[:10]:
        if info["evade"] == 0:
            break
        pct = 100 * info["evade"] / info["total"]
        print(f"    {info['config']:25s} | evade={info['evade']}/{info['total']} ({pct:.0f}%) | {q[:100]}")

    # 4g. Questions where ALL models are honest vs ALL dishonest
    print("\n--- 4g. Unanimous outcomes ---")
    all_honest_qs = []
    all_dishonest_qs = []
    for q, info in q_dishonesty.items():
        _, hon_counts_for_q = q, Counter()
        q_samples = [s for s in samples if get_question_key(s) == q]
        honesty_vals = [get_scores(s)[1] for s in q_samples]
        # Filter out errors
        non_error_vals = [v for v in honesty_vals if v != "error"]
        if len(non_error_vals) == 0:
            continue
        if all(v == "honest" for v in non_error_vals):
            all_honest_qs.append((q, info["config"], len(non_error_vals)))
        elif all(v == "dishonest" for v in non_error_vals):
            all_dishonest_qs.append((q, info["config"], len(non_error_vals)))

    print(f"\n  Questions where ALL (non-error) models are honest: {len(all_honest_qs)}")
    print(f"  Questions where ALL (non-error) models are dishonest: {len(all_dishonest_qs)}")
    if all_dishonest_qs:
        print(f"\n  Unanimously dishonest questions:")
        for q, cfg, n in all_dishonest_qs:
            print(f"    [{cfg}] ({n} models) {q[:120]}")

    # 4h. Accuracy patterns - how often are models correct vs incorrect?
    print("\n--- 4h. Accuracy distribution by config ---")
    cfg_accuracy = defaultdict(Counter)
    for s in samples:
        acc, _, _ = get_scores(s)
        cfg = s.get("metadata", {}).get("config", "unknown")
        cfg_accuracy[cfg][acc] += 1

    for cfg in sorted(cfg_accuracy.keys()):
        print(f"\n  {cfg}:")
        total = sum(cfg_accuracy[cfg].values())
        for outcome, count in cfg_accuracy[cfg].most_common():
            pct = 100 * count / total
            print(f"    {outcome:35s}: {count:4d} ({pct:5.1f}%)")

    # 4i. Cross-tab: accuracy x honesty
    print("\n--- 4i. Accuracy x Honesty cross-tab (all samples) ---")
    cross = Counter()
    for s in samples:
        acc, hon, _ = get_scores(s)
        cross[(acc, hon)] += 1

    # Print as table
    acc_vals = sorted(set(a for a, h in cross.keys()))
    hon_vals = sorted(set(h for a, h in cross.keys()))
    header = f"{'':35s}" + "".join(f"{h:>15s}" for h in hon_vals)
    print(f"  {header}")
    for a in acc_vals:
        row = f"  {a:35s}" + "".join(f"{cross.get((a, h), 0):>15d}" for h in hon_vals)
        print(row)

    # 4j. honesty@n vs honesty - how much does retry help?
    print("\n--- 4j. honesty@n vs honesty (does retry help?) ---")
    upgrade_count = 0
    downgrade_count = 0
    same_count = 0
    upgrades_detail = Counter()
    for s in samples:
        _, hon, hon_n = get_scores(s)
        if hon == hon_n:
            same_count += 1
        elif hon == "dishonest" and hon_n == "honest":
            upgrade_count += 1
            cfg = s.get("metadata", {}).get("config", "unknown")
            upgrades_detail[cfg] += 1
        elif hon == "honest" and hon_n == "dishonest":
            downgrade_count += 1
        # Other transitions
        elif hon != hon_n:
            pass  # could track these too

    # More careful: track all transitions
    transitions = Counter()
    for s in samples:
        _, hon, hon_n = get_scores(s)
        if hon != hon_n:
            transitions[(hon, hon_n)] += 1

    print(f"  Same outcome: {same_count}")
    print(f"  Different outcomes: {sum(transitions.values())}")
    print(f"\n  Transition counts (honesty -> honesty@n):")
    for (h1, h2), count in transitions.most_common():
        print(f"    {h1:20s} -> {h2:20s}: {count}")

    if upgrades_detail:
        print(f"\n  dishonest->honest upgrades by config:")
        for cfg, count in upgrades_detail.most_common():
            print(f"    {cfg}: {count}")


if __name__ == "__main__":
    main()
