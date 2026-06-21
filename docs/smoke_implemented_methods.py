#!/usr/bin/env python3
"""Smoke tests for implemented non-official method mechanisms.

This script intentionally uses tiny synthetic segments. It verifies that the
vendored implementations are executable without launching full training.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, List, Tuple


REPO = Path(__file__).resolve().parents[1]
PROJECT_LOCAL = REPO / "methods" / "ours" / "source" / "project_local"
sys.path.insert(0, str(PROJECT_LOCAL))

from core.data import Example, Segment  # noqa: E402
from core.models.lora_wrapper import DebugLoRAWrapper, LoRAConfig  # noqa: E402


class TinyModel:
    def __init__(self) -> None:
        self.steps = 0

    def fit_batch(self, pairs: List[Tuple[str, str]], targets: List[str], *, lr: float) -> dict[str, Any]:
        self.steps += 1
        return {
            "train_batch_acc": 1.0 if pairs and targets else 0.0,
            "train_loss": 0.1,
            "train_answer_token_acc": 1.0,
            "num_total_tokens": len(pairs),
            "num_supervised_tokens": len(targets),
        }


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _segment(segment_id: int) -> Segment:
    return Segment(
        segment_id=segment_id,
        segment_name=f"toy_{segment_id}",
        train=[
            Example("classify", f"input-{segment_id}-a", "yes"),
            Example("classify", f"input-{segment_id}-b", "no"),
        ],
        eval=[Example("classify", f"eval-{segment_id}", "yes")],
    )


def _debug_lora() -> DebugLoRAWrapper:
    return DebugLoRAWrapper(LoRAConfig(enabled=True))


def smoke_sequential_lora() -> dict[str, Any]:
    module = _load_module(
        "smoke_sequential_lora",
        REPO / "methods/sequential_lora/source/project_local/baselines/basic_baselines/sequential_lora/method.py",
    )
    method = module.SequentialLoRAMethod({})
    lora = _debug_lora()
    model = TinyModel()
    start = method.on_segment_start(segment=_segment(0), model=model, lora=lora)
    metrics = method.train_on_segment(segment=_segment(0), model=model, lora=lora, lr=1e-3, epochs=1, batch_size=1)
    assert metrics["batches"] == 2
    assert start["active_adapter"] == "default"
    assert metrics["replay_examples_used"] == 0
    assert metrics["projection_applied_calls"] == 0
    assert metrics["lbcl_injected_triplets"] == 0
    assert metrics["migu_masked_parameters"] == 0
    return {
        "batches": metrics["batches"],
        "active_adapter": metrics["active_adapter"],
        "disabled_mechanism_metrics": {
            "replay_examples_used": metrics["replay_examples_used"],
            "projection_applied_calls": metrics["projection_applied_calls"],
            "lbcl_injected_triplets": metrics["lbcl_injected_triplets"],
            "migu_masked_parameters": metrics["migu_masked_parameters"],
        },
    }


def smoke_replay_lora() -> dict[str, Any]:
    module = _load_module(
        "smoke_replay_lora",
        REPO / "methods/replay_lora/source/project_local/baselines/basic_baselines/replay_lora/method.py",
    )
    method = module.ReplayLoRAMethod({"replay": {"buffer_size": 8, "replay_ratio": 0.5}})
    lora = _debug_lora()
    model = TinyModel()
    method.on_segment_start(segment=_segment(0), model=model, lora=lora)
    first = method.train_on_segment(segment=_segment(0), model=model, lora=lora, lr=1e-3, epochs=1, batch_size=2)
    method.on_segment_start(segment=_segment(1), model=model, lora=lora)
    second = method.train_on_segment(segment=_segment(1), model=model, lora=lora, lr=1e-3, epochs=1, batch_size=2)
    assert first["replay_buffer_size"] == 2
    assert first["replay_examples_used"] == 0
    assert second["replay_examples_used"] > 0
    assert second["replay_buffer_size"] == 4
    return {
        "first_replay_examples_used": first["replay_examples_used"],
        "second_replay_examples_used": second["replay_examples_used"],
        "buffer_after_second_segment": second["replay_buffer_size"],
        "batches": second["batches"],
    }


def smoke_lb_cl() -> dict[str, Any]:
    module = _load_module(
        "smoke_lb_cl",
        REPO / "methods/lb_cl/source/project_local/baselines/advanced_baselines/lb_cl/method.py",
    )
    method = module.LBCLMethod(
        {
            "advanced_baseline": {
                "lb_cl": {
                    "top_triplets": 2,
                    "inject_top_triplets": 2,
                    "injection_strength": 0.5,
                    "projection_strength": 1.0,
                }
            }
        }
    )
    lora = _debug_lora()
    model = TinyModel()
    method.on_segment_start(segment=_segment(0), model=model, lora=lora)
    first = method.train_on_segment(segment=_segment(0), model=model, lora=lora, lr=1e-3, epochs=1, batch_size=1)
    second_start = method.on_segment_start(segment=_segment(1), model=model, lora=lora)
    second = method.train_on_segment(segment=_segment(1), model=model, lora=lora, lr=1e-3, epochs=1, batch_size=1)
    assert first["svd_top_triplets_recorded"] > 0
    assert second_start["lbcl_injection.injected_triplets"] > 0
    assert second["cached_knowledge_segments"] == 2
    return {
        "first_triplets": first["svd_top_triplets_recorded"],
        "second_injected_triplets": second_start["lbcl_injection.injected_triplets"],
        "projection_calls": second["gradient_projection_hook_calls"],
    }


def smoke_seq_glue() -> dict[str, Any]:
    module = _load_module(
        "smoke_seq_glue_stream",
        REPO / "benchmark/seq_glue/source/project_local/seq_glue_stream.py",
    )
    stream = module.load_seq_glue_stream(validate=True)
    summary = module.validate_seq_glue_stream(stream)
    expected = ["glue_sst2", "glue_mrpc", "glue_rte", "glue_cola", "super_glue_boolq", "super_glue_wic", "super_glue_cb", "super_glue_copa"]
    actual = [seg.segment_name for seg in stream.stream]
    assert actual == expected, actual
    assert summary["train_examples"] == 400
    assert summary["eval_examples"] == 80
    return {"segments": len(actual), "order": actual, "train_examples": summary["train_examples"], "eval_examples": summary["eval_examples"]}


def main() -> None:
    results = {
        "sequential_lora": smoke_sequential_lora(),
        "replay_lora": smoke_replay_lora(),
        "lb_cl": smoke_lb_cl(),
        "seq_glue": smoke_seq_glue(),
    }
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
