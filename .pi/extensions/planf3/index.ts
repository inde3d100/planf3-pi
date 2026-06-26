import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Extension lives at <repo>/.pi/extensions/planf3/index.ts.
// Skill content lives next to it at <repo>/.pi/skills/planf3/SKILL.md.
const EXTENSION_DIR = dirname(fileURLToPath(import.meta.url));
const SKILL_PATH = join(EXTENSION_DIR, "..", "..", "skills", "planf3", "SKILL.md");

function loadPlanf3Prompt(args: string | undefined) {
  const skill = readFileSync(SKILL_PATH, "utf8");
  const trimmed = String(args || "").trim();
  return trimmed ? `${skill}\n\nUser: ${trimmed}` : skill;
}

const PLANF3_SYSTEM_GUIDANCE = `

## Planf3 default planning/control artifact

Planf3 is the standard planning substrate on this VPS. For serious implementation work, multi-step changes, Agent House rooms, Command Center jobs, or cross-agent handoffs, create or bind a Plan Artifact v2 instead of using ad-hoc plans. Keep existing explicit plan paths when provided. For trivial direct answers, do not create unnecessary files, but prefer Planf3 whenever work will be executed, delegated, validated, or handed off.

Plan Artifact v2 should track purpose, relevant files, phases/status markers, validation commands, evidence paths, Agent House/Command Center ownership, commits, risks, and amendments. Do not mark work complete without concrete verification evidence.`;

export default function planf3Extension(pi: ExtensionAPI) {
  pi.registerCommand("planf3", {
    description: "Load the project-local Planf3 / Plan Artifact v2 meta-skill and run it with optional arguments.",
    handler: async (args, ctx) => {
      const prompt = loadPlanf3Prompt(args);
      ctx.ui.notify("Planf3 loaded as the project-local planning/control artifact.", "info");
      if (ctx.isIdle()) {
        pi.sendUserMessage(prompt);
      } else {
        pi.sendUserMessage(prompt, { deliverAs: "followUp" });
      }
    },
  });

  pi.on("before_agent_start", async (event) => {
    if (event.systemPrompt.includes("## Planf3 default planning/control artifact")) return;
    return { systemPrompt: event.systemPrompt + PLANF3_SYSTEM_GUIDANCE };
  });
}
