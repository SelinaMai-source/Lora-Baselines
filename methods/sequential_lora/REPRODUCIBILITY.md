# Sequential LoRA Reproducibility Notes

## Official Code Status

- Official code status: closest reproducible code; no standalone official Sequential LoRA repository verified.
- Paper status: Sequential LoRA is a baseline protocol, not a separate method paper in this package.
- Citing contexts: O-LoRA and other continual-learning papers use sequential LoRA-style baselines; IsCIL `seqlora` can be used as an additional implementation reference, but it is not vendored here.
- Closest reproducible source paths:
  - `methods/sequential_lora/source/project_local`
  - `methods/o_lora/source`
- Base code used: O-LoRA official GitHub, commit `07117e1fc4a5f5ad9308a815a42cee8f46502dc8`.

## Source Relationship

The project-local source implements the baseline protocol used by this package. O-LoRA provides the closest official continual-learning LoRA code base and can reproduce the same baseline protocol by disabling mechanisms beyond plain sequential LoRA training.

Do not describe this entry as an official Sequential LoRA release. It is a baseline reconstruction from public O-LoRA-style continual-learning code plus project-local configs.

## Required Baseline Settings

To reproduce the baseline:

- Train LoRA adapters sequentially over the task stream.
- Keep the same model, task order, LoRA rank, optimizer, epochs, and evaluation cadence as the paper or project setting being compared.
- Do not add replay buffers, orthogonal projection, LB-CL knowledge injection, MIGU gradient masking, adapter routing, or other continual-learning mechanisms.
- Evaluate after each task or at the final checkpoint according to the cited comparison protocol.

`source/project_local/baselines/basic_baselines/sequential_lora/method.py` enforces this by reusing the single `default` adapter and reporting zero replay/projection/injection/MIGU activity in training metrics. A synthetic smoke test imported and instantiated the method and verified those disabled-mechanism metrics.

Any result using additional mechanisms should be labeled with that method name rather than Sequential LoRA.
