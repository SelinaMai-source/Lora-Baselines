# Lora-Baselines Source Manifest

This repository is organized for selected LoRA continual learning methods and benchmarks. Root-level ordinary files are intentionally avoided; all documentation and helper scripts live under `docs/`.

## Repository Layout Policy

- Root directories: `methods/`, `benchmark/`, `docs/`.
- No git submodules are used, because `.gitmodules` would add a root-level ordinary file.
- Official code should be vendored under each entry's `source/` directory after download, with the nested `.git` directory removed and the exact upstream commit recorded here.
- Experiment settings must follow the published paper or official code. Do not infer missing hyperparameters.

## Download Attempt Summary

Official GitHub sources were attempted from this environment on 2026-06-21. Both HTTPS and SSH clone attempts to GitHub official repositories timed out on `cmnfriend/O-LoRA`; GitHub API requests for commit resolution also timed out. Therefore, public official repositories are recorded but not vendored, except for local project-owner code found under `/root/autodl-tmp/Lora-code` for `Ours`.

Use `docs/download_official_sources.sh` in a network-stable environment to fetch vendor copies and write commit records.

## Methods

### Sequential LoRA

- Paper / source context: baseline in "Orthogonal Subspace Learning for Language Model Continual Learning".
- Paper URL: https://aclanthology.org/2023.findings-emnlp.715/
- Official code URL: https://github.com/cmnfriend/O-LoRA
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: O-LoRA official repository scripts, especially `scripts/order_*.sh`, plus the paper baseline definition for SeqLoRA.
- Data / model / dependency requirements: T5-large or LLaMA2 setup as required by O-LoRA; benchmark data from the O-LoRA repository or referenced datasets.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out. No separate official Sequential LoRA repository was verified; treat this as the O-LoRA paper baseline, not an independent method implementation.

### Replay LoRA

- Paper / source context: replay baseline in "Orthogonal Subspace Learning for Language Model Continual Learning"; exact LoRA-specific replay implementation was not verified as a separate official repository.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.715/
- Official code URL: https://github.com/cmnfriend/O-LoRA
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: O-LoRA official repository scripts and baseline sections; verify whether the official code implements replay with LoRA adapters or full-model replay before running.
- Data / model / dependency requirements: same as O-LoRA baseline environment.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out; separate official Replay LoRA source not verified.

### O-LoRA

- Paper title: Orthogonal Subspace Learning for Language Model Continual Learning.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.715/
- Official code URL: https://github.com/cmnfriend/O-LoRA
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: `scripts/order_*.sh` in the official repository.
- Data / model / dependency requirements: pretrained T5-large or LLaMA2 base model, official scripts, and task data referenced by the repository.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out.

### LB-CL

- Paper title: Learn More but Bother Less: Parameter Efficient Continual Learning.
- Paper URL: currently unresolved from a stable official source in this environment; search results referenced NeurIPS 2024 material but did not provide a verifiable official code repository.
- Official code URL: not verified.
- Commit / tag / release: not available.
- Original experiment configuration location: not available.
- Data / model / dependency requirements: not available without official source.
- Downloaded: no.
- Not downloaded reason: no public official code source was verified. Do not substitute non-official implementations without project-owner approval.

### Progressive Prompts

- Paper title: Progressive Prompts: Continual Learning for Language Models.
- Paper URL: https://openreview.net/forum?id=UJTgQBc91_
- Official code URL: https://github.com/arazd/ProgressivePrompts
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: official repository `T5_codebase/` and `BERT_codebase/`, especially training scripts such as `train_t5_cl.py` and `train_cl2.py`.
- Data / model / dependency requirements: datasets folder plus Hugging Face datasets and datasets linked from the paper; standard PyTorch and Transformers setup.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out.

### Continual-T0

- Paper title: Fine-tuned Language Models are Continual Learners.
- Paper URL: https://arxiv.org/abs/2205.12393
- Official code URL: https://github.com/ThomasScialom/T0_continual_learning
- Official model URL: https://huggingface.co/ThomasNLG/CT0-11B
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: official repository README points to a Colab notebook for dataset creation, rehearsal formatting, and evaluation; training hyperparameters are in the paper.
- Data / model / dependency requirements: Google Drive material linked by the official README, CT0/T0 checkpoints, and raw datasets; some raw datasets may have broken links.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out; model/data are large and partly Google Drive based.

### LFPT5

- Paper title: LFPT5: A Unified Framework for Lifelong Few-shot Language Learning Based on Prompt Tuning of T5.
- Paper URL: https://openreview.net/forum?id=HCRVf71PMF
- Official code URL: https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: official repository scripts and configuration files; project page documents LM-adapted T5 conversion.
- Data / model / dependency requirements: LM-adapted T5 checkpoint `t5.1.1.lm100k`, conversion to PyTorch checkpoint, task datasets, PyTorch.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out; model checkpoint is large and requires separate download/conversion.

### Ours

- Paper title: project-owner method, not a published external paper in this repository.
- Paper URL: source required from project owner.
- Official code URL: local source found at `/root/autodl-tmp/Lora-code`.
- Commit / tag / release: local git commit `d711d912926c58c13acc02b3c3e4cfddd9f2c969`; local tree was dirty, so copied files should be reviewed before publication.
- Original experiment configuration location: copied from local `configs/ours.yaml` and `configs/paper/published_setting/*__ours__s123*.yaml`.
- Data / model / dependency requirements: local configuration references `assets/pretrained/meta-llama/Llama-3.1-8B-Instruct` and processed benchmark streams under `data/processed`.
- Downloaded: yes, selected local source/config files only.
- Not downloaded reason: no external official source or paper URL was provided. Full local repository was not copied because it contains large logs, caches, archives, and unrelated dirty working-tree changes.

## Benchmarks

### InstrDialog

- Paper title: CITB: A Benchmark for Continual Instruction Tuning.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.633/
- Official code URL: https://github.com/hyintell/CITB
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: official repository `data/` and `scripts/data_scripts/`; InstrDialog stream consists of 19 dialogue-related tasks.
- Data / model / dependency requirements: Super-NaturalInstructions derived task data provided in CITB `data/`.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out.

### InstrDialog++

- Paper title: CITB: A Benchmark for Continual Instruction Tuning.
- Paper URL: https://aclanthology.org/2023.findings-emnlp.633/
- Official code URL: https://github.com/hyintell/CITB
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: official repository `data/` and `scripts/data_scripts/`; InstrDialog++ stream consists of InstrDialog plus 19 additional tasks.
- Data / model / dependency requirements: Super-NaturalInstructions derived task data provided in CITB `data/`.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out.

### TRACE

- Paper title: TRACE: A Comprehensive Benchmark for Continual Learning in Large Language Models.
- Paper URL: https://openreview.net/forum?id=3qa4YLkcEw
- Official code URL: https://github.com/BeyonderXX/TRACE
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: official repository scripts such as `scripts/train_seq_cl.sh` and `scripts/infer_seq.sh`.
- Data / model / dependency requirements: official TRACE data, including ScienceQA, FOMC, MeetingBank, C-STANCE, 20Minuten, Py150/CodeXGLUE, and NumGLUE-derived tasks; supplementary material references Google Drive distribution and original dataset links.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out; full datasets include Google Drive / upstream dataset downloads and may be large.

### MultiWOZ NLG

- Paper title: MultiWOZ - A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling.
- Paper URL: https://arxiv.org/abs/1810.00278
- Official dataset/code URL: https://github.com/budzianowski/multiwoz
- Evaluation code URL: https://github.com/Tomiinek/MultiWOZ_Evaluation
- Commit / tag / release: not resolved in this environment; GitHub access timed out.
- Original experiment configuration location: MultiWOZ repository `data/` and baseline code; context-to-response evaluation in `Tomiinek/MultiWOZ_Evaluation`.
- Data / model / dependency requirements: MultiWOZ 2.0/2.1/2.2 data depending on published setting; NLG evaluation requires standardized Inform, Success, BLEU scripts.
- Downloaded: no.
- Not downloaded reason: GitHub clone/API timed out.

### Seq-GLUE

- Paper / benchmark context: sequence of GLUE tasks used in continual learning papers; no single official Seq-GLUE-only repository was verified in this environment.
- Paper URL: GLUE benchmark paper https://openreview.net/forum?id=rJ4km2R5t7
- Official GLUE source URL: https://gluebenchmark.com/
- Candidate implementation sources: LFPT5 and Progressive Prompts official repositories include GLUE-style continual task usage; verify exact sequence against the target published paper before running.
- Commit / tag / release: not available.
- Original experiment configuration location: not verified as an official Seq-GLUE source.
- Data / model / dependency requirements: GLUE datasets, usually downloaded through Hugging Face datasets or official GLUE scripts depending on the paper.
- Downloaded: no.
- Not downloaded reason: no standalone official Seq-GLUE source was verified; do not infer sequence/order without a paper-specific source.
