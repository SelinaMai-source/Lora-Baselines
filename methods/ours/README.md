# Ours Method

The v2 branch exposes `methods/ours/core_code/` as the review entry point for
our method. The actual curated implementation remains in
`methods/ours/source/project_local/`, so reviewers get a clear index without a
duplicated project tree.

Core code entry points:

- `methods/ours/core_code/README.md`
- `methods/ours/source/project_local/core/train.py`
- `methods/ours/source/project_local/core/evaluate.py`
- `methods/ours/source/project_local/core/methods/`
- `methods/ours/source/project_local/core/models/`
- `methods/ours/source/project_local/scripts/`

Large assets are not included here. See `docs/model_assets.md` for required
checkpoint/cache locations.
