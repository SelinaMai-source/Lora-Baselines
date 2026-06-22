#!/usr/bin/env bash
set -euo pipefail

# Official ARPER/SCLSTM baseline wrapper.
# Source command: /root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/run.sh
# This wrapper keeps official run_woz3.py args and writes a dialogue-act config
# copy outside Git so Path B can be launched when the exact official backbone is
# required.

ARPER_ROOT="${ARPER_ROOT:-/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper}"
MODE="${1:-train}"
SEED="${ARPER_SEED:-1111}"
OUT_ROOT="${ARPER_OUT_ROOT:-/root/autodl-tmp/lora-baselines-run_v1/results/arper_official_sclstm}"
LOG_DIR="${ARPER_LOG_DIR:-/root/autodl-tmp/lora-baselines-run_v1/logs}"
CONFIG_PATH="${ARPER_RUNTIME_CONFIG:-${OUT_ROOT}/config_arper_woz3_unique_da.cfg}"

mkdir -p "${OUT_ROOT}" "${LOG_DIR}"
cd "${ARPER_ROOT}"

python - <<'PY'
from configparser import ConfigParser
from pathlib import Path
import os

root = Path(os.environ.get("ARPER_ROOT", "/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper"))
out_root = Path(os.environ.get("ARPER_OUT_ROOT", "/root/autodl-tmp/lora-baselines-run_v1/results/arper_official_sclstm"))
cfg_path = Path(os.environ.get("ARPER_RUNTIME_CONFIG", str(out_root / "config_arper_woz3_unique_da.cfg")))

cfg = ConfigParser()
cfg.read(root / "config/config.cfg")
cfg["EXPERIMENT"]["experiment_prefix"] = str(out_root / "experiments/da/") + "/"
cfg["DATA"]["feat_file"] = "./resource/woz3/feat_unique_da.json"
cfg["DATA"]["text_file"] = "./resource/woz3/text_unique_da.json"
cfg["DATA"]["data_split"] = "./resource/woz3/data_split/all_unique_da_datasplit.json"
cfg["DATA"]["granularity"] = "1"
cfg["DATA"]["task_seq"] = "1,7,0,6,4,2,8"
cfg["TESTING"]["output_log"] = "True"
cfg_path.parent.mkdir(parents=True, exist_ok=True)
with cfg_path.open("w", encoding="utf-8") as f:
    cfg.write(f)
print(cfg_path)
PY

echo "ARPER official SCLSTM wrapper"
echo "mode=${MODE}"
echo "config=${CONFIG_PATH}"
echo "out_root=${OUT_ROOT}"

if [[ "${MODE}" == "recover" || "${MODE}" == "test" ]]; then
    CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}" python3 -W ignore run_woz3.py \
        --mode "${MODE}" \
        --random_seed "${SEED}" \
        --sv_len_weight 0.5 \
        --adaptive True \
        --ewc_importance 300000 \
        --config_file "${CONFIG_PATH}" \
        --recovered_tasks "${ARPER_RECOVERED_TASKS:-0}"
else
    CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}" python3 -W ignore run_woz3.py \
        --mode "${MODE}" \
        --random_seed "${SEED}" \
        --sv_len_weight 0.5 \
        --adaptive True \
        --ewc_importance 300000 \
        --lr 0.005 \
        --dropout 0 \
        --_lambda 2.0 \
        --config_file "${CONFIG_PATH}"
fi
