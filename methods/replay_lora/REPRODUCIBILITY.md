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

To reproduce a Replay LoRA baseline from the closest available code:

- Start from sequential LoRA/O-LoRA training for the target model and task stream.
- Add an experience replay buffer containing past-task examples.
- Mix current-task data with replayed past-task samples according to the cited paper setting. The ACL paper describes LoRAReplay as training new tasks on LoRA while mixing 2% past-task data.
- Keep LoRA hyperparameters, task order, replay ratio, seed count, and evaluation cadence aligned with the paper being reproduced.
- If reproducing LoRA Replay + MIGU from the ACL paper, additionally apply MIGU's magnitude-based gradient update mask and threshold settings from that paper.

Do not label the project-local or ACL ZIP code as official code for "Combining replay and LoRA" unless a later author source verifies that relationship.
