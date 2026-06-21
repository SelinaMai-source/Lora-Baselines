# LB-CL

Official code status: no official verified.

Paper: "Learn more, but bother less: parameter efficient continual learning".

Paper/source pages checked include OpenReview https://openreview.net/forum?id=ZxtaNh5UYB, NeurIPS https://neurips.cc/virtual/2024/poster/94599, and the NeurIPS proceedings PDF https://proceedings.neurips.cc/paper_files/paper/2024/file/b0bc711f48724237b38823c4d9cee10b-Paper-Conference.pdf.

Closest reproducible source: `source/project_local/` plus O-LoRA official source at `../o_lora/source`.

Base code used: O-LoRA official GitHub commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.

Project-local source: `/root/autodl-tmp/Lora-code` at `d711d912926c58c13acc02b3c3e4cfddd9f2c969`; dirty status recorded in `docs/source_manifest.md`.

Required paper modifications are documented in `REPRODUCIBILITY.md`: implement LB-CL's SVD-triplet sensitivity scoring, prior-task knowledge extraction/injection, and orthogonal-subspace training on top of the O-LoRA-style baseline.

Do not claim this is strict official LB-CL paper code unless later verified against an author release or project-owner equivalence review.
