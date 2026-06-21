#!/usr/bin/env bash
set -euo pipefail

# Prepare local model assets outside Git.
#
# Defaults:
#   MODEL_CACHE_ROOT=/root/autodl-tmp/model_cache
#   HF_HOME=/root/autodl-tmp/hf_cache
#
# Optional proxy usage:
#   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 \
#     bash docs/prepare_model_assets.sh all
#
# Full weight downloads are opt-in:
#   DOWNLOAD_CT0_WEIGHTS=1 bash docs/prepare_model_assets.sh ct0
#   DOWNLOAD_LFPT5_WEIGHTS=1 CONVERT_LFPT5=1 bash docs/prepare_model_assets.sh lfpt5

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_CACHE_ROOT="${MODEL_CACHE_ROOT:-/root/autodl-tmp/model_cache}"
HF_HOME="${HF_HOME:-/root/autodl-tmp/hf_cache}"
LOG_DIR="${MODEL_CACHE_ROOT}/logs"

export HF_HOME

mkdir -p "${MODEL_CACHE_ROOT}" "${HF_HOME}" "${LOG_DIR}"

usage() {
  cat <<'EOF'
Usage: bash docs/prepare_model_assets.sh [all|ct0|ct0-metadata|lfpt5|lfpt5-metadata]

Environment:
  MODEL_CACHE_ROOT        Default: /root/autodl-tmp/model_cache
  HF_HOME                 Default: /root/autodl-tmp/hf_cache
  HTTP_PROXY/HTTPS_PROXY  Optional proxy settings
  HF_TOKEN                Optional Hugging Face token, if required by the hub
  DOWNLOAD_CT0_WEIGHTS    Set to 1 to download full ThomasNLG/CT0-11B snapshot
  DOWNLOAD_LFPT5_WEIGHTS  Set to 1 to download full LFPT5 TensorFlow checkpoint
  CONVERT_LFPT5           Set to 1 to convert LFPT5 TensorFlow checkpoint to PyTorch
EOF
}

need_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "${command_name}" >&2
    return 1
  fi
}

print_space() {
  df -h "${MODEL_CACHE_ROOT}" || true
}

download_ct0_metadata() {
  local dest="${MODEL_CACHE_ROOT}/ThomasNLG/CT0-11B"
  mkdir -p "${dest}"
  need_command hf

  printf 'Downloading CT0 metadata to %s\n' "${dest}"
  hf download ThomasNLG/CT0-11B \
    config.json \
    tokenizer.json \
    tokenizer_config.json \
    special_tokens_map.json \
    --local-dir "${dest}" \
    >"${LOG_DIR}/ct0_metadata_download.log" 2>&1
}

download_ct0_full() {
  local dest="${MODEL_CACHE_ROOT}/ThomasNLG/CT0-11B"
  mkdir -p "${dest}"
  need_command hf

  if [ "${DOWNLOAD_CT0_WEIGHTS:-0}" != "1" ]; then
    printf 'Skipping CT0 full weights. Set DOWNLOAD_CT0_WEIGHTS=1 to enable.\n'
    return 0
  fi

  print_space
  printf 'Downloading full CT0 snapshot to %s\n' "${dest}"
  hf download ThomasNLG/CT0-11B \
    --local-dir "${dest}" \
    >"${LOG_DIR}/ct0_full_download.log" 2>&1
}

download_lfpt5_metadata() {
  local dest="${MODEL_CACHE_ROOT}/lfpt5/t5.1.1.lm100k"
  mkdir -p "${dest}"

  python - "$dest" "${LOG_DIR}/lfpt5_metadata_download.log" <<'PY'
from pathlib import Path
import os
import sys
import urllib.request

dest = Path(sys.argv[1])
log = Path(sys.argv[2])
base = "https://storage.googleapis.com/t5-data/pretrained_models/t5.1.1.lm100k.large"
files = [
    "checkpoint",
    "model-info.txt",
    "operative_config.gin",
    "model.ckpt-1100000.index",
]
proxy = urllib.request.ProxyHandler({
    "http": os.environ.get("HTTP_PROXY"),
    "https": os.environ.get("HTTPS_PROXY"),
})
opener = urllib.request.build_opener(proxy)
with log.open("w") as lf:
    for name in files:
        url = f"{base}/{name}"
        target = dest / name
        try:
            with opener.open(url, timeout=120) as response:
                target.write_bytes(response.read())
            lf.write(f"ok\t{name}\t{target.stat().st_size}\n")
        except Exception as exc:
            lf.write(f"failed\t{name}\t{type(exc).__name__}: {exc}\n")
            raise
PY
}

download_lfpt5_full() {
  local dest="${MODEL_CACHE_ROOT}/lfpt5/t5.1.1.lm100k"
  mkdir -p "${dest}"

  if [ "${DOWNLOAD_LFPT5_WEIGHTS:-0}" != "1" ]; then
    printf 'Skipping LFPT5 full TensorFlow checkpoint. Set DOWNLOAD_LFPT5_WEIGHTS=1 to enable.\n'
    return 0
  fi

  need_command gsutil
  print_space
  printf 'Downloading full LFPT5 TensorFlow checkpoint to %s\n' "${dest}"
  gsutil -m cp \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/checkpoint" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model-info.txt" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model.ckpt-1100000.data-00000-of-00004" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model.ckpt-1100000.data-00001-of-00004" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model.ckpt-1100000.data-00002-of-00004" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model.ckpt-1100000.data-00003-of-00004" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model.ckpt-1100000.index" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/model.ckpt-1100000.meta" \
    "gs://t5-data/pretrained_models/t5.1.1.lm100k.large/operative_config.gin" \
    "${dest}/" \
    >"${LOG_DIR}/lfpt5_full_download.log" 2>&1
}

convert_lfpt5() {
  local raw="${MODEL_CACHE_ROOT}/lfpt5/t5.1.1.lm100k"
  local out="${MODEL_CACHE_ROOT}/lfpt5/t5.1.1.lm100k-pytorch"
  local script="${ROOT_DIR}/methods/lfpt5/source/convertmodel.py"

  if [ "${CONVERT_LFPT5:-0}" != "1" ]; then
    printf 'Skipping LFPT5 PyTorch conversion. Set CONVERT_LFPT5=1 to enable.\n'
    return 0
  fi

  for required in checkpoint model.ckpt-1100000.index model.ckpt-1100000.data-00000-of-00004 model.ckpt-1100000.data-00001-of-00004 model.ckpt-1100000.data-00002-of-00004 model.ckpt-1100000.data-00003-of-00004; do
    if [ ! -e "${raw}/${required}" ]; then
      printf 'Cannot convert LFPT5; missing %s\n' "${raw}/${required}" >&2
      return 1
    fi
  done

  mkdir -p "${out}"
  python - "$script" "$raw" "$out" <<'PY'
import importlib.util
import sys

script, raw, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("lfpt5_convertmodel", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.convert_tf_checkpoint_to_pytorch(raw, out, "google/t5-v1_1-large")
PY
}

verify_assets() {
  python - "$MODEL_CACHE_ROOT" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
ct0 = root / "ThomasNLG" / "CT0-11B"
lfpt5 = root / "lfpt5" / "t5.1.1.lm100k"
lfpt5_pt = root / "lfpt5" / "t5.1.1.lm100k-pytorch"

ct0_weights = any(ct0.glob("*.bin")) or any(ct0.glob("*.safetensors"))
lfpt5_required = [
    "checkpoint",
    "model-info.txt",
    "model.ckpt-1100000.data-00000-of-00004",
    "model.ckpt-1100000.data-00001-of-00004",
    "model.ckpt-1100000.data-00002-of-00004",
    "model.ckpt-1100000.data-00003-of-00004",
    "model.ckpt-1100000.index",
    "operative_config.gin",
]
lfpt5_missing = [name for name in lfpt5_required if not (lfpt5 / name).exists()]

print(f"ct0_metadata={((ct0 / 'config.json').exists() and (ct0 / 'tokenizer.json').exists())}")
print(f"ct0_weights={ct0_weights}")
print(f"lfpt5_tf_complete={not lfpt5_missing}")
print(f"lfpt5_tf_missing={lfpt5_missing}")
print(f"lfpt5_pytorch={(lfpt5_pt / 'pytorch_model.bin').exists()}")
PY
}

target="${1:-all}"

case "${target}" in
  all)
    download_ct0_metadata
    download_ct0_full
    download_lfpt5_metadata
    download_lfpt5_full
    convert_lfpt5
    verify_assets
    ;;
  ct0)
    download_ct0_metadata
    download_ct0_full
    verify_assets
    ;;
  ct0-metadata)
    download_ct0_metadata
    verify_assets
    ;;
  lfpt5)
    download_lfpt5_metadata
    download_lfpt5_full
    convert_lfpt5
    verify_assets
    ;;
  lfpt5-metadata)
    download_lfpt5_metadata
    verify_assets
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
