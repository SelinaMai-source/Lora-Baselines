# Sequential LoRA

Official code status: closest reproducible code; no separate official Sequential LoRA repository was verified.

Role: baseline protocol rather than an independent method paper in this package.

Implemented sources:

- Project-local method class/config view: `source/project_local/baselines/basic_baselines/sequential_lora/method.py`.
- Official O-LoRA continual-learning reference: `../o_lora/source`.

Official O-LoRA reference source: https://github.com/cmnfriend/O-LoRA

Official O-LoRA reference commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`

Implemented baseline settings:

- Reuses the single `default` LoRA adapter across segments.
- Calls only `model.fit_batch` and `lora.step_adapter` in sequence.
- Explicitly disables/avoids replay, orthogonal projection, LB-CL injection, MIGU masking, router, and prompt modules.

Smoke validation imported and instantiated `SequentialLoRAMethod`; synthetic training reported `replay_examples_used=0`, `projection_applied_calls=0`, `lbcl_injected_triplets=0`, and `migu_masked_parameters=0`.

See `REPRODUCIBILITY.md` for closest reproducible code and paper-adaptation rules.
Implementation status: implemented in `source/project_local/baselines/basic_baselines/sequential_lora/method.py` as plain sequential LoRA training on the default adapter.

Smoke validation: `python docs/smoke_implemented_methods.py` passed; the baseline trained two synthetic batches on the default adapter with no replay or extra mechanisms.
