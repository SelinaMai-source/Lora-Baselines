#!/usr/bin/env bash
set -euo pipefail

# Optional proxy usage:
#   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 \
#     bash docs/download_official_sources.sh
#
# This helper never writes git config and never downloads model weights,
# gated datasets, or Google Drive material.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMMIT_LOG="${ROOT_DIR}/docs/vendor_commits.tsv"
ATTEMPT_LOG="${ROOT_DIR}/docs/vendor_download_attempts.tsv"

clone_vendor() {
  local label="$1"
  local repo="$2"
  local dest="$3"

  if [ -e "${dest}" ]; then
    printf "%s\t%s\tgit-clone\tskipped\tdestination exists\n" "${label}" "${repo}" >> "${ATTEMPT_LOG}"
    return 0
  fi

  mkdir -p "$(dirname "${dest}")"
  printf "%s\t%s\tgit-clone\tstarted\tofficial shallow clone\n" "${label}" "${repo}" >> "${ATTEMPT_LOG}"
  git clone --depth 1 "${repo}" "${dest}"
  local sha
  sha="$(git -C "${dest}" rev-parse HEAD)"
  rm -rf "${dest}/.git"
  printf "%s\t%s\t%s\t%s\tyes\tno\tofficial git clone at resolved HEAD\n" \
    "${label}" "${repo}" "${sha}" "${dest#${ROOT_DIR}/}" >> "${COMMIT_LOG}"
  printf "%s\t%s\tgit-clone\tok\t%s\n" "${label}" "${repo}" "${sha}" >> "${ATTEMPT_LOG}"
}

mkdir -p "${ROOT_DIR}/methods" "${ROOT_DIR}/benchmark" "${ROOT_DIR}/docs"
printf "label\tofficial_url\tcommit\ttarget_path\tproxy\tmirror\tverification\n" > "${COMMIT_LOG}"
printf "label\tofficial_url\tstage\tresult\tdetail\n" > "${ATTEMPT_LOG}"

clone_vendor "o_lora" "https://github.com/cmnfriend/O-LoRA.git" "${ROOT_DIR}/methods/o_lora/source"
clone_vendor "progressive_prompts" "https://github.com/arazd/ProgressivePrompts.git" "${ROOT_DIR}/methods/progressive_prompts/source"
clone_vendor "continual_t0" "https://github.com/ThomasScialom/T0_continual_learning.git" "${ROOT_DIR}/methods/continual_t0/source"
clone_vendor "lfpt5" "https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning.git" "${ROOT_DIR}/methods/lfpt5/source"
clone_vendor "citb_instrdialog" "https://github.com/hyintell/CITB.git" "${ROOT_DIR}/benchmark/instrdialog/source"
clone_vendor "citb_instrdialogpp" "https://github.com/hyintell/CITB.git" "${ROOT_DIR}/benchmark/instrdialogpp/source"
clone_vendor "trace" "https://github.com/BeyonderXX/TRACE.git" "${ROOT_DIR}/benchmark/trace/source"
clone_vendor "multiwoz" "https://github.com/budzianowski/multiwoz.git" "${ROOT_DIR}/benchmark/multiwoz_nlg/source_multiwoz"
clone_vendor "multiwoz_evaluation" "https://github.com/Tomiinek/MultiWOZ_Evaluation.git" "${ROOT_DIR}/benchmark/multiwoz_nlg/source_evaluation"

echo "Vendor download complete. Review ${COMMIT_LOG} and docs/source_manifest.md before committing."
