# CCF-A Three-Suite Alignment Status

Updated: 2026-06-22 05:35 UTC+8

This file records the current machine-local preparation state for the v2
CCF-A three-suite experiments. Large repositories, data, model snapshots, logs,
and run outputs are kept outside Git under `/root/autodl-tmp`.

## Proxy

- Clash/mihomo config root: `/root/autodl-tmp/Lora-code/configs/clash`.
- Runtime config: `/root/autodl-tmp/Lora-code/configs/clash/runtime/d18255a-GS.no_geoip.yaml`.
- Existing processes were found, so no duplicate proxy was started:
  `mihomo -d /root/autodl-tmp/Lora-code/configs/clash/runtime -f /root/autodl-tmp/Lora-code/configs/clash/runtime/d18255a-GS.no_geoip.yaml`.
- Open local ports: HTTP `127.0.0.1:7890`, SOCKS `127.0.0.1:7891`,
  controller `127.0.0.1:9090`.
- Download commands used:
  `HTTP_PROXY=http://127.0.0.1:7890`,
  `HTTPS_PROXY=http://127.0.0.1:7890`,
  `ALL_PROXY=http://127.0.0.1:7890`, with `NO_PROXY` cleared for Hugging Face.

## Downloaded Official Sources

All source clones below were downloaded from their official GitHub URLs through
the local proxy. No GitHub mirror was needed for these repositories.

- CITB: `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb`,
  official URL `https://github.com/hyintell/CITB`, commit
  `bf50533b5bced4c388691ecc75e26773da96b3fd`.
- O-LoRA: `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora`,
  official URL `https://github.com/cmnfriend/O-LoRA`, commit
  `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.
- LFPT5:
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/lfpt5`,
  official URL `https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning`,
  commit `cf7d17ce7de6a707d929d0542b3d5e639569855f`.
- Progressive Prompts:
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/progressive_prompts`,
  official URL `https://github.com/arazd/ProgressivePrompts`, commit
  `01572d6a73c0576b070ceee00dbe4f5bc278423f`.
- ARPER:
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper`,
  official URL `https://github.com/MiFei/Continual-Learning-for-NLG`, commit
  `99019defe6bf35e8459ca6abd6f25882724bc956`.
- ToDCL:
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl`,
  official URL `https://github.com/andreamad8/ToDCL`, commit
  `e70c1edf937f6eb570296ea2897dbc8d6815bc6d`.

Verification is by official URL, local Git commit hash, and directory/script
names matching each paper's README and experiment commands. No source mirror is
being represented as official.

## Runtime Artifacts

- Runtime manifest:
  `/root/autodl-tmp/lora-baselines-run_v1/ccfa_three_suite_manifest.csv`.
- Generated full-data streams:
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite`.
- Runtime configs:
  `/root/autodl-tmp/lora-baselines-run_v1/configs/ccfa_three_suite`.
- Queue script:
  `/root/autodl-tmp/lora-baselines-run_v1/run_ccfa_citb_caveat_queue.sh`.
- Queue log:
  `/root/autodl-tmp/lora-baselines-run_v1/logs/ccfa_citb_caveat_queue.log`.

## Suite A: CITB

Status: `caveat_ready` for three InstrDialog ours-only runs; strict paper
alignment remains `blocked`.

Prepared:

- Official CITB source/data are local at
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb`.
- InstrDialog streams were generated for official orders 1/2/3 under
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb`.
- Target split is 500 train / 50 dev / 100 test. Four official tasks do not
  contain enough remaining train instances after dev/test allocation, so the
  generated streams use all available official train examples for those tasks:
  `task1590_diplomacy_text_generation` has 8 train, `task639_multi_woz_user_utterance_generation`
  has 28 train, `task1713_convai3_sentence_generation` has 32 train, and
  `task766_craigslist_bargains_classification` has 50 train.
- InstrDialog++ streams were generated for 38 tasks with target 100 / 50 / 100.
- CITB official metric definitions were inspected in
  `collect_results.py`: final average/AR, FWT, BWT, official test score,
  and initial multitask score are matrix-derived.
- Current machine has a runnable local causal-LM backbone at
  `/root/autodl-tmp/model_cache/meta-llama/Llama-3.1-8B-Instruct`.

Started:

- tmux session: `ccfa_citb_caveat_ours`.
- Queue: three InstrDialog runs, orders/seeds 1, 2, 3.
- W&B project: `lora- baselines-run_v1`.
- First run startup was verified: W&B initialized, the stream loaded with
  19 segments, and model weights began loading successfully.

Strict blockers:

- The current ours runner builds `AutoModelForCausalLM` and PEFT
  `TaskType.CAUSAL_LM`; it does not yet implement a T5 seq2seq PEFT path.
- CITB README/scripts specify `google/t5-small-lm-adapt` for Stage 1, but do
  not provide a ready-made 100-SuperNI-init checkpoint. A local HF download for
  `google/t5-small-lm-adapt` is in progress under
  `/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt`.
- Paper-strict CITB result reporting still needs export of the same score
  matrix fields expected by `collect_results.py`.

## Suite B: Standard T5-Large PEFT CL

Status: `blocked` for strict ours runs; official resources and streams are
prepared.

Prepared:

- O-LoRA official source is local and provides standard order scripts using
  `initial_model/t5-large`:
  order1 `dbpedia -> amazon -> yahoo -> agnews`,
  order2 `dbpedia -> amazon -> agnews -> yahoo`,
  order3 `yahoo -> amazon -> agnews -> dbpedia`.
- O-LoRA `CL_Benchmark` and `configs/order*_configs` were converted into
  unified streams under
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft`.
- LFPT5 official README was inspected. It requires LM-adapted T5-large from
  the official Google T5 checkpoint prefix
  `gs://t5-data/pretrained_models/t5.1.1.lm100k.large/` and conversion via
  `convertmodel.py`.
- Progressive Prompts official README was inspected. Its T5 example uses
  `t5-large`, `select_k_per_class=1000`, prompt length 10, and task lists passed
  directly on the command line.
- A Hugging Face snapshot download for `t5-large` is in progress/partial under
  `/root/autodl-tmp/model_cache/hf_snapshots/t5-large`.

Blockers:

- Current ours does not have a T5-large seq2seq PEFT runner.
- `t5-large` weights were not complete at the time this status file was written.
- LFPT5 sample-equivalence with the O-LoRA four-task standard benchmark still
  needs final paper/code reconciliation; LFPT5 is lifelong few-shot prompt
  tuning and its README points to LM-adapted T5-large rather than O-LoRA's
  `initial_model/t5-large` directory layout.

## Suite C: Dialogue NLG

Status: `blocked` for ours runs; official/backup resources and streams are
prepared.

Prepared:

- ARPER official source is local at
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper`.
- ARPER WOZ3 `resource/woz3` includes unique-domain and unique-dialogue-act
  JSON resources plus data split files. These were converted into streams under
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/arper`.
- ARPER official BLEU-4 implementation is `bleu.py`, using NLTK
  `corpus_bleu` with 4-gram weights.
- ARPER default config uses SCLSTM (`model_type = lm`), domain granularity,
  task sequence `0,5,2,1,3,4`, and exemplar size 250.
- ToDCL official backup source is local at
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl`. Its README
  documents the 37-domain benchmark, GPT-2 backbone, BLEU/EER scorer, and
  official data download script.

Blockers:

- Current ours causal-LM instruction runner is not aligned to ARPER's SCLSTM
  dialogue NLG setup.
- ARPER SER/EER integration over ours generated outputs is not implemented.
- If switching to ToDCL as the runnable backup, its four upstream datasets
  (`SGD`, `Taskmaster`, `MultiWOZ`) still need full local download and
  preprocessing through the official `data/download.sh`/`utils/preprocess.py`
  path.

