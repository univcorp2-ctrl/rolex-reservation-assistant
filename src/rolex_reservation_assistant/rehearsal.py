from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime

from .applicant import ApplicantProfile
from .destinations import resolve_destinations
from .e2e import SelectorProfile, build_playwright_script
from .input_plan import build_input_plan, validate_input_plan
from .preferences import DEFAULT_AFTERNOON_SLOTS, TOKYO


@dataclass(frozen=True)
class RehearsalResult:
    iterations: int
    plans_checked: int
    scripts_checked: int


def run_rehearsal(
    profile: ApplicantProfile,
    location: str,
    selectors: SelectorProfile,
    iterations: int,
    local_url: str = "http://127.0.0.1:8765",
) -> RehearsalResult:
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    destinations = resolve_destinations(location)
    plans_checked = 0
    scripts_checked = 0
    fixed_now = datetime(2026, 6, 22, 12, 0, tzinfo=TOKYO)

    for index in range(iterations):
        rng = random.Random(index)
        for destination in destinations:
            plan = build_input_plan(profile, destination, now=fixed_now, rng=rng)
            validate_input_plan(plan)
            if plan.preferences.preferred_time_window not in DEFAULT_AFTERNOON_SLOTS:
                raise AssertionError("preferred_time_window must be an afternoon slot")
            if not plan.preferences.preferred_date:
                raise AssertionError("preferred_date must be selected")
            script = build_playwright_script(
                plan=plan,
                selectors=selectors,
                url=local_url,
                submit=True,
            )
            required_fragments = ["fill_with_fallback", "Submit did not show a success marker"]
            for fragment in required_fragments:
                if fragment not in script:
                    raise AssertionError(f"Missing generated script fragment: {fragment}")
            plans_checked += 1
            scripts_checked += 1
    return RehearsalResult(
        iterations=iterations,
        plans_checked=plans_checked,
        scripts_checked=scripts_checked,
    )
