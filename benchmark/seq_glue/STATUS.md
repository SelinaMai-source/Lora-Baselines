# Seq-GLUE

Status: no standalone official Seq-GLUE-only repository was verified. A project-local 8-task stream, conversion scripts, and published-setting configs are vendored in `source/project_local_seqglue/`.

The local stream is `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`, stored as `seqglue_cl_tasks_train50_eval10.json`. Candidate external contexts include method-specific repositories such as LFPT5, Progressive Prompts, TRACE, and general continual-learning frameworks, but no single strict official Seq-GLUE source was verified here.

See `docs/source_manifest.md`.
