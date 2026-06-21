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

No public author-maintained LB-CL experiment repository has been verified in this package. The files under `source/project_local` are project-local scaffold/config material and must not be described as official LB-CL paper code.

The closest reproducible path is an adaptation from O-LoRA, because the LB-CL paper explicitly compares against O-LoRA and keeps the orthogonal-subspace continual-learning setting while adding a knowledge-transfer stage.

## Required Paper Modifications

To reproduce LB-CL from the closest available code, start from O-LoRA and implement the paper-specific changes:

- Replace plain per-task LoRA initialization with the LB-CL knowledge extraction and injection stage.
- Decompose previous task low-rank parameters with SVD and compute sensitivity scores for SVD triplets.
- Use the sensitivity metric to select/inject prior-task parametric knowledge into the new task low-rank parameters.
- Preserve the O-LoRA-style orthogonal-subspace training constraint for new tasks.
- Keep the continual task stream, model, LoRA rank, optimizer, and evaluation protocol aligned with the paper setting being reproduced.

This package records the adaptation recipe and project-local scaffold only; it does not certify equivalence to an unreleased official implementation.
