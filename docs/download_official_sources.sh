#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMMIT_LOG="${ROOT_DIR}/docs/vendor_commits.tsv"

clone_vendor() {
  local repo="$1"
  local dest="$2"
  local label="$3"

  if [ -e "${dest}" ]; then
    echo "SKIP ${label}: ${dest} already exists" >&2
    return 0
  fi

  mkdir -p "$(dirname "${dest}")"
  git clone --depth 1 "${repo}" "${dest}"
  local sha
  sha="$(git -C "${dest}" rev-parse HEAD)"
  printf "%s\t%s\t%s\n" "${label}" "${repo}" "${sha}" >> "${COMMIT_LOG}"
  rm -rf "${dest}/.git"
}

mkdir -p "${ROOT_DIR}/methods" "${ROOT_DIR}/benchmark" "${ROOT_DIR}/docs"
printf "label\trepo\tcommit\n" > "${COMMIT_LOG}"

clone_vendor "git@github.com:cmnfriend/O-LoRA.git" "${ROOT_DIR}/methods/o_lora/source" "method:o_lora"
clone_vendor "git@github.com:arazd/ProgressivePrompts.git" "${ROOT_DIR}/methods/progressive_prompts/source" "method:progressive_prompts"
clone_vendor "git@github.com:ThomasScialom/T0_continual_learning.git" "${ROOT_DIR}/methods/continual_t0/source" "method:continual_t0"
clone_vendor "git@github.com:qcwthu/Lifelong-Fewshot-Language-Learning.git" "${ROOT_DIR}/methods/lfpt5/source" "method:lfpt5"

clone_vendor "git@github.com:hyintell/CITB.git" "${ROOT_DIR}/benchmark/instrdialog/source" "benchmark:instrdialog"
clone_vendor "git@github.com:hyintell/CITB.git" "${ROOT_DIR}/benchmark/instrdialogpp/source" "benchmark:instrdialogpp"
clone_vendor "git@github.com:BeyonderXX/TRACE.git" "${ROOT_DIR}/benchmark/trace/source" "benchmark:trace"
clone_vendor "git@github.com:budzianowski/multiwoz.git" "${ROOT_DIR}/benchmark/multiwoz_nlg/source_multiwoz" "benchmark:multiwoz_nlg:dataset"
clone_vendor "git@github.com:Tomiinek/MultiWOZ_Evaluation.git" "${ROOT_DIR}/benchmark/multiwoz_nlg/source_evaluation" "benchmark:multiwoz_nlg:evaluation"

echo "Vendor download complete. Review ${COMMIT_LOG} and update docs/source_manifest.md with exact commits."
