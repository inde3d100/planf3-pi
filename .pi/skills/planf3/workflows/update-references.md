# Update References — Pi Adapter

Use this workflow when the user asks to refresh plan metadata, references, commits, source links, goal/evidence ids, or session information.

## Steps

1. **Locate the canonical plan**
   - Prefer `specs/<name>.md`.
   - If the plan has an HTML preview, keep it in sync only if requested.

2. **Read current metadata**
   - Created
   - Modified list
   - Goal id
   - Command Center job id
   - Agent House room/run
   - Backrefs and forward refs
   - Commits
   - Evidence map

3. **Collect current facts**
   - `git rev-parse --short HEAD` for current commit when relevant.
   - `git status --short` for dirty state.
   - Goal/evidence ids from the active Pi goal if available.
   - Source note paths, Obsidian wikilinks, room result folders, and Command Center board ids.

4. **Append-only update**
   - Append new modified timestamp.
   - Append new commits/evidence/backrefs/forward refs.
   - Do not delete prior metadata unless it is a clear typo; if changing meaning, add an amendment.

5. **Report**
   - Return updated metadata fields.
   - Mention whether canonical Markdown and optional HTML preview are in sync.
