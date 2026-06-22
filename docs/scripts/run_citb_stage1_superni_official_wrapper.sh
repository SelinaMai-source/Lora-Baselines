#!/usr/bin/env bash
set -euo pipefail

# Official parameter source:
# /root/autodl-tmp/lora-baselines-run_v1/external_sources/citb/scripts/run_initial_multitask_tuning.sh
# This wrapper only pins local paths/cache/proxy/output for the paper's Stage-1
# 100-SuperNI initial multitask tuning checkpoint.

CITB_ROOT="${CITB_ROOT:-/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb}"
LOCAL_MODEL="${CITB_STAGE1_MODEL:-/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt}"
HF_HOME="${HF_HOME:-/root/autodl-tmp/model_cache/hf_home}"
TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-/root/autodl-tmp/model_cache/hf_transformers}"
HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-/root/autodl-tmp/model_cache/hf_datasets}"
OUTPUT_ROOT="${CITB_STAGE1_OUTPUT_ROOT:-/root/autodl-tmp/model_cache/citb_superni_stage1}"
LOG_DIR="${CITB_STAGE1_LOG_DIR:-/root/autodl-tmp/lora-baselines-run_v1/logs}"
SEED="${CITB_STAGE1_SEED:-$(shuf -i 10-999 -n 1)}"

export HF_HOME TRANSFORMERS_CACHE HF_DATASETS_CACHE
export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7890}"
export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7890}"
export ALL_PROXY="${ALL_PROXY:-http://127.0.0.1:7890}"
export NO_PROXY="${NO_PROXY:-localhost,127.0.0.1}"

mkdir -p "${OUTPUT_ROOT}" "${LOG_DIR}" "${HF_HOME}" "${TRANSFORMERS_CACHE}" "${HF_DATASETS_CACHE}"
cd "${CITB_ROOT}"

per_device_train_batch_size=8
per_device_eval_batch_size=32
learning_rate=1e-05
num_train_epochs=15
gradient_accumulation_steps=1

data_dir_for_official_test="data/CIT_data/official_test_data"
data_dir="data/CIT_data/initial_multitask_learning/defintion_pos_2"
task_dir="data/tasks/"
output_dir="${OUTPUT_ROOT}/base_epoch${num_train_epochs}_lr${learning_rate}_seed${SEED}"

echo "CITB Stage-1 official wrapper"
echo "citb_root=${CITB_ROOT}"
echo "model=${LOCAL_MODEL}"
echo "seed=${SEED}"
echo "output_dir=${output_dir}"
echo "log_dir=${LOG_DIR}"
echo "hf_home=${HF_HOME}"

python continual_learning/run_initial_multitask_tuning.py \
    --do_train \
    --do_eval \
    --do_predict \
    --predict_with_generate \
    --model_name_or_path "${LOCAL_MODEL}" \
    --data_dir "${data_dir}" \
    --data_dir_for_official_test "${data_dir_for_official_test}" \
    --max_source_length 1024 \
    --max_target_length 128 \
    --generation_max_length 128 \
    --add_task_name False \
    --add_task_definition True \
    --num_pos_examples 2 \
    --num_neg_examples 0 \
    --add_explanation False \
    --tk_instruct False \
    --data_dir "${data_dir}" \
    --task_dir "${task_dir}" \
    --output_dir "${output_dir}" \
    --cache_dir "${HF_HOME}" \
    --overwrite_cache \
    --per_device_train_batch_size "${per_device_train_batch_size}" \
    --per_device_eval_batch_size "${per_device_eval_batch_size}" \
    --gradient_accumulation_steps "${gradient_accumulation_steps}" \
    --learning_rate "${learning_rate}" \
    --num_train_epochs "${num_train_epochs}" \
    --lr_scheduler_type constant \
    --warmup_steps 0 \
    --logging_strategy steps \
    --logging_steps 250 \
    --eval_strategy steps \
    --eval_steps 500 \
    --save_strategy steps \
    --save_steps 500 \
    --save_total_limit 1 \
    --load_best_model_at_end \
    --metric_for_best_model 'rougeL' \
    --bf16 \
    --run_name "initial_multitask_model" \
    --seed "${SEED}"
