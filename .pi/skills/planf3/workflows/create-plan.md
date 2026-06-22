# Create Plan — Pi Adapter

Use this workflow when the user asks to plan, spec, design, or create a new Planf3 / Plan Artifact v2 artifact and no existing plan path is referenced.

## Steps

1. **Analyze the request**
   - Identify the actual work to plan.
   - Decide whether it is simple enough for the existing `writing-plans` skill or serious enough for Planf3.
   - Use Planf3 when the work involves multiple phases, Agent House, Command Center, Obsidian, git/evidence tracking, or multi-agent handoff.

2. **Explore context**
   - Read relevant repo files, existing specs, docs, Obsidian source notes, and prior plans.
   - For Agent House/Command Center work, inspect `/root/agent-house/README.md`, `/root/agent-house/COMMANDS.md`, `/root/agent-house/bin/agent-house`, and `/root/agent-house/command-center/` as needed.

3. **Create/link a goal when available**
   - If the parent Pi session has `goal_create`, create a goal for the planned work.
   - Put the returned goal id in the plan metadata.
   - If goal tools are unavailable, write `Goal ID: pending`.

4. **Design the approach**
   - Preserve existing workflows unless replacement is explicitly requested.
   - Prefer opt-in integration before default behavior.
   - Include status markers: `[]`, `[wip]`, `[x]`, `[f]`.
   - Include validation commands and evidence mapping.

5. **Write canonical Markdown**
   - Save the plan to `specs/<descriptive-kebab-name>.md`.
   - Use the skeleton from `SKILL.md`.
   - Include metadata, purpose/problem/solution, relevant files, Agent House integration, Command Center integration, phases, validation, evidence map, notes, and amendments.

6. **Optionally export HTML**
   - If the user asks for a preview/browser artifact, also read `workflows/export-html.md` and create `specs/<same-name>.html`.
   - HTML is not canonical for Pi testing; Markdown is.

7. **Optionally add image slots**
   - If images would clarify the plan, add image slots/captions in Markdown.
   - Do not generate images unless the user asks, or unless the task explicitly requests a visual plan.
   - If generating, read `workflows/image-generation.md`.

8. **Report paths**
   - Return the canonical Markdown path first.
   - Return optional HTML/images paths if created.
   - Mention the goal id if created.

## Output contract

A successful create workflow returns:

```text
Plan: specs/<name>.md
Preview: specs/<name>.html      # only if generated
Goal: goal_...                  # if created
Next: build/update/export/images command suggestion
```
