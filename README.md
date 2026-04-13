# Mapping Deception

Code and data for the blog post [**Mapping Deception**](https://sdsimmons.com/assets/writing/mask-blog-post/mask_eval.html), a replication of the [MASK benchmark](https://arxiv.org/abs/2503.03750) for evaluating AI honesty.

## What's here

| Path | Description |
|---|---|
| `blog/` | Blog post source: sections, figures, and the build pipeline |
| `eval_logs/` | Encrypted (`.eval.enc`) eval logs from the replication runs |

## Build the blog post

The eval logs are encrypted to comply with the [MASK dataset access policy](https://huggingface.co/datasets/cais/MASK).
To build you need `age_private.key` (the private key) in the repo root. Open an issue with your email and I'll send it.

```bash
uv sync
make build                # decrypts eval_logs/ → eval_logs_dec/, scans, generates build/blog_post.html
make serve                # local preview at localhost:9437
```

## Explore the eval results

Explore the raw eval logs (requires `age_private.key`):

```bash
make decrypt              # (if not already done) decrypts to eval_logs_dec/
uv run inspect view eval_logs_dec/
```

Run the eval yourself against a model of your choice. See [usage instructions](https://ukgovernmentbeis.github.io/inspect_evals/evals/safeguards/mask/#usage).

## Contributions welcome

Suggested extensions:

- Add additional models
- Extend the analysis (see footnotes for some directions that I think would be interesting).
- Spot mistakes in the write-up

## Adding additional models: contributions encouraged!

The public key (`age.pub`) is in the repo.

```bash
make encrypt-log LOG=path/to/your.eval   # produces eval_logs/your.eval.enc
```

Then open a PR with the `.enc` file.

I will update the blog post when a good number of additional models have been added.

## Citation

```bibtex
@misc{simmons2025mappingdeception,
      title={Mapping Deception},
      author={Scott Simmons},
      year={2025},
      url={https://sdsimmons.com/assets/writing/mask-blog-post/mask_eval.html},
}
```
