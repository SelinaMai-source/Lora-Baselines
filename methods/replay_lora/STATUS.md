# Replay LoRA

Official code status: closest reproducible code; no standalone official Replay LoRA repository was verified.

Paper route A: "Combining replay and LoRA for continual learning in natural language understanding". Web search found bibliographic pages but no author-maintained code repository; paper/code links need manual verification.

Paper route B: "Unlocking Continual Learning Abilities in Language Models" (Findings of EMNLP 2024).

- Paper URL: https://aclanthology.org/2024.findings-emnlp.379/
- Software ZIP URL: https://aclanthology.org/attachments/2024.findings-emnlp.379.software.zip
- ACL software source path: `source/acl_software_unlocking_cl/`.

Project-local replay source: `source/project_local/`.

Official O-LoRA reference source: https://github.com/cmnfriend/O-LoRA

Official O-LoRA reference commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`

Required replay modifications are documented in `REPRODUCIBILITY.md`: add a past-task replay buffer to sequential LoRA/O-LoRA training and use the replay ratio, task order, and evaluation protocol from the paper being reproduced. The ACL paper describes LoRAReplay as mixing 2% past-task data.

Do not claim the ACL ZIP or project-local code is official code for the separate "Combining replay and LoRA" paper.

See `REPRODUCIBILITY.md` for closest reproducible code and paper-adaptation rules.
