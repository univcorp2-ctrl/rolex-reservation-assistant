from __future__ import annotations

from datetime import datetime, timezone


def parse_deadline(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Deadline must be ISO 8601, e.g. 2026-06-22T23:59:00+09:00") from exc
    if parsed.tzinfo is None:
        raise ValueError("Deadline must include a timezone offset, e.g. +09:00")
    return parsed


def remaining_time_text(deadline: datetime, now: datetime | None = None) -> str:
    current = now or datetime.now(timezone.utc)
    delta = deadline.astimezone(timezone.utc) - current.astimezone(timezone.utc)
    seconds = int(delta.total_seconds())
    if seconds <= 0:
        return "締切を過ぎています"
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    days, hour = divmod(hours, 24)
    parts: list[str] = []
    if days:
        parts.append(f"{days}日")
    if hour:
        parts.append(f"{hour}時間")
    if minute:
        parts.append(f"{minute}分")
    if not parts:
        parts.append(f"{sec}秒")
    return "残り" + "".join(parts)
