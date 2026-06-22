from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ApplicantProfile:
    family_name: str
    given_name: str
    family_name_kana: str
    given_name_kana: str
    email: str
    phone: str
    birth_date: str
    postal_code: str = ""
    prefecture: str = ""
    city: str = ""
    address_line1: str = ""
    address_line2: str = ""
    preferred_date: str = "auto"
    preferred_time_window: str = "afternoon"
    preferred_model: str = "auto"
    preferred_models: tuple[str, ...] = ()
    visit_purpose: str = "購入相談"
    notes: str = ""
    date_window_days: int = 10

    @property
    def full_name(self) -> str:
        return f"{self.family_name} {self.given_name}".strip()

    @property
    def full_name_kana(self) -> str:
        return f"{self.family_name_kana} {self.given_name_kana}".strip()

    @property
    def address(self) -> str:
        return " ".join(
            part
            for part in [
                self.postal_code,
                self.prefecture,
                self.city,
                self.address_line1,
                self.address_line2,
            ]
            if part
        )

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "ApplicantProfile":
        required = [
            "family_name",
            "given_name",
            "family_name_kana",
            "given_name_kana",
            "email",
            "phone",
            "birth_date",
        ]
        missing = [key for key in required if not data.get(key)]
        if missing:
            raise ValueError(f"Missing profile fields: {', '.join(missing)}")

        preferred_models_raw = data.get("preferred_models", [])
        if isinstance(preferred_models_raw, str):
            preferred_models = (preferred_models_raw,)
        elif isinstance(preferred_models_raw, list):
            preferred_models = tuple(str(item) for item in preferred_models_raw if str(item).strip())
        else:
            raise ValueError("preferred_models must be a string or list of strings")

        date_window_days = int(data.get("date_window_days", 10))
        if date_window_days < 1:
            raise ValueError("date_window_days must be >= 1")

        return cls(
            family_name=str(data["family_name"]),
            given_name=str(data["given_name"]),
            family_name_kana=str(data["family_name_kana"]),
            given_name_kana=str(data["given_name_kana"]),
            email=str(data["email"]),
            phone=str(data["phone"]),
            birth_date=str(data["birth_date"]),
            postal_code=str(data.get("postal_code", "")),
            prefecture=str(data.get("prefecture", "")),
            city=str(data.get("city", "")),
            address_line1=str(data.get("address_line1", "")),
            address_line2=str(data.get("address_line2", "")),
            preferred_date=str(data.get("preferred_date", "auto")),
            preferred_time_window=str(data.get("preferred_time_window", "afternoon")),
            preferred_model=str(data.get("preferred_model", "auto")),
            preferred_models=preferred_models,
            visit_purpose=str(data.get("visit_purpose", "購入相談")),
            notes=str(data.get("notes", "")),
            date_window_days=date_window_days,
        )


def load_profile(path: str | Path) -> ApplicantProfile:
    profile_path = Path(path)
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Profile file not found: {profile_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Profile file is not valid JSON: {profile_path}") from exc
    if not isinstance(data, dict):
        raise ValueError("Profile JSON must be an object")
    return ApplicantProfile.from_mapping(data)
