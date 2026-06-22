# Pi-local Planf3 adoption note

This is a project-local adoption of IndyDevDan/disler `planf3`.

- Upstream source: https://github.com/disler/planf3
- Fork: https://github.com/inde3d100/planf3-pi
- Branch: `pi-native-plan-artifact-v2`
- Scope: local/project-only; do not install globally until tested.

Bootstrap usage for this repo:

1. Use Planf3's meta-skill pattern to create living plan artifacts under `specs/`.
2. Keep upstream `.claude/skills/planf3/` intact for lineage.
3. Use `.pi/skills/planf3/` as the Pi-facing staged skill copy.
4. Adapt toward Plan Artifact v2: Markdown canonical, optional HTML export, goal/evidence integration, Agent House/Command Center integration.
