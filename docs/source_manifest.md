# Lora-Baselines Source Manifest

This repository is organized for selected LoRA continual learning methods and benchmarks. Root-level ordinary files are intentionally avoided; all documentation and helper scripts live under `docs/`.

## Repository Layout Policy

- Root directories: `methods/`, `benchmark/`, `docs/`.
- No git submodules are used, because `.gitmodules` would add a root-level ordinary file.
- Official code is vendored under each entry's `source/` directory with nested `.git` directories removed.
- Experiment settings must follow the published paper or official code. Do not infer missing hyperparameters.
- Do not commit proxy configs, tokens, model weights, gated datasets, or local machine paths.

## Download Attempt Summary

Official GitHub and Hugging Face sources were retried on 2026-06-22 through a local Clash/mihomo proxy using `HTTP_PROXY`/`HTTPS_PROXY` environment variables only. No global git config was changed.

No non-official mirror or replacement implementation was used. GitHub codeload archives are treated as official GitHub delivery for the resolved upstream commit, not as mirrors.

The environment has limited free disk space, so large datasets/checkpoints and repositories that could not be fetched reliably were not forced. CT0-11B model weights were intentionally not downloaded; only small metadata/config files were saved.

See `docs/vendor_commits.tsv` for the exact vendored commit table and `docs/vendor_download_attempts.tsv` for low-level attempt logs.

## Methods

### Sequential LoRA

- Paper / source context: baseline in "Orthogonal Subspace Learning for Language Model Continual Learning".
- Paper URL: https://aclanthology.org/2023.findings-emnlp.715/
- Official code URL: https://github.com/cmnfriend/O-LoRA
- Commit / tag / release: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8` via O-LoRA official source.
- Original experiment configuration location: O-LoRA official repository scripts, especially `scripts/order_*.sh`, plus the paper baseline definition for SeqLoRA.
- Data / model / dependency requirements: T5-large or LLaMA2 setup as required by O-LoRA; benchmark data from the O-LoRA repository or referenced datasets.
- Downloaded: no separate source; use `methods/o_lora/source`.
- Not downloaded reason: no separate official Sequential LoRA repository was verified; it is documented as an O-LoRA paper baseline.

### Replay LoRA

- Paper / source context: replay baseline in "Orthogonal Subspace Learning for Language Model Continual Learning".
- Paper URL: https://aclanthology.org/2023.findings-emnlp.715/
- Official code URL: https://github.com/cmnfriend/O-LoRA
- Commit / tag / release: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8` via O-LoRA official source.
- Original experiment configuration location: O-LoRA official repository scripts and baseline sections; verify whether the official code implements replay with LoRA adapters or full-model replay before running.
- Data / model / dependency requirements: same as O-LoRA baseline environment.
- Downloaded: no separate source; use `methods/o_lora/source`.
- Not downloaded reason: separate official Replay LoRA source not verified.

### O-LoRA

- Paper title: Orthogonal Subspace Learning for Language Model Continual Learning.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.715/
- Official code URL: https://github.com/cmnfriend/O-LoRA
- Commit / tag / release: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Source location: `methods/o_lora/source`.
- Original experiment configuration location: `scripts/order_*.sh` in the official repository.
- Data / model / dependency requirements: pretrained T5-large or LLaMA2 base model, official scripts, and task data referenced by the repository.
- Downloaded: yes, official GitHub source through proxy. Nested `.git` removed.
- Mirror / alternative source: none.

### LB-CL

- Paper title: Learn more, but bother less: parameter efficient continual learning.
- Paper URL: https://openreview.net/forum?id=ZxtaNh5UYB and https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf
- Official code URL: not found in the paper, OpenReview page, or NeurIPS listing.
- Commit / tag / release: not available.
- Original experiment configuration location: not available.
- Data / model / dependency requirements: not available without official source.
- Downloaded: no.
- Not downloaded reason: no public official code source was verified. Do not substitute non-official implementations without project-owner approval.

### Progressive Prompts

- Paper title: Progressive Prompts: Continual Learning for Language Models.
- Paper URL: https://openreview.net/forum?id=UJTgQBc91_
- Official code URL: https://github.com/arazd/ProgressivePrompts
- Commit / tag / release: `01572d6a73c0576b070ceee00dbe4f5bc278423f`.
- Source location: `methods/progressive_prompts/source`.
- Original experiment configuration location: official repository `T5_codebase/` and `BERT_codebase/`, especially training scripts such as `train_t5_cl.py` and `train_cl2.py`.
- Data / model / dependency requirements: datasets folder plus Hugging Face datasets and datasets linked from the paper; standard PyTorch and Transformers setup.
- Downloaded: yes, official GitHub source through proxy. Nested `.git` removed.
- Mirror / alternative source: none.

### Continual-T0

- Paper title: Fine-tuned Language Models are Continual Learners.
- Paper URL: https://arxiv.org/abs/2205.12393
- Official code URL: https://github.com/ThomasScialom/T0_continual_learning
- Official model URL: https://huggingface.co/ThomasNLG/CT0-11B
- Commit / tag / release: code `4841ca267b2447d1b58d677a992b6808d9eaacf2`; HF model metadata commit `0bcf0791efba90ff3e47f48fc7377e644339fb7a`.
- Source location: `methods/continual_t0/source`; small HF metadata in `methods/continual_t0/hf_metadata`.
- Original experiment configuration location: official repository README points to a Colab notebook for dataset creation, rehearsal formatting, and evaluation; training hyperparameters are in the paper.
- Data / model / dependency requirements: Google Drive material linked by the official README, CT0/T0 checkpoints, and raw datasets; some raw datasets may have broken links.
- Downloaded: official code and small HF metadata/config files only.
- Not downloaded reason: CT0-11B weights are large and should be fetched separately only when storage/permission allow.
- Mirror / alternative source: none.

### LFPT5

- Paper title: LFPT5: A Unified Framework for Lifelong Few-shot Language Learning Based on Prompt Tuning of T5.
- Paper URL: https://openreview.net/forum?id=HCRVf71PMF
- Official code URL: https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning
- Commit / tag / release: `cf7d17ce7de6a707d929d0542b3d5e639569855f`.
- Source location: `methods/lfpt5/source`.
- Original experiment configuration location: official repository scripts and configuration files; project page documents LM-adapted T5 conversion.
- Data / model / dependency requirements: LM-adapted T5 checkpoint `t5.1.1.lm100k`, conversion to PyTorch checkpoint, task datasets, PyTorch.
- Downloaded: yes, official GitHub source through proxy/archive. Nested `.git` removed.
- Not downloaded reason: large model checkpoint is not included.
- Mirror / alternative source: none.

### Ours

- Paper title: source required from project owner.
- Paper URL: source required from project owner.
- Official code URL: source required from project owner.
- Commit / tag / release: not available.
- Original experiment configuration location: source required from project owner.
- Data / model / dependency requirements: source required from project owner.
- Downloaded: no.
- Not downloaded reason: no published paper, official experiment code, or project-owner-approved source was provided in this repository. Placeholder files under `methods/ours/` must not be used as strict experiment settings.

## Benchmarks

### InstrDialog

- Paper title: CITB: A Benchmark for Continual Instruction Tuning.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.633/
- Official code URL: https://github.com/hyintell/CITB
- Commit / tag / release: official HEAD resolved as `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Original experiment configuration location: official repository `data/` and `scripts/data_scripts/`; InstrDialog stream consists of 19 dialogue-related tasks.
- Data / model / dependency requirements: Super-NaturalInstructions derived task data provided in CITB `data/`.
- Downloaded: no.
- Not downloaded reason: official clone/archive attempts failed or stalled under the current network and disk constraints; a failed clone hit `No space left on device`. Do not substitute non-official CITB reproductions as strict sources.
- Mirror / alternative source: none used.

### InstrDialog++

- Paper title: CITB: A Benchmark for Continual Instruction Tuning.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.633/
- Official code URL: https://github.com/hyintell/CITB
- Commit / tag / release: official HEAD resolved as `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Original experiment configuration location: official repository `data/` and `scripts/data_scripts/`; InstrDialog++ stream consists of InstrDialog plus 19 additional tasks.
- Data / model / dependency requirements: Super-NaturalInstructions derived task data provided in CITB `data/`.
- Downloaded: no.
- Not downloaded reason: same CITB official source download constraints as InstrDialog.
- Mirror / alternative source: none used.

### TRACE

- Paper title: TRACE: A Comprehensive Benchmark for Continual Learning in Large Language Models.
- Paper URL: https://openreview.net/forum?id=3qa4YLkcEw
- Official code URL: https://github.com/BeyonderXX/TRACE
- Commit / tag / release: `462e39f616134f4f819efeb3baea8638c03c7db4`.
- Source location: `benchmark/trace/source`.
- Original experiment configuration location: official repository scripts such as `scripts/train_seq_cl.sh` and `scripts/infer_seq.sh`.
- Data / model / dependency requirements: official TRACE data, including ScienceQA, FOMC, MeetingBank, C-STANCE, 20Minuten, Py150/CodeXGLUE, and NumGLUE-derived tasks; supplementary material references Google Drive distribution and original dataset links.
- Downloaded: yes, official GitHub source through proxy/archive. Nested `.git` removed.
- Not downloaded reason: external large datasets/checkpoints are not bundled beyond the repository contents.
- Mirror / alternative source: none.

### MultiWOZ NLG

- Paper title: MultiWOZ - A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling.
- Paper URL: https://arxiv.org/abs/1810.00278
- Official dataset/code URL: https://github.com/budzianowski/multiwoz
- Evaluation code URL: https://github.com/Tomiinek/MultiWOZ_Evaluation
- Commit / tag / release: MultiWOZ official HEAD resolved as `fe0c8e65cfcd8462bd33c86e35f21addc84ca82b`; evaluation code `cd3f0ee3a936a2d1c8567f440a0b71b215d7f991`.
- Source location: evaluation code in `benchmark/multiwoz_nlg/source_evaluation`.
- Original experiment configuration location: MultiWOZ repository `data/` and baseline code; context-to-response evaluation in `Tomiinek/MultiWOZ_Evaluation`.
- Data / model / dependency requirements: MultiWOZ 2.0/2.1/2.2 data depending on published setting; NLG evaluation requires standardized Inform, Success, BLEU scripts.
- Downloaded: evaluation code yes; main MultiWOZ dataset/code no.
- Not downloaded reason: main MultiWOZ official archive attempt was interrupted before completion; do not force large dataset downloads in this low-space environment.
- Mirror / alternative source: none used.

### Seq-GLUE

- Paper / benchmark context: sequence of GLUE tasks used in continual learning papers; no single official Seq-GLUE-only repository was verified in this environment.
- Paper URL: GLUE benchmark paper https://openreview.net/forum?id=rJ4km2R5t7
- Official GLUE source URL: https://gluebenchmark.com/
- Candidate implementation sources: LFPT5 and Progressive Prompts official repositories include GLUE-style continual task usage; verify exact sequence against the target published paper before running.
- Commit / tag / release: not available.
- Original experiment configuration location: not verified as an official Seq-GLUE source.
- Data / model / dependency requirements: GLUE datasets, usually downloaded through Hugging Face datasets or official GLUE scripts depending on the paper.
- Downloaded: no standalone source.
- Not downloaded reason: no standalone official Seq-GLUE source was verified; do not infer sequence/order without a paper-specific source.
