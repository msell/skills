Canonical skills live at `skills/<category>/<skill-name>`. Templates live outside that tree so installers never discover them.

Every skill must follow the Agent Skills specification, keep its directory name and frontmatter `name` identical, and include `agents/openai.yaml`. Skill names must be unique across categories because user-level installers flatten them into one directory.

Choose invocation deliberately. A user-invoked skill has both `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. A model-invoked skill omits the Claude field and allows implicit invocation in OpenAI metadata.

Keep `SKILL.md` on the common path. Put branch-specific details in relative references and deterministic helpers in `scripts/`.

Run `./scripts/skills check` after changing any skill or its metadata. Run `./scripts/skills link` after adding or renaming a skill in this checkout.
