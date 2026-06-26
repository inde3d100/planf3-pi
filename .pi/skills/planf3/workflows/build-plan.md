# Build Plan — Pi Adapter

Use this workflow when the user asks to execute, implement, or carry out an existing Planf3 / Plan Artifact v2 plan.

Task status markers: `[]` idle · `[wip]` in progress · `[x]` complete · `[f]` failed/blocked.

## Steps

1. **Locate the canonical plan**
   - Prefer `specs/<name>.md`.
   - If the user gives an HTML plan, look for the matching Markdown file first.
   - If no plan path is given, infer the most likely plan and ask before building.

2. **Absorb context**
   - Read the full plan.
   - Read depth-1 backrefs that are necessary for implementation.
   - Check current git status.
   - Confirm whether this is low-risk. Ask before high-impact actions: deletion, auth changes, production deploys, spending money, or global installs.

3. **Connect goal state**
   - If a goal id exists and goal tools are available, call `goal_update` as phases start/finish.
   - If no goal exists and the build is serious, create one before implementing.

4. **Execute phases top-to-bottom**
   - Set the active phase/task to `[wip]` in the plan.
   - Implement only the current task.
   - Run that phase's validation commands.
   - If validation passes, mark task `[x]` and record evidence.
   - If validation cannot pass, mark `[f]`, explain why, and record needed input or blocker.
   - Do not skip ahead unless the plan explicitly allows it.

5. **Record evidence**
   - For each validation command, capture command + relevant output.
   - If goal tools exist, call `goal_evidence` with file paths/commands/output.
   - Append evidence links to the plan's Evidence map.

6. **Commit when appropriate**
   - For repo changes, make focused commits after coherent phases.
   - Append commit SHAs to plan metadata after commit.

7. **Final validation**
   - Run global validation commands.
   - Use verification-before-completion discipline: no success claim without output.

8. **Report**
   - Return changed files, validation output, goal evidence ids, commit SHA(s), and remaining `[f]` items.

## Agent House / Command Center build rule

If the plan includes Agent House or Command Center sections, preserve current manual handoff and board policies unless the plan explicitly says to change them. Plan Artifact v2 should improve coordination before it changes defaults.
