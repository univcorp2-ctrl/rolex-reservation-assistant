from __future__ import annotations

import pytest

from rolex_reservation_assistant.applicant import ApplicantProfile
from rolex_reservation_assistant.validation import (
    InputValidationError,
    normalize_birth_date,
    normalize_email,
    normalize_japanese_phone,
)


def test_normalize_birth_date_accepts_dot_format() -> None:
    assert normalize_birth_date("1981.11.05") == "1981-11-05"


def test_normalize_japanese_phone_accepts_mobile_digits() -> None:
    assert normalize_japanese_phone("090-0000-0000") == "09000000000"


def test_normalize_email_rejects_invalid_value() -> None:
    with pytest.raises(InputValidationError):
        normalize_email("not-an-email")


def test_applicant_profile_normalizes_core_fields() -> None:
    profile = ApplicantProfile.from_mapping(
        {
            "family_name": "山田",
            "given_name": "太郎",
            "family_name_kana": "ヤマダ",
            "given_name_kana": "タロウ",
            "email": "taro@example.com",
            "phone": "090-0000-0000",
            "birth_date": "1981.11.05",
        }
    )
    assert profile.phone == "09000000000"
    assert profile.birth_date == "1981-11-05"


def test_applicant_profile_requires_kana_fields() -> None:
    with pytest.raises(InputValidationError, match="family_name_kana"):
        ApplicantProfile.from_mapping(
            {
                "family_name": "山田",
                "given_name": "太郎",
                "email": "taro@example.com",
                "phone": "09000000000",
                "birth_date": "1981-11-05",
            }
        )
