# Seq-GLUE Reproducibility Notes

Official external code status: no standalone Seq-GLUE-only official repository was verified.

Official base benchmark: GLUE, https://gluebenchmark.com/.

Closest reproducible source: project-local stream/configs/scripts at `benchmark/seq_glue/source/project_local`.

Stream used in this repo:

`sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`

Required adaptation:

- Construct the continual benchmark stream from GLUE/SuperGLUE-style tasks using the project-local processed stream `seqglue_cl_tasks_train50_eval10.json`.
- Keep the task order and train/eval split sizes used in the project-local published-setting configs.
- When reproducing a specific method paper, cross-check whether that paper uses the same GLUE task order before claiming strict comparability.
- Report this as a project-local Seq-GLUE construction over official GLUE tasks, not as a standalone official Seq-GLUE codebase.
