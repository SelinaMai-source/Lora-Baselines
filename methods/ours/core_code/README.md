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
- `../source/project_local/core/models/seq2seq_lora_wrapper.py`: T5-style
  `AutoModelForSeq2SeqLM` backbone for seq2seq PEFT runs.
- `../source/project_local/core/ccfa_metrics.py`: CCF-A score matrix and
  postprocess JSON/CSV exports.
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

- CITB: ours-only code path is `smoke_ready` for T5 seq2seq PEFT using local
  `google__t5-small-lm-adapt`. The config keeps a clear TODO for a verified
  100-SuperNI-init checkpoint. Matrix exports include per-task per-time scores
  and CITB postprocess fields (`AR`, `FWT`, `BWT`, `Tinit`, `Tunseen`), with
  pre-training/unseen probes null until those passes are added.
- Standard T5-Large PEFT CL: ours-only code path is `smoke_ready` for
  `AutoModelForSeq2SeqLM` + PEFT `SEQ_2_SEQ_LM`, with local `t5-large` config
  templates and final average/per-task matrix/forgetting/BWT exports.
- Dialogue NLG / MultiWOZ CL: ours-only code path is `smoke_ready` for ARPER
  WOZ3 streams with seq2seq generation, corpus BLEU-4, and an auditable
  slot-missing SER scorer over dialogue-act values.

The original blocked launch manifest is `docs/ccfa_three_suite_manifest.csv`.
New ours-only seq2seq templates are under `docs/configs/ccfa_three_suite/` with
the suffix `_ours_seq2seq.yaml`.

## Dependencies And Excluded Assets

Runtime dependencies follow the project-local source snapshot and the selected
suite runner. Large model weights, Hugging Face caches, W&B runs/logs, generated
training outputs, Python caches, proxy configs, keys, and secrets are excluded
from Git. See `docs/model_assets.md` for required local checkpoint/cache paths.
