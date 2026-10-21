---
name: no-comments
description: Spawn Comment Sicko, fix accepted findings, and offer enforceable replacements for claimed constraints.
disable-model-invocation: true
license: MIT
compatibility: Requires Git and the installed comment-sicko subagent.
metadata:
  source: https://github.com/cursor/plugins/blob/ce649c03ac3b75b6ae80cbd15b7e2c536caedb5a/pstack/skills/no-comments/SKILL.md
---

# No comments

Spawn Comment Sicko. Act on accepted findings. Give its fresh perspective a fair hearing.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including staged and unstaged changes. Record the starting state so rejected edits can be undone without disturbing existing work.

## Steps

1. Spawn the existing `comment-sicko` subagent using the harness's delegation tool; use its plugin-qualified name when applicable. Pass the scope without restating its rules. Tell it to investigate source, callers, and history directly if its named helper skills are unavailable. If the agent is missing, stop and explain that it must be installed through the repository's plugin or `./scripts/skills link-agents` from a checkout of `msell/skills`; `npx skills` installs skills only.

2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on surprises in our own code stay actionable; keep those comments deleted. A keep needs proof that it concerns something we cannot change. Audit missed lint and TypeScript suppressions within scope. Suppressions of correctness or safety checks stay actionable `MUST KILL` findings.

   Restore deletions only with an exact exception and evidence from the scoped code. For thin `IMPORTANT` or `do not remove` claims, trace the named symbol, its callers, and relevant history before accepting a deletion or a keep. Ambiguous deletions stay deleted; refuted or ambiguous keeps are deleted. Undo only the rejected subagent edits and rerun once with the failure named. Reject a second report, report the remaining work, and mark the run failed.

3. Fix trivial accepted findings directly by deleting a dead path, dropping a parameter, or using the real API. If a finding needs a structural change, sketch the proposed shape once for the accepted findings and surrounding code before implementing it. Name the affected symbols and how the shape removes the workaround or need for the comment.

4. Implement the smallest root-cause fix within scope. Remove the accepted workarounds. When the root cause lies outside scope, make only a sound in-scope fix and report the rest open; if none is possible, leave the finding open. Keep the scope fixed and avoid adding symptom guards. Run relevant checks for application-code or suppression changes, and report any failures.

5. For constraint comments such as `do not remove`, `do not change wording`, or `talk to X before changing`, preserve proven exceptions about things we cannot change. Otherwise offer the cheapest in-scope enforcement through a type, runtime check, test, or CI lint. Use existing caller approval if it covers the proposed enforcement; otherwise wait for interactive approval. Unattended runs require caller pre-approval. When approved, encode the constraint before deleting its comment. Without approval, delete the non-exempt comment, report the constraint as unenforced, and sketch any work outside scope.

6. Report the deletion count, restored comments and their exceptions, reruns, structural sketch if needed, fixes, checks, enforcement offers and implementations, unenforced constraints, and other open work. Distinguish completed changes from unresolved findings.
