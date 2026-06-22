from __future__ import annotations

import random
from datetime import datetime

import pytest

from rolex_reservation_assistant.applicant import ApplicantProfile
from rolex_reservation_assistant.destinations import DESTINATIONS
from rolex_reservation_assistant.input_plan import build_input_plan, validate_input_plan
from rolex_reservation_assistant.preferences import DEFAULT_AFTERNOON_SLOTS, TOKYO


def sample_profile() -> ApplicantProfile:
    return ApplicantProfile.from_mapping(
        {
            "family_name": "山田",
            "given_name": "太郎",
            "family_name_kana": "ヤマダ",
            "given_name_kana": "タロウ",
            "email": "taro@example.com",
            "phone": "09000000000",
            "birth_date": "1980-01-01",
            "preferred_date": "auto",
            "preferred_time_window": "afternoon",
            "preferred_model": "auto",
            "preferred_models": ["レイトナー", "コスモグラフ デイトナ"],
            "date_window_days": 3,
        }
    )


def test_build_input_plan_resolves_near_date_afternoon_and_model() -> None:
    profile = sample_profile()
    plan = build_input_plan(
        profile,
        DESTINATIONS["ginza"],
        now=datetime(2026, 6, 22, 9, 0, tzinfo=TOKYO),
        rng=random.Random(0),
    )

    validate_input_plan(plan)
    assert plan.preferences.preferred_date in {"2026-06-23", "2026-06-24", "2026-06-25"}
    assert plan.preferences.preferred_time_window in DEFAULT_AFTERNOON_SLOTS
    assert plan.preferences.preferred_model in {"レイトナー", "コスモグラフ デイトナ"}
    assert "希望モデル" in [field.label for field in plan.fields]
    application_text = next(field.value for field in plan.fields if field.key == "application_text")
    assert "希望モデル" in application_text


def test_required_profile_fields_are_validated() -> None:
    data = {
        "family_name": "山田",
        "given_name": "太郎",
        "family_name_kana": "ヤマダ",
        "given_name_kana": "タロウ",
        "email": "taro@example.com",
        "phone": "09000000000",
    }
    with pytest.raises(ValueError, match="birth_date"):
        ApplicantProfile.from_mapping(data)
