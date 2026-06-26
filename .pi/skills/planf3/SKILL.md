---
name: planf3
description: Global Planf3 meta-skill for creating, updating, building from, and exporting living implementation plan artifacts. Use as the default planning/control artifact for serious implementation work, Agent House rooms, Command Center jobs, multi-agent handoffs, or when the user asks for planf3, Plan Artifact v2, a spec, or a living plan.
argument-hint: "[create|update|build|export|images] [user-prompt-or-plan-path] [questionable]"
---

# Planf3 for Pi — Global Default Adapter

## Purpose

Use Planf3 as the **standard planning/control meta-skill** for serious work. It creates and maintains the living plan artifact that Pi sessions, Agent House, Command Center, goal tools, reviewers, and handoffs can read, execute, update, review, and close out.

Legacy planning skills such as `writing-plans` and `executing-plans` are compatibility entrypoints only; route their work into Planf3 unless the user explicitly requests otherwise.

## Output policy for this Pi adapter

- Canonical plan: `specs/<descriptive-kebab-name>.md`
- Optional browser preview/export: `specs/<descriptive-kebab-name>.html`
- Optional images: `specs/<descriptive-kebab-name>/images/*.png`
- Upstream lineage: keep `/root/projects/planf3-pi/.claude/skills/planf3/` intact; this global copy is the Pi-facing default adapter.

## Core idea

A plan artifact is the control surface for:

```text
create → update → build → validate → update references → close out
```

It should connect:

- user request
- source notes / Obsidian links
- goal id and checklist
- Agent House room ownership
- Command Center board/job id when present
- implementation phases and status markers
- validation commands
- evidence paths / `goal_evidence` notes
- git commits
- amendments and review findings

## Variables

- `USER_PROMPT`: the user's requested work or instruction
- `QUESTIONABLE`: optional flag; when true, surface open decisions instead of silently deciding
- `PLAN_OUTPUT_DIRECTORY`: `specs/`
- `PLAN_FILE_MD`: `specs/<descriptive-kebab-name>.md`
- `PLAN_FILE_HTML`: `specs/<descriptive-kebab-name>.html`
- `IMAGES_OUTPUT_DIR`: `specs/<descriptive-kebab-name>/images/`
- `BROWSER`: optional; on this VPS use browser tools or save the file path rather than opening a local GUI browser

## Required plan sections

Every canonical Markdown plan should include:

1. Title and metadata
2. Purpose / problem / solution
3. Backrefs and forward refs
4. Goal integration
5. Agent House integration
6. Command Center integration
7. Relevant files
8. Implementation phases with status markers
9. Validation commands and evidence mapping
10. Questionables when requested
11. Notes / risks / rejected approaches
12. Amendments

Use status markers:

```text
[] idle · [wip] in progress · [x] complete · [f] failed/blocked
```

## Goal/evidence behavior

When the parent Pi session has goal tools available:

- For new serious work, create or link a goal with `goal_create`.
- When a phase starts or completes, update the goal with `goal_update`.
- When validation commands pass, record concrete output with `goal_evidence`.
- Do not mark complete until verification evidence exists.

If goal tools are unavailable, write clear placeholders in the plan:

```text
Goal ID: pending
Evidence: pending
```

## Image generation behavior

Images are optional but supported. Prefer the installed Codex GPT Image 2 helper:

```bash
/usr/local/bin/codex-image-generate --aspect landscape --quality high -o specs/<plan-name>/images/<slot>.png '<prompt>'
```

Rules:

- Use images only when they clarify architecture, UI, workflow, or handoff state.
- Keep image text under 10 words total.
- Match the plan's visual identity.
- Save prompts or captions in the Markdown plan.
- If `/usr/local/bin/codex-image-generate` is unavailable or auth is expired, mark image generation `[f]` with the reason instead of blocking the whole plan.
- The upstream OpenAI API scripts in `scripts/` remain as fallback/reference only; normal Pi testing should use `codex-image-generate`.

## Workflow routing

Read exactly one workflow before acting:

| Workflow | Use when | File |
| --- | --- | --- |
| Create Plan | User asks to plan/spec/design new work and no existing plan path is referenced | `workflows/create-plan.md` |
| Update Plan | User asks to revise or extend an existing plan | `workflows/update-plan.md` |
| Build Plan | User asks to execute/carry out an existing plan | `workflows/build-plan.md` |
| Update References | User asks to refresh metadata, backrefs, forward refs, commits, or session info | `workflows/update-references.md` |
| Export HTML | User asks for browser preview/export from Markdown | `workflows/export-html.md` |
| Image Generation | User asks to generate/fill/update plan images | `workflows/image-generation.md` |

## Create-plan template skeleton

When creating a canonical Markdown plan, use this shape:

```markdown
# <Plan Title>

## Metadata

- Created: <ISO timestamp>
- Modified: <ISO timestamp list>
- Source request: <short quote/summary>
- Goal ID: <goal id or pending>
- Command Center job: <id or n/a>
- Agent House room: <room or n/a>
- Status: [] draft
- Backrefs:
  - <paths/links>
- Forward refs:
  - <expected files/links>
- Commits:
  - pending

## Purpose

<why this plan exists>

## Problem

<problem being solved>

## Solution

<technical/workflow approach>

## Relevant files

### Existing

- `<path>` — <why relevant>

### New

- `<path>` — <why needed>

## Agent House integration

<how rooms consume/update/handoff this plan>

## Command Center integration

<how board/jobs reference this plan>

## Implementation phases

### [] Phase 1: <name>

<objective>

- [] <specific action>
- [] <specific action>

#### Validation

- [] `<command>` — <what it proves>

## Global validation

- [] `<command>` — <what it proves>

## Evidence map

- <requirement/status> → <goal_evidence command/path/output>

## Questionables

- <only if requested or needed>

## Notes

<context, risks, rejected approaches>

## Amendments

- <append-only>
```

## Testing this adapter

See `docs/pi-planf3-test-runbook.md` in this repo for exact launch commands and test prompts.
