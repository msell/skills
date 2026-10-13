# Matt Sell's Agent Skills

A personal, curated collection of agent skills. The repository keeps one canonical copy of each skill and exposes it to Claude Code, Codex, Cursor, and other Agent Skills-compatible harnesses.

This repository intentionally starts without skills. Add only workflows you have written, tested, and want to maintain.

## Repository layout

```text
skills/
  <category>/
    <skill-name>/
      SKILL.md
      agents/
        openai.yaml
      scripts/       # optional
      references/    # optional
      assets/        # optional
templates/
  model-invoked/
  user-invoked/
scripts/
  skills
```

`skills/` is the only installable tree. Category directories are organizational; every skill name must be unique across the repository.

Each skill follows the [Agent Skills specification](https://agentskills.io/specification):

- `SKILL.md` is required.
- Its `name` must match the containing directory.
- Its `description` explains what the skill does and when it should activate.
- Supporting files stay inside the skill directory and are referenced relative to it.
- `agents/openai.yaml` carries OpenAI-specific interface and invocation metadata.

## Add a skill

Choose the invocation model first:

- **Model-invoked**: the agent may activate the skill when its description matches the request.
- **User-invoked**: the skill runs only when you explicitly invoke it.

Copy the matching template:

```bash
mkdir -p skills/<category>
cp -R templates/model-invoked skills/<category>/<skill-name>
# or
cp -R templates/user-invoked skills/<category>/<skill-name>
```

Replace `skill-name`, the descriptions, and the template body. Then validate:

```bash
./scripts/skills check
./scripts/skills list
```

### Keep invocation behavior aligned

| Behavior | Claude Code and Cursor `SKILL.md` | OpenAI `agents/openai.yaml` |
| --- | --- | --- |
| Model-invoked | Omit `disable-model-invocation` | `policy.allow_implicit_invocation: true` or omit the policy |
| User-invoked | `disable-model-invocation: true` | `policy.allow_implicit_invocation: false` |

Cursor honors `disable-model-invocation`. Codex and ChatGPT use `agents/openai.yaml` for the equivalent OpenAI policy.

## Install from this checkout

Symlinks are the default for personal use. Editing a skill here updates every local harness immediately, and pulling the repository updates the installed skills without copying files.

```bash
./scripts/skills link
```

The default links each skill into both canonical user locations:

- `~/.claude/skills` for Claude Code
- `~/.agents/skills` for Codex, Cursor, and other compatible harnesses

Install for one harness family instead:

```bash
./scripts/skills link --harness claude-code
./scripts/skills link --harness codex
./scripts/skills link --harness cursor
```

Codex and Cursor intentionally share `~/.agents/skills`; selecting either reaches the same destination. The installer refuses to replace a real file, directory, or symlink it does not own.

Remove only symlinks managed by this checkout:

```bash
./scripts/skills unlink
```

## Install agents

Agents live in `agents/<name>.md`. The file name must match the frontmatter `name`.

```bash
./scripts/skills link-agents
./scripts/skills unlink-agents
```

`link-agents` symlinks each agent into `~/.claude/agents` for Claude Code. Codex needs TOML, so it also generates `~/.codex/agents/<name>.toml`. Run `link-agents` again after you edit an agent, because the TOML is a generated copy.

`npx skills` does not install agents. It discovers only `SKILL.md` directories, mostly under `skills/`. The `agents/` directory at the repository root is invisible to it. Agents reach a machine through the plugin or through `link-agents` in a checkout of this repository.

## Install as a plugin

The repository is also a plugin, so other people get skills and agents in one step. This is the only route that installs the agents in `agents/`.

```bash
claude plugin marketplace add msell/skills
claude plugin install msell-skills@msell-skills
```

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` serve Claude Code. Claude Code finds `skills/` and `agents/` at the repository root by default, so the manifest lists neither.
- `.cursor-plugin/plugin.json` serves Cursor. It sets `"skills": "./skills/"` and `"agents": "./agents/"`, the same fields the Cursor `pstack` plugin uses.
- Plugin agents are namespaced. Claude Code shows `comment-sicko` as `msell-skills:comment-sicko`.
- The manifests set no `version`, so Claude Code treats every commit as a new version.
- Codex has no plugin manifest here. Codex users run `link-agents` from a checkout.
- Cursor installs from its own marketplace. Another user can install this plugin only after it is listed there. I did not verify how to list it.

Run `claude plugin validate .` after you change a manifest. The warning about a missing `version` is intended.

Claude Code finds plugin skills only as `skills/<name>/SKILL.md`. If you add category directories under `skills/`, list each category in the `skills` field of `.claude-plugin/plugin.json`, for example `"skills": ["./skills/<category>/"]`.

## Install without cloning

Once the GitHub repository is public, use the cross-agent installer to copy selected skills into a project or user profile:

```bash
npx skills@latest add msell/skills
```

`npx skills` installs skills only. It never installs the agents in `agents/`. For agents, use [Install as a plugin](#install-as-a-plugin) or [Install agents](#install-agents).

Copied installs are independent snapshots. Use symlinks when this checkout is your source of truth; use `npx skills` when you want an editable copy elsewhere.

## Commands

```text
./scripts/skills check    Validate names, frontmatter, and invocation parity
./scripts/skills list     List canonical skills and invocation behavior
./scripts/skills link     Link skills into local harness directories
./scripts/skills unlink   Remove links owned by this checkout
./scripts/skills link-agents    Install agents for Claude Code and Codex
./scripts/skills unlink-agents  Remove agents installed by this checkout
```

## Harness references

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenAI skills](https://developers.openai.com/codex/skills)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [skills.sh installer](https://skills.sh/docs)
