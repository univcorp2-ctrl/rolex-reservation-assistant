from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .applicant import ApplicantProfile

TOKYO = timezone(timedelta(hours=9), name="Asia/Tokyo")
DEFAULT_AFTERNOON_SLOTS = ("13:00-15:00", "15:00-17:00", "17:00-19:00")
DEFAULT_MODEL_CANDIDATES = (
    "コスモグラフ デイトナ",
    "サブマリーナー",
    "GMTマスターⅡ",
    "エクスプローラー",
    "デイトジャスト",
    "ランドドゥエラー",
    "レイトナー",
)


@dataclass(frozen=True)
class ResolvedPreferences:
    preferred_date: str
    preferred_time_window: str
    preferred_model: str


def resolve_preferences(
    profile: ApplicantProfile,
    now: datetime | None = None,
    rng: random.Random | None = None,
) -> ResolvedPreferences:
    chooser = rng or random.SystemRandom()
    current = (now or datetime.now(TOKYO)).astimezone(TOKYO)

    if profile.preferred_date.lower() == "auto":
        days_ahead = chooser.randint(1, profile.date_window_days)
        preferred_date = (current.date() + timedelta(days=days_ahead)).isoformat()
    else:
        preferred_date = profile.preferred_date

    if profile.preferred_time_window.lower() in {"auto", "afternoon", "午後"}:
        preferred_time_window = chooser.choice(DEFAULT_AFTERNOON_SLOTS)
    else:
        preferred_time_window = profile.preferred_time_window

    candidates = profile.preferred_models or DEFAULT_MODEL_CANDIDATES
    if profile.preferred_model.lower() in {"auto", "random", "適宜"}:
        preferred_model = chooser.choice(tuple(candidates))
    else:
        preferred_model = profile.preferred_model

    return ResolvedPreferences(
        preferred_date=preferred_date,
        preferred_time_window=preferred_time_window,
        preferred_model=preferred_model,
    )
