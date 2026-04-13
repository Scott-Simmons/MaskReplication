# Mapping Deception

Code and data for the blog post [**Mapping Deception**](https://sdsimmons.com/assets/writing/mask-blog-post/mask_eval.html) — a replication of the [MASK benchmark](https://arxiv.org/abs/2503.03750) for evaluating AI honesty.

## What's here

| Path | Description |
|---|---|
| `blog/` | Blog post source — sections, figures, and the build pipeline |
| `eval_logs/` | Encrypted (`.eval.enc`) eval logs from the replication runs |

## Build the blog post

The eval logs are encrypted to comply with the [MASK dataset access policy](https://github.com/LRNLab/MASK).
To build you need `age.key` (the private key) in the repo root — contact the repo owner to request it.

```bash
uv sync
make build                # decrypts eval_logs/, scans, generates build/blog_post.html
make serve                # local preview at localhost:9437
```

## If you are interested

Explore the raw eval logs (requires `age.key`):

```bash
make decrypt              # decrypts to eval_logs_dec/
uv run inspect view eval_logs_dec/
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

**Adding your own eval logs:** The public key (`age.pub`) is in the repo — you can encrypt your own logs without needing anything from the repo owner:

```bash
make encrypt-log LOG=path/to/your.eval   # produces eval_logs/your.eval.enc
```

Then open a PR with the `.enc` file.

## Citation

```bibtex
@misc{simmons2025mappingdeception,
      title={Mapping Deception},
      author={Scott Simmons},
      year={2025},
      url={https://sdsimmons.com/assets/writing/mask-blog-post/mask_eval.html},
}
```
