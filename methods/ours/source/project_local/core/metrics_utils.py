"""Shared token-level metrics for eval (deduped from evaluate.py)."""
from __future__ import annotations

import math
from pathlib import Path
import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

_NLG_METRIC_LIBS: Dict[str, bool] = {}


def token_f1(pred: str, gold: str) -> float:
    p = [t for t in pred.split() if t]
    g = [t for t in gold.split() if t]
    if not p and not g:
        return 1.0
    if not p or not g:
        return 0.0
    g_counts: Dict[str, int] = {}
    for t in g:
        g_counts[t] = g_counts.get(t, 0) + 1
    tp = 0
    for t in p:
        c = g_counts.get(t, 0)
        if c > 0:
            tp += 1
            g_counts[t] = c - 1
    prec = tp / max(1, len(p))
    rec = tp / max(1, len(g))
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)


def lcs_length(a_tokens: List[str], b_tokens: List[str]) -> int:
    n, m = len(a_tokens), len(b_tokens)
    if n == 0 or m == 0:
        return 0
    dp = [0] * (m + 1)
    for i in range(1, n + 1):
        prev = 0
        for j in range(1, m + 1):
            cur = dp[j]
            if a_tokens[i - 1] == b_tokens[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = cur
    return int(dp[m])


def lcs_overlap(pred: str, gold: str) -> float:
    a = pred.split()
    b = gold.split()
    if not a or not b:
        return 0.0
    lcs = lcs_length(a, b)
    return float(lcs / max(1, len(b)))


def rouge_l_fscore(pred: str, gold: str) -> float:
    """Token-level ROUGE-L F1 (fallback when rouge-score is unavailable)."""
    if bool(_NLG_METRIC_LIBS.get("rouge_score")):
        try:
            from rouge_score import rouge_scorer

            scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
            return float(scorer.score(gold, pred)["rougeL"].fmeasure)
        except Exception:
            pass
    a = [t for t in pred.split() if t]
    b = [t for t in gold.split() if t]
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    lcs = lcs_length(a, b)
    prec = lcs / max(1, len(a))
    rec = lcs / max(1, len(b))
    if prec + rec == 0:
        return 0.0
    return float(2 * prec * rec / (prec + rec))


def sentence_bleu4(pred: str, gold: str) -> float:
    """Sentence BLEU-4 with add-one smoothing; prefers sacrebleu when installed."""
    if bool(_NLG_METRIC_LIBS.get("sacrebleu")):
        try:
            from sacrebleu.metrics import BLEU

            return float(BLEU().sentence_score(pred, [gold]).score / 100.0)
        except Exception:
            pass
    hyp = [t for t in pred.split() if t]
    ref = [t for t in gold.split() if t]
    if not hyp and not ref:
        return 1.0
    if not hyp or not ref:
        return 0.0
    max_n = min(4, len(hyp), len(ref))
    if max_n <= 0:
        return 0.0
    weights = [0.25] * 4
    weight_sum = sum(weights[:max_n])
    norm_weights = [w / weight_sum for w in weights[:max_n]]
    log_precisions: List[float] = []
    for n in range(1, max_n + 1):
        hyp_ngrams: Dict[Tuple[str, ...], int] = {}
        for i in range(len(hyp) - n + 1):
            ng = tuple(hyp[i : i + n])
            hyp_ngrams[ng] = hyp_ngrams.get(ng, 0) + 1
        ref_ngrams: Dict[Tuple[str, ...], int] = {}
        for i in range(len(ref) - n + 1):
            ng = tuple(ref[i : i + n])
            ref_ngrams[ng] = ref_ngrams.get(ng, 0) + 1
        overlap = 0
        for ng, c in hyp_ngrams.items():
            overlap += min(c, ref_ngrams.get(ng, 0))
        precision = (overlap + 1.0) / (max(1, len(hyp) - n + 1) + 1.0)
        log_precisions.append(float(precision))
    if any(p <= 0 for p in log_precisions):
        return 0.0
    s = sum(w * math.log(p) for w, p in zip(norm_weights, log_precisions))
    ref_len, hyp_len = len(ref), len(hyp)
    if hyp_len > ref_len:
        bp = 1.0
    else:
        bp = math.exp(1.0 - ref_len / max(1, hyp_len))
    return float(bp * math.exp(s))


def corpus_bleu4(predictions: List[str], references: List[str]) -> float:
    """Corpus BLEU-4 compatible with ARPER's NLTK corpus_bleu path when available."""
    pairs = [(str(p or ""), str(r or "")) for p, r in zip(predictions, references)]
    if not pairs:
        return 0.0
    try:
        from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu

        refs = [[[tok for tok in ref.split() if tok]] for _pred, ref in pairs]
        hyps = [[tok for tok in pred.split() if tok] for pred, _ref in pairs]
        return float(corpus_bleu(refs, hyps, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=SmoothingFunction().method1))
    except Exception:
        vals = [sentence_bleu4(pred, ref) for pred, ref in pairs]
        return float(sum(vals) / max(1, len(vals)))


def starts_incorrectly(pred: str, gold: str) -> bool:
    p = [t for t in pred.split() if t]
    g = [t for t in gold.split() if t]
    if not p or not g:
        return False
    k = min(3, len(p), len(g))
    return p[:k] != g[:k]


_DIALOGUE_ACT_RE = re.compile(r"([A-Za-z0-9_-]+)\((.*?)\)")
_DIALOGUE_ACT_SLOT_RE = re.compile(r"([A-Za-z0-9_-]+)\s*=\s*\"([^\"]*)\"")
_NON_ENTITY_VALUES = {"true", "false", "yes", "no", "?", "none", ""}
DEFAULT_ARPER_WOZ3_TEMPLATE = Path(
    "/root/autodl-tmp/lora-baselines-run_v1/external_sources/arper/resource/woz3/template.txt"
)
_ARPER_TEMPLATE_BASES_CACHE: Dict[str, Tuple[str, ...]] = {}


def parse_dialogue_act_values(act_text: str) -> List[str]:
    """Extract entity values from AdapterCL-style dialogue acts.

    MultiWOZ NLG inputs encode required content as strings such as
    `restaurant_inform(name="foo",area="centre")`. The published dialogue NLG
    scorer checks whether these required values appear in the generated text.
    """

    values: List[str] = []
    for _intent, body in _DIALOGUE_ACT_RE.findall(str(act_text or "")):
        for _slot, value in _DIALOGUE_ACT_SLOT_RE.findall(body):
            normalized = value.strip().lower()
            if normalized not in _NON_ENTITY_VALUES:
                values.append(normalized)
    return values


def dialogue_slot_error_rate(act_text: str, prediction: str) -> Optional[float]:
    """Return missing required slot-value rate, or None when no slots exist.

    This mirrors the available AdapterCL/ToDCL NLG `EER` implementation's
    missing-entity component: missing required act values divided by the number
    of required act values. Superfluous-slot counting is not possible from the
    local `instruction/input/output` stream alone because it has no ontology or
    delexicalized entity inventory.
    """

    values = parse_dialogue_act_values(act_text)
    if not values:
        return None
    pred = str(prediction or "").lower()
    missing = sum(1 for value in values if value not in pred)
    return float(missing / max(1, len(values)))


def dialogue_slot_error_counts(act_text: str, prediction: str) -> Dict[str, int]:
    values = parse_dialogue_act_values(act_text)
    pred = str(prediction or "").lower()
    missing = sum(1 for value in values if value not in pred)
    return {"required_slots": int(len(values)), "missing_slots": int(missing)}


def looks_like_arper_woz3_features(text: str) -> bool:
    """Return True for ARPER WOZ3 feature strings such as `Booking-Book-Day-1|...`."""

    s = str(text or "").strip()
    if not s or "(" in s or "=" in s:
        return False
    return bool(re.search(r"\b[A-Za-z]+-[A-Za-z]+-[A-Za-z]+-\d+\b", s))


def arper_template_slot_bases(template_path: Optional[str] = None) -> Tuple[str, ...]:
    """Load official ARPER `d-a-s-v:*` slot bases, matching `util.score`.

    Official ARPER strips the trailing value index from each `d-a-s-v` template
    row and ignores non-entity values (`none`, `?`, `yes`, `no`).
    """

    p = str(Path(template_path) if template_path else DEFAULT_ARPER_WOZ3_TEMPLATE)
    cached = _ARPER_TEMPLATE_BASES_CACHE.get(p)
    if cached is not None:
        return cached

    bases: List[str] = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            row = line.strip()
            if "d-a-s-v:" not in row:
                continue
            if "-none" in row or "-?" in row or "-yes" in row or "-no" in row:
                continue
            base = "-".join(row.split("-")[:-1])
            if base not in bases:
                bases.append(base)
    out = tuple(bases)
    _ARPER_TEMPLATE_BASES_CACHE[p] = out
    return out


def arper_woz3_slot_error_counts(
    features: str,
    prediction: str,
    *,
    template_path: Optional[str] = None,
) -> Dict[str, int]:
    """Official-equivalent ARPER WOZ3 SER counts for one generation.

    This mirrors `external_sources/arper/util.py::score`: for every ontology
    slot base, count required feature occurrences and generated
    `slot-<domain-act-slot>` tokens, then accumulate redundant and missing
    counts.
    """

    feat_items = {f"d-a-s-v:{x.strip()}" for x in str(features or "").split("|") if x.strip()}
    pred_tokens = str(prediction or "").split()
    total = 0
    redundant = 0
    missing = 0

    for base in arper_template_slot_bases(template_path):
        expected = 0
        base_orders = {f"{base}-{i}" for i in range(20)}
        for item in feat_items:
            if item in base_orders:
                expected += 1

        slot_token = "slot-" + base.split(":", 1)[1].lower()
        generated = pred_tokens.count(slot_token)
        diff = generated - expected
        if diff > 0:
            redundant += diff
        else:
            missing += -diff
        total += expected

    return {"total": int(total), "redunt": int(redundant), "miss": int(missing)}


def arper_woz3_slot_error_rate(
    features: str,
    prediction: str,
    *,
    template_path: Optional[str] = None,
) -> Optional[float]:
    counts = arper_woz3_slot_error_counts(features, prediction, template_path=template_path)
    total = int(counts.get("total", 0))
    if total <= 0:
        return None
    return float((int(counts.get("redunt", 0)) + int(counts.get("miss", 0))) / total)


def arper_woz3_corpus_bleu4_from_examples(examples: Iterable[Dict[str, Any]]) -> float:
    """Compute ARPER-style grouped multi-reference BLEU-4 from eval debug rows."""

    rows = list(examples)
    if not rows:
        return 0.0
    try:
        from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu

        refs_by_feat: Dict[str, List[str]] = {}
        for row in rows:
            feat = str(row.get("input_text", ""))
            ref = str(row.get("normalized_gold", row.get("gold_output", "")))
            refs_by_feat.setdefault(feat, []).append(ref)

        references: List[List[List[str]]] = []
        hypotheses: List[List[str]] = []
        for row in rows:
            feat = str(row.get("input_text", ""))
            pred = str(row.get("normalized_prediction", row.get("raw_generated_output", "")))
            references.append([[tok for tok in ref.split() if tok] for ref in refs_by_feat.get(feat, [])])
            hypotheses.append([tok for tok in pred.split() if tok])
        return float(
            corpus_bleu(
                references,
                hypotheses,
                weights=(0.25, 0.25, 0.25, 0.25),
                smoothing_function=SmoothingFunction().method1,
            )
        )
    except Exception:
        return corpus_bleu4(
            [str(row.get("normalized_prediction", row.get("raw_generated_output", ""))) for row in rows],
            [str(row.get("normalized_gold", row.get("gold_output", ""))) for row in rows],
        )


def _probe_nlg_metric_libs() -> None:
    global _NLG_METRIC_LIBS
    if _NLG_METRIC_LIBS:
        return
    for name, mod in (("rouge_score", "rouge_score"), ("sacrebleu", "sacrebleu")):
        try:
            __import__(mod)
            _NLG_METRIC_LIBS[name] = True
        except ImportError:
            _NLG_METRIC_LIBS[name] = False


_probe_nlg_metric_libs()
