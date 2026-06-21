# Ours Core Code Index

This directory is the v2 review entry point for our method. The implementation
is kept in the existing curated source snapshot at
`methods/ours/source/project_local/` to avoid duplicating a large project tree.

## Core Implementation Files

- `../source/project_local/core/train.py`: training entry point, segment loop,
  branch/router hooks, run artifacts, and evaluation calls.
- `../source/project_local/core/evaluate.py`: generation, per-segment scoring,
  routing diagnostics, and text/dialogue metric summaries.
- `../source/project_local/core/data.py`: continual stream dataclasses and
  processed JSON loaders.
- `../source/project_local/core/methods/drift_detector.py`: online drift
  scoring over anchor/reference examples.
- `../source/project_local/core/methods/lora_bank.py`: LoRA branch creation,
  activation, freezing, and branch metadata.
- `../source/project_local/core/methods/router.py`: branch routing and
  prototype logic without relying on paper-baseline task IDs at inference.
- `../source/project_local/core/methods/overlap_loss.py`: overlap and
  orthogonality-style penalties for reducing branch interference.
- `../source/project_local/core/methods/hsic.py`: dependence regularization
  helper.
- `../source/project_local/core/methods/ours_spectral_replay.py`: sparse
  spectral gate helper.
- `../source/project_local/core/models/base_model.py`: backbone construction.
- `../source/project_local/core/models/lora_wrapper.py`: adapter wrapper and
  LoRA vector utilities.
- `../source/project_local/core/metrics_utils.py`: ROUGE/BLEU/dialogue metric
  helpers.
- `../source/project_local/core/wandb_tracker.py`: optional W&B wrapper. It does
  not contain keys; credentials must remain in the user environment.

## Mechanism Summary

The method maintains a bank of LoRA branches for online continual adaptation.
Incoming data is monitored for drift, the training loop either reuses an
existing branch or creates a new one, and the router chooses/blends branches
without requiring explicit task IDs at inference. Overlap and orthogonality-style
losses are used to reduce interference between branches while preserving prior
branches.

## Three-Suite Integration

- CITB: blocked until official InstrDialog/InstrDialog++ streams,
  T5-small LM-adapted plus 100-SuperNI-init loading, and ROUGE-L matrix metrics
  are aligned.
- Standard T5-Large PEFT CL: blocked until O-LoRA/LFPT5/Progressive-Prompts task
  orders and sample settings are converted and verified.
- Dialogue NLG / MultiWOZ CL: blocked until ARPER MultiWOZ-2.0 streams and
  BLEU-4/SER scoring are aligned; ToDCL remains an extension/backup route.

The blocked launch manifest is `docs/ccfa_three_suite_manifest.csv`; configs are
under `docs/configs/ccfa_three_suite/`.

## Dependencies And Excluded Assets

Runtime dependencies follow the project-local source snapshot and the selected
suite runner. Large model weights, Hugging Face caches, W&B runs/logs, generated
training outputs, Python caches, proxy configs, keys, and secrets are excluded
from Git. See `docs/model_assets.md` for required local checkpoint/cache paths.
