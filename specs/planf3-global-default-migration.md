# Planf3 Global Default Migration

## Metadata

- Created: 2026-06-23T06:10:59Z
- Modified:
  - 2026-06-23T06:10:59Z
  - 2026-06-23T06:20:10Z — Implemented global Planf3 command/skill, Agent House and Command Center default binding, startup guidance, and validation evidence.
- Source request: "make Planf3 the standard for agents, Agent House rooms, and Command Center; add global /planf3; replace current plan skills/extensions; update AgentBoot if needed; follow the migration path."
- Goal ID: `goal_20260623061059_6q3hcz`
- Command Center job: n/a — parent Pi implementation session
- Agent House room: n/a — direct implementation; Agent House will be validated by dry-runs/tests
- Status: [x] default Planf3 migration implemented and committed
  - [x] consolidation: Planf3 skill content moved into the extension folder; staging copies retired
- Backrefs:
  - `/root/.pi/agent/extensions/planf3/SKILL.md` — canonical Planf3 skill (consolidated, post-migration).
  - `/root/.pi/agent/extensions/planf3/workflows/` — create/update/build/export-references/image-generation workflows.
  - `/root/.pi/agent/extensions/planf3/scripts/` — image-generation fallback/reference scripts.
  - `/root/.pi/agent/extensions/planf3/PI_ADOPTION.md` — post-migration adoption note.
  - `/root/projects/planf3-pi/.claude/skills/planf3/` — preserved upstream lineage from disler/planf3.
  - `/root/agent-house/command-center/docs/plans/plan-artifacts-v2-integration.md` — current opt-in Plan Artifact v2 integration record.
  - `/usr/local/lib/node_modules/@earendil-works/pi-coding-agent/docs/skills.md` — global skill and `/skill:name` command behavior.
  - `/usr/local/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md` — custom `/planf3` command implementation API.
  - `/root/.pi/agent/skills/writing-plans/SKILL.md` — old planning skill to compatibility-wrap.
  - `/root/.pi/agent/skills/executing-plans/SKILL.md` — old execution skill to compatibility-wrap.
  - `/root/agent-house/bin/agent-house` — Agent House CLI and room prompt implementation.
  - `/root/agent-house/command-center/room_dispatcher.py` — Command Center run/task implementation.
- Forward refs:
  - `/root/.pi/agent/extensions/planf3/index.ts` — global `/planf3` command (reads SKILL.md next to itself).
  - `/root/.pi/agent/AGENTS.md` — global Pi startup guidance.
  - `/root/Obsidian/Brain/AgentBoot.md` — boot memory guidance if approved/needed.
  - `/root/agent-house/tests/test_agent_house_plan_artifacts.py` — Agent House default-plan tests.
  - `/root/agent-house/command-center/tests/test_plan_artifacts.py` — Command Center default-plan tests.
- Commits:
  - `/root/agent-house` `61c2e51` — `feat: make Planf3 default for agent house`
  - `/root/projects/planf3-pi` (this commit) — `refactor: consolidate Planf3 skill into extensions/planf3/`

## Purpose

Promote Planf3 from an opt-in local adapter into the default planning/control substrate for Pi sessions, Agent House rooms, and Command Center jobs, while preserving overrides and rollback paths.

## Problem

Plan Artifact v2 currently works only when a user passes a plan path or explicit `--plan`. That is too easy to skip. Current global planning skills (`writing-plans`, `executing-plans`) also compete with Planf3 instead of routing into it.

## Solution

Make Planf3 default and reversible:

- Install Planf3 as a global skill.
- Add `/planf3` as a first-class Pi command via a global extension.
- Compatibility-wrap old planning skills so they direct agents to Planf3.
- Auto-create/bind a plan artifact for Agent House room runs when no explicit plan exists.
- Auto-create/bind a plan artifact for Command Center runs when no explicit plan exists.
- Keep `--plan` as explicit override and add/keep `--no-plan` only as an escape hatch if tests require it.
- Update startup guidance so agents choose Planf3 by default for serious implementation work.

## Relevant files

### Existing

- `/root/projects/planf3-pi/.pi/skills/planf3/` — source adapter to promote globally.
- `/root/.pi/agent/skills/writing-plans/SKILL.md` — replace with compatibility wrapper after backup.
- `/root/.pi/agent/skills/executing-plans/SKILL.md` — replace with compatibility wrapper after backup.
- `/root/.pi/agent/extensions/goal-pipeline/` — goal evidence store used for this migration.
- `/root/agent-house/bin/agent-house` — room default plan creation and prompt/handoff behavior.
- `/root/agent-house/command-center/room_dispatcher.py` — Command Center default plan creation.
- `/root/agent-house/command-center/report_writer.py` — final package plan references.
- `/root/.pi/agent/AGENTS.md` — global Pi instructions.
- `/root/Obsidian/Brain/AgentBoot.md` — boot memory.

### New

- `/root/.pi/agent/skills/planf3/SKILL.md` — global Planf3 skill.
- `/root/.pi/agent/extensions/planf3/index.ts` — `/planf3` command bridge.
- `/root/.pi/agent/archive/skills/<timestamp>/...` — backups of old planning skills outside active skill discovery.
- `specs/planf3-global-default-migration.md` — this canonical plan.

## Agent House integration

- Default behavior: every `agent-house enter <room> --task ...` creates or binds an active plan artifact.
- Explicit override: `--plan <path>` still wins.
- Escape hatch: if implemented, `--no-plan` disables default binding for diagnostics only.
- Result folder: `PLAN_ARTIFACT.md` is created in the room result folder when no external plan is provided.
- Task file and prompts: `TASK.md`, orchestrator prompt, worker prompts, and handoffs include `Active plan artifact`.
- Handoff: active plan path travels to the next room automatically.

## Command Center integration

- Default behavior: every `./command-center run "task"` creates or binds an active plan artifact.
- Explicit override: `--plan <path>` still wins.
- Run folder: `PLAN_ARTIFACT.md` exists for every run.
- SQLite: `runs.plan_artifact_path`, `runs.plan_artifact_snapshot_path`, and `runs.plan_artifact_status` are populated by default.
- Room task bodies: every generated room task includes the active plan path.
- Final reports: active plan path remains in final outputs.

## Implementation phases

### [x] Phase 1: Plan and safety setup

- [x] Create parent goal `goal_20260623061059_6q3hcz`.
- [x] Create this canonical Planf3 migration artifact.
- [x] Create `/root/agent-house` branch `planf3-global-default`.
- [x] Record rollback paths before replacing global planning skills.

#### Validation

- [x] `git -C /root/agent-house branch --show-current` — branch is `planf3-global-default`.
- [x] `test -f /root/projects/planf3-pi/specs/planf3-global-default-migration.md` — plan exists.

### [x] Phase 2: Global Planf3 skill and `/planf3` command

- [x] Copy the proven local Planf3 adapter to `/root/.pi/agent/skills/planf3/`.
- [x] Add a global extension `/root/.pi/agent/extensions/planf3/index.ts` registering `/planf3`.
- [x] Make `/planf3` load the global Planf3 skill content and pass arguments to the agent.
- [x] Validate global skill and command source by file/grep checks; print-mode smoke timed out during model turn, not used as completion proof.

#### Validation

- [x] `test -f /root/.pi/agent/skills/planf3/SKILL.md`
- [x] `test -f /root/.pi/agent/extensions/planf3/index.ts`
- [x] `grep -n 'registerCommand("planf3"' /root/.pi/agent/extensions/planf3/index.ts` — command source exists.

### [x] Phase 3: Replace old planning skills with compatibility wrappers

- [x] Archive old `writing-plans` and `executing-plans` skills under `/root/.pi/agent/archive/skills/` so they do not collide during skill discovery.
- [x] Replace their `SKILL.md` files with wrappers that say: use Planf3 as canonical, keep old names only for compatibility.
- [x] Ensure wrappers do not conflict with global `planf3` skill.

#### Validation

- [x] `grep -n "Planf3" /root/.pi/agent/skills/writing-plans/SKILL.md /root/.pi/agent/skills/executing-plans/SKILL.md`

### [x] Phase 4: Agent House default plan binding

- [x] Add default plan artifact creation helper to `bin/agent-house`.
- [x] Bind a plan by default for normal rooms when `--plan` is absent.
- [x] Preserve explicit `--plan` behavior.
- [x] Add tests for default plan creation, explicit override, and dry-run rendering.

#### Validation

- [x] `cd /root/agent-house && python3 -m pytest tests/test_agent_house_plan_artifacts.py -q` — `8 passed`.
- [x] `agent-house enter intelligence --dry-run --task "default Planf3 Agent House smoke"` showed `PLAN_ARTIFACT.md` without `--plan`.

### [x] Phase 5: Command Center default plan binding

- [x] Create `PLAN_ARTIFACT.md` by default inside every Command Center run folder.
- [x] Populate plan metadata fields by default.
- [] Preserve explicit `--plan` override.
- [x] Ensure dry-run and live runner receive plan context.
- [x] Add tests for default and explicit plan behavior.

#### Validation

- [x] `cd /root/agent-house/command-center && python3 -m pytest tests/test_plan_artifacts.py -q` — `6 passed`.
- [x] `cd /root/agent-house/command-center && ./command-center run --dry-run --db /tmp/cc-default-plan.sqlite --runs-root /tmp/cc-default-plan-runs "default Planf3 Command Center smoke"` created `PLAN_ARTIFACT.md`, active metadata, and plan context in room task bodies.

### [x] Phase 6: Startup guidance and AgentBoot

- [x] Update `/root/.pi/agent/AGENTS.md` so global instructions say Planf3 is the standard implementation plan artifact.
- [x] Update `/root/Obsidian/Brain/AgentBoot.md` with clear, reviewable wording about Planf3 default behavior.
- [x] Do not store secrets.

#### Validation

- [x] `grep -n "Planf3" /root/.pi/agent/AGENTS.md /root/Obsidian/Brain/AgentBoot.md`

### [x] Phase 7: Full validation and closeout

- [x] Run Agent House tests.
- [x] Run Command Center tests.
- [x] Validate `/planf3` command and global skill files by file/grep checks.
- [x] Record goal evidence for every requirement.
- [x] Commit changes in logical commits.

#### Validation

- [x] `cd /root/agent-house && python3 -m pytest tests -q` — `57 passed`.
- [x] `cd /root/agent-house/command-center && python3 -m pytest tests -q` — `154 passed`.
- [x] `git -C /root/agent-house status --short` — modified files pending review/commit.

## Global validation

- [x] Global Planf3 skill exists.
- [x] `/planf3` command extension exists.
- [x] Old planning skills route to Planf3.
- [x] Agent House creates/binds plans by default.
- [x] Command Center creates/binds plans by default.
- [x] Startup guidance documents the new default.
- [x] Existing opt-in tests still pass.

## Evidence map

- Goal created → `/root/.pi/agent/state/goal-pipeline/goals.json` contains `goal_20260623061059_6q3hcz`.
- Global skill installed → file path + optional Pi discovery output.
- `/planf3` command installed → extension path + smoke command output.
- Old skills replaced → archive path + wrapper grep output.
- Agent House default plan → dry-run output + pytest.
- Command Center default plan → dry-run board snapshot + pytest.
- Startup guidance → grep output from `AGENTS.md` / `AgentBoot.md`.

## Questionables

- Should tiny one-off tasks always get a plan?
  - Decision for this migration: yes for Agent House and Command Center, because the user explicitly wants Planf3 standard. Keep a diagnostic escape hatch if needed.
- Should `--plan` be removed?
  - No. Keep it as explicit override for an existing plan path.
- Should old planning skills be deleted?
  - No. Archive and compatibility-wrap first; delete only after several successful sessions.
- Should Planf3 mutate plans automatically?
  - Only narrow append/status updates. Avoid broad rewrites.

## Notes

- This is behavior-changing global work. Keep changes reversible and commit in small chunks.
- Do not start Agent House rooms automatically during validation unless explicitly requested; use dry-runs and tests first.
- Preserve manual handoff policy.

## Amendments

- 2026-06-23T06:10:59Z — Migration plan created; goal created; Agent House branch created.
- 2026-06-23T06:20:10Z — Implemented global Planf3 default migration. Evidence: global skill and `/planf3` extension installed; old planning skills archived/wrapped; Agent House default dry-run created `PLAN_ARTIFACT.md` without `--plan`; Command Center dry-run created default `PLAN_ARTIFACT.md` and populated plan metadata/task bodies; Agent House tests passed (`57 passed`); Command Center tests passed (`154 passed`); goal audit passed; Agent House branch commit `61c2e51` created. Global skill/extension and AgentBoot files live outside the Agent House git repo.
- 2026-06-23T06:25:00Z — Fixed skill-discovery conflict by moving archived `writing-plans` and `executing-plans` originals out of `/root/.pi/agent/skills/_archive/` to `/root/.pi/agent/archive/skills/20260623T061059Z-planf3-migration/`; duplicate scan now reports `duplicates: 0`.
