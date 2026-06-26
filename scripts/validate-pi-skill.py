#!/usr/bin/env python3
"""Validate the project-local Planf3 skill + extension (both live under .pi/)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".pi" / "skills" / "planf3" / "SKILL.md"
EXTENSION = ROOT / ".pi" / "extensions" / "planf3"
SETTINGS = ROOT / ".pi" / "settings.json"
REQUIRED_WORKFLOWS = [
    "create-plan.md",
    "update-plan.md",
    "build-plan.md",
    "update-references.md",
    "export-html.md",
    "image-generation.md",
]


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise SystemExit("SKILL.md missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise SystemExit("SKILL.md frontmatter not closed")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def main() -> None:
    missing = []
    for path in [SKILL, EXTENSION / "index.ts", SETTINGS, ROOT / "docs" / "pi-planf3-test-runbook.md"]:
        if not path.exists():
            missing.append(str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path))
    workflows_dir = SKILL.parent / "workflows"
    for name in REQUIRED_WORKFLOWS:
        if not (workflows_dir / name).exists():
            missing.append(str((workflows_dir / name).relative_to(ROOT)))
    if missing:
        raise SystemExit("Missing required files:\n" + "\n".join(missing))

    text = SKILL.read_text(encoding="utf-8")
    fm = frontmatter(text)
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", name):
        raise SystemExit(f"Invalid skill name: {name!r}")
    if not desc:
        raise SystemExit("Missing skill description")
    if len(desc) > 1024:
        raise SystemExit("Skill description exceeds 1024 chars")
    if "codex-image-generate" not in text:
        raise SystemExit("SKILL.md does not mention codex-image-generate")
    if "Markdown" not in text or "canonical" not in text:
        raise SystemExit("SKILL.md does not clearly state Markdown canonical policy")

    print("Pi Planf3 skill adapter validation passed")
    print(f"skill: {SKILL}")
    print(f"workflows: {len(REQUIRED_WORKFLOWS)}")


if __name__ == "__main__":
    main()
