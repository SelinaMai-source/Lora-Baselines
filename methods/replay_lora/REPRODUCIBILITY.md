# Replay LoRA Reproducibility Notes

Official external code status: no standalone author GitHub for `Combining Replay and LoRA` was verified.

Closest reproducible sources:

- O-LoRA official code at `methods/o_lora/source`.
- Project-local Replay LoRA baseline at `methods/replay_lora/source/project_local`.
- ACL Anthology software zip for `Unlocking Continual Learning Abilities in Language Models` at `methods/replay_lora/source/acl_software_unlocking_cl`.

ACL source:

- Paper: https://aclanthology.org/2024.findings-emnlp.379/
- Software: https://aclanthology.org/attachments/2024.findings-emnlp.379.software.zip
- The zip extracts to `MIGU/` and includes LoRA/LoRA Replay/MIGU-related continual-learning code and scripts.

Required adaptation:

- Use the O-LoRA continual T5/LoRA pipeline as the base when matching papers that describe their code as derived from O-LoRA.
- Add replay by mixing current-task data with a memory buffer of previous-task samples, matching the chosen paper's replay ratio, memory selection rule, and task order.
- For MIGU/Unlocking CL experiments, use the ACL software scripts/configs directly where possible, especially `scripts/t5_large/*`, `scripts/llama2/*`, and corresponding config folders.
- Do not label project-local replay code or the ACL MIGU zip as the official code for `Combining Replay and LoRA`; label them as closest reproducible sources.
