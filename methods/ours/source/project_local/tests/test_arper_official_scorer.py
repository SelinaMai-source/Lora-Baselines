from __future__ import annotations

from pathlib import Path
import sys


PROJECT_LOCAL = Path(__file__).resolve().parents[1]
if str(PROJECT_LOCAL) not in sys.path:
    sys.path.insert(0, str(PROJECT_LOCAL))


def test_arper_woz3_ser_matches_official_counting(tmp_path: Path) -> None:
    from core.metrics_utils import arper_woz3_slot_error_counts, arper_woz3_slot_error_rate

    template = tmp_path / "template.txt"
    template.write_text(
        "\n".join(
            [
                "d:Booking",
                "d-a:Booking-Book",
                "d-a-s-v:Booking-Book-Day-1",
                "d-a-s-v:Booking-Book-Day-2",
                "d-a-s-v:Booking-Book-Name-1",
                "d-a-s-v:Booking-Book-Name-2",
                "d-a-s-v:Booking-Book-Ref-none",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    counts = arper_woz3_slot_error_counts(
        "Booking-Book-Day-1|Booking-Book-Name-1",
        "slot-booking-book-day slot-booking-book-day",
        template_path=str(template),
    )

    assert counts == {"total": 2, "redunt": 1, "miss": 1}
    assert arper_woz3_slot_error_rate(
        "Booking-Book-Day-1|Booking-Book-Name-1",
        "slot-booking-book-day slot-booking-book-day",
        template_path=str(template),
    ) == 1.0


def test_arper_woz3_bleu_groups_references_by_feature() -> None:
    from core.metrics_utils import arper_woz3_corpus_bleu4_from_examples

    examples = [
        {
            "input_text": "Booking-Book-Ref-1",
            "normalized_gold": "booking was successful reference number is slot-booking-book-ref .",
            "normalized_prediction": "booking was successful reference number is slot-booking-book-ref .",
        },
        {
            "input_text": "Booking-Book-Ref-1",
            "normalized_gold": "your reference number is slot-booking-book-ref .",
            "normalized_prediction": "your reference number is slot-booking-book-ref .",
        },
    ]

    assert arper_woz3_corpus_bleu4_from_examples(examples) > 0.99
