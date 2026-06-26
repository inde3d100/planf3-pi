# Pi Planf3 Test Runbook

This runbook tests the project-local Planf3 meta-skill and its companion extension. Both live inside the project's `.pi/` folder so Pi auto-discovers them when running in this repo.

## Repo

```text
/root/projects/planf3-pi
```

## What is configured

- Skill (canonical): `.pi/skills/planf3/SKILL.md`
- Workflows: `.pi/skills/planf3/workflows/`
- Scripts (reference only): `.pi/skills/planf3/scripts/`
- Extension: `.pi/extensions/planf3/index.ts`
- Upstream lineage copy (untouched): `.claude/skills/planf3/`
- Skill commands enabled for this repo: `.pi/settings.json` (`enableSkillCommands: true`)
- Canonical plan output: `specs/*.md`
- Optional preview output: `specs/*.html`
- Optional images: `specs/<plan-name>/images/*.png`
- Image helper: `/usr/local/bin/codex-image-generate`

## Launch Pi

Project-local skill + extension auto-discover when you launch Pi in this repo:

```bash
cd /root/projects/planf3-pi
pi --approve
```

If you want to isolate the test to just Planf3 (no other skills, no other extensions):

```bash
cd /root/projects/planf3-pi
pi --approve --no-extensions --no-skills --skill .pi/skills/planf3
```

Why this command:

- `--approve` trusts project-local files for the run.
- `--no-extensions` skips every extension except the ones you point at.
- `--no-skills --skill .pi/skills/planf3` disables global skill discovery and loads only this project's skill.

## Test 1 — create a canonical Markdown plan

Inside Pi, send:

```text
/skill:planf3 create a Plan Artifact v2 implementation plan for integrating plan artifacts into Agent House handoffs and Command Center board jobs. Use questionable=true. Save Markdown canonical under specs/ and include optional image slots but do not generate images yet.
```

Or, with the extension enabled, use the slash command:

```text
/planf3 create a Plan Artifact v2 implementation plan for integrating plan artifacts into Agent House handoffs and Command Center board jobs. Use questionable=true.
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

`python3 scripts/validate-pi-skill.py` should print `Pi Planf3 skill adapter validation passed`.

## Install scope

Planf3 for Pi lives entirely inside this repo's `.pi/` folder. The skill + extension are siblings under `.pi/` (`skills/planf3/` and `extensions/planf3/`) and Pi auto-discovers both when running in this repo. There is no global copy under `/root/.pi/agent/`; the previous consolidation into `~/.pi/agent/extensions/planf3/` was rolled back in favour of this project-local layout.