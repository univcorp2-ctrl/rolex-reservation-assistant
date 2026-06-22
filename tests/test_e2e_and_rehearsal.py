from __future__ import annotations

from rolex_reservation_assistant.applicant import ApplicantProfile
from rolex_reservation_assistant.destinations import DESTINATIONS
from rolex_reservation_assistant.e2e import SelectorProfile, build_playwright_script
from rolex_reservation_assistant.input_plan import build_input_plan
from rolex_reservation_assistant.rehearsal import run_rehearsal


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
            "preferred_models": ["レイトナー", "デイトジャスト"],
        }
    )


def selectors() -> SelectorProfile:
    return SelectorProfile(
        fields={
            "family_name": ["#family_name", "input[name='family_name']"],
            "given_name": ["#given_name"],
            "email": ["#email"],
            "phone": ["#phone"],
            "birth_date": ["#birth_date"],
            "preferred_date": ["#preferred_date"],
            "preferred_time_window": ["#preferred_time_window"],
            "preferred_model": ["#preferred_model"],
            "application_text": ["#application_text"],
        },
        submit_selectors=["#submit", "button[type='submit']"],
        success_selectors=["#success"],
    )


def test_e2e_script_contains_fallback_submit_and_success_check() -> None:
    plan = build_input_plan(sample_profile(), DESTINATIONS["ginza"])
    script = build_playwright_script(
        plan=plan,
        selectors=selectors(),
        url="http://127.0.0.1:8765",
        submit=True,
    )
    assert "fill_with_fallback" in script
    assert "submit_button.click()" in script
    assert "Submit did not show a success marker" in script


def test_rehearsal_runs_100_iterations() -> None:
    result = run_rehearsal(
        profile=sample_profile(),
        location="all",
        selectors=selectors(),
        iterations=100,
    )
    assert result.iterations == 100
    assert result.plans_checked == 500
    assert result.scripts_checked == 500
