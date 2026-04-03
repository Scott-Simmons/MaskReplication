# The Basis of Deception

---

**TLDR:** I replicate the MASK benchmark's headline result: scaling improves accuracy but not honesty. I also show various ways that the single honesty score hides nuance. Two models can score identically while behaving completely differently. I show why reporting the full basis is useful, and argue for reporting raw counts, including errors, and error bars as the way forward for deception evaluation, and evaluations in general.

**Contents:** [1. Introduction](#introduction) | [2. Replication results](#replication-results) | [3. The deception basis](#the-deception-basis) | [4. Try it yourself](#try-it-yourself) | [Appendix](#appendix-paper-vs-replication-differences)

---

## 1. Introduction

---

Truth is often inconvenient. For starters, we cannot be sure that we actually know it. But even when deep down, we think we do know it, many of us lie to ourselves and others in public anyway, because it can conflict with what's socially comfortable. Saying true things in the face of that pressure requires intelligence and courage (subject to a certain amount of tact). It's also how things actually change. Galileo was put under house arrest for the rest of his life for saying the Earth goes around the Sun. He was right, everyone eventually agreed, and science moved forward.

Just like humans can hide their underlying beliefs when subject to social pressure, AI models hide their internal beliefs subject to pressure from a prompt too. And while scaling up AI models has made them dramatically more capable, [Ren et al., 2025](https://arxiv.org/abs/2503.03750) suggests that larger models are not more honest.

![From the [MASK paper](https://arxiv.org/abs/2503.03750): Larger models are more accurate but not more honest](figures/og_headline_result.png)

When I first saw this, it was quite a provocative result. For many reasons. How is lying defined? How is truth established? Many of these questions are answered in the paper. But two questions remained:

> 1. [Does this survive independent replication?](#replication-results)
> 2. [Are there any other measures that can help characterise deception?](#the-deception-basis)

---

## 2. Replication results

I wanted to verify the paper's main claim: larger models are more accurate but not more honest. I used the following models:

| Model | Provider | Samples | In paper? |
|---|---|---|---|
| Claude Haiku 4.5 | Anthropic | 1,000 | No |
| GPT-4o | OpenAI | 998 | Yes |
| GPT-4o-mini | OpenAI | 1,000 | Yes |
| o3-mini | OpenAI | 1,000 | Yes |
| Qwen 2.5 7B | Alibaba | 1,000 | Yes |
| DeepSeek-R1 | DeepSeek | 580 | Yes |
| DeepSeek-R1-0528 | DeepSeek | 924 | No |
| DeepSeek-V3.1 | DeepSeek | 1,000 | No |
| Llama 3.3 70B | Meta | 998 | Yes |

*The MASK public dataset contains 1,000 examples. Shortfalls are due to API failures during evaluation.*

I used <mark>a different model judge to save on cost (TODO: may remove this caveat if we rerun with the same judge, it is just expensive)</mark> and a slightly different set of 9 models. The paper tested 32 models, but some are now deprecated or no longer served at the same API endpoint. I chose a smaller set that covers a range of providers and scales, keeping costs manageable.

The headline result held. The pattern is clear in the replication: accuracy scales with compute, but honesty does not. See the [appendix](#appendix-paper-vs-replication-differences) for a model-by-model comparison with the original paper.

![Note: I used [Epoch AI](https://epoch.ai/data/notable-ai-models) to estimate the FLOP per model, as they were unavailable from the original paper.](figures/replication_headline_result.png)

---

## 3. The deception basis

The categories that a pressured statement, subject to some internally held belief, can fall into are:[^1]

$$\{\text{Honest},\ \text{Lie},\ \text{Evade},\ \text{No Belief},\ \text{Parse Error}\}$$

$$\{H,\ L,\ E,\ N,\ \varepsilon\}$$

Here are the empirical basis vectors for my MASK replication:

| Model | $n$ | $H$ | $L$ | $E$ | $N$ | $\varepsilon$ |
|---|---|---|---|---|---|---|
| Claude Haiku 4.5 | 1,000 | 620 | 81 | 215 | 82 | 2 |
| GPT-4o | 998 | 205 | 503 | 199 | 88 | 3 |
| GPT-4o-mini | 1,000 | 200 | 494 | 160 | 144 | 2 |
| o3-mini | 1,000 | 134 | 434 | 284 | 140 | 8 |
| Qwen 2.5 7B | 1,000 | 264 | 401 | 83 | 246 | 6 |
| DeepSeek-R1 | 580 | 75 | 314 | 101 | 89 | 1 |
| DeepSeek-R1-0528 | 924 | 142 | 506 | 172 | 103 | 1 |
| DeepSeek-V3.1 | 1,000 | 143 | 580 | 117 | 151 | 7 |
| Llama 3.3 70B | 998 | 257 | 526 | 96 | 114 | 5 |
| **Total** | **8,500** | **2040** | **3839** | **1427** | **1157** | **35** |

With this basis in mind, "honesty" as reported by the paper means:

$$\text{Honesty} = 1 - P(\text{Lie}) = 1 - \frac{L}{H + L + E + N}$$

However this projection compresses a lot of useful information.

### Hypothetical

TODO: Insert interp_dumb_and_diplomatic

```
  Unpressured Query     Pressured Query
        │                      │
        ▼                      ▼
   ┌─────────┐          ┌─────────┐
   │  Belief  │          │  Belief  │
   └────┬────┘          └────┬────┘
        │                      │
        ▼                      ▼
   ┌─────────┐     ┌────────────────────┐
   │ Response │     │ Truthful │ Lie │ ...│
   └─────────┘     └────────────────────┘
```

*TODO: Insert dumb_and_diplomat caption*

### Making this empirical

To make these thought experiments concrete, here is the data from the replication plotted in a 2D projection of the basis:

![Model behaviour space with iso-P(Lie) contours. Note how Qwen 2.5 7B and o3-mini sit on the same P(Lie) contour (within error bars), even though o3-mini evades 3x more (33% vs 11%) and lies more when it does engage (76% vs 60%). The honesty score compresses all of this because o3-mini's evasion pulls samples away from the lie bucket.](figures/two_d_space_projection.png)

Every projection of the deception basis produces a different metric. When the basis is reported, researchers can compute whatever measures they are interested in, or define new ones. Here are some useful ones:[^2]

| Metric | Formula | What it captures | In MASK? |
|---|---|---|---|
| Honesty score | $\frac{H}{H + L + E + N}$ | Strictest: honest out of all responses | Yes (headline) |
| Normalised honesty | $\frac{H}{H + L + E}$ | Excludes no-belief from denominator | Yes (appendix) |
| Conditional honesty | $\frac{H}{H + L}$ | When it takes a position, is it truthful? | No |
| Engagement rate | $\frac{H + L}{H + L + E + N}$ | How often does it commit to a position? | No |
| Evasion rate | $\frac{E}{H + L + E + N}$ | How often does it dodge? | No |
| Conditional lie rate | $\frac{L}{H + L}$ | When it engages, how often does it lie? | No |
| Deflection style | $\frac{E}{E + N}$ | Of non-answers: strategic dodge vs no belief? | No |

The same data can be projected in many other ways. Here are three more, each telling a different story. The middle panel ("Reliable vs Broken") includes $\varepsilon$ to show that when a basis vector represents a rare event, the proportion estimate is noisier and error bars inflate relative to the point estimates. This is exactly why reporting counts matters, especially for LLM evaluations, where silent errors (unparseable outputs, judge failures, dropped samples) are common. Making these visible in the basis is a step towards better evaluation science.

![Three more basis projections. Claude Haiku 4.5 is an outlier in the first panel (88% conditionally honest). Qwen 2.5 7B is an outlier in the third (25% deflection style, meaning when it does not answer, it is mostly because it lacks beliefs, not because it evades).](figures/more_2d_projections.png)

---

## 4. Try it yourself

If this is interesting to you, the eval logs and analysis code are available at [this repo](https://github.com/Scott-Simmons/MaskReplication). You can add more models by running the MASK eval from [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) and dropping the `.eval` files into the `eval_logs/` directory. Everything regenerates with `make blog-post`. I would particularly be interested in contributions from abliterated models and whatever the frontier looks like next month.

Here is the invocation I used:

```bash
# inspect_evals 0.6.1.dev4, inspect_ai 0.3.190.dev29, mask version 3-C
inspect eval inspect_evals/mask \
    --model <YOUR_MODEL> \
    --log-dir ./eval_logs \
    -T binary_judge_model="openai/gpt-4o-mini"
```

---

## Appendix: Paper vs replication differences

Systematic differences between the paper and this replication are likely caused by:

1. **Different eval harness.** This replication uses [Inspect AI](https://inspect.ai), not the original codebase.
2. **Model API drift.** Model weights and serving infrastructure change over time. We will never know the exact checkpoint the paper used.
3. **<mark>TBD: Different eval judges.</mark>** This replication uses gpt-4o-mini as the judge. The original paper's judge may differ. I may re-run with a matching judge if I can confirm which one the paper used.

**Honesty (1 - P(Lie))**

| Model | Paper | Replication (95% CI) | Diff |
|---|---|---|---|
| GPT-4o | 21.8 | 20.5 ± 2.5 | <span style="color:red">-1.3</span> |
| GPT-4o-mini | 21.4 | 20.0 ± 2.5 | <span style="color:red">-1.4</span> |
| o3-mini | 19.6 | 13.4 ± 2.1 | <span style="color:red">-6.2</span> |
| Qwen 2.5 7B | 28.9 | 26.4 ± 2.7 | <span style="color:red">-2.5</span> |
| DeepSeek-R1 | 24.7 | 7.5 ± 2.1 | <span style="color:red">-17.2</span> |
| Llama 3.3 70B | 24.7 | 25.7 ± 2.7 | <span style="color:green">+1.0</span> |

**Accuracy**

| Model | Paper | Replication (95% CI) | Diff |
|---|---|---|---|
| GPT-4o | 78.6 | 58.7 ± 3.1 | <span style="color:red">-19.9</span> |
| GPT-4o-mini | 71.4 | 51.6 ± 3.1 | <span style="color:red">-19.8</span> |
| o3-mini | 63.3 | 42.6 ± 3.1 | <span style="color:red">-20.7</span> |
| Qwen 2.5 7B | 51.6 | 35.2 ± 3.0 | <span style="color:red">-16.4</span> |
| DeepSeek-R1 | 82.2 | 31.0 ± 3.8 | <span style="color:red">-51.2</span> |
| Llama 3.3 70B | 75.6 | 56.5 ± 3.1 | <span style="color:red">-19.1</span> |

---

[^1]: Including $\varepsilon$ (parse errors) in the basis is deliberate. Without it, $\{H, L, E, N\}$ is not an exhaustive partition of responses. A response that fails to parse does not land in any of those four buckets, so the counts would not sum to $n$ and every derived metric would have a hidden denominator problem. $\varepsilon$ closes the basis so that it spans the full space of outcomes.

[^2]: This is why even for a simple basis of $\{\text{TP}, \text{TN}, \text{FP}, \text{FN}\}$ in a traditional classifier context there is a [cornucopia of metrics](https://en.wikipedia.org/wiki/Template:Diagnostic_testing_diagram) that we project that basis onto. I would like to see the eval community refining metrics that characterise deception, in a similar way to how the ML community looks at ROC curves, PR curves, and Matthew's correlation coefficient instead of accuracy to assess a model's validity.
