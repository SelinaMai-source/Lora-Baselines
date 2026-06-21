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

- Downloaded: no.
- Source path: intended `benchmark/instrdialog/source`, but no complete source was extracted.
- Official URL: https://github.com/hyintell/CITB
- Commit resolved: `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Not downloaded reason: official git clone failed with TLS early EOF; official GitHub codeload archive repeatedly ended with EOF / transfer closed after more than 36 minutes, so no complete archive was copied.

### InstrDialog++

- Downloaded: no.
- Source path: none.
- Official URL: https://github.com/hyintell/CITB
- Commit resolved: `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Not downloaded reason: same CITB download failure as InstrDialog; no duplicate large source tree was created.

### TRACE

- Downloaded: yes.
- Source path: `benchmark/trace/source`.
- Official URL: https://github.com/BeyonderXX/TRACE
- Commit: `462e39f616134f4f819efeb3baea8638c03c7db4`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable; source came from official GitHub.

### MultiWOZ NLG Dataset

- Downloaded: no.
- Source path: intended `benchmark/multiwoz_nlg/source/multiwoz`, but no complete source was extracted.
- Official URL: https://github.com/budzianowski/multiwoz
- Commit resolved: `fe0c8e65cfcd8462bd33c86e35f21addc84ca82b`.
- Proxy used: yes.
- Mirror used: no.
- Mirror consistency verification: not applicable.
- Not downloaded reason: official codeload attempt failed with incomplete read; official git clone failed with TLS early EOF. A later codeload attempt was not reached because the preceding CITB codeload command did not complete before manual termination.

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
