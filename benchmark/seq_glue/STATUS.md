# Seq-GLUE

Status: project-local Seq-GLUE stream/configs/scripts are vendored in `source/project_local/`; no standalone official Seq-GLUE-only repository was verified.

Official GLUE source: https://gluebenchmark.com/

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree at vendoring time.

Project-local stream: `seqglue_cl_tasks_train50_eval10.json` with sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa. Candidate external contexts include method-specific repositories such as LFPT5, Progressive Prompts, TRACE, and general continual-learning frameworks, but no single strict official Seq-GLUE source was verified here.

See `docs/source_manifest.md`.
