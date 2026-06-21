from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from core.data import Example, Segment


@dataclass
class SVDTriplet:
    adapter: str
    param_name: str
    rank: int
    singular_value: float
    sensitivity: float
    left_vector: Any = None
    right_vector: Any = None


class LBCLMethod:
    """
    LB-CL / "Learn more, but bother less" baseline.

    The implementation follows the paper mechanism on top of the O-LoRA-style
    loop used by this package:
      - train one task-specific LoRA adapter per segment;
      - extract previous-task knowledge as sensitive SVD triplets;
      - inject selected previous triplets into the newly created adapter;
      - keep the orthogonal-subspace gradient projection hook during training.
    """

    name = "lb_cl"

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        method_cfg = _method_cfg(cfg, "lb_cl")
        self.adapter_prefix = str(method_cfg.get("adapter_prefix", "lbcl_s"))
        self.top_triplets = int(method_cfg.get("top_triplets", 8))
        self.inject_top_triplets = int(method_cfg.get("inject_top_triplets", self.top_triplets))
        self.sensitivity_power = float(method_cfg.get("sensitivity_power", 2.0))
        self.injection_strength = float(method_cfg.get("injection_strength", 0.5))
        self.projection_strength = float(method_cfg.get("projection_strength", 1.0))
        self.freeze_previous_adapters = bool(method_cfg.get("freeze_previous_adapters", True))
        self._adapter_names: List[str] = []
        self._knowledge_cache: List[Dict[str, Any]] = []

    def on_segment_start(self, *, segment: Segment, model: Any, lora: Any) -> Dict[str, Any]:
        adapter_name = f"{self.adapter_prefix}{segment.segment_id}"
        if adapter_name not in lora.list_adapters():
            lora.create_adapter(adapter_name)

        if self.freeze_previous_adapters:
            for old_adapter in self._adapter_names:
                if old_adapter in lora.list_adapters() and hasattr(lora, "freeze_adapter"):
                    lora.freeze_adapter(old_adapter)

        lora.set_active_adapter(adapter_name)
        if adapter_name not in self._adapter_names:
            self._adapter_names.append(adapter_name)

        injection_stats = self._inject_previous_knowledge(lora, adapter_name)
        return {
            "active_adapter": lora.get_active_adapter_name(),
            "num_adapters": len(self._adapter_names),
            "cached_knowledge_segments": len(self._knowledge_cache),
            "top_triplets": self.top_triplets,
            "inject_top_triplets": self.inject_top_triplets,
            "injection_strength": self.injection_strength,
            **_prefix_keys("lbcl_injection", injection_stats),
            "implementation_status": "svd_sensitivity_extraction_injection_and_olora_projection_enabled",
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
        pairs, targets = _to_pairs(segment.train)
        metrics: Dict[str, Any] = {"batches": 0, "mean_batch_acc": 0.0}
        batch_accs: List[float] = []
        batch_losses: List[float] = []
        projection_calls = 0
        projected_calls = 0

        for _ in range(max(1, epochs)):
            for b_pairs, b_targets in _batch(pairs, targets, batch_size):
                out = model.fit_batch(b_pairs, b_targets, lr=lr)
                projection_stats = self._project_gradients(lora)
                projection_calls += int(bool(projection_stats.get("hook_available", False)))
                projected_calls += int(bool(projection_stats.get("projected", False)))
                step_stats = lora.step_adapter()
                batch_accs.append(float(out.get("train_batch_acc", 0.0)))
                batch_losses.append(float(out.get("train_loss", 0.0)))
                metrics["batches"] += 1

        active_adapter = lora.get_active_adapter_name()
        triplets = extract_sensitive_svd_triplets(
            lora,
            active_adapter,
            top_k=self.top_triplets,
            sensitivity_power=self.sensitivity_power,
        )
        self._knowledge_cache.append(
            {
                "segment_id": segment.segment_id,
                "adapter": active_adapter,
                "triplets": triplets,
            }
        )
        metrics["mean_batch_acc"] = sum(batch_accs) / max(1, len(batch_accs))
        metrics["train.loss"] = sum(batch_losses) / max(1, len(batch_losses))
        metrics["active_adapter"] = active_adapter
        metrics["num_adapters"] = len(self._adapter_names)
        metrics["cached_knowledge_segments"] = len(self._knowledge_cache)
        metrics["svd_summary_num_matrices"] = len({t.param_name for t in triplets})
        metrics["svd_top_triplets_recorded"] = len(triplets)
        metrics["svd_max_sensitivity"] = max([t.sensitivity for t in triplets], default=0.0)
        metrics["gradient_projection_hook_calls"] = int(projection_calls)
        metrics["gradient_projection_applied_calls"] = int(projected_calls)
        metrics["projection_strength"] = self.projection_strength
        metrics["grad_norm"] = float(step_stats.get("grad_norm", 0.0)) if "step_stats" in locals() else 0.0
        metrics["implementation_status"] = "lbcl_svd_triplets_cached_for_future_injection"
        return metrics

    def _reference_adapters(self, active_adapter: str) -> List[str]:
        return [row["adapter"] for row in self._knowledge_cache if row.get("adapter") != active_adapter]

    def _project_gradients(self, lora: Any) -> Dict[str, Any]:
        if not hasattr(lora, "project_active_adapter_gradients"):
            return {"hook_available": False, "projected": False}
        active = lora.get_active_adapter_name()
        return lora.project_active_adapter_gradients(
            reference_adapters=self._reference_adapters(active),
            strength=self.projection_strength,
        )

    def _inject_previous_knowledge(self, lora: Any, active_adapter: str) -> Dict[str, Any]:
        previous_triplets = [
            triplet
            for row in self._knowledge_cache
            for triplet in row.get("triplets", [])
            if isinstance(triplet, SVDTriplet) and triplet.adapter != active_adapter
        ]
        return inject_svd_triplets_into_adapter(
            lora,
            active_adapter=active_adapter,
            triplets=previous_triplets,
            top_k=self.inject_top_triplets,
            strength=self.injection_strength,
        )


def extract_sensitive_svd_triplets(
    lora: Any,
    adapter_name: str,
    *,
    top_k: int = 8,
    sensitivity_power: float = 2.0,
) -> List[SVDTriplet]:
    """Extract LB-CL SVD triplets and score them by singular-value sensitivity."""
    torch = _optional_torch()
    if torch is None:
        return _extract_summary_triplets(lora, adapter_name, top_k=top_k, sensitivity_power=sensitivity_power)

    triplets: List[SVDTriplet] = []
    peft_model = getattr(lora, "peft_model", None)
    if peft_model is not None and hasattr(peft_model, "named_parameters"):
        with torch.no_grad():
            for param_name, param in peft_model.named_parameters():
                if f"lora_A.{adapter_name}." not in param_name and f"lora_B.{adapter_name}." not in param_name:
                    continue
                matrix = param.detach().float()
                if matrix.ndim != 2 or min(matrix.shape) == 0:
                    continue
                try:
                    u, s, vh = torch.linalg.svd(matrix, full_matrices=False)
                except RuntimeError:
                    continue
                limit = min(max(0, int(top_k)), int(s.numel()))
                for rank_idx in range(limit):
                    singular = float(s[rank_idx].item())
                    sensitivity = float(abs(singular) ** float(sensitivity_power))
                    triplets.append(
                        SVDTriplet(
                            adapter=adapter_name,
                            param_name=param_name,
                            rank=int(rank_idx),
                            singular_value=singular,
                            sensitivity=sensitivity,
                            left_vector=u[:, rank_idx].detach().cpu(),
                            right_vector=vh[rank_idx, :].detach().cpu(),
                        )
                    )
    elif hasattr(lora, "get_adapter_vector"):
        vec = lora.get_adapter_vector(adapter_name, detach=True).float()
        if int(vec.numel()) > 0:
            side = int(max(1, vec.numel() ** 0.5))
            matrix = vec[: side * side].reshape(side, side)
            u, s, vh = torch.linalg.svd(matrix, full_matrices=False)
            for rank_idx in range(min(max(0, int(top_k)), int(s.numel()))):
                singular = float(s[rank_idx].item())
                triplets.append(
                    SVDTriplet(
                        adapter=adapter_name,
                        param_name=f"debug_lora_vector.{adapter_name}",
                        rank=int(rank_idx),
                        singular_value=singular,
                        sensitivity=float(abs(singular) ** float(sensitivity_power)),
                        left_vector=u[:, rank_idx].detach().cpu(),
                        right_vector=vh[rank_idx, :].detach().cpu(),
                    )
                )

    triplets.sort(key=lambda row: row.sensitivity, reverse=True)
    return triplets[: max(0, int(top_k))]


def inject_svd_triplets_into_adapter(
    lora: Any,
    *,
    active_adapter: str,
    triplets: Iterable[SVDTriplet],
    top_k: int,
    strength: float,
) -> Dict[str, Any]:
    selected = sorted(
        [t for t in triplets if t.left_vector is not None and t.right_vector is not None],
        key=lambda row: row.sensitivity,
        reverse=True,
    )[: max(0, int(top_k))]
    if not selected or strength <= 0:
        return {"available_triplets": len(selected), "injected_triplets": 0, "injected_tensors": 0}

    torch = _optional_torch()
    if torch is None:
        return {"available_triplets": len(selected), "injected_triplets": 0, "injected_tensors": 0, "reason": "torch_unavailable"}

    peft_model = getattr(lora, "peft_model", None)
    if peft_model is not None and hasattr(peft_model, "named_parameters"):
        by_param: Dict[str, List[SVDTriplet]] = {}
        for triplet in selected:
            target_name = triplet.param_name.replace(f".{triplet.adapter}.", f".{active_adapter}.")
            by_param.setdefault(target_name, []).append(triplet)

        injected_triplets = 0
        injected_tensors = 0
        with torch.no_grad():
            for param_name, param in peft_model.named_parameters():
                current = by_param.get(param_name, [])
                if not current:
                    continue
                reconstruction = torch.zeros_like(param.detach().float())
                tensor_triplets = 0
                for triplet in current:
                    left = triplet.left_vector.to(device=param.device, dtype=torch.float32)
                    right = triplet.right_vector.to(device=param.device, dtype=torch.float32)
                    contribution = float(triplet.singular_value) * torch.outer(left, right)
                    if tuple(contribution.shape) != tuple(reconstruction.shape):
                        continue
                    reconstruction.add_(contribution)
                    tensor_triplets += 1
                    injected_triplets += 1
                if tensor_triplets:
                    param.data.mul_(1.0 - float(strength)).add_(reconstruction.to(param.dtype), alpha=float(strength))
                    injected_tensors += 1
        return {
            "available_triplets": len(selected),
            "injected_triplets": int(injected_triplets),
            "injected_tensors": int(injected_tensors),
        }

    if hasattr(lora, "_adapter_vectors") and active_adapter in getattr(lora, "_adapter_vectors", {}):
        source = selected[0]
        if source.adapter in lora._adapter_vectors:
            with torch.no_grad():
                lora._adapter_vectors[active_adapter] = (
                    (1.0 - float(strength)) * lora._adapter_vectors[active_adapter]
                    + float(strength) * lora._adapter_vectors[source.adapter]
                )
            return {"available_triplets": len(selected), "injected_triplets": 1, "injected_tensors": 1}

    return {"available_triplets": len(selected), "injected_triplets": 0, "injected_tensors": 0, "reason": "no_mutable_lora_weights"}


def _extract_summary_triplets(
    lora: Any,
    adapter_name: str,
    *,
    top_k: int,
    sensitivity_power: float,
) -> List[SVDTriplet]:
    if not hasattr(lora, "summarize_adapter_svd"):
        return []
    summary = lora.summarize_adapter_svd(adapter_name, top_k=top_k)
    rows = summary.get("top_triplets", []) if isinstance(summary, dict) else []
    triplets: List[SVDTriplet] = []
    for row in rows:
        singular = float(row.get("singular_value", 0.0))
        triplets.append(
            SVDTriplet(
                adapter=adapter_name,
                param_name=str(row.get("param_name", "")),
                rank=int(row.get("rank", 0)),
                singular_value=singular,
                sensitivity=float(abs(singular) ** float(sensitivity_power)),
            )
        )
    triplets.sort(key=lambda row: row.sensitivity, reverse=True)
    return triplets[: max(0, int(top_k))]


def _optional_torch() -> Optional[Any]:
    try:
        import torch
    except Exception:
        return None
    return torch


def _prefix_keys(prefix: str, values: Dict[str, Any]) -> Dict[str, Any]:
    return {f"{prefix}.{key}": value for key, value in values.items()}


def _method_cfg(cfg: Dict[str, Any], name: str) -> Dict[str, Any]:
    advanced_cfg = cfg.get("advanced_baseline", {}) if isinstance(cfg.get("advanced_baseline", {}), dict) else {}
    method_cfg = advanced_cfg.get(name, {}) if isinstance(advanced_cfg.get(name, {}), dict) else {}
    return method_cfg


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
