# Lora-Baselines Source Manifest

This repository is organized for selected LoRA continual learning methods and benchmarks. Root-level ordinary files are intentionally avoided; all documentation and helper scripts live under `docs/`.

## Repository Layout Policy

- Root directories: `methods/`, `benchmark/`, `docs/`.
- No git submodules are used, because `.gitmodules` would add a root-level ordinary file.
- Vendored official sources live under each entry's `source/` directory with nested `.git` directories removed.
- Large model weights, gated assets, and generated experiment outputs are not vendored.
- Git LFS is used for complete benchmark files that exceed GitHub's 100MB per-file limit; this requires the hidden root `.gitattributes` file.

## Network And Proxy Verification

- Clash/mihomo config directory inspected: `/root/autodl-tmp/Lora-code/configs/clash`.
- Local proxy used: `HTTP_PROXY=http://127.0.0.1:7890`, `HTTPS_PROXY=http://127.0.0.1:7890`.
- `curl -I https://github.com` through the proxy succeeded.
- `git ls-remote https://github.com/cmnfriend/O-LoRA.git HEAD` through the proxy succeeded and returned `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- No global git config was modified.
- No Clash config, subscription, proxy node, token, or secret is committed.

## Methods

### Sequential LoRA

- Downloaded: yes, as project-local baseline plus official O-LoRA reference.
- Source path: `methods/sequential_lora/source/project_local`; official reference source at `methods/o_lora/source`.
- Official URL: https://github.com/cmnfriend/O-LoRA
- Official reference commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`.
- Proxy used: yes for official reference.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: no separate official Sequential LoRA repository was verified; project-local baseline implementation/configs are included for the complete v1 package.

### Replay LoRA

- Downloaded: yes, as project-local replay baseline plus official O-LoRA reference.
- Source path: `methods/replay_lora/source/project_local`; official reference source at `methods/o_lora/source`.
- Official URL: https://github.com/cmnfriend/O-LoRA
- Official reference commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`.
- Proxy used: yes for official reference.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: no separate official Replay LoRA repository was verified; project-local replay implementation/configs are included for the complete v1 package.

### O-LoRA

- Downloaded: yes.
- Source path: `methods/o_lora/source`.
- Official URL: https://github.com/cmnfriend/O-LoRA
- Commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub.
- Notes: nested `.git` removed. Generated `logs_and_outputs` and Python cache files were not retained in the vendored copy because they are experiment outputs/caches rather than source code.

### LB-CL

- Downloaded: yes, as project-local scaffold/configs.
- Source path: `methods/lb_cl/source/project_local`.
- Official URL: not verified.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`.
- Proxy used: not applicable for project-local source.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: no public official LB-CL experiment code was verified. The project-local README marks LB-CL as a scaffold, so it is included for completeness but must not be claimed as strict official paper code without owner verification.

### Progressive Prompts

- Downloaded: yes.
- Source path: `methods/progressive_prompts/source`.
- Official URL: https://github.com/arazd/ProgressivePrompts
- Commit: `01572d6a73c0576b070ceee00dbe4f5bc278423f`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub.

### Continual-T0

- Downloaded: yes.
- Source path: `methods/continual_t0/source`.
- Official URL: https://github.com/ThomasScialom/T0_continual_learning
- Commit: `4841ca267b2447d1b58d677a992b6808d9eaacf2`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub.
- Hugging Face CT0-11B metadata: small metadata files are stored under `methods/continual_t0/hf_metadata`; large model weights were intentionally not downloaded because CT0-11B weights are large model artifacts and outside the source-vendoring scope.

### LFPT5

- Downloaded: yes.
- Source path: `methods/lfpt5/source`.
- Official URL: https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning
- Commit: `cf7d17ce7de6a707d929d0542b3d5e639569855f`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub archive/HEAD.
- Notes: full clone initially failed with `No space left on device` while checking out generated `transformers/build` files. The vendored source excludes that generated build tree.

### Ours

- Downloaded: yes, as project-owner local source snapshot.
- Source path: `methods/ours/source/project_local`.
- Official URL: project-owner local source `/root/autodl-tmp/Lora-code`.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`.
- Proxy used: not applicable.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: local source tree was dirty when inspected; logs, caches, archives, model assets, and result outputs are excluded. This is not an external published official repository.

## Benchmarks

### InstrDialog

- Downloaded: yes, complete official CITB source/data.
- Source path: `benchmark/instrdialog/source`.
- Official URL: https://github.com/hyintell/CITB
- Commit: `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- LFS used: no file in CITB exceeds GitHub's 100MB per-file limit; complete `data/tasks` is committed as regular Git files.
- Notes: vendored from the official local clone at `/root/autodl-tmp/CITB`; nested `.git` removed.

### InstrDialog++

- Downloaded: yes, via shared complete CITB source.
- Source path: uses `benchmark/instrdialog/source`.
- Official URL: https://github.com/hyintell/CITB
- Commit: `bf50533b5bced4c388691ecc75e26773da96b3fd` for the shared CITB source.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: InstrDialog++ uses the same official CITB source as InstrDialog. No duplicate source tree is committed to avoid redundant benchmark files.

### TRACE

- Downloaded: yes.
- Source path: `benchmark/trace/source`.
- Official URL: https://github.com/BeyonderXX/TRACE
- Commit: `462e39f616134f4f819efeb3baea8638c03c7db4`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub.

### MultiWOZ NLG Dataset

- Downloaded: yes, complete official MultiWOZ source/data with Git LFS for oversized JSON files.
- Source path: `benchmark/multiwoz_nlg/source/multiwoz`.
- Official URL: https://github.com/budzianowski/multiwoz
- Commit: `fe0c8e65cfcd8462bd33c86e35f21addc84ca82b`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- LFS used: yes for `data/MultiWOZ_2.1/data.json` and `data/MultiWOZ_2.2/data.json`, which exceed GitHub's 100MB per-file limit.
- Notes: vendored from the official local clone at `/root/autodl-tmp/Lora-code/data/raw/multiwoz/multiwoz_repo`; nested `.git` removed.

### MultiWOZ Evaluation

- Downloaded: yes.
- Source path: `benchmark/multiwoz_nlg/source/evaluation`.
- Official URL: https://github.com/Tomiinek/MultiWOZ_Evaluation
- Commit: `cd3f0ee3a936a2d1c8567f440a0b71b215d7f991`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub and HEAD was verified.

### Seq-GLUE

- Downloaded: yes, as project-local benchmark stream/configs.
- Source path: `benchmark/seq_glue/source/project_local`.
- Official URL: no standalone official Seq-GLUE-only source was verified; GLUE official source is https://gluebenchmark.com/.
- Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`.
- Proxy used: not applicable for project-local source.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: includes project-local 8-task stream `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`, conversion scripts, and published-setting configs. Treat as project-local Seq-GLUE package, not a standalone official Seq-GLUE repository.
