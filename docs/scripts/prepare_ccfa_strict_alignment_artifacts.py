#!/usr/bin/env python3
"""Generate strict CCF-A three-suite configs and manifests."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path


REPO_ROOT = Path("/root/Lora-Baselines")
RUN_ROOT = Path("/root/autodl-tmp/lora-baselines-run_v1")
DOC_CONFIG_ROOT = REPO_ROOT / "docs" / "configs" / "ccfa_three_suite"
RUNTIME_CONFIG_ROOT = RUN_ROOT / "configs" / "ccfa_three_suite"
DOC_MANIFEST = REPO_ROOT / "docs" / "ccfa_three_suite_manifest.csv"
RUNTIME_MANIFEST = RUN_ROOT / "ccfa_three_suite_manifest.csv"

T5_SMALL = "/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt"
T5_LARGE = "/root/autodl-tmp/model_cache/hf_snapshots/t5-large"
CITB_STAGE1 = (
    "/root/autodl-tmp/lora-baselines-run_v1/models/"
    "citb_stage1_superni_t5_small_lm_adapt/checkpoint-best"
)


def rows() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    citb_specs = [
        (
            "instrdialog",
            "InstrDialog",
            "train500_dev50_test100",
            "needs-stage1",
            "100-SuperNI-init checkpoint is not present locally; run official Stage-1 first.",
        ),
        (
            "instrdialogpp",
            "InstrDialog++",
            "train100_dev50_test100",
            "blocked",
            "Official long-stream scripts use max_num_instances_per_eval_task=25, while requested split is 100/50/100; also needs Stage-1 checkpoint.",
        ),
    ]
    for key, label, split, status, blocker in citb_specs:
        for order in (1, 2, 3):
            out.append(
                {
                    "suite": "CITB",
                    "benchmark": f"{label}-order{order}",
                    "seed": str(order),
                    "status": status,
                    "backbone": "T5-small LM-adapted + 100 SuperNI init",
                    "data_path": str(
                        RUN_ROOT
                        / "data"
                        / "ccfa_three_suite"
                        / "citb"
                        / f"citb_{key}_order{order}_{split}.json"
                    ),
                    "config_name": f"citb_{key}_order{order}_seed{order}_ours_strict.yaml",
                    "metrics": "ROUGE-L AR;FWT;BWT;Tinit;Tunseen",
                    "blocker": blocker,
                    "evidence": "CITB README; scripts/run_initial_multitask_tuning.sh; scripts/*_stream_scripts/run_cit_ft_instr.sh; collect_results.py; data/CIT_data/task_orders",
                }
            )

    standard_orders = {
        1: "dbpedia -> amazon -> yahoo -> agnews",
        2: "dbpedia -> amazon -> agnews -> yahoo",
        3: "yahoo -> amazon -> agnews -> dbpedia",
    }
    for order, task_order in standard_orders.items():
        out.append(
            {
                "suite": "Standard PEFT CL",
                "benchmark": f"O-LoRA standard order{order}",
                "seed": str(order),
                "status": "ready",
                "backbone": "T5-large",
                "data_path": str(
                    RUN_ROOT
                    / "data"
                    / "ccfa_three_suite"
                    / "standard_peft"
                    / f"olora_standard_order{order}_t5large.json"
                ),
                "config_name": f"standard_peft_cl_o_lora_standard_order{order}_seed{order}_ours_strict.yaml",
                "metrics": "final average accuracy;forgetting;BWT",
                "blocker": "",
                "evidence": f"O-LoRA README; scripts/order_{order}.sh; configs/order{order}_configs; CL_Benchmark; order {task_order}; src/run_uie_lora.py",
            }
        )

    for seed in (1, 2, 3):
        out.append(
            {
                "suite": "Dialogue NLG",
                "benchmark": "ARPER WOZ3 dialogue-act",
                "seed": str(seed),
                "status": "blocked",
                "backbone": "ARPER SCLSTM official / ours T5 seq2seq not yet metric-strict",
                "data_path": str(
                    RUN_ROOT
                    / "data"
                    / "ccfa_three_suite"
                    / "arper"
                    / "arper_woz3_unique_dialogue_act.json"
                ),
                "config_name": f"dialogue_nlg_arper_woz3_dialogue_act_seed{seed}_ours_strict.yaml",
                "metrics": "BLEU-4;SER;forgetting",
                "blocker": "Official ARPER SER scorer is not yet wired to ours generated outputs, and ours T5 seq2seq path is not the official SCLSTM backbone.",
                "evidence": "ARPER config/config.cfg; run.sh; run_woz3.py evaluate(); bleu.py; resource/woz3 unique DA split",
            }
        )
    return out


def config_text(row: dict[str, str]) -> str:
    suite = row["suite"]
    if suite == "CITB":
        model_path = CITB_STAGE1
        base_path = T5_SMALL
        max_source, max_target, gen_tokens = 1024, 128, 128
        train_lr = "1e-05"
        epochs = "15"
        batch = "16" if "++" in row["benchmark"] else "8"
        official = """
  stage1_command: "cd /root/autodl-tmp/lora-baselines-run_v1/external_sources/citb && bash scripts/run_initial_multitask_tuning.sh"
  base_model_name: google/t5-small-lm-adapt
  local_base_model_path: /root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt
  required_stage1_checkpoint: /root/autodl-tmp/lora-baselines-run_v1/models/citb_stage1_superni_t5_small_lm_adapt/checkpoint-best
  stage1_train_tasks: 100
  stage1_instances_per_task: 100
  stage2_learning_rate: 1e-05
  stage2_epochs: 15
"""
    elif suite == "Standard PEFT CL":
        model_path = T5_LARGE
        base_path = T5_LARGE
        max_source, max_target, gen_tokens = 512, 50, 50
        train_lr = "1e-04"
        epochs = "1"
        batch = "1"
        official = f"""
  official_script: /root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/scripts/order_{row['seed']}.sh
  model_name_or_path_in_official_script: initial_model/t5-large
  local_model_path: /root/autodl-tmp/model_cache/hf_snapshots/t5-large
  official_learning_rate: 1e-03
  official_epochs: 1
  official_train_batch_size: 8
  official_eval_batch_size: 128
  official_max_source_length: 512
  official_max_target_length: 50
  official_generation_max_length: 50
"""
    else:
        model_path = T5_SMALL
        base_path = T5_SMALL
        max_source, max_target, gen_tokens = 512, 128, 96
        train_lr = "1e-04"
        epochs = "1"
        batch = "1"
        official = """
  official_config: /root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/config/config.cfg
  official_run_script: /root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/run.sh
  official_metric_code: /root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/run_woz3.py
  official_model_type: lm
  official_decoder: sclstm
  official_exemplar_size: 250
"""

    metrics = ", ".join(f'"{m.strip()}"' for m in row["metrics"].split(";"))
    return f"""# Strict CCF-A v2 alignment config. Do not replace with Llama caveat configs.
experiment_name: {Path(row['config_name']).stem}
mode: ours
seed: {row['seed']}
strict_alignment:
  status: {row['status']}
  blocker: "{row['blocker']}"
  official_evidence: "{row['evidence']}"
paths:
  project_root: /root/Lora-Baselines
  processed_stream_file: {row['data_path']}
  results_dir: /root/autodl-tmp/lora-baselines-run_v1/results
data:
  suite: "{suite}"
  benchmark: "{row['benchmark']}"
  stream_format: unified_ccfa_stream
  ready: {str(row['status'] == 'ready').lower()}
model:
  architecture: seq2seq_lm
  task_type: seq2seq_lm
  backbone: "{row['backbone']}"
  hf_model_name_or_path: {model_path}
  base_model_path: {base_path}
  torch_dtype: bfloat16
  device: auto
  max_source_len: {max_source}
  max_target_len: {max_target}
  gen_max_new_tokens: {gen_tokens}
  gen_num_beams: 1
  gen_do_sample: false
lora:
  enabled: true
  r: 16
  alpha: 32
  dropout: 0.05
  target_modules: ["q", "v"]
train:
  lr: {train_lr}
  epochs_per_segment: {epochs}
  batch_size: {batch}
  hard_early_stop_enabled: false
modules:
  use_drift_detector: true
  use_lora_bank: true
  use_router: true
  use_overlap_loss: true
eval_normalization:
  enable_task_aware_score: true
  auto_short_answer_max_new_tokens: {str(suite == 'Standard PEFT CL').lower()}
output:
  run_name: {Path(row['config_name']).stem}
  tracking:
    use_wandb: false
paper:
  strict_ready: {str(row['status'] == 'ready').lower()}
  status: {row['status']}
  metrics: [{metrics}]
  postprocess: ccfa_postprocess/summary.json
  notes: "{row['blocker']}"
official_reference:{official}
"""


def write_configs(rs: list[dict[str, str]]) -> None:
    DOC_CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    RUNTIME_CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    for row in rs:
        doc_path = DOC_CONFIG_ROOT / row["config_name"]
        doc_path.write_text(config_text(row), encoding="utf-8")
        shutil.copy2(doc_path, RUNTIME_CONFIG_ROOT / row["config_name"])


def write_manifest(rs: list[dict[str, str]]) -> None:
    fields = ["suite", "benchmark", "seed", "backbone", "config_path", "command", "metrics", "status", "blocker"]
    for manifest, config_root in [(DOC_MANIFEST, DOC_CONFIG_ROOT), (RUNTIME_MANIFEST, RUNTIME_CONFIG_ROOT)]:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        with manifest.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rs:
                cfg = config_root / row["config_name"]
                writer.writerow(
                    {
                        "suite": row["suite"],
                        "benchmark": row["benchmark"],
                        "seed": row["seed"],
                        "backbone": row["backbone"],
                        "config_path": str(cfg),
                        "command": f"cd /root/Lora-Baselines/methods/ours/source/project_local && python core/train.py --config {cfg}",
                        "metrics": row["metrics"],
                        "status": row["status"],
                        "blocker": row["blocker"],
                    }
                )


def main() -> None:
    rs = rows()
    write_configs(rs)
    write_manifest(rs)
    print(f"Wrote {len(rs)} strict configs")
    print(f"Wrote {DOC_MANIFEST}")
    print(f"Wrote {RUNTIME_MANIFEST}")


if __name__ == "__main__":
    main()
