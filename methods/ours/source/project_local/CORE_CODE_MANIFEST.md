# Ours Core Code Manifest

This manifest identifies the files that reviewers should inspect for the v2
ours implementation. The code lives in this folder and is not copied into a
second tree.

## Training And Evaluation

- `core/train.py`: main training loop, W&B setup, run manifests, segment loop,
  branch/router hook calls, and per-segment evaluation calls.
- `core/evaluate.py`: per-segment generation/scoring, task-aware diagnostics,
  routing diagnostics, ROUGE/BLEU/slot-error summaries.
- `core/data.py`: processed continual stream dataclasses and loaders.
- `core/run_artifacts.py`: reproducibility artifacts and run manifest helpers.
- `core/utils.py`: config loading, seed setup, file output helpers.

## Ours Method Modules

- `core/methods/drift_detector.py`: anchor-set drift scoring and drift events.
- `core/methods/lora_bank.py`: branch creation, freezing, activation, and bank
  metadata.
- `core/methods/router.py`: prototype/learned routing utilities.
- `core/methods/overlap_loss.py`: activation/weight overlap penalties.
- `core/methods/hsic.py`: dependence regularization helper.
- `core/methods/ours_spectral_replay.py`: sparse spectral gate helper.

## Model And Metric Modules

- `core/models/base_model.py`: backbone adapter for supported local models.
- `core/models/lora_wrapper.py`: LoRA wrapper and adapter vector utilities.
- `core/metrics_utils.py`: text-generation and dialogue metric helpers.
- `core/normalize_answer.py`: answer normalization.
- `core/causal_lm_metrics.py`: token-level teacher-forced metrics.
- `core/formatting.py`: prompt formatting.
- `core/train_labels.py`: supervised label construction.

## Benchmark Conversion / Audit Scripts

- `scripts/convert_seqglue_to_stream.py`: local Seq-GLUE diagnostic converter.
- `scripts/convert_multiwoz_to_stream.py`: local MultiWOZ diagnostic converter.
- `scripts/convert_trace_to_stream.py`: TRACE diagnostic converter.
- `scripts/preflight_official_prompt_baselines.py`: prompt-baseline preflight.
- `scripts/smoke_published_setting_pipeline.py`: smoke validation entry point.

## Existing Baseline Adapters Used For Comparison/Smoke Checks

These are not the ours mechanism, but they are kept with the source snapshot
because the unified training/evaluation package imports them in smoke tests and
historical configs:

- `baselines/basic_baselines/sequential_lora/method.py`
- `baselines/basic_baselines/replay_lora/method.py`
- `baselines/advanced_baselines/o_lora/method.py`
- `baselines/advanced_baselines/lb_cl/method.py`
- `baselines/advanced_baselines/progressive_prompts/method.py`
- `baselines/advanced_baselines/continual_t0/method.py`

## v2 Readiness

The code folder is present and reviewable. The CCF-A three-suite configs remain
blocked because official data streams, checkpoint paths, and metric exporters
still need alignment; see `docs/ccfa_three_suite_manifest.csv`.
