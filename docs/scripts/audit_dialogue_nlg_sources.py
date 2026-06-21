#!/usr/bin/env python3
"""Audit Dialogue NLG / MultiWOZ CL source readiness for v2.

ARPER is the preferred P1 route. ToDCL is documented as an extension path.
This script records which local assets are present and which official sources
still need to be fetched or converted.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def exists(path: str) -> dict[str, object]:
    p = Path(path)
    return {"path": path, "exists": p.exists(), "is_dir": p.is_dir()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="docs/ccfa_dialogue_nlg_audit.json")
    args = parser.parse_args()

    audit = {
        "status": "audit_only_not_ready",
        "priority": "ARPER MultiWOZ NLG first; ToDCL NLG/E2E as extension",
        "arper": {
            "paper": "https://aclanthology.org/2020.findings-emnlp.310/",
            "official_repo": "https://github.com/MiFei/Continual-Learning-for-NLG",
            "local_source": exists("benchmark/arper/source"),
            "target": "MultiWOZ-2.0 domain/dialogue-act intent continual NLG, 250/500 exemplar published baselines, BLEU-4/SER",
            "blocker": "Official ARPER source is not vendored yet; current local MultiWOZ stream is 5-domain train50/eval10 and not paper-aligned.",
        },
        "todcl": {
            "paper": "https://aclanthology.org/2021.emnlp-main.590/",
            "official_repo": "https://github.com/andreamad8/ToDCL",
            "local_source": exists("benchmark/todcl/source"),
            "target": "37-domain ToD NLG/E2E, BLEU/EER",
            "blocker": "Official ToDCL source/data are not vendored yet; keep as backup/extension until ARPER route is aligned.",
        },
        "local_multiwoz_assets": {
            "multiwoz_repo": exists("benchmark/multiwoz_nlg/source/multiwoz"),
            "multiwoz_eval": exists("benchmark/multiwoz_nlg/source/evaluation"),
            "current_converter": exists("methods/ours/source/project_local/scripts/convert_multiwoz_to_stream.py"),
        },
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote Dialogue NLG audit to {out}")
    print("Status: audit_only_not_ready")


if __name__ == "__main__":
    main()
