#!/usr/bin/env python3
"""Prepare CCF-A three-suite data/config artifacts outside Git.

This script only converts official/local source assets into auditable stream
JSON and blocked config templates. It does not mark a run ready unless the
model/checkpoint/metric blockers are cleared elsewhere.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


RUN_ROOT = Path("/root/autodl-tmp/lora-baselines-run_v1")
DEFAULT_OUT_ROOT = RUN_ROOT / "data" / "ccfa_three_suite"
DEFAULT_CONFIG_ROOT = RUN_ROOT / "configs" / "ccfa_three_suite"
DEFAULT_MANIFEST = RUN_ROOT / "ccfa_three_suite_manifest.csv"


@dataclass(frozen=True)
class CitbSpec:
    benchmark: str
    citb_stream: str
    train: int
    dev: int
    test: int
    expected_tasks: int
    status: str
    blocker: str


CITB_SPECS = {
    "instrdialog": CitbSpec(
        benchmark="InstrDialog",
        citb_stream="cl_dialogue_tasks",
        train=500,
        dev=50,
        test=100,
        expected_tasks=19,
        status="blocked",
        blocker=(
            "Official order/data stream generated, but ours still needs T5-small "
            "LM-adapted + 100-SuperNI-init seq2seq checkpoint loading and CITB "
            "ROUGE-L matrix export."
        ),
    ),
    "instrdialogpp": CitbSpec(
        benchmark="InstrDialog++",
        citb_stream="cl_dialogue_long_tasks",
        train=100,
        dev=50,
        test=100,
        expected_tasks=38,
        status="blocked",
        blocker=(
            "Official order/task files are present, but published long-stream "
            "scripts use max_num_instances_per_eval_task=25; reconcile against "
            "the requested 100/50/100 split before launch. Ours also needs "
            "T5-small LM-adapted + 100-SuperNI-init seq2seq loading and CITB "
            "ROUGE-L matrix export."
        ),
    ),
}

STANDARD_ORDERS = {
    "order1": ["dbpedia", "amazon", "yahoo", "agnews"],
    "order2": ["dbpedia", "amazon", "agnews", "yahoo"],
    "order3": ["yahoo", "amazon", "agnews", "dbpedia"],
}

TASK_TYPE_TO_FOLDER = {
    "SC": "SC",
    "TC": "TC",
    "NLI": "NLI",
    "QQP": "QQP",
    "WiC": "WiC",
    "MultiRC": "MultiRC",
    "COPA": "COPA",
    "BoolQA": "BoolQA",
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def first_text(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    if value is None:
        return ""
    return str(value)


def as_outputs(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if value is None:
        return [""]
    return [str(value)]


def read_order(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def citb_instance_to_example(task_instruction: str, inst: dict[str, Any]) -> dict[str, Any]:
    refs = as_outputs(inst.get("output"))
    return {
        "instruction": task_instruction,
        "input": str(inst.get("input", "")),
        "output": refs[0],
        "references": refs,
        "source_id": str(inst.get("id", "")),
    }


def split_citb_instances(
    instances: list[dict[str, Any]], *, train_n: int, dev_n: int, test_n: int, seed: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    test = list(instances[:test_n])
    dev = list(instances[test_n : test_n + dev_n])
    remaining = list(instances[test_n + dev_n :])
    random.Random(seed).shuffle(remaining)
    train = remaining[:train_n]
    return train, dev, test


def build_citb_streams(citb_root: Path, out_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    tasks_dir = citb_root / "data" / "tasks"
    if not tasks_dir.exists():
        raise FileNotFoundError(f"Missing CITB tasks dir: {tasks_dir}")

    for suite_key, spec in CITB_SPECS.items():
        for order_idx in (1, 2, 3):
            order_name = f"order{order_idx}"
            order_path = (
                citb_root
                / "data"
                / "CIT_data"
                / "task_orders"
                / f"stream={spec.citb_stream}"
                / f"{order_name}.txt"
            )
            task_names = read_order(order_path)
            if len(task_names) != spec.expected_tasks:
                raise ValueError(f"{order_path} has {len(task_names)} tasks; expected {spec.expected_tasks}")

            segments = []
            split_counts = []
            missing = []
            for segment_id, task_name in enumerate(task_names):
                task_path = tasks_dir / f"{task_name}.json"
                if not task_path.exists():
                    missing.append(task_name)
                    continue
                task_obj = read_json(task_path)
                instances = task_obj.get("Instances") or []
                if not isinstance(instances, list):
                    raise ValueError(f"Instances is not a list in {task_path}")
                train_i, dev_i, test_i = split_citb_instances(
                    instances, train_n=spec.train, dev_n=spec.dev, test_n=spec.test, seed=order_idx
                )
                instruction = first_text(task_obj.get("Definition"))
                train = [citb_instance_to_example(instruction, x) for x in train_i]
                dev = [citb_instance_to_example(instruction, x) for x in dev_i]
                test = [citb_instance_to_example(instruction, x) for x in test_i]
                segments.append(
                    {
                        "segment_id": segment_id,
                        "segment_name": task_name,
                        "train": train,
                        "dev": dev,
                        "eval": test,
                    }
                )
                split_counts.append(
                    {
                        "task": task_name,
                        "train": len(train),
                        "dev": len(dev),
                        "test": len(test),
                        "available_instances": len(instances),
                    }
                )
            if missing:
                raise FileNotFoundError(f"Missing CITB task JSON files: {missing}")

            out_path = out_root / "citb" / f"citb_{suite_key}_{order_name}_train{spec.train}_dev{spec.dev}_test{spec.test}.json"
            stream = {
                "benchmark": f"CITB-{spec.benchmark}",
                "version": "ccfa_official_order_v1",
                "metadata": {
                    "official_repo": "https://github.com/hyintell/CITB",
                    "official_paper": "https://aclanthology.org/2023.findings-emnlp.633/",
                    "citb_root": str(citb_root),
                    "order_file": str(order_path),
                    "split_policy": "test first, dev second, train shuffled from remaining; counts follow requested CCF-A alignment target",
                    "target_split": {"train": spec.train, "dev": spec.dev, "test": spec.test},
                    "split_counts": split_counts,
                },
                "stream": segments,
            }
            write_json(out_path, stream)
            rows.append(
                {
                    "suite": "CITB",
                    "benchmark": f"{spec.benchmark}-{order_name}",
                    "seed": order_idx,
                    "data_path": str(out_path),
                    "status": spec.status,
                    "blocker": spec.blocker,
                }
            )
    return rows


def load_instruction_map(olora_root: Path) -> dict[str, str]:
    raw = read_json(olora_root / "configs" / "instruction_config.json")
    out = {}
    for task, items in raw.items():
        zero = [x for x in items if x.get("instruction_type") == "zero-shot"]
        out[task] = str(zero[0]["instruction"] if zero else items[0]["instruction"])
    return out


def active_task_type(task_config: dict[str, Any]) -> tuple[str, str] | None:
    active = []
    for task_type, entries in task_config.items():
        for entry in entries:
            if entry:
                active.append((task_type, str(entry["dataset name"])))
    if not active:
        return None
    if len(active) != 1:
        raise ValueError(f"Expected exactly one active O-LoRA task config, got {active}")
    return active[0]


def olora_example(task_type: str, dataset_name: str, instruction_map: dict[str, str], instance: dict[str, Any], idx: int) -> dict[str, str]:
    labels = instance.get("_labels", [])
    labels_str = ", ".join(str(x) for x in labels)
    base_instruction = instruction_map.get(task_type, "{0}\nAnswer:")
    if task_type == "COPA":
        instruction = "{0}\nAnswer:"
    else:
        instruction = f"{base_instruction}Option: {labels_str} \n{{0}}\nAnswer:"
    return {
        "instruction": instruction,
        "input": str(instance.get("sentence", "")),
        "output": str(instance.get("label", "")),
        "source_id": str(idx),
        "task_type": task_type,
        "dataset": dataset_name,
    }


def load_olora_split(olora_root: Path, task_type: str, dataset_name: str, split: str) -> list[dict[str, Any]]:
    folder = olora_root / "CL_Benchmark" / TASK_TYPE_TO_FOLDER[task_type] / dataset_name
    instances = read_json(folder / f"{split}.json")
    labels = read_json(folder / "labels.json")
    if not isinstance(instances, list):
        raise ValueError(f"Expected list in {folder / f'{split}.json'}")
    for inst in instances:
        inst["_labels"] = labels
    return instances


def build_olora_streams(olora_root: Path, out_root: Path) -> list[dict[str, Any]]:
    rows = []
    instruction_map = load_instruction_map(olora_root)
    for order_name, tasks in STANDARD_ORDERS.items():
        segments = []
        split_counts = []
        for segment_id, task_name in enumerate(tasks):
            cfg_dir = olora_root / "configs" / f"{order_name}_configs" / task_name
            train_active = active_task_type(read_json(cfg_dir / "train_tasks.json"))
            if train_active is None:
                raise ValueError(f"Missing active train O-LoRA config in {cfg_dir}")
            train_type, train_dataset = train_active
            dev_active = active_task_type(read_json(cfg_dir / "dev_tasks.json")) or train_active
            dev_type, dev_dataset = dev_active
            test_type, test_dataset = train_active
            if (train_type, train_dataset) != (dev_type, dev_dataset) or (train_type, train_dataset) != (test_type, test_dataset):
                raise ValueError(f"Mismatched split configs in {cfg_dir}")
            train_raw = load_olora_split(olora_root, train_type, train_dataset, "train")
            dev_raw = load_olora_split(olora_root, train_type, train_dataset, "dev")
            test_raw = load_olora_split(olora_root, train_type, train_dataset, "test")
            train = [olora_example(train_type, train_dataset, instruction_map, x, i) for i, x in enumerate(train_raw)]
            dev = [olora_example(train_type, train_dataset, instruction_map, x, i) for i, x in enumerate(dev_raw)]
            test = [olora_example(train_type, train_dataset, instruction_map, x, i) for i, x in enumerate(test_raw)]
            segments.append(
                {
                    "segment_id": segment_id,
                    "segment_name": task_name,
                    "train": train,
                    "dev": dev,
                    "eval": test,
                }
            )
            split_counts.append({"task": task_name, "train": len(train), "dev": len(dev), "test": len(test)})
        out_path = out_root / "standard_peft" / f"olora_standard_{order_name}_t5large.json"
        stream = {
            "benchmark": "O-LoRA-standard-T5-large-CL",
            "version": "ccfa_olora_standard_v1",
            "metadata": {
                "official_repo": "https://github.com/cmnfriend/O-LoRA",
                "official_paper": "https://aclanthology.org/2023.findings-emnlp.715/",
                "olora_root": str(olora_root),
                "order": tasks,
                "split_counts": split_counts,
                "paper_setting_notes": "T5-large, official O-LoRA CL_Benchmark/configs/order*_configs, 1 epoch per task in scripts/order_*.sh.",
            },
            "stream": segments,
        }
        write_json(out_path, stream)
        rows.append(
            {
                "suite": "Standard PEFT CL",
                "benchmark": f"O-LoRA standard {order_name}",
                "seed": int(order_name[-1]),
                "data_path": str(out_path),
                "status": "blocked",
                "blocker": "Official O-LoRA data stream generated, but ours still lacks a T5-large seq2seq PEFT runner/checkpoint path and LFPT5/Progressive-Prompts sample-equivalence verification.",
            }
        )
    return rows


def arper_task_name(meta: dict[str, Any], granularity: str) -> str:
    first_da = sorted(meta.keys())[0]
    parts = first_da.split("-")
    return parts[0] if granularity == "domain" else parts[1]


def arper_feat_string(meta: dict[str, Any]) -> str:
    feats = []
    for da, slots in sorted(meta.items()):
        for slot in slots:
            feats.append("-".join([da, str(slot[0]), str(slot[1])]))
    return "|".join(sorted(feats))


def build_arper_stream(arper_root: Path, out_root: Path, granularity: str) -> tuple[Path, list[dict[str, Any]]]:
    resource = arper_root / "resource" / "woz3"
    suffix = "do" if granularity == "domain" else "da"
    text = read_json(resource / f"text_unique_{suffix}.json")
    feat = read_json(resource / f"feat_unique_{suffix}.json")
    split = read_json(resource / "data_split" / f"all_unique_{suffix}_datasplit.json")
    by_task: dict[str, dict[str, list[dict[str, Any]]]] = {}

    for split_name, split_key in (("train", "train"), ("dev", "valid"), ("eval", "test")):
        for dial_idx, turn_idx, _ in split[split_key]:
            if turn_idx not in feat.get(dial_idx, {}):
                continue
            meta = feat[dial_idx][turn_idx]
            task = arper_task_name(meta, granularity)
            item_text = text[dial_idx][turn_idx]
            by_task.setdefault(task, {"train": [], "dev": [], "eval": []})
            by_task[task][split_name].append(
                {
                    "instruction": "Generate the delexicalized system utterance from the dialogue-act slot-value features.",
                    "input": arper_feat_string(meta),
                    "output": str(item_text.get("delex", "")),
                    "original_output": str(item_text.get("ori", "")),
                    "metadata": {"dial_idx": dial_idx, "turn_idx": turn_idx, "meta": meta},
                }
            )

    segments = []
    split_counts = []
    for segment_id, task in enumerate(sorted(by_task)):
        data = by_task[task]
        segments.append({"segment_id": segment_id, "segment_name": task, **data})
        split_counts.append(
            {
                "task": task,
                "train": len(data["train"]),
                "dev": len(data["dev"]),
                "test": len(data["eval"]),
            }
        )

    out_path = out_root / "arper" / f"arper_woz3_unique_{granularity}.json"
    stream = {
        "benchmark": f"ARPER-WOZ3-unique-{granularity}",
        "version": "ccfa_arper_official_resource_v1",
        "metadata": {
            "official_repo": "https://github.com/MiFei/Continual-Learning-for-NLG",
            "official_paper": "https://aclanthology.org/2020.findings-emnlp.310/",
            "arper_root": str(arper_root),
            "paper_setting_notes": "ARPER resource/woz3 provides default preprocessed unique-domain/unique-dialogue-act splits and official BLEU/SER utilities.",
            "split_counts": split_counts,
        },
        "stream": segments,
    }
    write_json(out_path, stream)
    rows = []
    if granularity == "dialogue_act":
        for seed in (1, 2, 3):
            rows.append(
                {
                    "suite": "Dialogue NLG",
                    "benchmark": "ARPER MultiWOZ NLG dialogue-act",
                    "seed": seed,
                    "data_path": str(out_path),
                    "status": "blocked",
                    "blocker": "ARPER official resource stream generated, but ours still needs dialogue-NLG backbone selection, official SER scorer integration over generated outputs, and confirmation that WOZ3 resource is the intended MultiWOZ-2.0 comparison target.",
                }
            )
    return out_path, rows


def config_text(row: dict[str, Any]) -> str:
    suite = row["suite"]
    benchmark = row["benchmark"]
    seed = row["seed"]
    run_slug = (
        benchmark.lower()
        .replace("++", "pp")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )
    if suite == "CITB":
        backbone = "google/t5-small-lm-adapt + 100 SuperNI init"
        model_path = "TODO_local_t5_small_lm_adapt_superni_init_checkpoint"
        metrics = ["ROUGE-L AR", "FWT", "BWT", "Tinit", "Tunseen"]
    elif suite == "Standard PEFT CL":
        backbone = "t5-large"
        model_path = "TODO_local_or_hf_t5_large_seq2seq_checkpoint"
        metrics = ["final_average_accuracy", "forgetting", "BWT"]
    else:
        backbone = "TODO_ARPER_dialogue_NLG_backbone"
        model_path = "TODO_dialogue_nlg_checkpoint"
        metrics = ["BLEU-4", "SER", "forgetting"]
    metrics_yaml = "[" + ", ".join(json.dumps(m) for m in metrics) + "]"
    return f"""# ready: false
# suite: {suite}
# benchmark: {benchmark}
# blocker: {row['blocker']}
experiment_name: ccfa_v2_{run_slug}_seed{seed}_ours
mode: ours
seed: {seed}
paths:
  project_root: /root/Lora-Baselines
  processed_stream_file: {row['data_path']}
  results_dir: /root/autodl-tmp/lora-baselines-run_v1/results
data:
  suite: {json.dumps(suite)}
  benchmark: {json.dumps(benchmark)}
  stream_format: unified_ccfa_stream
  ready: false
model:
  backbone: {json.dumps(backbone)}
  hf_model_name_or_path: {json.dumps(model_path)}
output:
  run_name: ccfa_v2_{run_slug}_seed{seed}_ours
  tracking:
    use_wandb: true
    wandb_project: lora- baselines-run_v1
    wandb_group: ccfa_v2_three_suite
paper:
  ready: false
  metrics: {metrics_yaml}
  notes: {json.dumps(row['blocker'])}
"""


def write_configs(rows: list[dict[str, Any]], config_root: Path) -> None:
    config_root.mkdir(parents=True, exist_ok=True)
    stale_names = [
        "standard_peft_order1_seed1_ours.blocked.yaml",
        "standard_peft_order2_seed2_ours.blocked.yaml",
        "standard_peft_order3_seed3_ours.blocked.yaml",
        "arper_multiwoz_nlg_seed1_ours.blocked.yaml",
        "arper_multiwoz_nlg_seed2_ours.blocked.yaml",
        "arper_multiwoz_nlg_seed3_ours.blocked.yaml",
    ]
    for name in stale_names:
        stale = config_root / name
        if stale.exists():
            stale.unlink()
    for row in rows:
        name = (
            f"{row['suite']}_{row['benchmark']}_seed{row['seed']}_ours.blocked.yaml"
            .lower()
            .replace("++", "pp")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
        )
        (config_root / name).write_text(config_text(row), encoding="utf-8")


def write_manifest(rows: list[dict[str, Any]], manifest_path: Path, config_root: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "suite",
        "benchmark",
        "seed",
        "backbone",
        "config_path",
        "command",
        "metrics",
        "status",
        "blocker",
    ]
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            cfg_name = (
                f"{row['suite']}_{row['benchmark']}_seed{row['seed']}_ours.blocked.yaml"
                .lower()
                .replace("++", "pp")
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
            )
            if row["suite"] == "CITB":
                backbone = "T5-small LM-adapted + 100 SuperNI init"
                metrics = "ROUGE-L AR;FWT;BWT;Tinit;Tunseen"
            elif row["suite"] == "Standard PEFT CL":
                backbone = "T5-large"
                metrics = "Final average accuracy;forgetting;BWT"
            else:
                backbone = "ARPER dialogue NLG backbone TBD"
                metrics = "BLEU-4;SER;forgetting"
            config_path = str(config_root / cfg_name)
            writer.writerow(
                {
                    "suite": row["suite"],
                    "benchmark": row["benchmark"],
                    "seed": row["seed"],
                    "backbone": backbone,
                    "config_path": config_path,
                    "command": f"python methods/ours/source/project_local/core/train.py --config {config_path}",
                    "metrics": metrics,
                    "status": row["status"],
                    "blocker": row["blocker"],
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default="/root/Lora-Baselines")
    parser.add_argument("--citb-root", default="/root/Lora-Baselines/benchmark/instrdialog/source")
    parser.add_argument("--olora-root", default="/root/Lora-Baselines/methods/o_lora/source")
    parser.add_argument("--arper-root", default="/root/autodl-tmp/lora-baselines-run_v1/external/arper")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    parser.add_argument("--config-root", default=str(DEFAULT_CONFIG_ROOT))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args()

    out_root = Path(args.out_root)
    rows: list[dict[str, Any]] = []
    rows.extend(build_citb_streams(Path(args.citb_root), out_root))
    rows.extend(build_olora_streams(Path(args.olora_root), out_root))
    if Path(args.arper_root).exists():
        build_arper_stream(Path(args.arper_root), out_root, "domain")
        _, arper_rows = build_arper_stream(Path(args.arper_root), out_root, "dialogue_act")
        rows.extend(arper_rows)
    else:
        rows.append(
            {
                "suite": "Dialogue NLG",
                "benchmark": "ARPER MultiWOZ NLG",
                "seed": 1,
                "data_path": "",
                "status": "blocked",
                "blocker": f"ARPER source not found at {args.arper_root}; fetch https://github.com/MiFei/Continual-Learning-for-NLG",
            }
        )

    config_root = Path(args.config_root)
    write_configs(rows, config_root)
    write_manifest(rows, Path(args.manifest), config_root)
    print(f"Wrote streams under {out_root}")
    print(f"Wrote blocked configs under {config_root}")
    print(f"Wrote manifest {args.manifest}")
    print("No run was marked ready or launched.")


if __name__ == "__main__":
    main()
