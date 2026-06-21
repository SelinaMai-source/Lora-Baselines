# Lora-Baselines Source Manifest

This repository is organized for selected LoRA continual learning methods and benchmarks. Root-level ordinary files are intentionally avoided; all documentation and helper scripts live under `docs/`.

## Repository Layout Policy

- Root directories: `methods/`, `benchmark/`, `docs/`.
- No git submodules are used, because `.gitmodules` would add a root-level ordinary file.
- Vendored official sources live under each entry's `source/` directory with nested `.git` directories removed.
- Large model weights, gated assets, and generated experiment outputs are not vendored.

## Network And Proxy Verification

- Clash/mihomo config directory inspected: `/root/autodl-tmp/Lora-code/configs/clash`.
- Local proxy used: `HTTP_PROXY=http://127.0.0.1:7890`, `HTTPS_PROXY=http://127.0.0.1:7890`.
- `curl -I https://github.com` through the proxy succeeded.
- `git ls-remote https://github.com/cmnfriend/O-LoRA.git HEAD` through the proxy succeeded and returned `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- No global git config was modified.
- No Clash config, subscription, proxy node, token, or secret is committed.

## Methods

### Sequential LoRA

- Downloaded: no separate source tree.
- Source path: none; uses the O-LoRA official baseline source at `methods/o_lora/source`.
- Official URL: https://github.com/cmnfriend/O-LoRA
- Commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8` for the referenced O-LoRA source.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: no separate official Sequential LoRA repository was verified; this is documented as the baseline in the O-LoRA paper/source.

### Replay LoRA

- Downloaded: no separate source tree.
- Source path: none; uses the O-LoRA official baseline source at `methods/o_lora/source`.
- Official URL: https://github.com/cmnfriend/O-LoRA
- Commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8` for the referenced O-LoRA source.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: no separate official Replay LoRA repository was verified; this is documented as the baseline in the O-LoRA paper/source.

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

- Downloaded: no.
- Source path: none.
- Official URL: not verified.
- Commit: not available.
- Proxy used: not applicable.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Not downloaded reason: no public official code source was verified.

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

- Downloaded: no.
- Source path: none.
- Official URL: source required from project owner.
- Commit: not available.
- Proxy used: not applicable.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Not downloaded reason: no published paper, official experiment code, or project-owner-approved source was provided.

## Benchmarks

### InstrDialog

- Downloaded: partial official source.
- Source path: `benchmark/instrdialog/source`.
- Official URL: https://github.com/hyintell/CITB
- Commit: `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: vendored from the official local clone at `/root/autodl-tmp/CITB`. The nested `.git` directory is not committed. Official `data/CIT_data`, `data/splits`, scripts, scores, and source code are included. Official `data/tasks` is not committed because it is about 3.1G; use the official CITB repository to restore it before running full experiments.

### InstrDialog++

- Downloaded: no separate duplicate source tree.
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

- Downloaded: partial official source.
- Source path: `benchmark/multiwoz_nlg/source/multiwoz`.
- Official URL: https://github.com/budzianowski/multiwoz
- Commit: `fe0c8e65cfcd8462bd33c86e35f21addc84ca82b`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Notes: vendored from the official local clone at `/root/autodl-tmp/Lora-code/data/raw/multiwoz/multiwoz_repo`. Official code, database files, and available small official zip distributions are included. Unzipped `data/MultiWOZ_2.1/data.json` and `data/MultiWOZ_2.2/data.json` are not committed because they exceed GitHub's 100MB per-file limit; restore them from the official repository or unzip official releases in the experiment environment before full runs.

### MultiWOZ Evaluation

- Downloaded: yes.
- Source path: `benchmark/multiwoz_nlg/source/evaluation`.
- Official URL: https://github.com/Tomiinek/MultiWOZ_Evaluation
- Commit: `cd3f0ee3a936a2d1c8567f440a0b71b215d7f991`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub and HEAD was verified.

### Seq-GLUE

- Downloaded: no.
- Source path: none.
- Official URL: no standalone official Seq-GLUE-only source was verified.
- Commit: not available.
- Proxy used: not applicable.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Not downloaded reason: no standalone official Seq-GLUE source was verified; use task sequences from method-specific official repositories only after matching the target paper.
