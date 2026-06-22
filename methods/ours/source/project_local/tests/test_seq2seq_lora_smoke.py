from __future__ import annotations

from pathlib import Path
import sys


PROJECT_LOCAL = Path(__file__).resolve().parents[1]
if str(PROJECT_LOCAL) not in sys.path:
    sys.path.insert(0, str(PROJECT_LOCAL))


def test_t5_small_seq2seq_lora_one_batch() -> None:
    from core.models.base_model import build_backbone
    from core.models.lora_wrapper import build_lora_wrapper

    model_path = Path("/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt")
    if not model_path.is_dir():
        raise AssertionError(f"Missing local smoke-test model: {model_path}")

    backbone = build_backbone(
        {
            "architecture": "seq2seq_lm",
            "hf_model_name_or_path": str(model_path),
            "device": "cpu",
            "torch_dtype": "float32",
            "max_source_len": 64,
            "max_target_len": 16,
            "gen_max_new_tokens": 8,
        },
        mode="ours",
        seed=7,
    )
    lora = build_lora_wrapper(
        backbone,
        {
            "enabled": True,
            "r": 2,
            "alpha": 4,
            "dropout": 0.0,
            "target_modules": ["q", "v"],
        },
    )
    out = backbone.fit_batch([("Translate English to German.", "hello")], ["hallo"], lr=1e-4)
    step = lora.step_adapter()
    pred = backbone.generate(["Translate English to German.\n\nInput:\nhello"], max_new_tokens=4)

    assert out["num_supervised_tokens"] > 0
    assert "SEQ_2_SEQ_LM" in str(lora.info().get("peft_task_type", ""))
    assert isinstance(step["grad_norm"], float)
    assert len(pred) == 1
