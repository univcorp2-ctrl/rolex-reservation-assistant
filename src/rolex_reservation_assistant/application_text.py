from __future__ import annotations

from .applicant import ApplicantProfile
from .destinations import Destination
from .preferences import ResolvedPreferences


def generate_application_text(
    profile: ApplicantProfile,
    destination: Destination,
    preferences: ResolvedPreferences,
) -> str:
    """Generate a polite Japanese application note for a reservation form."""

    extra_notes = f"\n補足: {profile.notes}" if profile.notes else ""
    return (
        f"{destination.label}店への来店予約を希望します。\n"
        f"希望日: {preferences.preferred_date}\n"
        f"希望時間帯: {preferences.preferred_time_window}\n"
        f"希望モデル: {preferences.preferred_model}\n"
        f"来店目的: {profile.visit_purpose}\n"
        "本人確認書類を持参し、店舗の案内と予約条件に従って来店します。"
        "予約枠の状況に応じて、可能な日時をご案内いただけますと幸いです。"
        f"{extra_notes}"
    )
