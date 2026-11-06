---
name: format-skill
description: Create, format, or repair agent skills for Claude Code, Codex, and Cursor while preserving their workflow and aligning installation paths and invocation metadata.
disable-model-invocation: true
---

# Format skill

Create a skill from the user's idea, or format and repair an existing skill supplied by name or path. Use Claude Code, Codex, and Cursor as the local targets unless the user specifies others. Check the target providers' current official documentation before translating provider-specific behavior.

## Choose the operation

- For a new skill, read [Create a skill](references/create.md).
- For an existing or installed skill, read [Repair a skill](references/repair.md). Existing paths are expected in this branch.

Finish locating the canonical source before editing. A checkout's `skills/<category>/<name>/` is canonical when its installer manages the skill. Outside a managed checkout, use `~/.agents/skills/<name>/` for a standalone user skill and a relative Claude link at `~/.claude/skills/<name>` pointing to `../../.agents/skills/<name>`.

## Format and check portability

1. Keep the workflow, inputs, outputs, and authorization boundaries intact. Every skill has `SKILL.md` and `agents/openai.yaml`. Names use 1–64 lowercase letters, numbers, and single hyphens; the directory and frontmatter names match, and the name is unique across categories.
2. Keep shared instructions in `SKILL.md`, branch-specific detail in relative references, and deterministic helpers in `scripts/`. Preserve supported Agent Skills fields, licenses, scripts, assets, and references when repairing.
3. Examine the body and supporting instructions for provider-only substitutions, dynamic shell injection, named tools, subagents, hooks, execution modes, and absolute paths. Replace constructs such as `$ARGUMENTS` with explicit instructions to read the user's request. Use portable operations or documented provider branches for tool and execution differences. Preserve required permissions and isolation; flag behavior with no equivalent rather than silently removing it.
4. Inventory required CLIs, MCP services, other skills, and agents. Verify each dependency is available to each target provider or document the setup required. Check resource paths from the skill directory and preserve executable permissions. A valid metadata file alone does not establish portability.
5. Apply the metadata rules below, preserving unrelated interface, policy, and dependency fields. Preserve an existing invocation choice; ask if conflicting settings leave the intended choice unclear. For new skills, honor the user's choice and otherwise default to user-invoked.
6. Verify the result and report compatibility separately for each target provider, distinguishing runtime checks, static walkthroughs, and unresolved dependencies.

## SKILL.md frontmatter

Use Agent Skills fields for shared metadata. Keep `disable-model-invocation` aligned with the OpenAI policy. For an existing skill's other vendor fields, preserve their behavior through a documented provider branch or report the incompatibility before removing them.

```yaml
---
name: <name>
description: <what the skill does, and the requests that should trigger it>
disable-model-invocation: true
---
```

- Omit `disable-model-invocation` for a model-invoked skill. Do not write `false`.
- Keep the description to 1024 characters or fewer.

## agents/openai.yaml

```yaml
interface:
  display_name: "<Title Case Name>"
  short_description: "<one line for people browsing the skill>"
  default_prompt: "Use $<name> to <do the task>."

policy:
  allow_implicit_invocation: false
```

- Set `allow_implicit_invocation` to `false` for a user-invoked skill.
- Set it to `true` for a model-invoked skill.
- `default_prompt` must contain `$<name>`.
- `short_description` may be shorter than the `SKILL.md` description. Do not copy trigger phrases into it.
- Keep `short_description` between 25 and 64 characters. The default prompt should demonstrate the supported operation, including repair when applicable.

## Verify

1. In a managed checkout, run `./scripts/skills check`. After adding or moving a skill, run `./scripts/skills link`. If a new category was added, include it in `.claude-plugin/plugin.json` and run `claude plugin validate .`.
2. For checkout installations, verify that both `~/.agents/skills/<name>` and `~/.claude/skills/<name>` are symlinks resolving to the canonical checkout directory and expose its `SKILL.md`. Accept absolute or relative link text. For standalone installations, verify the real directory under `~/.agents/skills`, the relative Claude link specified above, and that both paths expose the same files. Project-local installations use the selected providers' documented project roots instead.
3. Check valid YAML, matching directory/frontmatter names, and aligned invocation settings: user-invoked means `disable-model-invocation: true` and `allow_implicit_invocation: false`; model-invoked means omitting the former and allowing the latter.
4. Compare repairs with the original: preserve the task's behavior, optional metadata, licenses, resource contents, executable permissions, and valid resource links except for deliberate compatibility changes.
5. Walk through a representative request for each target provider using its available tools and dependency setup. Where practical, confirm discovery and invocation in that provider. Report a static walkthrough as such; report unavailable providers or dependencies as unverified rather than claiming runtime compatibility.

Fix failures introduced by the changes and rerun the affected checks. If installation conflicts with an unrelated existing path, report the exact path and leave it intact. Report changed source paths, checks run, and any remaining incompatibilities or installation blockers.
