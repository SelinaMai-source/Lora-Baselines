from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from core.data import Example, Segment


@dataclass
class ReplayItem:
    instruction: str
    input_text: str
    target: str
    segment_id: int


class ReplayLoRAMethod:
    """
    Baseline B: Replay LoRA

    - Single LoRA branch, matching Sequential LoRA.
    - Maintain a past-task replay buffer across segments.
    - Train each new segment with current samples plus sampled past-task samples.
    - Optionally apply a MIGU-style magnitude threshold mask to LoRA gradients.
    """

    name = "replay_lora"

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        replay_cfg = cfg.get("replay", {})
        self.enabled = bool(replay_cfg.get("enabled", True))
        self.buffer_size = int(replay_cfg.get("buffer_size", 256))
        self.replay_ratio = float(replay_cfg.get("replay_ratio", 0.02))
        self.strategy = str(replay_cfg.get("strategy", "uniform"))
        self.seed = int(cfg.get("seed", replay_cfg.get("seed", 0)))
        self._rng = random.Random(self.seed)
        migu_cfg = cfg.get("migu", {}) if isinstance(cfg.get("migu", {}), dict) else {}
        self.migu_enabled = bool(migu_cfg.get("enabled", False))
        self.migu_threshold = float(migu_cfg.get("threshold", migu_cfg.get("ini_threshold", 0.5)))
        self._buffer: List[ReplayItem] = []

    def on_segment_start(self, *, segment: Segment, model: Any, lora: Any) -> Dict[str, Any]:
        if hasattr(lora, "set_soft_routing"):
            lora.set_soft_routing(None, None)
        if "default" in lora.list_adapters():
            lora.set_active_adapter("default")
        return {
            "active_adapter": lora.get_active_adapter_name(),
            "replay_enabled": self.enabled,
            "replay_buffer_size": len(self._buffer),
            "replay_ratio": self.replay_ratio,
            "migu_enabled": self.migu_enabled,
            "migu_threshold": self.migu_threshold,
        }

    def train_on_segment(
        self,
        *,
        segment: Segment,
        model: Any,
        lora: Any,
        lr: float,
        epochs: int,
        batch_size: int,
    ) -> Dict[str, Any]:
        current_pairs, current_targets = _to_pairs(segment.train)

        metrics: Dict[str, Any] = {"batches": 0, "mean_batch_acc": 0.0}
        batch_accs = []
        batch_losses = []
        grad_norms = []
        replay_examples_used = 0
        migu_masked_parameters = 0
        migu_total_parameters = 0

        for _ in range(max(1, epochs)):
            # Mix current-task samples with samples from previous tasks only.
            mix_pairs, mix_targets = self._mix_current_and_replay(current_pairs, current_targets)
            replay_examples_used += max(0, len(mix_pairs) - len(current_pairs))
            for b_pairs, b_targets in _batch(mix_pairs, mix_targets, batch_size):
                out = model.fit_batch(b_pairs, b_targets, lr=lr)
                mask_stats = self._apply_migu_gradient_mask(lora)
                step_stats = lora.step_adapter()
                batch_accs.append(float(out.get("train_batch_acc", 0.0)))
                batch_losses.append(float(out.get("train_loss", 0.0)))
                grad_norms.append(float(step_stats.get("grad_norm", 0.0)))
                migu_masked_parameters += int(mask_stats.get("masked_parameters", 0))
                migu_total_parameters += int(mask_stats.get("total_parameters", 0))
                metrics["batches"] += 1

        self._add_to_buffer(current_pairs, current_targets, segment_id=segment.segment_id)
        metrics["mean_batch_acc"] = sum(batch_accs) / max(1, len(batch_accs))
        metrics["train.loss"] = sum(batch_losses) / max(1, len(batch_losses))
        metrics["grad_norm"] = sum(grad_norms) / max(1, len(grad_norms))
        metrics["active_adapter"] = lora.get_active_adapter_name()
        metrics["replay_buffer_size"] = len(self._buffer)
        metrics["replay_examples_used"] = int(replay_examples_used)
        metrics["replay_ratio"] = float(self.replay_ratio if self.enabled else 0.0)
        metrics["replay_strategy"] = self.strategy
        metrics["migu_enabled"] = self.migu_enabled
        metrics["migu_masked_parameters"] = int(migu_masked_parameters)
        metrics["migu_total_parameters"] = int(migu_total_parameters)
        metrics["migu_mask_fraction"] = (
            float(migu_masked_parameters) / float(migu_total_parameters) if migu_total_parameters > 0 else 0.0
        )
        return metrics

    def _add_to_buffer(self, pairs: List[Tuple[str, str]], targets: List[str], *, segment_id: int) -> None:
        for (instruction, input_text), y in zip(pairs, targets):
            self._buffer.append(
                ReplayItem(instruction=instruction, input_text=input_text, target=y, segment_id=int(segment_id))
            )
        # keep buffer size
        if len(self._buffer) > self.buffer_size:
            overflow = len(self._buffer) - self.buffer_size
            # simple policy: drop oldest
            self._buffer = self._buffer[overflow:]

    def _mix_current_and_replay(
        self, pairs: List[Tuple[str, str]], targets: List[str]
    ) -> Tuple[List[Tuple[str, str]], List[str]]:
        if not self.enabled or not self._buffer or self.replay_ratio <= 0:
            return pairs, targets

        num_replay = int(round(len(pairs) * self.replay_ratio))
        num_replay = max(0, min(num_replay, len(self._buffer)))

        if num_replay == 0:
            return pairs, targets

        replay_items = self._sample_replay_items(num_replay)
        replay_pairs = [(it.instruction, it.input_text) for it in replay_items]
        replay_targets = [it.target for it in replay_items]

        mixed_pairs = pairs + replay_pairs
        mixed_targets = targets + replay_targets
        return mixed_pairs, mixed_targets

    def _sample_replay_items(self, count: int) -> List[ReplayItem]:
        if self.strategy == "oldest":
            return list(self._buffer[:count])
        if self.strategy == "recent":
            return list(self._buffer[-count:])
        return self._rng.sample(self._buffer, k=count)

    def _apply_migu_gradient_mask(self, lora: Any) -> Dict[str, Any]:
        if not self.migu_enabled:
            return {"enabled": False, "masked_parameters": 0, "total_parameters": 0}
        torch = _optional_torch()
        peft_model = getattr(lora, "peft_model", None)
        if torch is None or peft_model is None or not hasattr(peft_model, "named_parameters"):
            return {"enabled": True, "masked_parameters": 0, "total_parameters": 0, "reason": "no_peft_gradients"}

        active = lora.get_active_adapter_name() if hasattr(lora, "get_active_adapter_name") else "default"
        masked = 0
        total = 0
        threshold = min(max(float(self.migu_threshold), 0.0), 1.0)
        with torch.no_grad():
            for param_name, param in peft_model.named_parameters():
                is_active_lora = f"lora_A.{active}." in param_name or f"lora_B.{active}." in param_name
                if not is_active_lora or param.grad is None:
                    continue
                grad_abs = param.grad.detach().abs().float()
                if grad_abs.numel() == 0:
                    continue
                cutoff = torch.quantile(grad_abs.reshape(-1), threshold)
                mask = (grad_abs > cutoff).to(param.grad.dtype)
                param.grad.mul_(mask)
                masked += int(mask.numel() - int(mask.sum().item()))
                total += int(mask.numel())
        return {
            "enabled": True,
            "masked_parameters": int(masked),
            "total_parameters": int(total),
            "threshold": float(threshold),
        }


def _to_pairs(examples: List[Example]) -> Tuple[List[Tuple[str, str]], List[str]]:
    pairs: List[Tuple[str, str]] = []
    targets: List[str] = []
    for ex in examples:
        pairs.append((ex.instruction, ex.input))
        targets.append(ex.output)
    return pairs, targets


def _batch(pairs: List[Tuple[str, str]], targets: List[str], batch_size: int):
    bs = max(1, int(batch_size))
    for i in range(0, len(pairs), bs):
        yield pairs[i : i + bs], targets[i : i + bs]


def _optional_torch() -> Optional[Any]:
    try:
        import torch
    except Exception:
        return None
    return torch

