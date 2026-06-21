# Replay LoRA Reproducibility Notes

## Official Code Status

- Official code status: closest reproducible code; no standalone official Replay LoRA repository verified.
- Paper path A: "Combining replay and LoRA for continual learning in natural language understanding".
  - Verified paper/code URL: needs manual verification. Web search found bibliographic pages but no author-maintained code repository.
- Paper path B: "Unlocking Continual Learning Abilities in Language Models".
  - Paper URL: https://aclanthology.org/2024.findings-emnlp.379/
  - PDF URL: https://aclanthology.org/2024.findings-emnlp.379.pdf
  - ACL Software ZIP URL: https://aclanthology.org/attachments/2024.findings-emnlp.379.software.zip
  - Local source path: `methods/replay_lora/source/acl_software_unlocking_cl`.
- Project-local source path: `methods/replay_lora/source/project_local`.
- O-LoRA base source path: `methods/o_lora/source`.
- Base code used: O-LoRA official GitHub, commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.

## Source Relationship

This package records two reproducibility routes:

- Route A is the Replay LoRA paper route. No official author code has been verified, so only the paper identity is documented here pending manual source verification.
- Route B is the ACL Software ZIP for "Unlocking Continual Learning Abilities in Language Models". That paper includes LoRA Replay and LoRA Replay + MIGU baselines, and its appendix states that the T5 continual-learning experiments are adapted from O-LoRA. The ZIP is a reproducible software source for that paper's LoRA Replay baseline, not an official repository for "Combining replay and LoRA".

The extracted ACL package contains a `MIGU/` code tree with O-LoRA-derived imports under `src/olora`, continual-learning task configs, and scripts for LoRA/O-LoRA/MIGU-style runs. It should be cited as ACL software source when used.

## Required Paper Modifications

The project-local Replay LoRA baseline implements the closest available replay route as follows:

- Starts from sequential LoRA/O-LoRA training for the target model and task stream.
- Adds an experience replay buffer containing completed past-task examples.
- Mixes current-task data with replayed past-task samples in `ReplayLoRAMethod._mix_current_and_replay`. The ACL paper describes LoRAReplay as training new tasks on LoRA while mixing 2% past-task data, and the published replay configs now set `replay_ratio: 0.02`.
- Keep LoRA hyperparameters, task order, replay ratio, seed count, and evaluation cadence aligned with the paper being reproduced.
- If reproducing LoRA Replay + MIGU from the ACL paper, enable the optional MIGU-style magnitude threshold gradient mask with `migu.enabled: true` and `migu.threshold`.

Smoke validation imported and instantiated `ReplayLoRAMethod`, verified that the first task had no replay data, and verified that the second task mixed replay examples from the first completed task.

Do not label the project-local or ACL ZIP code as official code for "Combining replay and LoRA" unless a later author source verifies that relationship.
