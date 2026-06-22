from __future__ import annotations

from datetime import datetime, timezone

import pytest

from rolex_reservation_assistant.captcha import (
    CaptchaAutomationNotSupportedError,
    estimate_captcha_cost,
    get_captcha_provider,
)
from rolex_reservation_assistant.deadline import parse_deadline, remaining_time_text
from rolex_reservation_assistant.guardrails import UnsafeAutomationTargetError, ensure_e2e_target_is_safe


def test_captcha_cost_estimate() -> None:
    estimate = estimate_captcha_cost("enterprise-placeholder", 5, "2.99")
    assert str(estimate.total_cost) == "0.01"


def test_captcha_provider_does_not_solve() -> None:
    provider = get_captcha_provider("enterprise-placeholder")
    with pytest.raises(CaptchaAutomationNotSupportedError):
        provider.solve()


def test_deadline_remaining_text() -> None:
    deadline = parse_deadline("2026-06-22T23:59:00+09:00")
    now = datetime(2026, 6, 22, 14, 59, tzinfo=timezone.utc)
    assert remaining_time_text(deadline, now=now) == "残り0秒" or "締切" in remaining_time_text(deadline, now=now)


def test_guardrails_allow_local_and_block_public_reservation_url() -> None:
    ensure_e2e_target_is_safe("http://127.0.0.1:8765")
    with pytest.raises(UnsafeAutomationTargetError):
        ensure_e2e_target_is_safe("https://reservation.rolexboutique-lexia.jp/ginza/reservation")
