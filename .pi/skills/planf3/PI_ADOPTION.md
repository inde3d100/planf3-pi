# Planf3 for Pi — adoption note

The Planf3 meta-skill lives entirely inside the project's `.pi/` folder. Both the skill content and the extension's runtime glue are siblings under `.pi/`, so Pi auto-discovers them when working in this repo.

Layout:

```text
.pi/
├── extensions/planf3/
│   └── index.ts                         # registers /planf3 + before_agent_start hook
└── skills/planf3/
    ├── SKILL.md                         # canonical meta-skill
    ├── PI_ADOPTION.md                   # this file
    ├── workflows/                       # create / update / build / export / image-gen
    └── scripts/                         # image-generation fallback/reference only
```

- Extension path: `<repo>/.pi/extensions/planf3/index.ts`
- Skill path: `<repo>/.pi/skills/planf3/SKILL.md`
- The extension resolves `SKILL.md` via a relative path (`../../skills/planf3/SKILL.md`), so the layout is portable to any clone of this repo.

Upstream lineage from IndyDevDan/disler `planf3` remains preserved at:

- `/root/projects/planf3-pi/.claude/skills/planf3/` — untouched reference copy

Image generation uses the existing VPS helper, not the bundled Python scripts:

```bash
/usr/local/bin/codex-image-generate --aspect landscape --quality high -o specs/<plan-name>/images/<slot>.png '<prompt>'
```

The bundled Python scripts under `scripts/` are kept as fallback/reference only; normal Pi sessions should prefer `codex-image-generate`. If that helper is unavailable or auth is expired, mark image generation `[f]` with the reason instead of blocking the whole plan.