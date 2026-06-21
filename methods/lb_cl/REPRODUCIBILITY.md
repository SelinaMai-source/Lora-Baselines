# LB-CL Reproducibility Notes

Official external code status: no public author code repository was verified.

Paper source: Learn more, but bother less: parameter efficient continual learning.

Closest reproducible base: O-LoRA official code at `methods/o_lora/source` plus the project-local LB-CL scaffold/configs at `methods/lb_cl/source/project_local`.

Required adaptation from the paper:

- Start from the O-LoRA continual LoRA training/evaluation pipeline and keep the same benchmark streams and order-specific scripts where applicable.
- Replace the plain sequential/O-LoRA adapter update with the LB-CL project-local SVD/projection scaffold in `baselines/advanced_baselines/lb_cl/method.py`.
- Use the published-setting configs under `methods/lb_cl/source/project_local/configs/paper/published_setting`.
- Treat this as closest reproducible code, not official LB-CL paper code, until an author repository or project-owner equivalence review confirms it.
