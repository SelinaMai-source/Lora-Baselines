# Lora-Baselines Source Manifest

This repository is organized for selected LoRA continual learning methods and benchmarks. Root-level ordinary files are intentionally avoided; all documentation and helper scripts live under `docs/`.

## Repository Layout Policy

- Root directories: `methods/`, `benchmark/`, `docs/`.
- No git submodules are used, because `.gitmodules` would add a root-level ordinary file.
- Vendored official sources live under each entry's `source/` directory with nested `.git` directories removed.
- Large model weights, gated assets, generated experiment outputs, caches, logs, archives, proxy configs, and secrets are not vendored.
- Git LFS is used for complete benchmark files that exceed GitHub's 100MB per-file limit; this requires the hidden root `.gitattributes` file.

## Network, Proxy, And LFS Verification

- Clash/mihomo config directory inspected outside the repo: `/root/autodl-tmp/Lora-code/configs/clash`.
- Local proxy available/used for source verification: `HTTP_PROXY=http://127.0.0.1:7890`, `HTTPS_PROXY=http://127.0.0.1:7890`.
- No proxy config, subscription, proxy node, token, or secret is committed.
- No global git config was modified. `git-lfs` was initialized with `git-lfs install --local` for this repository only.
- LFS tracking file: root `.gitattributes`.
- LFS-tracked data over 100MB:
  - `benchmark/multiwoz_nlg/source/multiwoz/data/MultiWOZ_2.1/data.json`
  - `benchmark/multiwoz_nlg/source/multiwoz/data/MultiWOZ_2.2/data.json`

## Methods

### Sequential LoRA

- Official code status: closest reproducible code; no standalone official Sequential LoRA repository verified.
- Downloaded: yes, as project-local baseline plus official O-LoRA reference.
- Source path: `methods/sequential_lora/source/project_local`; closest reproducible external base at `methods/o_lora/source`.
- Official URL: no separate official Sequential LoRA-only source verified; O-LoRA baseline context is https://github.com/cmnfriend/O-LoRA.
- Paper URL: not applicable as an independent method paper in this package; Sequential LoRA is a baseline protocol cited by O-LoRA-style continual-learning papers.
- Base code used: O-LoRA official commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree.
- Proxy used: yes for official reference/public-source verification.
- Mirror used: no.
- LFS usage: no.
- Required paper adaptation: train LoRA adapters sequentially over the task stream and keep replay, orthogonal projection, LB-CL injection, MIGU masks, routing, prompt modules, and other extra continual-learning mechanisms disabled.
- Notes: see `methods/sequential_lora/REPRODUCIBILITY.md`; project-local baseline implementation/configs are included for the complete v1 package and must not be represented as an external official release.

### Replay LoRA

- Official code status: closest reproducible code; no standalone official Replay LoRA repository verified.
- Downloaded: yes, as project-local replay baseline, official O-LoRA reference, and ACL software source for the LoRA Replay baseline in "Unlocking Continual Learning Abilities in Language Models".
- Source paths:
  - Project-local replay baseline: `methods/replay_lora/source/project_local`.
  - ACL software package: `methods/replay_lora/source/acl_software_unlocking_cl`.
  - Closest external base: `methods/o_lora/source`.
- Paper route A: "Combining replay and LoRA for continual learning in natural language understanding"; paper/code URL needs manual verification beyond bibliographic pages, and no author official code was verified.
- Paper route B: "Unlocking Continual Learning Abilities in Language Models", https://aclanthology.org/2024.findings-emnlp.379/; PDF https://aclanthology.org/2024.findings-emnlp.379.pdf.
- ACL Software ZIP URL: https://aclanthology.org/attachments/2024.findings-emnlp.379.software.zip.
- Official URL: no separate official Replay LoRA-only source verified; O-LoRA baseline context is https://github.com/cmnfriend/O-LoRA.
- Base code used: O-LoRA official commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`; the ACL paper states its T5 continual-learning experiments are adapted from O-LoRA.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree.
- Proxy used: yes for official reference/public-source verification.
- Mirror used: no.
- LFS usage: no.
- Required paper adaptation: add a past-task replay buffer to sequential LoRA/O-LoRA training; mix current-task samples with replayed past-task samples according to the cited paper setting. The ACL paper describes LoRAReplay as mixing 2% past-task data; LoRA Replay + MIGU additionally applies the MIGU magnitude-based gradient mask and threshold settings.
- Notes: see `methods/replay_lora/REPRODUCIBILITY.md`; project-local replay implementation/configs and the ACL ZIP are included as reproducible sources and must not be represented as an external official release for the separate "Combining replay and LoRA" paper.

### O-LoRA

- Downloaded: yes.
- Source path: `methods/o_lora/source`.
- Official URL: https://github.com/cmnfriend/O-LoRA
- Commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.
- Notes: nested `.git` removed. Generated `logs_and_outputs` and Python cache files were not retained in the vendored copy because they are experiment outputs/caches rather than source code.

### LB-CL

- Official code status: no official verified.
- Downloaded: yes, as project-local scaffold/configs plus O-LoRA closest reproducible base.
- Source path: `methods/lb_cl/source/project_local`; closest reproducible external base at `methods/o_lora/source`.
- Official URL: no official code URL verified. Paper pages checked include OpenReview https://openreview.net/forum?id=ZxtaNh5UYB, NeurIPS https://neurips.cc/virtual/2024/poster/94599, and the proceedings PDF https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf.
- Paper URL: https://openreview.net/forum?id=ZxtaNh5UYB.
- Base code used: O-LoRA official commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree.
- Proxy used: yes for web/GitHub verification.
- Mirror used: no.
- LFS usage: no.
- Required paper adaptation: implement LB-CL's SVD-triplet sensitivity scoring, previous-task knowledge extraction/injection into new low-rank parameters, and orthogonal-subspace training on top of the O-LoRA-style baseline.
- Notes: see `methods/lb_cl/REPRODUCIBILITY.md`; do not claim strict official LB-CL paper code without later author-source or project-owner equivalence verification.

### Progressive Prompts

- Downloaded: yes.
- Source path: `methods/progressive_prompts/source`.
- Official URL: https://github.com/arazd/ProgressivePrompts
- Commit: `01572d6a73c0576b070ceee00dbe4f5bc278423f`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.

### Continual-T0

- Downloaded: yes.
- Source path: `methods/continual_t0/source`.
- Official URL: https://github.com/ThomasScialom/T0_continual_learning
- Commit: `4841ca267b2447d1b58d677a992b6808d9eaacf2`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.
- Hugging Face CT0-11B metadata: small metadata files are stored under `methods/continual_t0/hf_metadata`; large model weights were intentionally not downloaded because CT0-11B weights are large model artifacts and outside the source-vendoring scope.

### LFPT5

- Downloaded: yes.
- Source path: `methods/lfpt5/source`.
- Official URL: https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning
- Commit: `cf7d17ce7de6a707d929d0542b3d5e639569855f`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.
- Notes: full clone initially failed with `No space left on device` while checking out generated `transformers/build` files. The vendored source excludes that generated build tree.

### Ours

- Downloaded: yes, as project-owner local source snapshot.
- Source path: `methods/ours/source/project_local`.
- Official URL: project-owner local source `/root/autodl-tmp/Lora-code`, not an external published official repository.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`.
- Local dirty status: dirty at vendoring time; 143 status entries were present, including modified `core/train.py`, `core/evaluate.py`, `core/metrics_utils.py`, `core/wandb_tracker.py`, modified/new `configs/paper/published_setting/*`, and local generated/state/cache paths that were excluded.
- Proxy used: not applicable for the local source itself.
- Mirror used: no.
- LFS usage: no.
- Notes: vendored subset includes `core/`, relevant `baselines/`, `configs/paper/published_setting`, selected scripts, and the small Seq-GLUE processed stream. It intentionally excludes model weights, Hugging Face caches, results, logs, W&B runs, archives, conda/env folders, proxy configs, and generated outputs.

## Benchmarks

### InstrDialog

- Downloaded: yes, complete official CITB source/data.
- Source path: `benchmark/instrdialog/source`.
- Official URL: https://github.com/hyintell/CITB
- Commit: `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Local source path: `/root/autodl-tmp/CITB`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no; no individual `data/tasks` file exceeded 100MB.
- Notes: official `data/tasks` is now included under `benchmark/instrdialog/source/data/tasks`. Nested `.git` removed.

### InstrDialog++

- Downloaded: yes, via shared complete CITB source.
- Source path: uses `benchmark/instrdialog/source`.
- Official URL: https://github.com/hyintell/CITB
- Commit: `bf50533b5bced4c388691ecc75e26773da96b3fd` for the shared CITB source.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.
- Notes: InstrDialog++ reuses the same official CITB source as InstrDialog. No duplicate source tree is committed to avoid redundant benchmark files.

### TRACE

- Downloaded: yes.
- Source path: `benchmark/trace/source`.
- Official URL: https://github.com/BeyonderXX/TRACE
- Commit: `462e39f616134f4f819efeb3baea8638c03c7db4`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.

### MultiWOZ NLG Dataset

- Downloaded: yes, complete official MultiWOZ source/data with Git LFS for oversized JSON files.
- Source path: `benchmark/multiwoz_nlg/source/multiwoz`.
- Official URL: https://github.com/budzianowski/multiwoz
- Commit: `fe0c8e65cfcd8462bd33c86e35f21addc84ca82b`.
- Local source path: `/root/autodl-tmp/Lora-code/data/raw/multiwoz/multiwoz_repo`.
- Local source status: official clone at the target commit with untracked extracted data directories/files: `data/MultiWOZ_2.1/`, `data/MultiWOZ_2.2/data.json`, and `data/__MACOSX/`; `__MACOSX` was excluded as unzip metadata.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: yes for `data/MultiWOZ_2.1/data.json` and `data/MultiWOZ_2.2/data.json`, which exceed GitHub's 100MB per-file limit.
- Notes: complete official data directory is vendored, including unzipped `MultiWOZ_2.1/data.json` and `MultiWOZ_2.2/data.json` through Git LFS; nested `.git` removed.

### MultiWOZ Evaluation

- Downloaded: yes.
- Source path: `benchmark/multiwoz_nlg/source/evaluation`.
- Official URL: https://github.com/Tomiinek/MultiWOZ_Evaluation
- Commit: `cd3f0ee3a936a2d1c8567f440a0b71b215d7f991`.
- Proxy used: yes.
- Mirror used: no.
- LFS usage: no.

### Seq-GLUE

- Official code status: project-local benchmark stream; no standalone official Seq-GLUE-only repository verified.
- Downloaded: yes, as project-local benchmark stream/configs/scripts.
- Source path: `benchmark/seq_glue/source/project_local`.
- Official URL: no standalone official Seq-GLUE-only URL verified. Official GLUE source is https://gluebenchmark.com/; candidate continual-learning contexts include method-specific repositories such as LFPT5, Progressive Prompts, TRACE, and general continual-learning frameworks, but they do not establish one strict Seq-GLUE-only official source for this repo.
- Paper/source setting: the local stream order is the project published setting and should be cited through the CL paper/project setting that adopts this order, not as an independent official Seq-GLUE repository.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree.
- Proxy used: yes for web verification.
- Mirror used: no.
- LFS usage: no.
- Required construction: use the GLUE/SuperGLUE task definitions, construct the stream as `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`, and keep the local sampling/formatting policy from `seqglue_cl_tasks_train50_eval10.json`.
- Notes: see `benchmark/seq_glue/REPRODUCIBILITY.md`; published-setting configs for 8 methods are included.
