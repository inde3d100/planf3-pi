# Image Generation — Pi Adapter

Use this workflow when the user asks to generate, fill, update, or regenerate images for a plan artifact.

Normal Pi testing uses the installed Codex GPT Image 2 helper, not the upstream OpenAI API scripts.

## Primary tool

```bash
/usr/local/bin/codex-image-generate --aspect landscape --quality high -o <output.png> '<prompt>'
```

Prompt from file/stdin:

```bash
/usr/local/bin/codex-image-generate --aspect landscape --quality high -o <output.png> < <prompt-file.md>
```

## Output location

For plan `specs/example-plan.md`, save images under:

```text
specs/example-plan/images/
```

Use descriptive names:

```text
hero.png
problem.png
solution.png
phase-1.png
agent-house-flow.png
command-center-flow.png
```

## Shared image rules

- Generate only when useful for architecture, UI, workflow, or handoff clarity.
- Landscape aspect by default.
- Professional, focused, minimal.
- Match the plan's visual identity.
- Keep text shown in the image under 10 words total.
- Prefer diagrams/conceptual visuals over decorative art.
- Store the image prompt or short caption in the Markdown plan.

## Create images

1. Read the canonical Markdown plan.
2. Identify image slots or sections that need visuals.
3. Create `IMAGES_OUTPUT_DIR`.
4. Write one focused prompt per image.
5. Run `codex-image-generate` for each image.
6. Update the Markdown plan with relative image links:

```markdown
![Agent House flow](example-plan/images/agent-house-flow.png)
```

7. If an HTML preview exists, update/re-export it.

## Update images

The helper currently supports generation, not structured image editing. For updates:

1. Write a new prompt that describes the revised image.
2. Generate a replacement PNG to the same path or a versioned path.
3. If overwriting, optionally back up the old image as `<name>.bak.png`.
4. Update Markdown captions/links if needed.

## Fallback

The upstream scripts remain available as reference/fallback:

```bash
uv run scripts/generate_gpt_image.py '<prompt>' <output.png> --size 1536x1024 --quality high
uv run scripts/edit_gpt_image.py '<instruction>' <output.png> <input.png> --size 1536x1024 --quality high
```

They require `OPENAI_API_KEY`. Prefer `codex-image-generate` on this VPS because it uses existing Codex OAuth.

## Failure behavior

If image auth/tooling fails:

- Do not block the entire plan.
- Mark the image task `[f]` with the reason.
- Leave the image slot/caption in the plan for later retry.
