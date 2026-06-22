# Update Plan — Pi Adapter

Use this workflow when the user asks to revise, extend, correct, or append to an existing Planf3 / Plan Artifact v2 plan.

## Steps

1. **Locate the plan**
   - Resolve the plan path from the prompt.
   - Prefer canonical Markdown: `specs/<name>.md`.
   - If only an HTML plan exists, update it carefully but recommend creating a Markdown canonical version before serious use.

2. **Read context**
   - Read the full plan.
   - Read mentioned backrefs if the requested change depends on them.
   - Check current git status before editing.

3. **Apply the smallest useful update**
   - Preserve existing status markers and completed evidence.
   - Append to metadata and amendments; do not rewrite history.
   - If changing scope, add an amendment explaining why.
   - If the change affects Agent House or Command Center, update those sections explicitly.

4. **Sync related outputs**
   - If an HTML preview exists and the Markdown changed materially, either update the HTML or clearly say it is stale.
   - If images are affected, read `workflows/image-generation.md` before regenerating.

5. **Update metadata**
   - Append modified ISO timestamp.
   - Append agent/session when known.
   - Append commit SHA after commit, or leave `pending` until committed.

6. **Report**
   - Return the plan path.
   - Summarize changed sections.
   - Note whether preview/images are current or stale.

## Rules

- Do not silently delete old decisions; move them to rejected approaches or amendments.
- Do not mark tasks `[x]` without evidence.
- Keep Markdown canonical.
