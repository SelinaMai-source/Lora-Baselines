#!/usr/bin/env python3
"""Audit the O-LoRA standard/long CL benchmark definitions.

The v2 standard PEFT suite must not reuse the local Seq-GLUE diagnostic stream.
This script extracts the official O-LoRA task order/config evidence already
vendored in the repository.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STANDARD_ORDERS = {
    "order1": ["dbpedia", "amazon", "yahoo", "agnews"],
    "order2": ["dbpedia", "amazon", "agnews", "yahoo"],
    "order3": ["yahoo", "amazon", "agnews", "dbpedia"],
}

LONG_ORDER = [
    "yelp",
    "amazon",
    "MNLI",
    "CB",
    "COPA",
    "QQP",
    "RTE",
    "IMDB",
    "SST-2",
    "dbpedia",
    "agnews",
    "yahoo",
    "MultiRC",
    "BoolQA",
    "WiC",
]


def load_json(path: Path) -> object:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def inspect_task_config(root: Path, config_dir: str, task: str) -> dict[str, object]:
    d = root / config_dir / task
    out: dict[str, object] = {"task": task, "config_dir": str(d), "exists": d.exists()}
    for split in ("train", "dev", "test"):
        path = d / f"{split}_tasks.json"
        if path.exists():
            data = load_json(path)
            out[f"{split}_tasks_json"] = str(path)
            out[f"{split}_keys"] = list(data.keys()) if isinstance(data, dict) else []
        else:
            out[f"{split}_tasks_json"] = None
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--olora-root", default="methods/o_lora/source")
    parser.add_argument("--out", default="docs/ccfa_standard_peft_cl_audit.json")
    args = parser.parse_args()

    root = Path(args.olora_root)
    if not (root / "scripts" / "order_1.sh").exists():
        raise FileNotFoundError(f"Missing O-LoRA scripts under {root}")

    audit: dict[str, object] = {
        "official_paper": "https://aclanthology.org/2023.findings-emnlp.715/",
        "official_repo": "https://github.com/cmnfriend/O-LoRA",
        "status": "audit_only_not_ready",
        "standard_orders": {},
        "long_order": LONG_ORDER,
        "blocker": "Convert O-LoRA CL_Benchmark/configs into ours stream format and verify LFPT5/Progressive Prompts sample equivalence before launch.",
    }

    for order_name, tasks in STANDARD_ORDERS.items():
        config_dir = f"configs/{order_name}_configs"
        audit["standard_orders"][order_name] = {
            "tasks": tasks,
            "script": str(root / "scripts" / f"{order_name.replace('order', 'order_')}.sh"),
            "configs": [inspect_task_config(root, config_dir, task) for task in tasks],
        }

    audit["long_configs"] = [inspect_task_config(root, "configs/long_configs", task) for task in LONG_ORDER]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote Standard PEFT CL audit to {out}")
    print("Status: audit_only_not_ready")


if __name__ == "__main__":
    main()
