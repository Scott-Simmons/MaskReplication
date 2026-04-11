# Mapping Deception

Code and data for the blog post [**Mapping Deception**](https://sdsimmons.com/assets/writing/mask-blog-post/mask_eval.html) — a replication of the [MASK benchmark](https://arxiv.org/abs/2503.03750) for evaluating AI honesty.

## What's here

| Path | Description |
|---|---|
| `blog/` | Blog post source — sections, figures, and the build pipeline |
| `eval_logs/` | Raw `.eval` log files from the replication runs |

## Build the blog post

```bash
uv sync
make build                # scans eval_logs/, generates build/blog_post.html
make serve                # local preview at localhost:9437
```

## If you are interested

Explore the raw eval logs:

```bash
uv run inspect view eval_logs/
```

Run the eval yourself against a model of your choice:

```bash
uv run inspect eval inspect_evals/mask --model openai/gpt-4o
```

More details on running the eval [here](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/#usage).

## Contributions welcome

Found an error, have better data, or want to extend the analysis? Please open an issue or PR. Suggested directions:

- Replicate with additional models
- Extend the honesty dimension analysis
- Spot mistakes in the write-up

The eval is also on [Inspect Evals](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/).

## Citation

```bibtex
@misc{simmons2025mappingdeception,
      title={Mapping Deception},
      author={Scott Simmons},
      year={2025},
      url={https://sdsimmons.com/assets/writing/mask-blog-post/mask_eval.html},
}
```
