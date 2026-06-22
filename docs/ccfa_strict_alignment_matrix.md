# CCF-A Strict Alignment Matrix

Updated: 2026-06-22 20:15 UTC+8

Statuses mean: `ready` can be launched without known setting blockers;
`running-stage1` is actively producing the prerequisite checkpoint;
`ready` can be launched; `blocked` must not be reported as strict-ready.

## Suite Readiness

| Suite | Strict status | Local prepared paths | Remaining blocker |
|---|---|---|---|
| CITB InstrDialog | running-stage1 | Stage-1 tmux `ccfa_citb_stage1_superni`; log `/root/autodl-tmp/lora-baselines-run_v1/logs/citb_stage1_superni_seed469.log`; target `/root/autodl-tmp/model_cache/citb_superni_stage1/base_epoch15_lr1e-05_seed469` | Stage-1 checkpoint is still being generated; four official short-stream tasks have fewer than 500 train examples after the prepared 100 test + 50 dev allocation. |
| CITB InstrDialog++ | blocked | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialogpp_order*_train100_dev50_test100.json`; strict configs generated but blocked | Official long-stream scripts use `max_num_instances_per_eval_task=25`, conflicting with the requested `100/50/100`; some tasks also lack enough examples for that requested split. |
| Standard T5-Large PEFT CL | start-attempted / ready | O-LoRA `CL_Benchmark` streams under `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft`, local `t5-large`, strict configs | Launched in tmux `ccfa_standard_peft_strict_ours`; queue log `/root/autodl-tmp/lora-baselines-run_v1/logs/ccfa_standard_peft_strict_queue.log`. LFPT5/Progressive Prompt equivalence is cited through published comparison tables, not independently reproduced from their official repos. |
| Dialogue NLG / ARPER | ready / start-attempted | ARPER WOZ3 unique dialogue-act stream, official-equivalent scorer adapter, Path A ours T5 config, and Path B SCLSTM wrapper | Path A starts and trains; full run was terminated by local runtime/resource pressure, so keep CPU runtime or rerun when GPU is free. |

## Row Checklist

| Suite | Item | Official evidence path/link | Local prepared path | Status | Notes |
|---|---|---|---|---|---|
| CITB | Paper setup | `https://aclanthology.org/2023.findings-emnlp.633/`; local web/PDF notes confirm LM-adapted T5-small, 100 initial tasks, InstrDialog 500/50/100 | `/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt` | running-stage1 | Web search found no public `checkpoint-14000` download; official Stage-1 script is now running through the local wrapper. |
| CITB | Stage-1 command | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/run_initial_multitask_tuning.sh`; wrapper `docs/scripts/run_citb_stage1_superni_official_wrapper.sh` | target `/root/autodl-tmp/model_cache/citb_superni_stage1/base_epoch15_lr1e-05_seed469` | running-stage1 | Official params retained: T5-small LM-adapt, lr `1e-05`, epochs `15`, batch `8`, eval/save every `500`, best by `rougeL`; wrapper only overrides local paths/cache/proxy and modern library compatibility. |
| CITB | InstrDialog order/split | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/data/CIT_data/task_orders/stream=cl_dialogue_tasks/order{1,2,3}.txt`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/short_stream_scripts/run_cit_ft_instr.sh` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialog_order*_train500_dev50_test100.json` | running-stage1 | Official short script uses `max_num_instances_per_task=500`, `max_num_instances_per_eval_task=50`; test allocation is recorded in stream metadata. |
| CITB | InstrDialog++ order/split | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/data/CIT_data/task_orders/stream=cl_dialogue_long_tasks/order{1,2,3}.txt`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/long_stream_scripts/run_cit_ft_instr.sh` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialogpp_order*_train100_dev50_test100.json` | blocked | Official long script says train `100`, eval `25`; requested `100/50/100` is not script-strict. |
| CITB | Metrics | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/collect_results.py` | `docs/scripts/compute_ccfa_three_suite_metrics.py`; ours `ccfa_postprocess/score_matrix.json` | running-stage1 | AR maps to final average, FWT to next-task diagonal, BWT to final-vs-diagonal; Tinit/Tunseen require extra probes after Stage-1 completes. |
| Standard PEFT CL | O-LoRA model/order | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/README.md`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/scripts/order_{1,2,3}.sh` | `/root/autodl-tmp/model_cache/hf_snapshots/t5-large`; `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft/olora_standard_order*_t5large.json` | start-attempted | README requires `initial_model/t5-large`; scripts define three four-task orders and one epoch; ours strict queue is running in tmux `ccfa_standard_peft_strict_ours`. |
| Standard PEFT CL | O-LoRA task configs/data | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/configs/order*_configs/*/{train,dev,test}_tasks.json`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/CL_Benchmark` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft` | ready | Prepared streams are full-data official conversions, not local `seqglue` train50/eval10. |
| Standard PEFT CL | O-LoRA metric surface | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/src/run_uie_lora.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/src/uie_dataset_lora.py` | `docs/scripts/compute_ccfa_three_suite_metrics.py` | ready | Ours exports per-task matrices; final average accuracy/forgetting/BWT are computable. |
| Standard PEFT CL | LFPT5 source setting | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/lfpt5/README.md` | partial metadata under `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k` | blocked-for-reproduction | Official route needs GCS LM-adapted T5-large TF checkpoint and `convertmodel.py`; this is not required to launch ours on O-LoRA standard stream. |
| Standard PEFT CL | Progressive Prompts source setting | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/progressive_prompts/README.md` | source only | evidence-only | README example uses T5-large, prompt length `10`, `select_k_per_class=1000`; published O-LoRA/LB-CL tables are used for comparable baseline numbers. |
| Standard PEFT CL | LB-CL repo | NeurIPS/OpenReview pages; web search found no verified official repo | no local official repo | evidence-only | Use paper table only; do not cite an unofficial repo. |
| Dialogue NLG | ARPER official config | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/config/config.cfg`; wrapper `docs/scripts/run_arper_official_sclstm_wrapper.sh` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/arper/arper_woz3_unique_dialogue_act.json` | ready | Path A uses ours T5 seq2seq on the official WOZ3 DA stream; Path B wrapper launches official SCLSTM with DA config, task seq `1,7,0,6,4,2,8`, exemplar size `250`. |
| Dialogue NLG | ARPER metrics | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/run_woz3.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/bleu.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/util.py` | `core.metrics_utils` ARPER functions; `scripts/score_arper_woz3_outputs.py`; `ccfa_postprocess/summary.json` | ready | Official-equivalent SER counts `redunt/miss/total` from WOZ3 slot features and grouped multi-reference BLEU-4 over ours generated outputs. |
| Dialogue NLG | ToDCL backup | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl/README.md`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl/scorer.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl/results.txt` | official source/results local; raw upstream datasets not fully preprocessed locally | blocked | README documents 37 domains, NLG/E2E BLEU/EER; official result table contains Adapter NLG BLEU `21.7719` / EER `0.163975`. |

## Next Commands

CITB Stage-1 checkpoint generation is running:

```bash
tmux attach -t ccfa_citb_stage1_superni
# log: /root/autodl-tmp/lora-baselines-run_v1/logs/citb_stage1_superni_seed469.log
# target: /root/autodl-tmp/model_cache/citb_superni_stage1/base_epoch15_lr1e-05_seed469
```

Strict Standard PEFT queue launched:

```bash
tmux attach -t ccfa_standard_peft_strict_ours
# log: /root/autodl-tmp/lora-baselines-run_v1/logs/ccfa_standard_peft_strict_queue.log
```

ARPER Path A launch log: `/root/autodl-tmp/lora-baselines-run_v1/logs/arper_path_a_ours_seed1.log`; scorer adapter: `methods/ours/source/project_local/scripts/score_arper_woz3_outputs.py`.
