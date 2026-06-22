# Pi Planf3 Test Runbook

This runbook tests the project-local Planf3 meta-skill adapter without installing anything globally.

## Repo

```text
/root/projects/planf3-pi
```

## What is configured

- Project-local skill: `.pi/skills/planf3/SKILL.md`
- Skill commands enabled for this repo: `.pi/settings.json`
- Canonical plan output: `specs/*.md`
- Optional preview output: `specs/*.html`
- Optional images: `specs/<plan-name>/images/*.png`
- Image helper: `/usr/local/bin/codex-image-generate`

## Launch Pi with the local skill

Preferred explicit test command:

```bash
cd /root/projects/planf3-pi
pi --approve --no-extensions --no-skills --skill .pi/skills/planf3
```

Why this command:

- `--approve` trusts project-local files for the run.
- `--no-extensions` keeps the test focused.
- `--no-skills --skill .pi/skills/planf3` disables all other skills and loads only this local adapter.

Alternative, if you want normal project skill discovery:

```bash
cd /root/projects/planf3-pi
pi --approve --no-extensions
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

Do not copy this skill to `/root/.pi/agent/skills/` until the local tests prove it improves at least one real low-risk Agent House + Command Center workflow.
