# CCF-A Strict Alignment Matrix

Updated: 2026-06-22 UTC+8

Statuses mean: `ready` can be launched without known setting blockers;
`needs-stage1` has official data/configs ready but requires producing a
prerequisite checkpoint; `blocked` must not be reported as strict-ready.

## Suite Readiness

| Suite | Strict status | Local prepared paths | Remaining blocker |
|---|---|---|---|
| CITB InstrDialog | needs-stage1 | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialog_order*_train500_dev50_test100.json`; strict configs under `docs/configs/ccfa_three_suite` and `/root/autodl-tmp/lora-baselines-run_v1/configs/ccfa_three_suite` | 100-SuperNI-init checkpoint is not downloaded/provided. Four official short-stream tasks have fewer than 500 train examples after the prepared 100 test + 50 dev allocation. |
| CITB InstrDialog++ | blocked | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialogpp_order*_train100_dev50_test100.json`; strict configs generated but blocked | Official long-stream scripts use `max_num_instances_per_eval_task=25`, conflicting with the requested `100/50/100`; some tasks also lack enough examples for that requested split. |
| Standard T5-Large PEFT CL | ready | O-LoRA `CL_Benchmark` streams under `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft`, local `t5-large`, strict configs | No launch blocker for ours on the O-LoRA official standard stream. LFPT5/Progressive Prompt equivalence is cited through published comparison tables, not independently reproduced from their official repos. |
| Dialogue NLG / ARPER | blocked | ARPER WOZ3 unique domain/dialogue-act streams and official source are local | Official ARPER SER scorer is not yet wired to ours generated outputs, and ours T5 seq2seq path is not the official SCLSTM setting. |

## Row Checklist

| Suite | Item | Official evidence path/link | Local prepared path | Status | Notes |
|---|---|---|---|---|---|
| CITB | Paper setup | `https://aclanthology.org/2023.findings-emnlp.633/`; local web/PDF notes confirm LM-adapted T5-small, 100 initial tasks, InstrDialog 500/50/100 | `/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt` | needs-stage1 | Web search found no public `checkpoint-14000` download; official repo provides Stage-1 script. |
| CITB | Stage-1 command | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/run_initial_multitask_tuning.sh` | target `/root/autodl-tmp/lora-baselines-run_v1/models/citb_stage1_superni_t5_small_lm_adapt/checkpoint-best` | needs-stage1 | Official script uses `google/t5-small-lm-adapt`, lr `1e-05`, epochs `15`, batch `8`, eval/save every `500`, best by `rougeL`. |
| CITB | InstrDialog order/split | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/data/CIT_data/task_orders/stream=cl_dialogue_tasks/order{1,2,3}.txt`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/short_stream_scripts/run_cit_ft_instr.sh` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialog_order*_train500_dev50_test100.json` | needs-stage1 | Official short script uses `max_num_instances_per_task=500`, `max_num_instances_per_eval_task=50`; test allocation is recorded in stream metadata. |
| CITB | InstrDialog++ order/split | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/data/CIT_data/task_orders/stream=cl_dialogue_long_tasks/order{1,2,3}.txt`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/long_stream_scripts/run_cit_ft_instr.sh` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/citb/citb_instrdialogpp_order*_train100_dev50_test100.json` | blocked | Official long script says train `100`, eval `25`; requested `100/50/100` is not script-strict. |
| CITB | Metrics | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/collect_results.py` | `docs/scripts/compute_ccfa_three_suite_metrics.py`; ours `ccfa_postprocess/score_matrix.json` | needs-stage1 | AR maps to final average, FWT to next-task diagonal, BWT to final-vs-diagonal; Tinit/Tunseen require extra probes. |
| Standard PEFT CL | O-LoRA model/order | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/README.md`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/scripts/order_{1,2,3}.sh` | `/root/autodl-tmp/model_cache/hf_snapshots/t5-large`; `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft/olora_standard_order*_t5large.json` | ready | README requires `initial_model/t5-large`; scripts define three four-task orders and one epoch. |
| Standard PEFT CL | O-LoRA task configs/data | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/configs/order*_configs/*/{train,dev,test}_tasks.json`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/CL_Benchmark` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft` | ready | Prepared streams are full-data official conversions, not local `seqglue` train50/eval10. |
| Standard PEFT CL | O-LoRA metric surface | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/src/run_uie_lora.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/o_lora/src/uie_dataset_lora.py` | `docs/scripts/compute_ccfa_three_suite_metrics.py` | ready | Ours exports per-task matrices; final average accuracy/forgetting/BWT are computable. |
| Standard PEFT CL | LFPT5 source setting | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/lfpt5/README.md` | partial metadata under `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k` | blocked-for-reproduction | Official route needs GCS LM-adapted T5-large TF checkpoint and `convertmodel.py`; this is not required to launch ours on O-LoRA standard stream. |
| Standard PEFT CL | Progressive Prompts source setting | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/progressive_prompts/README.md` | source only | evidence-only | README example uses T5-large, prompt length `10`, `select_k_per_class=1000`; published O-LoRA/LB-CL tables are used for comparable baseline numbers. |
| Standard PEFT CL | LB-CL repo | NeurIPS/OpenReview pages; web search found no verified official repo | no local official repo | evidence-only | Use paper table only; do not cite an unofficial repo. |
| Dialogue NLG | ARPER official config | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/config/config.cfg` | `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/arper/arper_woz3_unique_dialogue_act.json` | blocked | Config default domain seq is `0,5,2,1,3,4`; comment gives DA seq `1,7,0,6,4,2,8`; exemplar size `250`; model `lm`/SCLSTM. |
| Dialogue NLG | ARPER metrics | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/run_woz3.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/bleu.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/util.py` | `docs/scripts/compute_ccfa_three_suite_metrics.py` | blocked | Official SER uses `get_slot_error`; ours currently needs exact scorer integration over generated outputs. |
| Dialogue NLG | ToDCL backup | `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl/README.md`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl/scorer.py`; `/root/autodl-tmp/lora-baselines-run_v1/external_sources/todcl/results.txt` | official source/results local; raw upstream datasets not fully preprocessed locally | blocked | README documents 37 domains, NLG/E2E BLEU/EER; official result table contains Adapter NLG BLEU `21.7719` / EER `0.163975`. |

## Next Commands

Produce the missing CITB Stage-1 checkpoint:

```bash
cd /root/autodl-tmp/lora-baselines-run_v1/external_sources/citb
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 HF_HOME=/root/autodl-tmp/hf_cache bash scripts/run_initial_multitask_tuning.sh
```

Launch the strict-ready Standard PEFT order 1 run:

```bash
cd /root/Lora-Baselines/methods/ours/source/project_local
python core/train.py --config /root/autodl-tmp/lora-baselines-run_v1/configs/ccfa_three_suite/standard_peft_cl_o_lora_standard_order1_seed1_ours_strict.yaml
```
