# Replay LoRA

Official code status: closest reproducible code; no standalone official Replay LoRA repository was verified.

Paper route A: "Combining replay and LoRA for continual learning in natural language understanding". Web search found bibliographic pages but no author-maintained code repository; paper/code links need manual verification.

Paper route B: "Unlocking Continual Learning Abilities in Language Models" (Findings of EMNLP 2024).

- Paper URL: https://aclanthology.org/2024.findings-emnlp.379/
- Software ZIP URL: https://aclanthology.org/attachments/2024.findings-emnlp.379.software.zip
- ACL software source path: `source/acl_software_unlocking_cl/`.

Project-local replay implementation: `source/project_local/baselines/basic_baselines/replay_lora/method.py`.

Official O-LoRA reference source: https://github.com/cmnfriend/O-LoRA

Official O-LoRA reference commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`

Implemented mechanisms:

- Sequential LoRA baseline plus a bounded past-task replay buffer.
- Current-task training mixed with sampled previous-task examples; the current task is added to the buffer only after its training finishes.
- Published replay configs use `replay_ratio: 0.02`, matching the ACL software route description of 2% past-task data.
- Optional MIGU-style magnitude threshold gradient mask is available through `migu.enabled` and `migu.threshold`.

Smoke validation imported and instantiated `ReplayLoRAMethod`; first segment used `0` replay examples, second segment used replay examples from the completed first segment, and the buffer grew to include both segments.

Do not claim the ACL ZIP or project-local code is official code for the separate "Combining replay and LoRA" paper.

See `REPRODUCIBILITY.md` for closest reproducible code and paper-adaptation rules.
Implementation status: implemented in `source/project_local/baselines/basic_baselines/replay_lora/method.py` with a bounded replay buffer and current+past example mixing. ACL software source remains vendored for the MIGU/LoRA Replay paper route.

Smoke validation: `python docs/smoke_implemented_methods.py` passed; replay buffer grew across two synthetic segments and mixed replay examples during second-segment training.
