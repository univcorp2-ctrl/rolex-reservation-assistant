from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "ci" / "python-ci.yml"
DESTINATION = ROOT / ".github" / "workflows" / "ci.yml"


def main() -> int:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Workflow template not found: {SOURCE}")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Installed workflow: {DESTINATION.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
