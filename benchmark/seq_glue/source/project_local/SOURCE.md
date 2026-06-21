# Seq-GLUE Project-Local Source

No standalone official Seq-GLUE-only repository was verified. This directory adds the project-local 8-task Seq-GLUE stream, conversion scripts, and published-setting configs from `/root/autodl-tmp/Lora-code` commit `d711d912926c58c13acc02b3c3e4cfddd9f2c969`. The GLUE benchmark source remains https://gluebenchmark.com/.

The stream order is `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`. Treat this as a project-local published-setting reconstruction from GLUE/SuperGLUE-style tasks, not an independent official Seq-GLUE repository. See `../../REPRODUCIBILITY.md`.
