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

## Install without cloning

Once the GitHub repository is public, use the cross-agent installer to copy selected skills into a project or user profile:

```bash
npx skills@latest add msell/skills
```

Copied installs are independent snapshots. Use symlinks when this checkout is your source of truth; use `npx skills` when you want an editable copy elsewhere.

## Commands

```text
./scripts/skills check    Validate names, frontmatter, and invocation parity
./scripts/skills list     List canonical skills and invocation behavior
./scripts/skills link     Link skills into local harness directories
./scripts/skills unlink   Remove links owned by this checkout
```

## Harness references

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenAI skills](https://developers.openai.com/codex/skills)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [skills.sh installer](https://skills.sh/docs)
