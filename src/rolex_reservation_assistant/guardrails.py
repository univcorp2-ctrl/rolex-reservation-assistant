from __future__ import annotations

from urllib.parse import urlparse

PRODUCTION_RESERVATION_HOSTS = {
    "reservation.rolexboutique-hiltonplaza-osaka.jp",
    "reservation.rolexboutique-lexia.jp",
    "reservation.rolexboutique-omotesando-tokyo.jp",
}

LOCAL_TEST_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


class UnsafeAutomationTargetError(RuntimeError):
    """Raised when E2E automation points at a production-like target."""


def hostname_from_url(url: str) -> str:
    return urlparse(url).hostname or ""


def is_local_test_url(url: str) -> bool:
    host = hostname_from_url(url).lower()
    return host in LOCAL_TEST_HOSTS or host.endswith(".localhost") or host.endswith(".test")


def is_production_reservation_url(url: str) -> bool:
    return hostname_from_url(url).lower() in PRODUCTION_RESERVATION_HOSTS


def ensure_e2e_target_is_safe(url: str) -> None:
    if is_production_reservation_url(url):
        raise UnsafeAutomationTargetError(
            "E2E automation is blocked for public reservation hosts. Use the local mock site "
            "or an approved internal test domain."
        )
    if not is_local_test_url(url):
        raise UnsafeAutomationTargetError(
            "E2E automation is limited to localhost/.test targets in this repository."
        )
