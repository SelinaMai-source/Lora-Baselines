#!/usr/bin/env python3
"""Audit CITB official assets before generating v2 streams.

This script intentionally does not invent processed data. It verifies the
vendored CITB task orders and records the exact stream targets that must be
converted into the ours runner format.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STREAMS = {
    "instrdialog": {
        "citb_stream": "cl_dialogue_tasks",
        "tasks": 19,
        "train": 500,
        "dev": 50,
        "test": 100,
    },
    "instrdialogpp": {
        "citb_stream": "cl_dialogue_long_tasks",
        "tasks": 38,
        "train": 100,
        "dev": 50,
        "test": 100,
        "blocker": "Vendored long-stream scripts use max_num_instances_per_eval_task=25; reconcile with paper/user target 50 dev + 100 test before writing final streams.",
    },
}


def read_order(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--citb-root",
        default="benchmark/instrdialog/source",
        help="Path to the vendored official CITB source.",
    )
    parser.add_argument(
        "--out",
        default="docs/ccfa_citb_stream_audit.json",
        help="Audit JSON to write. This is not a processed training stream.",
    )
    args = parser.parse_args()

    root = Path(args.citb_root)
    tasks_dir = root / "data" / "tasks"
    if not tasks_dir.exists():
        raise FileNotFoundError(f"Missing CITB tasks directory: {tasks_dir}")

    audit: dict[str, object] = {
        "official_paper": "https://aclanthology.org/2023.findings-emnlp.633/",
        "official_repo": "https://github.com/hyintell/CITB",
        "citb_root": str(root),
        "status": "audit_only_not_ready",
        "streams": {},
    }

    for suite, spec in STREAMS.items():
        stream_name = str(spec["citb_stream"])
        orders: dict[str, object] = {}
        for order in (1, 2, 3):
            order_path = root / "data" / "CIT_data" / "task_orders" / f"stream={stream_name}" / f"order{order}.txt"
            task_names = read_order(order_path)
            missing_tasks = [name for name in task_names if not (tasks_dir / f"{name}.json").exists()]
            orders[f"order{order}"] = {
                "order_file": str(order_path),
                "num_tasks": len(task_names),
                "expected_tasks": spec["tasks"],
                "task_names": task_names,
                "missing_task_json": missing_tasks,
                "order_ready": len(task_names) == int(spec["tasks"]) and not missing_tasks,
            }
        audit["streams"][suite] = {
            "target_split": {
                "train": spec["train"],
                "dev": spec["dev"],
                "test": spec["test"],
            },
            "blocker": spec.get("blocker", "Need converter from CITB NI dataset records to ours processed stream JSON."),
            "orders": orders,
        }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote CITB audit to {out}")
    print("Status: audit_only_not_ready")


if __name__ == "__main__":
    main()
