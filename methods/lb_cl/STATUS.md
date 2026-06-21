# LB-CL

Official code status: no official verified.

Paper: "Learn more, but bother less: parameter efficient continual learning".

Paper/source pages checked include OpenReview https://openreview.net/forum?id=ZxtaNh5UYB, NeurIPS https://neurips.cc/virtual/2024/poster/94599, and the NeurIPS proceedings PDF https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf.

Implemented source: `source/project_local/baselines/advanced_baselines/lb_cl/method.py` plus O-LoRA official source at `../o_lora/source`.

Base code used: O-LoRA official GitHub commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.

Project-local source: `/root/autodl-tmp/Lora-code` at `d711d912926c58c13acc02b3c3e4cfddd9f2c969`; dirty status recorded in `docs/source_manifest.md`.

Implemented mechanisms:

- SVD-triplet extraction from previous LoRA adapters with singular-value sensitivity scoring.
- Previous-task knowledge cache and top-triplet injection into newly created low-rank adapter parameters.
- O-LoRA-style orthogonal-subspace training through the existing `project_active_adapter_gradients` hook.
- Task-specific adapter creation/freezing via `LBCLMethod.on_segment_start`.

Smoke validation:

- Synthetic import/instantiate/train smoke passed.
- Second task reported `lbcl_injection.injected_triplets=1` and `gradient_projection_hook_calls=1`.

Do not claim this is strict official LB-CL paper code unless later verified against an author release or project-owner equivalence review.
Implementation status: implemented in `source/project_local/baselines/advanced_baselines/lb_cl/method.py` with SVD-triplet sensitivity extraction, prior-task knowledge injection, and O-LoRA-style gradient projection hook.

Smoke validation: `python docs/smoke_implemented_methods.py` passed; LB-CL recorded 2 SVD triplets, injected prior knowledge on the second segment, and called the projection hook.
