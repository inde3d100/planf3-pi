# Planf3 Pi adaptation

This repo is our Pi-native adaptation fork of [`disler/planf3`](https://github.com/disler/planf3).

## Intent

Adopt Planf3 as a meta-skill: a planning/control artifact generator that agents can create, update, build from, and keep referenced across implementation work.

## Local policy

- Keep upstream lineage intact.
- Do not install globally yet.
- Use project-local staged skill copy at `.pi/skills/planf3/`.
- Use `specs/` for bootstrap Planf3-style plan artifacts.
- Adapt toward Plan Artifact v2 for our Pi lab:
  - Markdown/Obsidian canonical source
  - optional HTML preview/export
  - `goal_create`, `goal_update`, `goal_evidence` integration
  - Agent House room handoff/control integration
  - Command Center board/job integration
  - verification output and git commit linkage

## Current bootstrap artifact

- `specs/pi-agent-house-command-center-plan-artifact-v2.html`
