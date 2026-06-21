# Ours-Only Experiment Plan v2

The v2 plan has exactly three main CCF-A experiment suites. We cite published
baselines from official papers/code and run only our method after data,
backbone, metric, and config alignment are complete.

Do not continue the old full baseline matrix.

## Main Suite 1: CITB Continual Instruction Tuning

Official paper and code:

- Paper: https://aclanthology.org/2023.findings-emnlp.633/
- Repo: https://github.com/hyintell/CITB

Run ours on:

- InstrDialog: 19 tasks, target 500 train / 50 dev / 100 test per task.
- InstrDialog++: 38 tasks, target 100 train / 50 dev / 100 test per task.
- Backbone: LM-adapted T5-small with the 100-SuperNI initial checkpoint.
- Seeds/orders: three official CITB orders.
- Metrics: ROUGE-L AR, FWT, BWT, Tinit, Tunseen.

Current status:

- Official CITB source/data are vendored under `benchmark/instrdialog/source`.
- Official task order files exist for `cl_dialogue_tasks` and
  `cl_dialogue_long_tasks`.
- Current local ours data under `methods/ours/source/project_local/data/processed`
  are `train50/eval10` diagnostics and are not official-setting comparable.
- No run is ready.

Next step:

- Run `python docs/scripts/prepare_citb_official_streams.py` to produce an audit
  JSON, then implement the actual converter and metric exporter.

## Main Suite 2: Standard T5-Large PEFT Continual Learning

Official papers and code:

- O-LoRA paper: https://aclanthology.org/2023.findings-emnlp.715/
- O-LoRA repo: https://github.com/cmnfriend/O-LoRA
- LFPT5 paper: https://openreview.net/forum?id=HCRVf71PMF
- LFPT5 repo: https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning
- Progressive Prompts paper: https://openreview.net/forum?id=UJTgQBc91_
- Progressive Prompts repo: https://github.com/arazd/ProgressivePrompts
- LB-CL paper: https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf
- LB-CL repo: no verified official repository.

Run ours on:

- T5-large.
- The official standard CL benchmark shared or compared across
  LFPT5/Progressive Prompts/O-LoRA/LB-CL.
- Metrics: final average accuracy, plus forgetting/BWT when aligned.

Verified local evidence:

- O-LoRA standard orders from vendored official scripts:
  - `dbpedia -> amazon -> yahoo -> agnews`
  - `dbpedia -> amazon -> agnews -> yahoo`
  - `yahoo -> amazon -> agnews -> dbpedia`
- The local `seqglue` stream is an 8-task `train50/eval10` project-local
  reconstruction and must not be used as this suite.

Current status:

- Blocked until O-LoRA `CL_Benchmark` and configs are converted into ours format
  and LFPT5/Progressive-Prompts sample equivalence is verified.

Next step:

- Run `python docs/scripts/audit_standard_peft_cl.py`, inspect the audit JSON,
  and then implement a converter for O-LoRA standard orders.

## Main Suite 3: Dialogue NLG / MultiWOZ Continual Learning

Primary route:

- ARPER paper: https://aclanthology.org/2020.findings-emnlp.310/
- ARPER repo: https://github.com/MiFei/Continual-Learning-for-NLG

Backup/extension route:

- ToDCL paper: https://aclanthology.org/2021.emnlp-main.590/
- ToDCL repo: https://github.com/andreamad8/ToDCL

Run ours on:

- ARPER MultiWOZ-2.0 domain/dialogue-act intent NLG first.
- Metrics: BLEU-4 and SER.
- ToDCL 37-domain NLG/E2E with BLEU/EER only after ARPER alignment or if ARPER
  source/data becomes blocked.

Current status:

- Official MultiWOZ and generic MultiWOZ evaluation sources are vendored.
- ARPER and ToDCL official sources are not vendored in this repo yet.
- Current local `multiwoz_nlg` stream is 5-domain `train50/eval10` and is not a
  direct ARPER/ToDCL comparison.
- No run is ready.

Next step:

- Run `python docs/scripts/audit_dialogue_nlg_sources.py`, then fetch or vendor
  ARPER official source and implement the ARPER stream/SER conversion.

## Appendix / Reference Only

- O-LoRA 15-task long-sequence PEFT benchmark can be added after the standard
  four-task suite is aligned.
- Continual-T0 is not a main v2 suite because CT0-11B weights and metric wrappers
  are not ready locally.
- TRACE is not a main v2 suite; keep it as optional robustness evidence only.

## Launch Policy

- Source of truth: `docs/ccfa_three_suite_manifest.csv`.
- Only rows with `status=ready` may be launched.
- Current v2 status: all rows are blocked, so no training should be started.
