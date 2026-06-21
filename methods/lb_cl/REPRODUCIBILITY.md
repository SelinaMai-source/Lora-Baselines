# LB-CL Reproducibility Notes

## Official Code Status

- Official code status: no official verified.
- Paper: "Learn more, but bother less: parameter efficient continual learning".
- Paper URLs:
  - https://openreview.net/forum?id=ZxtaNh5UYB
  - https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf
- Closest reproducible source path: `methods/lb_cl/source/project_local`.
- Closest external reproducible base: `methods/o_lora/source`.
- Base code used: O-LoRA official GitHub, commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.

## Source Relationship

No public author-maintained LB-CL experiment repository has been verified in this package. The files under `source/project_local` are a project-local implementation of the paper mechanism on the local O-LoRA-style training loop and must not be described as official LB-CL author code.

The closest reproducible path is an adaptation from O-LoRA, because the LB-CL paper explicitly compares against O-LoRA and keeps the orthogonal-subspace continual-learning setting while adding a knowledge-transfer stage.

## Implemented Paper Mechanism

The project-local method class now implements the paper-specific changes on top of the closest available O-LoRA-style code:

- Replaces plain per-task LoRA initialization with `LBCLMethod.on_segment_start`, which creates a new adapter and injects cached prior-task knowledge.
- Decomposes previous task low-rank parameters with SVD in `extract_sensitive_svd_triplets` and computes sensitivity scores for triplet selection.
- Uses the sensitivity metric in `inject_svd_triplets_into_adapter` to select and inject prior-task parametric knowledge into new low-rank parameters.
- Preserves the O-LoRA-style orthogonal-subspace training constraint by calling `project_active_adapter_gradients` after backward and before the adapter step.
- Keep the continual task stream, model, LoRA rank, optimizer, and evaluation protocol aligned with the paper setting being reproduced.

Smoke validation imported and instantiated the method with a synthetic LoRA wrapper, cached first-task triplets, injected one selected triplet into the second adapter, and called the projection hook. This does not certify bitwise equivalence to an unreleased official implementation.
