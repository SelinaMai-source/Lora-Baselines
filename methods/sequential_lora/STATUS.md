# Sequential LoRA

Official code status: closest reproducible code; no separate official Sequential LoRA repository was verified.

Role: baseline protocol rather than an independent method paper in this package.

Closest reproducible sources:

- Project-local baseline/config view: `source/project_local/`.
- Official O-LoRA continual-learning reference: `../o_lora/source`.

Official O-LoRA reference source: https://github.com/cmnfriend/O-LoRA

Official O-LoRA reference commit: `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`

Project-local source commit: `d711d912926c58c13acc02b3c3e4cfddd9f2c969`

Required baseline settings are documented in `REPRODUCIBILITY.md`: sequential adapter training with no replay, orthogonal projection, LB-CL knowledge injection, MIGU mask, or other extra continual-learning mechanisms.

See `REPRODUCIBILITY.md` for closest reproducible code and paper-adaptation rules.
