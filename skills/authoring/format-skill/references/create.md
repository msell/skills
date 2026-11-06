# Create a skill

1. Choose the name and source location. In a checkout with `scripts/skills`, follow its `AGENTS.md` and use `skills/<category>/<name>/`. Otherwise use the standalone layout in `SKILL.md`, unless the user requested a project-local skill.
2. Check the source and target installation paths for name collisions, including dangling symlinks. If the requested skill already exists, use the repair branch. If a different skill occupies a path, report the collision before writing.
3. Write the workflow and metadata using the common formatting and portability rules in `SKILL.md`. Include only resources the workflow needs.
4. In a checkout, use its installer. For a standalone skill, create missing parent directories, write the real skill under `~/.agents/skills/<name>/`, and create `~/.claude/skills/<name>` as a relative symlink to `../../.agents/skills/<name>`. Use the documented discovery paths for any other requested providers or project scope.
5. Return to the verification section in `SKILL.md`.
