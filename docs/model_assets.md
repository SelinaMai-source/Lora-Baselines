# Model Assets

This repository keeps source code, configs, and small metadata in Git. Large model
weights must stay outside Git under `/root/autodl-tmp/model_cache` or another
local cache root.

Current local cache root:

- `MODEL_CACHE_ROOT=/root/autodl-tmp/model_cache`
- `HF_HOME=/root/autodl-tmp/hf_cache`
- Proxy used for the latest preparation attempt: `HTTP_PROXY=http://127.0.0.1:7890`
  and `HTTPS_PROXY=http://127.0.0.1:7890`

Do not commit anything from `/root/autodl-tmp/model_cache`, `/root/autodl-tmp/hf_cache`,
proxy config directories, tokens, or downloaded model weight files.

## Local Status

Observed on 2026-06-22:

- `/root/autodl-tmp` had about 43G free before the latest T5 download attempt.
- `/root/autodl-tmp/model_cache/meta-llama/Llama-3.1-8B-Instruct` contains a
  complete local safetensors snapshot and is usable by the current causal-LM
  ours runner. It is used only for caveat-ready full-data runs, not as the
  paper-strict T5 comparison backbone.
- `/root/autodl-tmp/model_cache/hf_snapshots/t5-large` contains a completed
  T5-large snapshot including `pytorch_model.bin` (`2,950,825,948` bytes),
  `model.safetensors`, config, tokenizer files, and `spiece.model`. The
  standard Hugging Face snapshot API failed through the mirror, so the binary
  was completed with `curl -C -` from
  `https://hf-mirror.com/t5-large/resolve/main/pytorch_model.bin`.
- `/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt`
  contains a completed base snapshot including `pytorch_model.bin`, config,
  tokenizer files, and `spiece.model`.
- No verified CITB 100-SuperNI-init checkpoint is present under
  `/root/autodl-tmp/lora-baselines-run_v1/models/citb_stage1_superni_t5_small_lm_adapt`.
  Web/repo checks did not find an author-provided checkpoint download; use the
  official CITB Stage-1 script to produce it before strict CITB runs.
- `/root/autodl-tmp/model_cache/ThomasNLG/CT0-11B` exists and contains small
  Hugging Face config/tokenizer files only. Size observed: about 1.4M.
- `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k` exists and contains
  LFPT5/T5-large checkpoint metadata only: `checkpoint`, `model-info.txt`,
  `operative_config.gin`, and `model.ckpt-1100000.index`. Size observed:
  about 128K.
- `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k-pytorch` exists but is empty.

A local Llama causal-LM snapshot is ready for the current implementation.
`google/t5-small-lm-adapt` and `t5-large` are now present locally. LFPT5 still
needs `gsutil` or an equivalent Google Cloud Storage downloader for the official
`gs://t5-data/...` checkpoint objects if we choose the LFPT5-specific
LM-adapted T5-large route.

## v2 CCF-A Required Assets

### CITB

Required:

- `google/t5-small-lm-adapt` as the base LM-adapted T5-small checkpoint.
- The CITB initial instruction-tuned checkpoint trained from 100 SuperNI tasks.
- Official CITB task/data files from `benchmark/instrdialog/source`.

Current state:

- Official CITB source/data are vendored.
- Official CITB source/data are also downloaded outside Git at
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources/citb`.
- A `google/t5-small-lm-adapt` snapshot is complete under
  `/root/autodl-tmp/model_cache/hf_snapshots/google__t5-small-lm-adapt`.
- CITB does not provide a ready-made 100-SuperNI-init checkpoint in the README;
  it provides the Stage-1 training command using `google/t5-small-lm-adapt`.
- The ours runner now has a T5 seq2seq PEFT path, but strict CITB rows remain
  `needs-stage1` until the 100-SuperNI-init checkpoint is actually produced.

### Standard T5-Large PEFT CL

Required:

- T5-large runtime checkpoint compatible with O-LoRA/LFPT5/Progressive-Prompts
  comparisons.
- Converted/loaded official O-LoRA `CL_Benchmark` task data and order configs.

Current state:

- O-LoRA source/configs are vendored.
- O-LoRA, LFPT5, and Progressive Prompts official sources are also downloaded
  outside Git under `/root/autodl-tmp/lora-baselines-run_v1/external_sources`.
- The local `seqglue` stream is not the official standard PEFT CL suite.
- Official O-LoRA streams are generated under
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/standard_peft`.
- T5-large is complete and locally readable at
  `/root/autodl-tmp/model_cache/hf_snapshots/t5-large`; validation with
  Transformers `AutoConfig` and `AutoTokenizer` succeeded.
- Ours runner compatibility still blocks launch because the current path is
  causal-LM PEFT, not T5 seq2seq PEFT.

### Dialogue NLG / MultiWOZ CL

Required:

- ARPER MultiWOZ-2.0 source/data conversion and official BLEU-4/SER scorer.
- ToDCL 37-domain data and BLEU/EER scorer only if the extension route is used.

Current state:

- Generic MultiWOZ and MultiWOZ evaluation sources are vendored.
- ARPER and ToDCL official sources are downloaded outside Git under
  `/root/autodl-tmp/lora-baselines-run_v1/external_sources`.
- ARPER WOZ3 streams are generated under
  `/root/autodl-tmp/lora-baselines-run_v1/data/ccfa_three_suite/arper`.
- The current local MultiWOZ train50/eval10 stream is diagnostic only and is
  not used as the final ARPER stream.

## Continual-T0 / CT0

Official model:

- <https://huggingface.co/ThomasNLG/CT0-11B>

Target path:

- `/root/autodl-tmp/model_cache/ThomasNLG/CT0-11B`

Current state:

- `partial`: config/tokenizer metadata is present locally.
- `blocked`: CT0-11B weights are not downloaded because `/root/autodl-tmp`
  currently has about 3.1G free, which is not enough for an 11B model snapshot.
- Hugging Face access was unauthenticated during the latest preparation attempt;
  the metadata request succeeded, but full downloads may be rate limited unless
  `HF_TOKEN` is provided in the environment.

Metadata refresh command:

```bash
MODEL_CACHE_ROOT=/root/autodl-tmp/model_cache \
HF_HOME=/root/autodl-tmp/hf_cache \
HTTP_PROXY=http://127.0.0.1:7890 \
HTTPS_PROXY=http://127.0.0.1:7890 \
bash docs/prepare_model_assets.sh ct0-metadata
```

Full resume command, only after freeing enough space:

```bash
MODEL_CACHE_ROOT=/root/autodl-tmp/model_cache \
HF_HOME=/root/autodl-tmp/hf_cache \
HTTP_PROXY=http://127.0.0.1:7890 \
HTTPS_PROXY=http://127.0.0.1:7890 \
DOWNLOAD_CT0_WEIGHTS=1 \
bash docs/prepare_model_assets.sh ct0
```

Verify:

```bash
du -sh /root/autodl-tmp/model_cache/ThomasNLG/CT0-11B
python - <<'PY'
from pathlib import Path
root = Path("/root/autodl-tmp/model_cache/ThomasNLG/CT0-11B")
print("config:", (root / "config.json").exists())
print("tokenizer:", (root / "tokenizer.json").exists())
print("weights:", any(root.glob("*.bin")) or any(root.glob("*.safetensors")))
PY
```

Reference this model from local experiment overrides with:

```bash
--model_name_or_path /root/autodl-tmp/model_cache/ThomasNLG/CT0-11B
```

If a config uses another field name, use the same local directory for
`model_name_or_path`, `hf_model_name_or_path`, or the method-specific equivalent.

## LFPT5

Official source:

- <https://github.com/qcwthu/Lifelong-Fewshot-Language-Learning>

Official checkpoint instructions from the vendored LFPT5 README:

- `methods/lfpt5/source/README.md`
- LM-adapted T5 checkpoint:
  <https://github.com/google-research/text-to-text-transfer-transformer/blob/main/released_checkpoints.md#lm-adapted-t511lm100k>
- Official GCS prefix:
  `gs://t5-data/pretrained_models/t5.1.1.lm100k.large/`

Target paths:

- TensorFlow checkpoint:
  `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k`
- Converted PyTorch checkpoint:
  `/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k-pytorch`

Current state:

- `partial`: small metadata/index files are present locally.
- `blocked`: the four large TensorFlow data shards and optional `.meta` file are
  not downloaded because only about 3.1G is free.
- `blocked`: `gsutil` is not currently installed, so the official `gs://...`
  command cannot run as-is.
- `blocked`: PyTorch conversion cannot run until the complete TensorFlow
  checkpoint is present.

Metadata refresh command:

```bash
MODEL_CACHE_ROOT=/root/autodl-tmp/model_cache \
HTTP_PROXY=http://127.0.0.1:7890 \
HTTPS_PROXY=http://127.0.0.1:7890 \
bash docs/prepare_model_assets.sh lfpt5-metadata
```

Full resume command, only after freeing enough space and installing `gsutil`:

```bash
MODEL_CACHE_ROOT=/root/autodl-tmp/model_cache \
HF_HOME=/root/autodl-tmp/hf_cache \
HTTP_PROXY=http://127.0.0.1:7890 \
HTTPS_PROXY=http://127.0.0.1:7890 \
DOWNLOAD_LFPT5_WEIGHTS=1 \
CONVERT_LFPT5=1 \
bash docs/prepare_model_assets.sh lfpt5
```

The official TensorFlow files are:

- `checkpoint`
- `model-info.txt`
- `model.ckpt-1100000.data-00000-of-00004`
- `model.ckpt-1100000.data-00001-of-00004`
- `model.ckpt-1100000.data-00002-of-00004`
- `model.ckpt-1100000.data-00003-of-00004`
- `model.ckpt-1100000.index`
- `model.ckpt-1100000.meta`
- `operative_config.gin`

Verify:

```bash
python - <<'PY'
from pathlib import Path
raw = Path("/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k")
pt = Path("/root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k-pytorch")
required = [
    "checkpoint",
    "model-info.txt",
    "model.ckpt-1100000.data-00000-of-00004",
    "model.ckpt-1100000.data-00001-of-00004",
    "model.ckpt-1100000.data-00002-of-00004",
    "model.ckpt-1100000.data-00003-of-00004",
    "model.ckpt-1100000.index",
    "operative_config.gin",
]
missing = [name for name in required if not (raw / name).exists()]
print("raw_complete:", not missing)
print("missing:", missing)
print("pytorch_model:", (pt / "pytorch_model.bin").exists())
PY
```

Reference the converted checkpoint in LFPT5 scripts by overriding the vendored
defaults:

```bash
--model_name google/t5-v1_1-large \
--lm_adapted_path /root/autodl-tmp/model_cache/lfpt5/t5.1.1.lm100k-pytorch/pytorch_model.bin \
--cache_path /root/autodl-tmp/hf_cache
```

The vendored shell scripts currently contain original author paths such as
`/data/qin/lm_adapted_t5model/...`; prefer local command-line overrides or a
private, uncommitted script copy instead of committing machine-specific config
rewrites.
