# Agent House + Command Center Plan Artifacts v2 Integration

## Metadata

- Created: 2026-06-22T20:29:22Z
- Modified:
  - 2026-06-22T20:29:22Z
- Source request: "create a Plan Artifact v2 implementation plan for integrating plan artifacts into Agent House handoffs and Command Center board jobs. Use questionable=true. Save Markdown canonical under specs/ and include optional image slots but do not generate images yet."
- Goal ID: pending
- Command Center job: n/a — plan artifact only; no board job started
- Agent House room: command-center suggested owner; no room started
- Status: [] draft
- Questionable: true
- Backrefs:
  - `/root/projects/planf3-pi/.pi/skills/planf3/SKILL.md` — project-local Planf3 Pi adapter (lives under this repo's `.pi/`).
  - `/root/projects/planf3-pi/.pi/skills/planf3/workflows/create-plan.md` — create-plan workflow followed.
  - `/root/projects/planf3-pi/.pi/extensions/planf3/index.ts` — project-local Planf3 extension runtime glue.
  - `/root/agent-house/README.md` — current Agent House room/result/handoff model.
  - `/root/agent-house/COMMANDS.md` — current CLI and manual handoff rules.
  - `/root/agent-house/bin/agent-house` — room prompts, handoff text, CLI startup, result-folder behavior.
  - `/root/agent-house/command-center/README.md` — current automated board/job model and goal audit layer.
  - `/root/agent-house/command-center/schema.sql` — board schema for runs/tasks/events/artifacts/goals.
  - `/root/agent-house/command-center/room_dispatcher.py` — run bootstrap, routing, task envelope, dashboard, closeout.
  - `/root/agent-house/command-center/result_contract.py` — `ROOM_RESULT.json` contract.
- Forward refs:
  - `/root/agent-house/bin/agent-house` — add plan-aware handoff/task prompt sections.
  - `/root/agent-house/tests/test_agent_house_plan_artifacts.py` — new Agent House tests.
  - `/root/agent-house/command-center/schema.sql` — add additive plan fields or registry table.
  - `/root/agent-house/command-center/room_dispatcher.py` — thread plan paths through runs/tasks and room prompts.
  - `/root/agent-house/command-center/tests/test_plan_artifacts.py` — new Command Center tests.
  - `/root/agent-house/command-center/runs/<run-id>/PLAN_ARTIFACT.md` — optional per-run copy/symlink target.
- Commits:
  - pending

## Purpose

Make Plan Artifact v2 the shared control surface for serious multi-room work: Agent House rooms should pass the active plan through handoffs, and Command Center board jobs should store, route, audit, and close out against the same plan artifact.

## Problem

Agent House handoffs and Command Center board jobs already create useful files, but the task intent, phase checklist, room ownership, evidence, defects, amendments, and closeout criteria can drift across `TASK.md`, `HANDOFF.md`, `ROOM_RESULT.json`, SQLite board rows, final reports, and goal audit exports.

Without a plan-aware integration, a room can continue from a handoff while missing the canonical plan, and Command Center can complete a run without proving that the plan's validation/evidence map was updated.

## Solution

Implement opt-in Plan Artifact v2 support across Agent House and Command Center without replacing current workflows:

1. Treat a Markdown plan path as an optional first-class context object.
2. Detect or accept the plan path at CLI/run creation time.
3. Copy or reference the active plan in result/run folders.
4. Require handoffs to include the active plan path and what was updated.
5. Add Command Center board metadata so runs/tasks know which plan they execute.
6. During closeout, verify the plan has current status markers, validation results, evidence paths, and amendments.

The first version should be conservative: no auto-started next rooms, no global skill install, no automatic edits to plans unless a room or Command Center step is explicitly operating from a plan path.

## Backrefs and forward refs

- Backrefs are listed in metadata and should be kept current when this plan is updated.
- Forward refs are expected implementation targets and test files; update them after implementation creates or changes those paths.
- When a Command Center run is created from this plan later, add the `run_id`, run folder, final evidence paths, and commit hashes here.

## Goal integration

Goal tools are not available in this parent Pi session, so this artifact uses placeholders.

- Goal ID: pending
- Parent goal objective: Integrate Plan Artifact v2 into Agent House handoffs and Command Center board jobs.
- Child goal candidates:
  - Agent House handoffs include and preserve active plan paths.
  - Command Center board runs/tasks persist plan artifact paths.
  - Command Center room attempts receive plan-aware task context.
  - Closeout validates plan status/evidence before marking done.
- Evidence: pending

When goal tools are available during build:

- Create/link a parent goal before implementation.
- Add `goal_evidence` for passing tests, dry-run output, schema migration proof, and a sample run folder.
- Do not mark complete until Agent House and Command Center validations pass.

## Agent House integration

Agent House should stay manual-handoff-first and plan-aware when a plan path exists.

Desired behavior:

- Input detection:
  - If `--task` contains a readable Markdown path matching `specs/*.md`, `/root/.../*.md`, or a `Plan artifact:` line, treat it as the active plan.
  - Optionally support an explicit future flag: `agent-house enter <room> --plan specs/example.md --task "..."`.
- Room startup:
  - Add the active plan path to `TASK.md` and the orchestrator initial message.
  - Tell the orchestrator to read the plan before delegation.
  - Tell workers to update only their assigned phase/status/evidence notes, not rewrite the whole plan casually.
- Result folders:
  - Add `PLAN_ARTIFACT.md` as a copy or symlink/reference file in the result folder.
  - Include a small `PLAN_ARTIFACT.json` metadata file only if useful for automation.
- Handoffs:
  - `HANDOFF.md` must include `Active plan artifact: <path>`.
  - The `Manual handoff` block must tell the next room to read the plan and the handoff.
  - Recommended command example:
    - `agent-house enter <room> --task "Read <HANDOFF.md> and <PLAN.md>; continue the next unchecked phase."`
- Safety:
  - Keep the existing rule: do not start the next room automatically.
  - Never invent room names; use only valid room slugs.
  - Ask before deleting data, changing auth, spending money, deploying, or making irreversible changes.

Likely code touchpoints:

- `agent-house/bin/agent-house`
  - `manual_handoff_instruction()`
  - `handoff_markdown()`
  - `handoff_initial_message()`
  - `orchestrator_initial_message()`
  - `room_agent_prompt()`
  - result folder creation / `TASK.md` writing paths

## Command Center integration

Command Center should store the active plan path in board state and route it through every room task.

Desired behavior:

- Run creation:
  - Accept an optional plan path, either detected from task text or via a future flag: `./command-center run --plan specs/example.md "..."`.
  - Validate that the plan path exists and is readable before bootstrapping a plan-bound run.
  - Store canonical absolute path plus optional per-run copy path.
- Board state:
  - Persist plan metadata on `runs` and, if needed, tasks.
  - Preferred minimal schema: additive nullable columns on `runs`: `plan_artifact_path`, `plan_artifact_snapshot_path`, `plan_artifact_status`.
  - Alternative schema: a `plan_artifacts` table linked to runs/tasks if multiple plans per run become necessary.
- Task envelope:
  - Add `plan_artifact_path` to `TaskEnvelope` or task metadata passed to `run_room_attempt()`.
  - Include the plan path in `_initial_task_body()` so every room receives it naturally.
- Artifacts/events:
  - Record plan snapshots/updates in `task_artifacts` with `kind='plan_artifact'` or `kind='plan_update'`.
  - Emit task events when a room starts with a plan, updates a phase, records evidence, or fails plan validation.
- Closeout:
  - Before writing final success, check that the plan has a current amendment or evidence/status update for the run.
  - Include the plan path in `FINAL_RESULT.md`, `ROOM_RESULTS.json`, `GOAL_AUDIT.json`/`GOALS.md` references, and final package `system/` or `handoffs/`.
- Dashboard/status:
  - Show active plan path in status/results panes without cluttering the main dashboard.

Likely code touchpoints:

- `/root/agent-house/command-center/schema.sql`
- `/root/agent-house/command-center/room_dispatcher.py`
- `/root/agent-house/command-center/room_runtime.py`
- `/root/agent-house/command-center/report_writer.py`
- `/root/agent-house/command-center/result_contract.py` only if `ROOM_RESULT.json` should include plan metadata directly.

## Relevant files

### Existing

- `/root/agent-house/bin/agent-house` — user-facing CLI, room prompts, result folders, manual handoff instructions.
- `/root/agent-house/README.md` — room model and result folder contract.
- `/root/agent-house/COMMANDS.md` — CLI behavior and manual handoff examples.
- `/root/agent-house/tests/` — Agent House CLI/room test suite.
- `/root/agent-house/command-center/README.md` — Command Center behavior and final output shape.
- `/root/agent-house/command-center/schema.sql` — SQLite board schema.
- `/root/agent-house/command-center/room_dispatcher.py` — run/task lifecycle, routing, dashboard, closeout.
- `/root/agent-house/command-center/room_runtime.py` — room attempt execution boundary.
- `/root/agent-house/command-center/result_contract.py` — room result validation.
- `/root/agent-house/command-center/report_writer.py` — final success/blocked package writing.
- `/root/agent-house/command-center/tests/` — Command Center regression suite.
- `/root/projects/planf3-pi/.pi/skills/planf3/SKILL.md` — project-local Planf3 skill contract.

### New

- `/root/agent-house/tests/test_agent_house_plan_artifacts.py` — tests for plan path detection, prompt text, and handoff rendering.
- `/root/agent-house/command-center/tests/test_plan_artifacts.py` — tests for schema, bootstrap, task context, events/artifacts, and closeout references.
- `/root/agent-house/command-center/docs/plans/plan-artifacts-v2-integration.md` — optional implementation notes if Command Center wants a local copy.
- `/root/agent-house/command-center/runs/<run-id>/PLAN_ARTIFACT.md` — per-run plan snapshot/copy/reference target.
- `/root/agent-house/<room>/results/<stamp>/PLAN_ARTIFACT.md` — per-room active plan snapshot/copy/reference target.

## Optional image slots

Images are planned placeholders only. Do not generate them until explicitly requested.

- [] `specs/agent-house-command-center-plan-artifacts-v2-integration/images/context-map.png`
  - Caption: Plan path connects rooms, board, evidence, and closeout.
  - Prompt: "Dark terminal workflow diagram. One markdown plan artifact links Agent House rooms, Command Center board, validation evidence, and final closeout. Minimal labels: Plan, Rooms, Board, Evidence."
- [] `specs/agent-house-command-center-plan-artifacts-v2-integration/images/handoff-flow.png`
  - Caption: Manual handoff keeps human control while preserving plan context.
  - Prompt: "Clean systems diagram of manual handoff from one agent room to next. Shared plan artifact travels with HANDOFF.md. Minimal labels: Room A, Plan, Room B."
- [] `specs/agent-house-command-center-plan-artifacts-v2-integration/images/board-schema.png`
  - Caption: Command Center stores the active plan on each run.
  - Prompt: "SQLite board schema concept with runs table linked to plan artifact, tasks, artifacts, and goal evidence. Minimal labels: runs, plan, tasks, evidence."

## Implementation phases

### [] Phase 1: Contract and acceptance criteria

Define the smallest Plan Artifact v2 integration contract before editing code.

- [] Define what counts as an active plan path in task text.
- [] Decide whether first implementation supports detection only or adds explicit `--plan` flags.
- [] Define whether Agent House result folders copy, symlink, or reference the canonical plan.
- [] Define whether Command Center stores plan data as additive columns or a new linked table.
- [] Define closeout criteria: plan path present, plan readable, run amendment exists, validation/evidence section updated.

#### Validation

- [] `grep -n "Active plan artifact" /root/agent-house/bin/agent-house` — after implementation, proves prompts/handoffs mention the active plan.
- [] `grep -n "plan_artifact" /root/agent-house/command-center/schema.sql /root/agent-house/command-center/room_dispatcher.py` — after implementation, proves Command Center has plan-aware state.

### [] Phase 2: Agent House plan-aware handoffs

Make room startup and manual handoff preserve the plan path.

- [] Add a helper to extract readable plan artifact paths from task text.
- [] Add an active-plan section to generated `TASK.md` when a plan exists.
- [] Update `room_agent_prompt()` so orchestrators/workers know how to consume and update a provided plan.
- [] Update `orchestrator_initial_message()` to read the plan before delegation.
- [] Update `manual_handoff_instruction()` to require `Active plan artifact` in `HANDOFF.md` when a plan exists.
- [] Update `handoff_markdown()` and `handoff_initial_message()` to carry the plan path to the target room.
- [] Add tests for path extraction, dry-run rendering, and handoff text.

#### Validation

- [] `cd /root/agent-house && python3 -m pytest tests/test_agent_house_plan_artifacts.py -q` — new Agent House plan tests pass.
- [] `cd /root/agent-house && python3 -m pytest tests -q` — existing Agent House tests still pass.
- [] `agent-house enter intelligence --dry-run --task "Read /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration.md and summarize next phase"` — dry-run carries plan-aware task text without starting a room.

### [] Phase 3: Command Center board schema and bootstrap

Persist the plan artifact on board jobs with an additive migration path.

- [] Add nullable plan artifact fields to `runs` via `schema.sql` and `_ensure_additive_schema()`.
- [] Add optional CLI argument `--plan` to `./command-center run` and/or path detection from task text.
- [] Validate readable plan paths before plan-bound run creation.
- [] Store canonical plan path and optional snapshot path in the run row.
- [] Write plan metadata into `BOARD_SNAPSHOT.json`.
- [] Add board/schema/bootstrap tests.

#### Validation

- [] `cd /root/agent-house/command-center && python3 -m pytest tests/test_plan_artifacts.py tests/test_board_schema.py tests/test_dispatcher_bootstrap.py -q` — schema/bootstrap plan tests pass.
- [] `cd /root/agent-house/command-center && ./command-center run --dry-run --plan /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration.md "Plan-bound dry run"` — creates board state without launching rooms.
- [] `sqlite3 /root/agent-house/command-center/automation-board.sqlite '.schema runs' | grep plan_artifact` — confirms additive fields exist after init.

### [] Phase 4: Command Center room task routing

Make each room attempt receive the active plan path and record plan-related artifacts/events.

- [] Add plan path to task metadata passed through the dispatcher/runtime boundary.
- [] Include plan path in `_initial_task_body()` for every pipeline room.
- [] Record `task_events` when a plan-bound room starts and completes.
- [] Record plan snapshot/reference in `task_artifacts` using a stable kind.
- [] Ensure Quality Gate receives the plan path and checks the plan evidence/status sections during review.
- [] Add tests using injected room runners so no live rooms start.

#### Validation

- [] `cd /root/agent-house/command-center && python3 -m pytest tests/test_dispatcher_loop.py tests/test_room_runtime.py tests/test_plan_artifacts.py -q` — dispatcher/runtime tests pass.
- [] `cd /root/agent-house/command-center && ./command-center events <run-id> -k task_created,plan_artifact --tail 20` — plan events are visible for a dry-run or test run.

### [] Phase 5: Closeout, reports, dashboard, and final package

Ensure final outputs and operator views point back to the plan.

- [] Add active plan path to `status`, dashboard detail panes, and final review output.
- [] Add plan references to success and blocked reports.
- [] Include plan snapshot/reference in the final package under `system/`, `handoffs/`, or a dedicated path.
- [] Block or warn on success if the plan has not been amended/updated during a plan-bound run.
- [] Add tests for final package output and blocked-plan validation.

#### Validation

- [] `cd /root/agent-house/command-center && python3 -m pytest tests/test_report_writer.py tests/test_results_output_ui.py tests/test_goal_audit.py tests/test_plan_artifacts.py -q` — closeout/report tests pass.
- [] `cd /root/agent-house/command-center && ./command-center status <run-id>` — status includes active plan path for plan-bound runs.

### [] Phase 6: End-to-end smoke test and adoption decision

Prove the integration reduces drift before making it default.

- [] Run an Agent House dry-run from this plan and inspect generated handoff text.
- [] Run a Command Center dry-run from this plan and inspect `BOARD_SNAPSHOT.json`.
- [] Run one low-risk live plan-bound workflow only after dry-run validations pass.
- [] Add evidence paths and run IDs to this plan's Amendments section.
- [] Decide whether to keep opt-in only, add default detection, or expose a documented `--plan` flag.

#### Validation

- [] `git -C /root/agent-house status --short` — implementation diff is reviewable.
- [] `cd /root/agent-house && python3 -m pytest tests -q && cd command-center && python3 -m pytest tests -q` — full local test suite passes.
- [] Inspect one run folder and confirm `TASK.md`, `HANDOFF.md`, board snapshot, final reports, and this plan all reference each other.

## Global validation

- [] `test -f /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration.md` — canonical Markdown plan exists.
- [] `grep -n "## Questionables" /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration.md` — questionable=true section exists.
- [] `grep -n "Optional image slots" /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration.md` — image slots are included without generated images.
- [] `find /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration -type f 2>/dev/null | wc -l` — should be `0` until image generation is explicitly requested.

## Evidence map

- Plan artifact created → `test -f /root/projects/planf3-pi/specs/agent-house-command-center-plan-artifacts-v2-integration.md`
- Questionables included → `grep -n "## Questionables" specs/agent-house-command-center-plan-artifacts-v2-integration.md`
- Agent House handoff support → pytest output from `/root/agent-house/tests/test_agent_house_plan_artifacts.py`
- Command Center schema support → pytest output from `/root/agent-house/command-center/tests/test_plan_artifacts.py` plus `.schema runs` evidence
- Room routing support → Command Center injected-runner test output and `BOARD_SNAPSHOT.json` containing plan path
- Closeout support → final package path containing active plan reference
- End-to-end proof → run folder path, final report path, and this plan's Amendments section updated with run ID/commit

## Questionables

- Should the first implementation add a public `--plan` flag or only detect plan paths in task text?
  - Recommendation: do both if small; detection preserves current UX, `--plan` makes tests and operator intent clearer.
- Should result folders copy, symlink, or only reference the canonical Markdown plan?
  - Recommendation: reference canonical path first; optionally copy a snapshot for Command Center final packages. Avoid symlinks unless tests prove they survive packaging and review.
- Should `ROOM_RESULT.json` require a plan field?
  - Recommendation: not initially. Keep `ROOM_RESULT.json` stable and record plan metadata in board/artifacts. Add optional `plan_artifact_path` later if Quality Gate needs machine-readable enforcement.
- Should Command Center mutate the plan automatically?
  - Recommendation: only append structured amendments/status evidence in narrow, tested places. Avoid broad rewrite automation.
- Should a plan-bound run fail if the plan was not updated?
  - Recommendation: warn in Phase 5 first; fail only after one live proof shows the check is reliable.
- Should Plan Artifact v2 become default for all Agent House tasks?
  - Recommendation: no. Keep it opt-in for serious/multi-room/Command Center work until it proves cleaner evidence and fewer handoff misses.
- Should image slots be generated as part of this plan?
  - Recommendation: no. The user explicitly requested slots only; generate later with `codex-image-generate` if visual handoff clarity is needed.

## Notes

- This plan is intentionally additive. It should not replace Agent House manual handoff policy or Command Center's existing board/goal audit layer.
- The safest first proof is a dry-run-only implementation test, followed by one low-risk live plan-bound task.
- Avoid behavior-changing global Planf3 installation until local evidence proves the workflow helps.
- Keep valid room slugs strict: `command-center`, `intelligence`, `build-studio`, `quality-gate`, `launch-room`, `growth-lab`, `product-design`.
- Rejected for v1: automatic next-room starts, mandatory plan artifacts for every room, broad automatic rewriting of Markdown plans, and user-facing publish/deploy behavior changes.

## Risks

- Plan mutation conflicts: multiple rooms could edit the same Markdown file concurrently.
  - Mitigation: append-only amendments and narrow status updates; Command Center can snapshot before/after.
- Board schema drift: adding columns without migration tests could break old DBs.
  - Mitigation: additive nullable columns plus `_ensure_additive_schema()` tests.
- Handoff verbosity: adding plan context could make prompts too long.
  - Mitigation: include path and next unchecked phase, not the whole plan body.
- False closeout failures: plan validation may block valid runs if too strict.
  - Mitigation: warn first, then hard-fail only after proof.

## Amendments

- 2026-06-22T20:29:22Z — Created canonical Markdown Plan Artifact v2 integration plan with questionable=true and image slots only; no images generated.
