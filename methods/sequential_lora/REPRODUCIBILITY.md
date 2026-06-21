# Sequential LoRA Reproducibility Notes

Official external code status: no separate Sequential LoRA-only official repository was verified.

Closest reproducible base: O-LoRA official code at `methods/o_lora/source` and the project-local baseline at `methods/sequential_lora/source/project_local`.

Required adaptation:

- Train LoRA adapters sequentially on the benchmark stream.
- Do not enable replay memory, orthogonal constraints, LB-CL projection, routing, or prompt-specific modules.
- Keep the benchmark order and hyperparameters from the paper/code that reports the Sequential LoRA baseline, especially O-LoRA baseline scripts/configs and the project-local published-setting configs.
- Report this as a baseline implementation derived from the closest reproducible source, not as an independent official method repository.
