# Pi Planf3 Test Runbook

This runbook tests the consolidated Planf3 meta-skill, which now lives entirely in the global Pi extension folder.

## Repo

```text
/root/projects/planf3-pi
```

## What is configured

- Canonical skill location: `/root/.pi/agent/extensions/planf3/SKILL.md`
- Workflows: `/root/.pi/agent/extensions/planf3/workflows/`
- Scripts (reference only): `/root/.pi/agent/extensions/planf3/scripts/`
- Upstream lineage copy (untouched): `/root/projects/planf3-pi/.claude/skills/planf3/`
- Canonical plan output: `specs/*.md`
- Optional preview output: `specs/*.html`
- Optional images: `specs/<plan-name>/images/*.png`
- Image helper: `/usr/local/bin/codex-image-generate`

## Launch Pi with the consolidated extension

Preferred explicit test command:

```bash
cd /root/projects/planf3-pi
pi --approve --no-extensions --skill planf3
```

Why this command:

- `--approve` trusts project-local files for the run.
- `--no-extensions` keeps the test focused.
- `--skill planf3` loads only the consolidated Planf3 skill (resolves to `/root/.pi/agent/extensions/planf3/SKILL.md`).

Alternative, if you want the global extension enabled (default `/planf3` slash command + `before_agent_start` system-prompt injection):

```bash
cd /root/projects/planf3-pi
pi --approve
```

## Test 1 — create a canonical Markdown plan

Inside Pi, send:

```text
/skill:planf3 create a Plan Artifact v2 implementation plan for integrating plan artifacts into Agent House handoffs and Command Center board jobs. Use questionable=true. Save Markdown canonical under specs/ and include optional image slots but do not generate images yet.
```

Expected result:

```text
specs/<descriptive-name>.md
```

Check:

```bash
test -f specs/<descriptive-name>.md
rg -n "Goal ID|Agent House integration|Command Center integration|Implementation phases|Global validation|Evidence map" specs/<descriptive-name>.md
```

## Test 2 — export HTML preview

Inside Pi, send:

```text
/skill:planf3 export specs/<descriptive-name>.md to HTML preview
```

Expected result:

```text
specs/<descriptive-name>.html
```

Check:

```bash
test -f specs/<descriptive-name>.html
! rg -n "\{\{" specs/<descriptive-name>.html
```

## Test 3 — generate one image

Inside Pi, send:

```text
/skill:planf3 generate one hero image for specs/<descriptive-name>.md using codex-image-generate. Keep image text under 10 words.
```

Expected result:

```text
specs/<descriptive-name>/images/hero.png
```

Manual helper command shape if needed:

```bash
/usr/local/bin/codex-image-generate --aspect landscape --quality high -o specs/<descriptive-name>/images/hero.png 'Minimal systems diagram showing one living plan artifact connecting Agent House rooms, Command Center board, goals, evidence, and git commits. Dark professional interface, clean lines, less than 10 words of text.'
```

## Test 4 — update plan

Inside Pi, send:

```text
/skill:planf3 update specs/<descriptive-name>.md to add a rule that Plan Artifact v2 is opt-in and must not replace writing-plans until a real low-risk task proves it.
```

Expected result:

- Metadata modified timestamp appended.
- Amendment added.
- Relevant section updated.

## Test 5 — build from plan dry run

Inside Pi, send:

```text
/skill:planf3 build specs/<descriptive-name>.md but stop after reading the plan and summarizing Phase 1. Do not modify files yet.
```

Expected result:

- Agent reads the plan.
- Agent identifies Phase 1.
- Agent does not start implementation unless explicitly told.

## Verification from shell

```bash
cd /root/projects/planf3-pi
python3 scripts/validate-pi-skill.py
git status --short
```

`git status --short` should be clean after committed configuration changes.

## Global install rule

The skill now lives only at `/root/.pi/agent/extensions/planf3/` (skill content co-located with the extension's `index.ts`). The previous `/root/.pi/agent/skills/planf3/` global copy and the project-local `.pi/skills/planf3/` staging copy have been retired.
