# Published Baseline Survey for Lora-Baselines v2

This survey replaces the earlier "run every baseline on every local benchmark" direction. The comparison target is now: cite published continual learning / instruction tuning / LoRA continual learning results where the paper setting is comparable, and run only our method in the matched setting.

## v2 CCF-A Scope

The CCF-A main experiments are limited to three suites:

- CITB Continual Instruction Tuning: paper https://aclanthology.org/2023.findings-emnlp.633/ and official repo https://github.com/hyintell/CITB.
- Standard T5-Large PEFT Continual Learning: O-LoRA paper/repo https://aclanthology.org/2023.findings-emnlp.715/ and https://github.com/cmnfriend/O-LoRA; LFPT5 paper/repo https://openreview.net/forum?id=HCRVf71PMF and https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning; Progressive Prompts paper/repo https://openreview.net/forum?id=UJTgQBc91_ and https://github.com/arazd/ProgressivePrompts; LB-CL paper https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf with no verified official repo.
- Dialogue NLG / MultiWOZ Continual Learning: ARPER paper/repo https://aclanthology.org/2020.findings-emnlp.310/ and https://github.com/MiFei/Continual-Learning-for-NLG; ToDCL paper/repo https://aclanthology.org/2021.emnlp-main.590/ and https://github.com/andreamad8/ToDCL.

Everything else in this document is appendix/reference unless explicitly
promoted later. ArXiv-only, unofficial, or unverified-code items must not be
presented as mandatory CCF-A baselines.

## Ground Rule

- Use published papers as required baselines: ACL Anthology papers, NeurIPS/ICLR/EMNLP proceedings, Findings, and similar archival venues.
- Use arXiv-only work as context or optional motivation, not as a mandatory baseline.
- Do not expand the old full method-by-benchmark queue. Existing non-ours runs should be treated as historical/pre-direction-change artifacts.
- Do not report numbers unless they are directly traceable to a paper, official page, or official code table. Items marked "needs verification" must not be used as final paper numbers.

## High-Priority Published Sources

### CITB: A Benchmark for Continual Instruction Tuning

- Status: published, Findings of EMNLP 2023.
- Paper: https://aclanthology.org/2023.findings-emnlp.633/
- Official code/data: https://github.com/hyintell/CITB
- Setting: continual instruction tuning with two streams, InstrDialog with 19 dialogue tasks and InstrDialog++ with 38 tasks.
- Backbone: LM-adapted T5-small, with an initial instruction-tuned checkpoint from 100 SuperNI tasks for most methods.
- Data size: InstrDialog uses 500/50/100 train/dev/test per task; InstrDialog++ uses 100/50/100 per task.
- Metrics: ROUGE-L based AR, FWT, BWT, plus Tinit and Tunseen ROUGE-L retention.
- Replay/buffer: AGEM and Replay use memory sizes 10 or 50 per task. FT-init, FT-no-init, L2, EWC, AdapterCL do not use replay.
- Task order: one randomly permuted stream order, run with three random seeds.
- Directly citable numbers:
  - InstrDialog AR: FT-init 35.7, L2 35.6, EWC 34.5, AGEM-10 33.2, AGEM-50 34.9, Replay-10 38.4, Replay-50 40.4, Multi 42.1.
  - InstrDialog BWT: FT-init -4.6, L2 -3.8, EWC -6.8, AGEM-10 -7.3, AGEM-50 -6.0, Replay-10 -1.3, Replay-50 1.6.
  - InstrDialog++ AR: FT-init 34.8, L2 36.1, EWC 38.6, AGEM-10 39.3, Replay-10 43.1, Multi 44.9.
  - InstrDialog++ BWT: FT-init -2.8, L2 -4.0, EWC -4.0, AGEM-10 -3.8, Replay-10 -3.6.
- Use as baseline: yes, for CITB/InstrDialog and InstrDialog++.
- Caveat for ours: current local configs use Llama-3.1-8B-Instruct and train50/eval10, so they are not yet paper-setting comparable. To cite CITB numbers as hard baselines, ours must either reproduce CITB data sizes and ROUGE-L/AR/FWT/BWT reporting or explicitly frame the comparison as a scaled-down/stronger-backbone diagnostic.

### LFPT5: A Unified Framework for Lifelong Few-shot Language Learning Based on Prompt Tuning of T5

- Status: published, ICLR 2022.
- Paper: https://openreview.net/forum?id=HCRVf71PMF
- Official code: https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning
- Setting: lifelong few-shot language learning; prompt tuning of frozen T5, with a prompt that both solves tasks and generates pseudo samples for rehearsal-like retention.
- Replay/buffer: uses generated pseudo labeled samples rather than a normal stored raw-data buffer.
- Benchmarks: standard text classification CL benchmark used by later Progressive Prompts / O-LoRA / LB-CL comparisons.
- Metrics: average test accuracy after the final task, usually averaged over task orders; some papers additionally discuss forgetting/transfer.
- Directly citable numbers in later published comparisons:
  - O-LoRA paper table: LFPT5 72.7 average on standard CL; 69.2 average on large-number-of-tasks benchmark.
  - LB-CL paper table: LFPT5 71.3 average on standard CL; 68.7 average on large-number-of-tasks benchmark.
- Use as baseline: yes, when ours is run on the same T5-large standard CL/long-sequence setting.
- Caveat for ours: LFPT5 is prompt tuning, few-shot, T5-centered, and uses generated replay. It is not an online task-agnostic LoRA-bank setting.

### Progressive Prompts: Continual Learning for Language Models

- Status: published, ICLR 2023.
- Paper: https://openreview.net/forum?id=UJTgQBc91_
- Official code: https://github.com/arazd/ProgressivePrompts
- Setting: frozen base model; learns one soft prompt per task and concatenates previously learned prompts.
- Replay/buffer: no raw data replay.
- Task identity: relies on task-specific prompt structure and task identity, especially at inference in later comparisons.
- Benchmarks: T5 few-shot standard CL benchmark and a 15-task long-sequence benchmark; BERT benchmark is also reported.
- Metrics: average test accuracy after the final task; FWT/BWT in appendix.
- Directly citable numbers:
  - ICLR paper long-sequence T5-Large: ProgPrompt 76.2/78.7/79.5 for 20/200/1000 samples per class; LFPT5 54.3/58.2/69.2; MTL 70.7/72.5/76.3; Per-task Finetune 68.2/73.7/78.1.
  - O-LoRA paper table: ProgPrompt 75.1 average on standard CL; 77.9 average on large-number-of-tasks benchmark.
  - LB-CL paper table: ProgPrompt 76.1 average on standard CL; 78.4 average on large-number-of-tasks benchmark.
- Use as baseline: yes, especially to argue that task-specific prompt expansion can be strong but is not ideal for online/task-agnostic settings.
- Caveat for ours: it depends on task identity and accumulates prompt length with task count; this is a core introduction point for why a routing/branching online method is needed.

### O-LoRA: Orthogonal Subspace Learning for Language Model Continual Learning

- Status: published, Findings of EMNLP 2023.
- Paper: https://aclanthology.org/2023.findings-emnlp.715/
- Official code: https://github.com/cmnfriend/O-LoRA
- Setting: LoRA-based continual learning; task-specific low-rank subspaces are kept orthogonal.
- Replay/buffer: no user data storage for replay.
- Task identity: requires task identification during training to train task-specific LoRA parameters; paper states this as a limitation.
- Backbones: T5-large for standard CL comparisons; LLaMA-7B for generalization/MMLU analysis.
- Metrics: average accuracy after the last task, averaged over 3 runs/orders; also MMLU zero-shot in LLaMA analysis.
- Directly citable numbers from Table 2:
  - Standard CL: SeqFT 28.5 avg, SeqLoRA 43.7, IncLoRA 66.4, Replay 57.8, EWC 50.3, LwF 52.3, L2P 60.7, LFPT5 72.7, O-LoRA 75.8, ProgPrompt 75.1, PerTaskFT 70.0, MTL 80.0.
  - Large-number-of-tasks: SeqFT 7.4 avg, SeqLoRA 1.6, IncLoRA 61.2, Replay 54.2, EWC 45.1, LwF 46.9, L2P 56.1, LFPT5 69.2, O-LoRA 69.6, ProgPrompt 77.9, PerTaskFT 78.1, MTL 76.5.
  - LLaMA/MMLU analysis: Alpaca-LoRA 37.5 MMLU and 46.7 CL; Alpaca-LoRA-CL 23.3; Alpaca-inc-LoRA-CL 28.6 and 33.1; Alpaca-O-LoRA-CL 33.6 and 76.8.
- Use as baseline: yes, the most important published LoRA continual baseline.
- Caveat for ours: O-LoRA is not replay-based and is directly relevant, but it is still task-aware during training and not designed for unknown online drift.

### LB-CL: Learn More, But Bother Less: Parameter Efficient Continual Learning

- Status: published, NeurIPS 2024.
- Paper: https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf
- Official code: no official repository verified in the current repo/source manifest.
- Setting: low-rank parameter/SVD triplet continual learning with sensitivity-based previous-task knowledge extraction, initialization, and gradient projection.
- Replay/buffer: no raw data replay in the main method; uses seed samples from the new task for sensitivity scoring.
- Task identity: does not use task ID during testing; still uses sequential task boundaries/training stages.
- Backbones: T5-large and T5-base.
- Metrics: testing performance on standard CL and large-number-of-tasks benchmarks, average over three task orders.
- Directly citable numbers from Table 2:
  - Standard CL averages: SeqLoRA 39.3, IncLoRA 63.6, Replay 53.0, EWC 47.9, LFPT5 71.3, O-LoRA 75.4, LB-CL 76.7, ProgPrompt 76.1, PerTaskFT 70.0, MTL 80.0.
  - Large-number-of-tasks averages: SeqLoRA 4.2, IncLoRA 60.5, Replay 54.1, EWC 44.8, LFPT5 68.7, O-LoRA 68.8, LB-CL 69.2, ProgPrompt 78.4, PerTaskFT 78.1, MTL 76.3.
- Use as baseline: yes, if ours is evaluated on the same T5-large benchmarks.
- Caveat for ours: highly relevant because it transfers low-rank knowledge, but it assumes clear task stages and sensitivity computation. It does not solve fully online, unlabeled drift/routing in the same way as ours.

### Continual-T0 / Fine-tuned Language Models are Continual Learners

- Status: published, EMNLP 2022.
- Paper: https://aclanthology.org/2022.emnlp-main.410/
- Official code: https://github.com/ThomasScialom/T0_continual_learning
- Setting: start from T0/T0pp and progressively learn 8 new NLG tasks.
- Replay/buffer: rehearsal over 1% of T0 training data; no rehearsal for T0 zero-shot evaluation tasks.
- Backbone: T0_3B and T0pp/CT0-11B.
- Metrics: task-specific NLG metrics, including ROUGE, BLEU, SARI, BERTScore, and custom metrics; T0 train/zero-shot retention.
- Directly citable numbers:
  - CT0pp maintains 99.8% of its upper-bound performance after the 8-task sequence.
  - CT03B maintains 98.0% of its upper-bound performance.
  - No task drops by more than 2% for T0pp.
  - ASSET simplification: CT0 reports 85.9 BLEU4 and 46.6 SARI versus MUSS 72.98 BLEU4 and 44.15 SARI.
- Use as baseline: yes for an instruction/NLG continual learning suite if ours can match the 8 NLG tasks and metrics.
- Caveat for ours: CT0 uses an 11B T0-family checkpoint and rehearsal of original T0 training data. The local CT0-11B weights are currently incomplete, and ours does not currently have a verified CT0-compatible wrapper.

### MIGU / Unlocking Continual Learning Abilities in Language Models

- Status: published, Findings of EMNLP 2024.
- Paper: https://aclanthology.org/2024.findings-emnlp.379/
- Official source: ACL software attachment is available from the ACL page; local source manifest records the software zip under the Replay LoRA entry.
- Setting: magnitude-based gradient updating for continual learning; can combine with FT, LoRA, IncLoRA, OIncLoRA, and LoRAReplay.
- Replay/buffer: base MIGU is rehearsal-free and task-label-free; LoRAReplay baseline uses 2% past-task data.
- Benchmarks: standard CL benchmark and long sequence benchmark with T5-large, following LFPT5/O-LoRA-style settings; also RoBERTa continual pretraining and Llama2 instruction-tuning analyses.
- Metrics: average accuracy on T5 benchmarks, plus MF1/ACC for RoBERTa.
- Directly citable numbers from Table 2 snippets:
  - LoRAReplay: 74.5 on standard CL and 75.2 on long sequence.
  - LoRAReplay + MIGU: 76.2 on standard CL and 76.5 on long sequence.
  - LoRA + MIGU improves LoRA by 15.2 points on the long sequence benchmark.
- Use as baseline: yes for comparing to rehearsal-free/task-label-free partial update ideas, but extract the full table from the PDF before final camera-ready numbers.
- Caveat for ours: MIGU is gradient-mask based and does not build an explicit router/bank. LoRAReplay uses old data, which is incompatible with strict no-replay online privacy settings.

### Continual Learning for NLG in Task-Oriented Dialogue Systems / ARPER

- Status: published, Findings of EMNLP 2020.
- Paper: https://aclanthology.org/2020.findings-emnlp.310/
- Official code: https://github.com/MiFei/Continual-Learning-for-NLG
- Setting: MultiWOZ-2.0 task-oriented NLG, continual learning over domains and dialogue-act intents.
- Replay/buffer: ARPER uses prioritized exemplar replay plus adaptive regularization; published tables include 250/500 exemplars.
- Metrics: slot error rate (SER, lower is better) and BLEU-4 (higher is better).
- Directly citable numbers:
  - 7 DA intents with 250 exemplars: ARPER SER 3.63 and BLEU-4 0.701 on all tasks; Full SER 3.08 and BLEU-4 0.694.
  - Ablation table: ARPER SER 4.82 and BLEU-4 0.592 under the reported 6-domain setting.
- Use as baseline: yes for a MultiWOZ NLG experiment if ours matches their domain/intent stream and SER/BLEU-4 metric.
- Caveat for ours: current local `multiwoz_nlg` config uses a 5-domain train50/eval10 stream and Llama-3.1, so it cannot directly cite ARPER numbers without reprocessing to the paper setting.

### ToDCL / AdapterCL: Continual Learning in Task-Oriented Dialogue Systems

- Status: published, EMNLP 2021.
- Paper: https://aclanthology.org/2021.emnlp-main.590/
- Official code: https://github.com/andreamad8/ToDCL
- Setting: 37-domain task-oriented dialogue benchmark over Intent, DST, NLG, and E2E; datasets include Taskmaster, SGD, and MultiWOZ.
- Replay/buffer: compares replay, regularization, architecture/adapters, LAMOL, and multi-task upper bound.
- Metrics: Intent accuracy, DST JGA, NLG BLEU and EER, E2E BLEU/EER, plus CL-specific averages/forgetting.
- Directly citable numbers from official code table:
  - Modularized NLG: Replay BLEU 21.4832 / EER 0.0559855; Adapter BLEU 21.7719 / EER 0.163975; Multi BLEU 26.1462 / EER 0.0341823.
  - E2E: Replay BLEU 16.2668 / EER 0.190309; Adapter BLEU 16.5768 / EER 0.331949; Multi BLEU 23.6073 / EER 0.12558.
- Use as baseline: yes for dialogue/NLG continual learning, especially if we position ours against task-specific adapter routing.
- Caveat for ours: ToDCL is not LoRA-based and uses a 37-domain ToD benchmark, not the local 5-domain MultiWOZ-only stream. Direct comparison needs a matched stream or must be labeled as related-work evidence.

## Lower-Priority or Reference-Only Sources

### TRACE: A Comprehensive Benchmark for Continual Learning in Large Language Models

- Status: OpenReview submission to NeurIPS 2024 Datasets and Benchmarks in the checked result; not verified as an archival published paper.
- Official code: https://github.com/BeyonderXX/TRACE
- Setting: 8 aligned-LLM tasks covering domain-specific tasks, multilingual, code, and math.
- Metrics: task-specific accuracy/ROUGE/BLEU-like measures plus general/instruction/safety degradation.
- Use as baseline: not as a mandatory published baseline unless archival acceptance is verified.
- Caveat for ours: current local `trace__ours__s123.yaml` has a `trace_three_h_delta` stub and train50/eval10; do not claim final TRACE comparability yet.

### Sequential LoRA

- Status: not an independent published method in this repo. It is a baseline protocol used in O-LoRA/LB-CL/MIGU-style papers.
- Use as baseline: cite only as a reported baseline inside published tables, not as a standalone paper.
- Caveat for ours: useful as a lower bound in related work, but no need to re-run it under the new direction.

## Introduction Material

- Standard rehearsal approaches can be strong, but they require storing old task data. This conflicts with online/privacy-sensitive settings and scales poorly as task streams grow.
- Prompt-expansion methods such as Progressive Prompts prevent forgetting well, but they rely on task-specific prompts and task identity. This becomes brittle when tasks arrive online and the system must infer which prior knowledge applies.
- O-LoRA and LB-CL are the most relevant LoRA/low-rank continual methods. They reduce interference by orthogonal subspaces or low-rank knowledge transfer, but still assume clear task stages and task-aware training signals.
- Continual-T0 shows instruction-tuned LMs can learn NLG streams with little forgetting, but it relies on rehearsal from original T0 data and very large T0-family checkpoints.
- CITB shows a surprising challenge: simple sequential fine-tuning of an instruction-tuned model can be competitive, and rich natural-language instructions themselves reduce forgetting. Therefore ours should not only beat vanilla LoRA; it must beat or match the strongest published instruction-aware baselines under their own setting.
- Dialogue/NLG continual learning papers show BLEU/SER trade-offs and the cost of replay/adapters. This supports positioning ours as a method for online domain drift where raw data replay or task-specific expert selection is undesirable.
- Expected solution mapping for ours: detect drift from incoming data, spawn/freeze LoRA branches when needed, route examples without relying on explicit task IDs, and penalize overlap between branches to reduce interference while preserving online deployability.

## Direct Citation Readiness

- Ready to cite directly after bibliographic cleanup: CITB Tables 1-2; O-LoRA Table 2 and Table 3; LB-CL Table 2; Progressive Prompts Tables 1-2; Continual-T0 headline retention claims and CT0 metrics; ToDCL official/paper NLG/E2E metrics; ARPER MultiWOZ NLG metrics.
- Needs exact PDF/table extraction before final paper: full MIGU Table 2 rows beyond the snippets above; exact ToDCL paper table values if using the paper PDF rather than the official repo table; TRACE acceptance status.
- Not suitable as mandatory published baseline: TRACE unless archival acceptance is verified; arXiv-only 2025 methods found during search; standalone Sequential LoRA.
