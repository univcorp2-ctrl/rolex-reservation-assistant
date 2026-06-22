from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .applicant import ApplicantProfile
from .application_text import generate_application_text
from .destinations import Destination
from .preferences import ResolvedPreferences, resolve_preferences


@dataclass(frozen=True)
class InputField:
    key: str
    label: str
    value: str
    required: bool = True


@dataclass(frozen=True)
class InputPlan:
    destination: Destination
    preferences: ResolvedPreferences
    fields: list[InputField]
    manual_steps: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "destination": {
                "key": self.destination.key,
                "label": self.destination.label,
                "url": self.destination.url,
            },
            "preferences": self.preferences.__dict__,
            "fields": [field.__dict__ for field in self.fields],
            "manual_steps": self.manual_steps,
        }


def build_input_plan(
    profile: ApplicantProfile,
    destination: Destination,
    now: datetime | None = None,
    rng: random.Random | None = None,
) -> InputPlan:
    preferences = resolve_preferences(profile, now=now, rng=rng)
    application_text = generate_application_text(profile, destination, preferences)
    fields = [
        InputField("family_name", "姓", profile.family_name),
        InputField("given_name", "名", profile.given_name),
        InputField("family_name_kana", "セイ", profile.family_name_kana),
        InputField("given_name_kana", "メイ", profile.given_name_kana),
        InputField("email", "メールアドレス", profile.email),
        InputField("phone", "電話番号", profile.phone),
        InputField("birth_date", "生年月日", profile.birth_date),
        InputField("postal_code", "郵便番号", profile.postal_code, required=False),
        InputField("prefecture", "都道府県", profile.prefecture, required=False),
        InputField("city", "市区町村", profile.city, required=False),
        InputField("address_line1", "住所1", profile.address_line1, required=False),
        InputField("address_line2", "住所2", profile.address_line2, required=False),
        InputField("preferred_date", "希望日", preferences.preferred_date, required=False),
        InputField("preferred_time_window", "希望時間帯", preferences.preferred_time_window, required=False),
        InputField("preferred_model", "希望モデル", preferences.preferred_model, required=False),
        InputField("visit_purpose", "来店目的", profile.visit_purpose, required=False),
        InputField("application_text", "応募文・備考", application_text, required=False),
    ]
    manual_steps = [
        "予約ページを1店舗だけ開く",
        "画面上の最新の注意事項、利用条件、入力欄を確認する",
        "入力計画を見ながら必要項目を入力する",
        "CAPTCHAが表示された場合は人間が画面上で解く",
        "入力内容、希望店舗、日時、連絡先に誤りがないことを確認する",
        "最終送信ボタンは人間が確認して押す",
        "全店舗を確認する場合は、十分な間隔を空けて次の店舗へ進む",
    ]
    return InputPlan(
        destination=destination,
        preferences=preferences,
        fields=fields,
        manual_steps=manual_steps,
    )


def validate_input_plan(plan: InputPlan) -> None:
    missing = [field.key for field in plan.fields if field.required and not field.value.strip()]
    if missing:
        raise ValueError(f"Missing required input fields: {', '.join(missing)}")
