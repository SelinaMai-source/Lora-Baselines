# Seq-GLUE Reproducibility Notes

## Official Code Status

- Official code status: project-local benchmark stream; no standalone official Seq-GLUE-only repository verified.
- Official GLUE source: https://gluebenchmark.com/
- Closest reproducible source path: `benchmark/seq_glue/source/project_local`.
- Stream order: `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`.
- Source type: project-local published-setting benchmark construction, not an independent official Seq-GLUE repository.

## Source Relationship

Seq-GLUE here is a continual-learning stream assembled from GLUE/SuperGLUE-style tasks and local published-setting configs. The GLUE benchmark is the official task source, while the exact eight-task stream is a project-local reconstruction aligned with the published setting used by this package and continual-learning papers that adopt this order.

Do not cite this directory as an official Seq-GLUE repository. Cite the original task sources and the paper/project setting that defines the stream order.

## Required Construction Steps

To reproduce this benchmark stream:

- Use the GLUE/SuperGLUE task definitions for the underlying datasets.
- Construct the task sequence in this exact order: `sst2`, `mrpc`, `rte`, `cola`, `boolq`, `wic`, `cb`, `copa`.
- Keep the same train/eval sampling policy as the project-local stream file, currently `seqglue_cl_tasks_train50_eval10.json`.
- Keep label verbalization, prompt/instruction formatting, and metric mapping consistent across methods.
- Report that the stream is project-local or paper-setting-derived unless a later independent official Seq-GLUE source is verified.
