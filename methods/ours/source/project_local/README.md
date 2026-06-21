# Ours Core Code Folder

This folder is the v2 reviewable implementation of our method. It is a
project-local source snapshot, not an external official repository.

## Core Mechanism

The method is built around online continual adaptation with LoRA branches:

- Online drift detection decides when the incoming stream should create or reuse
  a branch.
- A LoRA bank manages active, frozen, and newly spawned adapters.
- A router selects or blends branches without requiring paper-baseline task IDs
  at inference time.
- Orthogonality/overlap penalties reduce interference between branches.
- The training loop records branch, drift, routing, and evaluation artifacts so
  runs can be audited.

## Main Files

- `core/train.py`: unified training entry point.
- `core/evaluate.py`: unified evaluation entry point and per-segment metrics.
- `core/data.py`: continual stream loader for processed benchmark JSON.
- `core/methods/drift_detector.py`: online drift detection.
- `core/methods/lora_bank.py`: LoRA branch lifecycle and adapter state.
- `core/methods/router.py`: task-agnostic routing/prototype logic.
- `core/methods/overlap_loss.py`: branch overlap and anti-interference losses.
- `core/methods/ours_spectral_replay.py`: sparse spectral gate support.
- `core/models/base_model.py`: backbone construction.
- `core/models/lora_wrapper.py`: LoRA adapter wrapper.
- `core/metrics_utils.py`: ROUGE/BLEU/token and dialogue metric helpers.
- `core/wandb_tracker.py`: optional W&B logging wrapper.
- `scripts/convert_multiwoz_to_stream.py`: local MultiWOZ diagnostic converter.
- `scripts/convert_seqglue_to_stream.py`: local Seq-GLUE diagnostic converter.
- `scripts/convert_trace_to_stream.py`: TRACE diagnostic converter.

See `CORE_CODE_MANIFEST.md` for the curated file list and v2 status.

## CCF-A Suite Integration

The current v2 experiment materials live in `docs/`:

- `docs/ccfa_three_suite_execution_plan.md`
- `docs/ccfa_three_suite_manifest.csv`
- `docs/configs/ccfa_three_suite/*.blocked.yaml`
- `docs/scripts/prepare_citb_official_streams.py`
- `docs/scripts/audit_standard_peft_cl.py`
- `docs/scripts/audit_dialogue_nlg_sources.py`

The blocked configs point at this training entry point, but no v2 run is ready
until each suite has aligned data, backbone, metrics, and config.

## Assets Not Included

This folder intentionally excludes:

- model weights and Hugging Face caches;
- W&B runs, logs, and generated results;
- Python cache files;
- proxy configs, keys, and secrets;
- large temporary manifests or old full-matrix outputs.

For required T5-small/T5-large/checkpoint assets, see `docs/model_assets.md`.
