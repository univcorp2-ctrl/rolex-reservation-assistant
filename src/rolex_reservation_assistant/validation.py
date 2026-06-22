from __future__ import annotations

import re
from datetime import date, datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9]{10,11}$")


class InputValidationError(ValueError):
    """Raised when applicant input is malformed."""


def require_non_empty(value: object, field_name: str) -> str:
    text = str(value).strip()
    if not text:
        raise InputValidationError(f"{field_name} is required")
    return text


def normalize_email(value: object) -> str:
    email = require_non_empty(value, "email")
    if not EMAIL_RE.match(email):
        raise InputValidationError("email must look like name@example.com")
    return email


def normalize_japanese_phone(value: object) -> str:
    raw = require_non_empty(value, "phone")
    compact = raw.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if compact.startswith("+81"):
        compact = "0" + compact[3:]
    if not PHONE_RE.match(compact) or not compact.startswith("0"):
        raise InputValidationError("phone must be a 10 or 11 digit Japanese phone number")
    return compact


def normalize_birth_date(value: object) -> str:
    raw = require_non_empty(value, "birth_date")
    normalized = raw.replace("/", "-").replace(".", "-")
    try:
        parsed = datetime.strptime(normalized, "%Y-%m-%d").date()
    except ValueError as exc:
        raise InputValidationError("birth_date must be YYYY-MM-DD, YYYY.MM.DD, or YYYY/MM/DD") from exc
    if parsed < date(1900, 1, 1):
        raise InputValidationError("birth_date is too old")
    if parsed > date.today():
        raise InputValidationError("birth_date must not be in the future")
    return parsed.isoformat()


def validate_profile_shape(data: dict[str, object]) -> None:
    required = [
        "family_name",
        "given_name",
        "family_name_kana",
        "given_name_kana",
        "email",
        "phone",
        "birth_date",
    ]
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise InputValidationError(f"Missing profile fields: {', '.join(missing)}")
