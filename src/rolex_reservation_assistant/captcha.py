from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


class CaptchaAutomationNotSupportedError(RuntimeError):
    """Raised when a caller attempts unsupported CAPTCHA automation."""


@dataclass(frozen=True)
class CaptchaCostEstimate:
    provider: str
    expected_count: int
    cost_per_1000: Decimal

    @property
    def total_cost(self) -> Decimal:
        total = (Decimal(self.expected_count) / Decimal(1000)) * self.cost_per_1000
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def as_text(self) -> str:
        return (
            f"provider={self.provider}, expected_count={self.expected_count}, "
            f"cost_per_1000={self.cost_per_1000}, estimated_total={self.total_cost}"
        )


class CaptchaProvider:
    name = "base"

    def solve(self, *_args: object, **_kwargs: object) -> str:
        raise CaptchaAutomationNotSupportedError(
            "CAPTCHA automation is not implemented. Use manual verification or an approved "
            "enterprise human-review workflow outside this tool."
        )


class ManualCaptchaProvider(CaptchaProvider):
    name = "manual"

    def solve(self, *_args: object, **_kwargs: object) -> str:
        raise CaptchaAutomationNotSupportedError(
            "Manual CAPTCHA selected: complete the CAPTCHA in the browser yourself."
        )


class EnterprisePlaceholderCaptchaProvider(CaptchaProvider):
    name = "enterprise-placeholder"

    def solve(self, *_args: object, **_kwargs: object) -> str:
        raise CaptchaAutomationNotSupportedError(
            "enterprise-placeholder is a stub only. This repository does not call CAPTCHA "
            "bypass APIs. Replace this with a compliant, approved human-review workflow only."
        )


def get_captcha_provider(name: str) -> CaptchaProvider:
    providers: dict[str, CaptchaProvider] = {
        "manual": ManualCaptchaProvider(),
        "enterprise-placeholder": EnterprisePlaceholderCaptchaProvider(),
    }
    try:
        return providers[name]
    except KeyError as exc:
        raise ValueError(f"Unknown CAPTCHA provider: {name}") from exc


def estimate_captcha_cost(provider: str, expected_count: int, cost_per_1000: str) -> CaptchaCostEstimate:
    if expected_count < 0:
        raise ValueError("expected_count must be >= 0")
    return CaptchaCostEstimate(
        provider=provider,
        expected_count=expected_count,
        cost_per_1000=Decimal(cost_per_1000),
    )
