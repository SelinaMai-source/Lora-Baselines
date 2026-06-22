from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List

PROJECT_LOCAL = Path(__file__).resolve().parents[1]
if str(PROJECT_LOCAL) not in sys.path:
    sys.path.insert(0, str(PROJECT_LOCAL))

from core.metrics_utils import (  # noqa: E402
    arper_woz3_corpus_bleu4_from_examples,
    arper_woz3_slot_error_counts,
)


def _iter_debug_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    yield from sorted(path.glob("eval_segment_*.json"))


def _load_examples(path: Path) -> List[Dict[str, Any]]:
    examples: List[Dict[str, Any]] = []
    for file_path in _iter_debug_files(path):
        raw = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and isinstance(raw.get("examples"), list):
            examples.extend(raw["examples"])
        elif isinstance(raw, list):
            examples.extend(raw)
        else:
            raise ValueError(f"Unsupported ARPER score input shape: {file_path}")
    return examples


def score_examples(examples: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    redunt = 0
    miss = 0
    scored = 0
    for row in examples:
        feat = str(row.get("input_text", row.get("input", "")))
        pred = str(row.get("normalized_prediction", row.get("raw_generated_output", row.get("prediction", ""))))
        if not feat:
            continue
        counts = arper_woz3_slot_error_counts(feat, pred)
        total += int(counts["total"])
        redunt += int(counts["redunt"])
        miss += int(counts["miss"])
        scored += 1

    ser = float((redunt + miss) / total) if total > 0 else None
    return {
        "num_examples": int(len(examples)),
        "num_scored_examples": int(scored),
        "bleu4": arper_woz3_corpus_bleu4_from_examples(examples),
        "ser": ser,
        "ser_percent": None if ser is None else float(ser * 100.0),
        "redunt": int(redunt),
        "miss": int(miss),
        "total": int(total),
        "official_equivalence": "SER mirrors ARPER util.py score/get_slot_error; BLEU groups references by feature string like run_woz3.py.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score ours ARPER WOZ3 generations with official-equivalent BLEU/SER.")
    parser.add_argument("--input", required=True, type=Path, help="eval_debug dir, eval_segment_*.json, or examples JSON list")
    parser.add_argument("--out", type=Path, default=None, help="Optional metrics JSON output path")
    args = parser.parse_args()

    metrics = score_examples(_load_examples(args.input))
    text = json.dumps(metrics, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
