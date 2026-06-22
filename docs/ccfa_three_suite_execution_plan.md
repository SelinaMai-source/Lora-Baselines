# CCF-A Three-Suite Execution Plan

This is the v2 execution plan for the CCF-A submission experiments. It replaces
the old "run every baseline locally" direction: cite published baselines from
official papers/code, and run only our method in settings that are aligned well
enough to support a fair comparison.

No run should be launched until the row is marked `ready` in
`docs/ccfa_three_suite_manifest.csv`.

Strict alignment pass (2026-06-22):

- Use `docs/ccfa_strict_alignment_matrix.md` as the current checklist of
  paper/repo evidence, local prepared paths, and launch blockers.
- Use only `*_ours_strict.yaml` configs for strict runs. The old Llama
  caveat-ready configs are not final strict configs.
- Current launch state: Standard PEFT CL order 1/2/3 are `ready`; CITB
  InstrDialog is `needs-stage1`; CITB InstrDialog++ and ARPER Dialogue NLG are
  `blocked`.

## Ground Rules

- Do not report numbers unless they are traceable to a paper, official page, or
  official code artifact.
- Do not treat local `train50/eval10` diagnostic streams as official benchmark
  settings.
- Do not commit secrets, W&B keys, model weights, Hugging Face caches, generated
  logs, or run outputs.
- Keep large checkpoints outside Git. Only source, configs, manifests, and small
  metadata belong in this repository.
- Run ours serially when ready. Do not resume the old full baseline matrix.

## Suite A: CITB Continual Instruction Tuning

Purpose: this is the primary continual instruction-tuning benchmark and the
closest match to the paper narrative.

Official sources:

- Paper: [CITB: A Benchmark for Continual Instruction Tuning](https://aclanthology.org/2023.findings-emnlp.633/), Findings of EMNLP 2023.
- Official repo: [hyintell/CITB](https://github.com/hyintell/CITB).
- Vendored source: `benchmark/instrdialog/source`.

Official setting to match:

- Backbone/checkpoint: `google/t5-small-lm-adapt`, then initial instruction
  tuning on 100 SuperNI tasks.
- InstrDialog: `cl_dialogue_tasks`, 19 tasks, 500 train / 50 dev / 100 test per
  task according to the paper setting.
- InstrDialog++: 38 tasks. User-level target is 100 train / 50 dev / 100 test
  per task; the vendored long-stream CITB scripts currently expose
  `max_num_instances_per_task=100` and `max_num_instances_per_eval_task=25`,
  which needs final reconciliation against the paper/table before launch.
- Orders: official `order1.txt`, `order2.txt`, `order3.txt` under
  `benchmark/instrdialog/source/data/CIT_data/task_orders/`.
- Metrics: ROUGE-L AR, FWT, BWT, Tinit, Tunseen.

Published baseline targets:

- InstrDialog AR/BWT: FT-init 35.7/-4.6, L2 35.6/-3.8, EWC 34.5/-6.8,
  AGEM-10 33.2/-7.3, Replay-10 38.4/-1.3, Replay-50 40.4/1.6, Multi 42.1.
- InstrDialog++ AR/BWT: FT-init 34.8/-2.8, L2 36.1/-4.0, EWC 38.6/-4.0,
  AGEM-10 39.3/-3.8, Replay-10 43.1/-3.6, Multi 44.9.

Ours to run:

- Six rows: InstrDialog and InstrDialog++ across official orders/seeds 1, 2, 3.
- Configs are intentionally blocked in `docs/configs/ccfa_three_suite/` until:
  official processed streams are generated, T5-small LM-adapted/SuperNI-init
  loading is implemented, and CITB-compatible ROUGE-L matrix aggregation is
  wired to ours outputs.

Success standard:

- Primary: ours beats the strongest non-upper-bound published AR baseline while
  improving or matching BWT.
- Stronger claim: ours approaches Multi without storing old task data and
  without relying on task IDs at inference.

Immediate actions:

1. Generate official processed streams from vendored CITB using
   `docs/scripts/prepare_citb_official_streams.py`.
2. Add/verify T5-small LM-adapted + 100-SuperNI-init loading in the ours runner.
3. Add CITB-style result matrix aggregation so AR/FWT/BWT/Tinit/Tunseen are
   directly comparable to `benchmark/instrdialog/source/collect_results.py`.

## Suite B: Standard T5-Large PEFT Continual Learning

Purpose: this suite establishes comparison against published PEFT/LoRA
continual learning methods rather than only against local baselines.

Official sources:

- O-LoRA paper: [Orthogonal Subspace Learning for Language Model Continual Learning](https://aclanthology.org/2023.findings-emnlp.715/), Findings of EMNLP 2023.
- O-LoRA repo: [cmnfriend/O-LoRA](https://github.com/cmnfriend/O-LoRA).
- LFPT5 paper: [A Unified Framework for Lifelong Few-shot Language Learning Based on Prompt Tuning of T5](https://openreview.net/forum?id=HCRVf71PMF), ICLR 2022.
- LFPT5 repo: [qcwthu/Lifelong-Fewshot-Language-Learning](https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning).
- Progressive Prompts paper: [Progressive Prompts: Continual Learning for Language Models](https://openreview.net/forum?id=UJTgQBc91_), ICLR 2023.
- Progressive Prompts repo: [arazd/ProgressivePrompts](https://github.com/arazd/ProgressivePrompts).
- LB-CL paper: [Learn More, But Bother Less: Parameter Efficient Continual Learning](https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf), NeurIPS 2024.
- LB-CL repo status: no verified official repository.

Verified local evidence:

- O-LoRA official source is vendored under `methods/o_lora/source`.
- Standard O-LoRA scripts use T5-large and four task orders:
  - order1: `dbpedia -> amazon -> yahoo -> agnews`
  - order2: `dbpedia -> amazon -> agnews -> yahoo`
  - order3: `yahoo -> amazon -> agnews -> dbpedia`
- O-LoRA long script uses 15 tasks:
  `yelp -> amazon -> MNLI -> CB -> COPA -> QQP -> RTE -> IMDB -> SST-2 -> dbpedia -> agnews -> yahoo -> MultiRC -> BoolQA -> WiC`.
- Current local `seqglue` is an 8-task project-local `train50/eval10` stream and
  is not the verified O-LoRA/LFPT5/Progressive-Prompts standard benchmark.

Official setting to match:

- Backbone: T5-large.
- Data: O-LoRA/LFPT5/Progressive-Prompts standard CL benchmark, exact task
  configs and sizes from official code.
- Metrics: final average accuracy after the last task, plus forgetting/BWT when
  our evaluator can compute it consistently.

Published baseline targets:

- O-LoRA Table 2 standard CL averages: SeqLoRA 43.7, IncLoRA 66.4, Replay 57.8,
  EWC 50.3, LwF 52.3, L2P 60.7, LFPT5 72.7, O-LoRA 75.8, ProgPrompt 75.1,
  PerTaskFT 70.0, MTL 80.0.
- LB-CL Table 2 standard CL averages: SeqLoRA 39.3, IncLoRA 63.6, Replay 53.0,
  EWC 47.9, LFPT5 71.3, O-LoRA 75.4, LB-CL 76.7, ProgPrompt 76.1, PerTaskFT
  70.0, MTL 80.0.

Ours to run:

- Three blocked rows, one per verified standard order.
- Do not launch from `seqglue__ours__s123.yaml`.

Immediate actions:

1. Convert O-LoRA `CL_Benchmark` and `configs/order*_configs` into our unified
   stream format using `docs/scripts/audit_standard_peft_cl.py` as the first
   auditable extraction point.
2. Confirm whether LFPT5 and Progressive Prompts report the same four-task
   standard benchmark or a few-shot variant with different sample counts.
3. Add a T5-large seq2seq/PEFT runner path for ours, then regenerate configs.

## Suite C: Dialogue NLG / MultiWOZ Continual Learning

Purpose: this suite gives a task-oriented dialogue generation benchmark with
BLEU and semantic-error metrics, complementing ROUGE-L and classification
accuracy.

Priority choice:

- P1 starts with ARPER MultiWOZ NLG because it is closer to the vendored
  MultiWOZ assets and the desired BLEU-4/SER story.
- ToDCL is kept as an extension/backup because its 37-domain task-oriented
  benchmark is broader and requires a separate official data conversion path.

Official sources:

- ARPER paper: [Continual Learning for Natural Language Generation in Task-oriented Dialog Systems](https://aclanthology.org/2020.findings-emnlp.310/), Findings of EMNLP 2020.
- ARPER repo: [MiFei/Continual-Learning-for-NLG](https://github.com/MiFei/Continual-Learning-for-NLG).
- ToDCL paper: [Continual Learning in Task-Oriented Dialogue Systems](https://aclanthology.org/2021.emnlp-main.590/), EMNLP 2021.
- ToDCL repo: [andreamad8/ToDCL](https://github.com/andreamad8/ToDCL).
- Vendored local assets: MultiWOZ source under `benchmark/multiwoz_nlg/source/multiwoz`
  and generic MultiWOZ evaluation under `benchmark/multiwoz_nlg/source/evaluation`.

Official setting to match:

- ARPER: MultiWOZ-2.0 continual NLG over domain/dialogue-act intent streams;
  published baselines include 250/500 exemplars; metrics are BLEU-4 and SER.
- ToDCL: 37-domain ToD NLG/E2E; metrics are BLEU and EER.

Published baseline targets:

- ARPER 7 dialogue-act intent setting with 250 exemplars: ARPER SER 3.63 and
  BLEU-4 0.701; Full SER 3.08 and BLEU-4 0.694.
- ToDCL official table snippets: Modularized NLG Replay BLEU 21.4832 / EER
  0.0559855, Adapter BLEU 21.7719 / EER 0.163975, Multi BLEU 26.1462 / EER
  0.0341823.

Ours to run:

- Start with three blocked ARPER rows. Current local `multiwoz_nlg` is a
  5-domain `train50/eval10` diagnostic stream and is not a direct ARPER/ToDCL
  comparison.

Immediate actions:

1. Fetch or vendor ARPER official source if space/network permits, or keep the
   official link and extraction TODO explicit.
2. Rebuild MultiWOZ-2.0 DA-intent/domain streams to match ARPER, not the current
   local 5-domain sample.
3. Wire official BLEU-4/SER evaluation. Current missing-slot proxy is not enough
   for final paper comparison.

## Launch Order

1. P0 CITB InstrDialog and InstrDialog++ after official stream, checkpoint, and
   metric alignment are complete.
2. P0 Standard T5-large PEFT CL after O-LoRA/LFPT5/Progressive-Prompts benchmark
   conversion is complete.
3. P1 ARPER MultiWOZ NLG after official stream and SER metric are matched.
4. Appendix/reference only: O-LoRA 15-task long sequence, Continual-T0, TRACE.

## Current Status

Updated 2026-06-22:

- Generated auditable streams under
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/` using
  `docs/scripts/prepare_ccfa_three_suite_artifacts.py`.
- Generated blocked configs under
  `/root/autodl-tmp/lora-baselines-run_v1/configs/ccfa_three_suite/`.
- Updated runtime manifest:
  `/root/autodl-tmp/lora-baselines-run_v1/ccfa_three_suite_manifest.csv`.
- Added metric aggregation wrapper:
  `docs/scripts/compute_ccfa_three_suite_metrics.py`.

No training was launched. All 12 ours-only rows remain `blocked`; there is no
fully aligned run yet.

Suite-specific status:

- CITB InstrDialog: official order/task data were converted for 3 orders using
  the requested 500 train / 50 dev / 100 test target. Still blocked because ours
  currently lacks a T5-small LM-adapted + 100-SuperNI-init seq2seq runner path
  and CITB-compatible ROUGE-L result-matrix export.
- CITB InstrDialog++: official 38-task order/task data were converted using the
  requested 100 / 50 / 100 target for auditability, but launch remains blocked
  because vendored official long-stream scripts use
  `max_num_instances_per_eval_task=25`; this must be reconciled with the target
  split before any paper run.
- Standard T5-Large PEFT CL: O-LoRA standard orders 1/2/3 were converted from
  `CL_Benchmark` and `configs/order*_configs`. Still blocked because ours is
  still a causal-LM PEFT path (`CAUSAL_LM` LoRA wrapper) rather than a T5-large
  seq2seq PEFT runner, and LFPT5/Progressive-Prompts sample-equivalence still
  needs final verification.
- Dialogue NLG / ARPER: ARPER official source was fetched to
  `/root/autodl-tmp/lora-baselines-run_v1/external/arper` and its WOZ3
  unique-domain and unique-dialogue-act resources were converted. The 3 seed
  configs target the dialogue-act stream. Still blocked because ours needs a
  dialogue-NLG backbone decision, official SER scorer integration over generated
  outputs, and confirmation that this ARPER WOZ3 resource is the intended
  MultiWOZ-2.0 comparison target.

Current model/checkpoint blockers:

- `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k` contains only small
  metadata/index files; the large TensorFlow shards and converted PyTorch
  checkpoint are missing.
- No local `google/t5-small-lm-adapt` + 100-SuperNI-init checkpoint is configured
  for ours.
- The ours runner currently loads `AutoModelForCausalLM` and creates PEFT LoRA
  with `TaskType.CAUSAL_LM`; this is not aligned with the T5-small/T5-large
  seq2seq suites.
