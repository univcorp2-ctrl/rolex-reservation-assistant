from __future__ import annotations

from .input_plan import InputPlan


def render_plan(plan: InputPlan, remaining: str | None = None) -> str:
    lines = [
        f"店舗: {plan.destination.label} ({plan.destination.key})",
        f"URL: {plan.destination.url}",
    ]
    if remaining:
        lines.append(f"締切: {remaining}")
    lines.extend(
        [
            f"希望日: {plan.preferences.preferred_date}",
            f"希望時間帯: {plan.preferences.preferred_time_window}",
            f"希望モデル: {plan.preferences.preferred_model}",
            "",
            "入力項目:",
        ]
    )
    for field in plan.fields:
        required = "必須" if field.required else "任意"
        value = field.value.replace("\n", " / ")
        lines.append(f"- [{required}] {field.label} ({field.key}): {value}")
    lines.extend(["", "手動チェック:"])
    lines.extend(f"- {step}" for step in plan.manual_steps)
    return "\n".join(lines)
