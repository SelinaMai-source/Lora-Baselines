# Seq-GLUE

Official code status: project-local benchmark stream; no standalone official Seq-GLUE-only repository was verified.

Official GLUE source: https://gluebenchmark.com/

Closest reproducible source: `source/project_local/`.

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree at vendoring time.

Project-local stream: `seqglue_cl_tasks_train50_eval10.json` with `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`.

The stream is a project-local published-setting reconstruction from GLUE/SuperGLUE-style tasks and CL papers that adopt this order. Do not describe it as an independent official Seq-GLUE repository.

See `REPRODUCIBILITY.md` and `docs/source_manifest.md`.

See `REPRODUCIBILITY.md` for closest reproducible code and paper-adaptation rules.
Implementation status: implemented as a validated project-local stream at `source/project_local/data/processed/seqglue_cl_tasks_train50_eval10.json`, with conversion scripts under `source/project_local/scripts/`.

Smoke validation: `python docs/smoke_implemented_methods.py` passed; stream order and 50 train / 10 eval examples per segment were verified.
