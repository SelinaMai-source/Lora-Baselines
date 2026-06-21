#!/usr/bin/env python3
"""Loader and validator for the project-local 8-task Seq-GLUE stream."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


EXPECTED_TASK_ORDER: Tuple[str, ...] = ("sst2", "mrpc", "rte", "cola", "boolq", "wic", "cb", "copa")
DEFAULT_STREAM_PATH = Path(__file__).resolve().parent / "data/processed/seqglue_cl_tasks_train50_eval10.json"


@dataclass(frozen=True)
class SeqGlueExample:
    instruction: str
    input: str
    output: str


@dataclass(frozen=True)
class SeqGlueSegment:
    segment_id: int
    segment_name: str
    train: Tuple[SeqGlueExample, ...]
    eval: Tuple[SeqGlueExample, ...]


@dataclass(frozen=True)
class SeqGlueStream:
    benchmark: str
    version: str
    stream: Tuple[SeqGlueSegment, ...]


def load_seq_glue_stream(path: Path | str = DEFAULT_STREAM_PATH, *, validate: bool = True) -> SeqGlueStream:
    """Load a processed Seq-GLUE stream and optionally validate the 8-task contract."""
    stream_path = Path(path)
    with stream_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    stream = _parse_stream(raw)
    if validate:
        validate_seq_glue_stream(stream)
    return stream


def validate_seq_glue_stream(stream: SeqGlueStream) -> Dict[str, Any]:
    """Validate order, ids, names, and non-empty train/eval examples."""
    errors: List[str] = []
    if stream.benchmark != "Seq-GLUE":
        errors.append(f"benchmark must be Seq-GLUE, got {stream.benchmark!r}")
    if len(stream.stream) != len(EXPECTED_TASK_ORDER):
        errors.append(f"expected {len(EXPECTED_TASK_ORDER)} segments, got {len(stream.stream)}")

    observed_tasks: List[str] = []
    for expected_id, segment in enumerate(stream.stream):
        task = _task_from_segment_name(segment.segment_name)
        observed_tasks.append(task)
        if segment.segment_id != expected_id:
            errors.append(f"segment {segment.segment_name} has id {segment.segment_id}, expected {expected_id}")
        if expected_id < len(EXPECTED_TASK_ORDER) and task != EXPECTED_TASK_ORDER[expected_id]:
            errors.append(f"segment {expected_id} is {task!r}, expected {EXPECTED_TASK_ORDER[expected_id]!r}")
        if not segment.train:
            errors.append(f"segment {segment.segment_name} has empty train split")
        if not segment.eval:
            errors.append(f"segment {segment.segment_name} has empty eval split")
        _validate_examples(errors, segment.segment_name, "train", segment.train)
        _validate_examples(errors, segment.segment_name, "eval", segment.eval)

    if errors:
        raise ValueError("Invalid Seq-GLUE stream:\n- " + "\n- ".join(errors))
    return {
        "benchmark": stream.benchmark,
        "version": stream.version,
        "tasks": observed_tasks,
        "num_segments": len(stream.stream),
        "train_examples": sum(len(seg.train) for seg in stream.stream),
        "eval_examples": sum(len(seg.eval) for seg in stream.stream),
    }


def _parse_stream(raw: Dict[str, Any]) -> SeqGlueStream:
    segments = []
    for row in raw.get("stream", []):
        train = tuple(_parse_example(ex) for ex in row.get("train", []))
        eval_rows = tuple(_parse_example(ex) for ex in row.get("eval", []))
        segments.append(
            SeqGlueSegment(
                segment_id=int(row["segment_id"]),
                segment_name=str(row["segment_name"]),
                train=train,
                eval=eval_rows,
            )
        )
    return SeqGlueStream(
        benchmark=str(raw.get("benchmark", "")),
        version=str(raw.get("version", "")),
        stream=tuple(segments),
    )


def _parse_example(row: Dict[str, Any]) -> SeqGlueExample:
    missing = [key for key in ("instruction", "input", "output") if key not in row]
    if missing:
        raise ValueError(f"Seq-GLUE example missing keys {missing}: {row}")
    return SeqGlueExample(instruction=str(row["instruction"]), input=str(row["input"]), output=str(row["output"]))


def _task_from_segment_name(segment_name: str) -> str:
    for task in EXPECTED_TASK_ORDER:
        if segment_name == task or segment_name.endswith(f"_{task}"):
            return task
    return segment_name


def _validate_examples(
    errors: List[str],
    segment_name: str,
    split: str,
    examples: Sequence[SeqGlueExample],
) -> None:
    for idx, ex in enumerate(examples):
        if not ex.instruction.strip():
            errors.append(f"{segment_name}/{split}/{idx} has empty instruction")
        if ex.output.strip() == "":
            errors.append(f"{segment_name}/{split}/{idx} has empty output")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a processed project-local Seq-GLUE stream.")
    parser.add_argument("--path", type=Path, default=DEFAULT_STREAM_PATH)
    parser.add_argument("--json", action="store_true", help="Print validation summary as JSON.")
    args = parser.parse_args()

    stream = load_seq_glue_stream(args.path, validate=True)
    summary = validate_seq_glue_stream(stream)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            "Validated Seq-GLUE stream: "
            f"{summary['num_segments']} segments, "
            f"tasks={' -> '.join(summary['tasks'])}, "
            f"train={summary['train_examples']}, eval={summary['eval_examples']}"
        )


if __name__ == "__main__":
    main()
