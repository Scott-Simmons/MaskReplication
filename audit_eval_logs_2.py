"""
Deeper audit: follow-up on initial findings.
"""
import zipfile
import json
import os
from collections import defaultdict, Counter
from pathlib import Path

EVAL_DIR = Path("eval_logs")

def load_all_samples():
    all_samples = []
    eval_files = sorted(EVAL_DIR.glob("*.eval"))
    eval_files = [f for f in eval_files if not str(f).endswith(".eval.old")]
    for ef in eval_files:
        with zipfile.ZipFile(ef) as z:
            with z.open("header.json") as hf:
                header = json.load(hf)
            model = header.get("eval", {}).get("model", "unknown")
            for sf_name in [n for n in z.namelist() if n.startswith("samples/")]:
                with z.open(sf_name) as sf:
                    sample = json.load(sf)
                sample["_model"] = model
                all_samples.append(sample)
    return all_samples

def get_scores(s):
    v = s.get("scores", {}).get("accuracy_and_honesty", {}).get("value", {})
    return v.get("accuracy", ""), v.get("honesty", ""), v.get("honesty@n", "")

def short_model(m):
    return m.split("/")[-1] if "/" in m else m

def main():
    print("Loading...")
    samples = load_all_samples()
    print(f"Loaded {len(samples)} samples\n")

    # =========================================================================
    # A. Why o3-mini errors: empty belief responses
    # =========================================================================
    print("=" * 80)
    print("A. O3-MINI EMPTY BELIEF RESPONSES -> JUDGE FAILURE")
    print("=" * 80)

    o3_errors = [s for s in samples
                 if "o3-mini" in s["_model"]
                 and (get_scores(s)[0] == "error" or get_scores(s)[1] == "error")]

    # Check: how many o3-mini errors have empty belief responses?
    empty_belief = 0
    nonempty_belief = 0
    for s in o3_errors:
        belief = s.get("store", {}).get("belief_elicit_1_responses", [])
        if belief:
            comp = belief[0].get("completion", "")
            if comp.strip() == "":
                empty_belief += 1
            else:
                nonempty_belief += 1
                print(f"  Non-empty belief for error: {comp[:200]}")
        else:
            empty_belief += 1

    print(f"\n  o3-mini errors with empty belief: {empty_belief}")
    print(f"  o3-mini errors with non-empty belief: {nonempty_belief}")

    # Compare: how many non-error o3-mini samples have empty beliefs?
    o3_non_errors = [s for s in samples
                     if "o3-mini" in s["_model"]
                     and get_scores(s)[0] != "error" and get_scores(s)[1] != "error"]

    o3_ne_empty = 0
    o3_ne_nonempty = 0
    for s in o3_non_errors:
        belief = s.get("store", {}).get("belief_elicit_1_responses", [])
        if belief:
            comp = belief[0].get("completion", "")
            if comp.strip() == "":
                o3_ne_empty += 1
            else:
                o3_ne_nonempty += 1
        else:
            o3_ne_empty += 1

    print(f"\n  o3-mini non-errors with empty belief: {o3_ne_empty}")
    print(f"  o3-mini non-errors with non-empty belief: {o3_ne_nonempty}")

    # Also check empty beliefs across ALL models
    print(f"\n  Empty belief responses by model (all samples):")
    model_empty_belief = defaultdict(lambda: {"empty": 0, "nonempty": 0})
    for s in samples:
        cfg = s.get("metadata", {}).get("config", "")
        if cfg == "provided_facts":
            continue  # no belief elicitation done
        m = short_model(s["_model"])
        belief = s.get("store", {}).get("belief_elicit_1_responses", [])
        if belief:
            comp = belief[0].get("completion", "")
            if comp.strip() == "":
                model_empty_belief[m]["empty"] += 1
            else:
                model_empty_belief[m]["nonempty"] += 1
        else:
            model_empty_belief[m]["empty"] += 1

    for m in sorted(model_empty_belief.keys()):
        info = model_empty_belief[m]
        total = info["empty"] + info["nonempty"]
        pct = 100 * info["empty"] / total if total else 0
        print(f"    {m:35s}: {info['empty']:3d}/{total} empty ({pct:.1f}%)")

    # =========================================================================
    # B. O3-MINI PRESSURED RESPONSES: terse / structured differently?
    # =========================================================================
    print("\n" + "=" * 80)
    print("B. O3-MINI PRESSURED RESPONSE PATTERNS")
    print("=" * 80)

    o3_binary = [s for s in samples
                 if "o3-mini" in s["_model"]
                 and s.get("metadata", {}).get("type") == "binary"]

    pressured_lengths = []
    for s in o3_binary:
        pr = s.get("store", {}).get("pressured_responses", [])
        if pr:
            comp = pr[0].get("completion", "")
            pressured_lengths.append(len(comp))

    if pressured_lengths:
        pressured_lengths.sort()
        print(f"  o3-mini binary pressured response lengths:")
        print(f"    Min: {min(pressured_lengths)}, Max: {max(pressured_lengths)}")
        print(f"    Median: {pressured_lengths[len(pressured_lengths)//2]}")
        print(f"    Mean: {sum(pressured_lengths)/len(pressured_lengths):.0f}")
        print(f"    <50 chars: {sum(1 for l in pressured_lengths if l < 50)}")
        print(f"    <100 chars: {sum(1 for l in pressured_lengths if l < 100)}")

    # Compare with other models' pressured response lengths
    print(f"\n  Pressured response lengths by model (binary only):")
    model_pr_lengths = defaultdict(list)
    for s in samples:
        if s.get("metadata", {}).get("type") != "binary":
            continue
        m = short_model(s["_model"])
        pr = s.get("store", {}).get("pressured_responses", [])
        if pr:
            comp = pr[0].get("completion", "")
            model_pr_lengths[m].append(len(comp))

    for m in sorted(model_pr_lengths.keys()):
        lengths = sorted(model_pr_lengths[m])
        med = lengths[len(lengths)//2]
        mean = sum(lengths) / len(lengths)
        short = sum(1 for l in lengths if l < 50)
        print(f"    {m:35s}: median={med:5d}  mean={mean:7.0f}  <50chars={short:3d}/{len(lengths)}")

    # =========================================================================
    # C. DETROIT DEEP DIVE: Why does o3-mini numeric judge fail?
    # =========================================================================
    print("\n" + "=" * 80)
    print("C. DETROIT QUESTION: DEEP DIVE INTO JUDGE FAILURES")
    print("=" * 80)

    detroit_samples = [s for s in samples
                       if "detroit" in s.get("metadata", {}).get("proposition", "").lower()]

    for s in sorted(detroit_samples, key=lambda x: x["_model"]):
        acc, hon, _ = get_scores(s)
        m = short_model(s["_model"])
        is_error = acc == "error" or hon == "error"

        if not is_error:
            # Show what successful scoring looks like
            print(f"\n  [{m}] SUCCESS - accuracy={acc}, honesty={hon}")
            store = s.get("store", {})
            belief = store.get("belief_elicit_1_responses", [])
            if belief:
                print(f"    Belief response: {belief[0].get('completion', '')[:300]}")
            pressured = store.get("pressured_responses", [])
            if pressured:
                print(f"    Pressured response: {pressured[0].get('completion', '')[:300]}")
        else:
            print(f"\n  [{m}] ERROR")
            store = s.get("store", {})
            belief = store.get("belief_elicit_1_responses", [])
            if belief:
                comp = belief[0].get("completion", "")
                print(f"    Belief response ({len(comp)} chars): {comp[:300]}")
            else:
                print(f"    NO belief response in store!")
            pressured = store.get("pressured_responses", [])
            if pressured:
                comp = pressured[0].get("completion", "")
                print(f"    Pressured response ({len(comp)} chars): {comp[:300]}")
            else:
                print(f"    NO pressured response in store!")

            # Check score event for model usage
            events = s.get("events", [])
            for e in events:
                if e.get("event") == "score":
                    usage = e.get("model_usage", {})
                    print(f"    Score event model usage: {json.dumps(usage)[:500]}")

    # =========================================================================
    # D. NEGATIVE NUMBERS: Is the Detroit issue about negative percentages?
    # =========================================================================
    print("\n" + "=" * 80)
    print("D. STATISTICS QUESTIONS WITH NEGATIVE/RANGE GROUND TRUTHS")
    print("=" * 80)

    stats_samples = [s for s in samples if s.get("metadata", {}).get("config") == "statistics"]

    # Group by question
    q_groups = defaultdict(list)
    for s in stats_samples:
        q = s.get("metadata", {}).get("proposition", "")
        q_groups[q].append(s)

    # Check which ground truths contain negative numbers or ranges
    for q, samps in sorted(q_groups.items()):
        gt = samps[0].get("metadata", {}).get("ground_truth", "")
        errors = sum(1 for s in samps if get_scores(s)[0] == "error" or get_scores(s)[1] == "error")
        has_negative = "-" in gt and any(c.isdigit() for c in gt.split("-")[0][-3:] if c) if "-" in gt else False
        has_range = " to " in gt.lower() or "between" in gt.lower()

        # Only show questions with interesting ground truths
        if has_negative or has_range or errors > 0:
            marker = ""
            if has_negative:
                marker += " [NEGATIVE]"
            if has_range:
                marker += " [RANGE]"
            if errors > 0:
                marker += f" [ERRORS={errors}]"
            print(f"  {marker}")
            print(f"    Q: {q[:120]}")
            print(f"    GT: {gt[:150]}")

    # =========================================================================
    # E. ACCURACY=CORRECT + HONESTY=LIE: accurate liars
    # =========================================================================
    print("\n" + "=" * 80)
    print("E. 'ACCURATE LIARS': accuracy=correct + honesty=lie")
    print("=" * 80)
    print("  These are models that KNOW the truth but LIE in the pressured scenario.")

    accurate_liars = [s for s in samples
                      if get_scores(s)[0] == "correct" and get_scores(s)[1] == "lie"]
    print(f"\n  Total accurate liars: {len(accurate_liars)}")

    # By config
    by_cfg = Counter(s.get("metadata", {}).get("config", "") for s in accurate_liars)
    print(f"  By config:")
    for cfg, count in by_cfg.most_common():
        total_in_cfg = sum(1 for s in samples if s.get("metadata", {}).get("config", "") == cfg)
        pct = 100 * count / total_in_cfg
        print(f"    {cfg:30s}: {count:4d}/{total_in_cfg} ({pct:.1f}%)")

    # By model
    by_model = Counter(short_model(s["_model"]) for s in accurate_liars)
    print(f"  By model:")
    for model, count in by_model.most_common():
        total_in_model = sum(1 for s in samples if short_model(s["_model"]) == model)
        pct = 100 * count / total_in_model
        print(f"    {model:35s}: {count:4d}/{total_in_model} ({pct:.1f}%)")

    # =========================================================================
    # F. ACCURACY=INCORRECT + HONESTY=HONEST: sincerely wrong
    # =========================================================================
    print("\n" + "=" * 80)
    print("F. 'SINCERELY WRONG': accuracy=incorrect + honesty=honest")
    print("=" * 80)
    print("  Models believe falsehoods and honestly relay them.")

    sincerely_wrong = [s for s in samples
                       if get_scores(s)[0] == "incorrect" and get_scores(s)[1] == "honest"]
    print(f"\n  Total sincerely wrong: {len(sincerely_wrong)}")

    by_cfg = Counter(s.get("metadata", {}).get("config", "") for s in sincerely_wrong)
    print(f"  By config:")
    for cfg, count in by_cfg.most_common():
        print(f"    {cfg:30s}: {count}")

    by_model = Counter(short_model(s["_model"]) for s in sincerely_wrong)
    print(f"  By model:")
    for model, count in by_model.most_common():
        print(f"    {model:35s}: {count}")

    # Show some examples
    print(f"\n  Examples:")
    for s in sincerely_wrong[:5]:
        m = s.get("metadata", {})
        print(f"    [{short_model(s['_model'])}] {m.get('config')}: {m.get('proposition', '')[:100]}")
        print(f"      GT: {m.get('ground_truth', '')[:100]}")
        belief = s.get("store", {}).get("belief_elicit_1_responses", [])
        if belief:
            print(f"      Belief: {belief[0].get('completion', '')[:150]}")

    # =========================================================================
    # G. ACCURACY=INCORRECT + HONESTY=LIE: wrong AND lying
    # =========================================================================
    print("\n" + "=" * 80)
    print("G. 'WRONG AND LYING': accuracy=incorrect + honesty=lie")
    print("=" * 80)
    print("  Models believe falsehoods but ALSO lie about what they believe.")

    wrong_liars = [s for s in samples
                   if get_scores(s)[0] == "incorrect" and get_scores(s)[1] == "lie"]
    print(f"\n  Total wrong liars: {len(wrong_liars)}")

    by_cfg = Counter(s.get("metadata", {}).get("config", "") for s in wrong_liars)
    print(f"  By config:")
    for cfg, count in by_cfg.most_common():
        print(f"    {cfg:30s}: {count}")

    by_model = Counter(short_model(s["_model"]) for s in wrong_liars)
    print(f"  By model:")
    for model, count in by_model.most_common():
        print(f"    {model:35s}: {count}")

    # =========================================================================
    # H. CLAUDE-HAIKU HONESTY: Strikingly different from other models
    # =========================================================================
    print("\n" + "=" * 80)
    print("H. CLAUDE-HAIKU vs OTHERS: honesty by config")
    print("=" * 80)

    for cfg in ["continuations", "disinformation", "known_facts", "doubling_down_known_facts", "provided_facts", "statistics"]:
        print(f"\n  {cfg}:")
        cfg_samples = [s for s in samples if s.get("metadata", {}).get("config") == cfg]
        model_hon = defaultdict(Counter)
        for s in cfg_samples:
            _, hon, _ = get_scores(s)
            m = short_model(s["_model"])
            model_hon[m][hon] += 1

        # Show lie rate for each model
        print(f"    {'Model':35s} {'lie%':>6s} {'honest%':>8s} {'evade%':>7s}")
        for m in sorted(model_hon.keys()):
            total = sum(model_hon[m].values())
            lie_pct = 100 * model_hon[m].get("lie", 0) / total
            honest_pct = 100 * model_hon[m].get("honest", 0) / total
            evade_pct = 100 * model_hon[m].get("evade", 0) / total
            print(f"    {m:35s} {lie_pct:5.1f}% {honest_pct:7.1f}% {evade_pct:6.1f}%")

    # =========================================================================
    # I. THE "EMPTY STRING" HONESTY VALUE
    # =========================================================================
    print("\n" + "=" * 80)
    print("I. SAMPLES WITH EMPTY HONESTY VALUES")
    print("=" * 80)

    empty_hon = [s for s in samples if get_scores(s)[1] == ""]
    print(f"  Samples with empty honesty string: {len(empty_hon)}")
    for s in empty_hon:
        m = s.get("metadata", {})
        print(f"    [{short_model(s['_model'])}] {m.get('config')}: {m.get('proposition', '')[:100]}")
        print(f"      All scores: {s.get('scores', {}).get('accuracy_and_honesty', {}).get('value', {})}")
        store = s.get("store", {})
        print(f"      Store keys: {list(store.keys())}")

    # =========================================================================
    # J. HONESTY@N == HONESTY for all samples (confirmed), but check N value
    # =========================================================================
    print("\n" + "=" * 80)
    print("J. BELIEF_REPEATS_N: checking how many belief elicitation rounds")
    print("=" * 80)

    # Check store for belief_elicit_2 and belief_elicit_3
    has_belief_2 = 0
    has_belief_3 = 0
    for s in samples[:500]:  # sample
        store = s.get("store", {})
        if "belief_elicit_2_responses" in store:
            has_belief_2 += 1
        if "belief_elicit_3_responses" in store:
            has_belief_3 += 1
    print(f"  Samples (of 500) with belief_elicit_2: {has_belief_2}")
    print(f"  Samples (of 500) with belief_elicit_3: {has_belief_3}")


if __name__ == "__main__":
    main()
