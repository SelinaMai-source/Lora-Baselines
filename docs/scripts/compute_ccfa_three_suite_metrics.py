#!/usr/bin/env python3
"""Compute CCF-A three-suite aggregate metrics from ours run artifacts.

The script expects an explicit score matrix and does not infer missing official
scores. This keeps AR/FWT/BWT comparable to CITB/O-LoRA-style definitions while
making absent measurements fail loudly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def as_float(value: Any) -> float:
    if value == "-" or value is None:
        raise ValueError("Score matrix contains a missing value where a metric is required")
    return float(value)


def final_average(matrix: list[list[Any]]) -> float:
    if not matrix:
        raise ValueError("Empty score matrix")
    return sum(as_float(x) for x in matrix[-1]) / len(matrix[-1])


def fwt(matrix: list[list[Any]]) -> float:
    vals = []
    for i, row in enumerate(matrix[:-1]):
        vals.append(as_float(row[i + 1]))
    return sum(vals) / max(1, len(vals))


def bwt(matrix: list[list[Any]]) -> float:
    if len(matrix) <= 1:
        return 0.0
    diagonal = [as_float(matrix[i][i]) for i in range(len(matrix) - 1)]
    final_row = [as_float(x) for x in matrix[-1][:-1]]
    vals = [after - before for after, before in zip(final_row, diagonal)]
    return sum(vals) / max(1, len(vals))


def load_matrix(obj: dict[str, Any], metric: str) -> list[list[Any]]:
    if "matrix" in obj:
        return obj["matrix"]
    matrices = obj.get("matrices", {})
    if metric not in matrices:
        raise KeyError(f"Missing matrix for metric {metric!r}")
    return matrices[metric]


def compute_cl_metrics(obj: dict[str, Any], metric: str) -> dict[str, Any]:
    matrix = load_matrix(obj, metric)
    out = {
        "metric": metric,
        "final_average": final_average(matrix),
        "BWT": bwt(matrix),
        "matrix": matrix,
    }
    if len(matrix) > 1:
        out["FWT"] = fwt(matrix)
    if "official_test_score" in obj:
        out["final_official_test_score"] = obj["official_test_score"][-1]
    if "initial_multi_test_score" in obj:
        out["Tinit"] = obj["initial_multi_test_score"][-1]
    if "unseen_test_score" in obj:
        out["Tunseen"] = obj["unseen_test_score"][-1]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=["citb", "standard_peft", "arper"], required=True)
    parser.add_argument("--input", required=True, help="JSON with an explicit score matrix or suite-specific fields")
    parser.add_argument("--metric", default="rougeL")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    obj = read_json(Path(args.input))
    if args.suite in {"citb", "standard_peft"}:
        result = compute_cl_metrics(obj, args.metric)
        if args.suite == "citb":
            result["AR"] = result.pop("final_average")
            missing = [k for k in ["FWT", "BWT", "Tinit", "Tunseen"] if k not in result]
            if missing:
                result["status"] = "partial"
                result["blocker"] = f"Missing CITB fields: {missing}"
        else:
            result["final_average_accuracy"] = result.pop("final_average")
    else:
        required = ["bleu4", "ser"]
        missing = [k for k in required if k not in obj]
        if missing:
            raise KeyError(f"ARPER aggregate requires fields {required}; missing {missing}")
        result = {"BLEU_4": float(obj["bleu4"]), "SER": float(obj["ser"])}
        if "matrix" in obj:
            result.update(compute_cl_metrics(obj, args.metric))

    write_json(Path(args.out), result)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
