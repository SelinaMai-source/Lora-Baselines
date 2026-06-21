# Ours Method

The v2 branch uses `methods/ours/source/project_local/` as the curated ours core
code folder. This avoids duplicating the existing implementation while making
the reviewable code location explicit.

Core code entry points:

- `methods/ours/source/project_local/core/train.py`
- `methods/ours/source/project_local/core/evaluate.py`
- `methods/ours/source/project_local/core/methods/`
- `methods/ours/source/project_local/core/models/`
- `methods/ours/source/project_local/scripts/`

Large assets are not included here. See `docs/model_assets.md` for required
checkpoint/cache locations.
