# Seq-GLUE

Official code status: project-local benchmark stream; no standalone official Seq-GLUE-only repository was verified.

Official GLUE source: https://gluebenchmark.com/

Implemented source: `source/project_local/`.

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969` with dirty local working tree at vendoring time.

Project-local stream: `seqglue_cl_tasks_train50_eval10.json` with `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`.

Implemented benchmark entry points:

- `source/project_local/scripts/convert_seqglue_to_stream.py` converts raw GLUE/SuperGLUE-style JSON exports to the processed continual stream.
- `source/project_local/seq_glue_stream.py` provides `load_seq_glue_stream`, `validate_seq_glue_stream`, and a CLI validator.
- Published configs point at `seqglue_cl_tasks_train50_eval10.json` and can be used by the unified project-local training loop.

Smoke validation loaded the vendored processed stream and verified 8 segments, task order `sst2 -> mrpc -> rte -> cola -> boolq -> wic -> cb -> copa`, 400 train examples, and 80 eval examples.

The stream is a project-local published-setting reconstruction from GLUE/SuperGLUE-style tasks and CL papers that adopt this order. Do not describe it as an independent official Seq-GLUE repository.

See `REPRODUCIBILITY.md` and `docs/source_manifest.md`.

See `REPRODUCIBILITY.md` for closest reproducible code and paper-adaptation rules.
Implementation status: implemented as a validated project-local stream at `source/project_local/data/processed/seqglue_cl_tasks_train50_eval10.json`, with conversion scripts under `source/project_local/scripts/`.

Smoke validation: `python docs/smoke_implemented_methods.py` passed; stream order and 50 train / 10 eval examples per segment were verified.
