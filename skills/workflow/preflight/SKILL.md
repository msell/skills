---
name: preflight
description: Use before the first edit of any implementation work, such as a ticket, a spec, or a feature request. Confirms the repo, branch, worktree, and stack with the user, then waits for their answer.
---

# Preflight

Align with the user on where the work happens before any code is read or edited.

## Steps

1. Run `scripts/facts.py` from this skill's directory. Pass the ticket or spec path when the user gave one. Without a path, it reports on the current directory. The output lists the repo, branch, dirty files, worktrees, stack membership, and the ticket header lines. Done when you have read all of it. If the stack line says `unavailable`, fix the cause before you go on.

2. Build one proposal from the facts.
   - **Repo**: the ticket's `Repo:` line. Without one, use the repo that holds the files the request names.
   - **Stack**: the work is part of a stack when the ticket header says so, the ticket or spec mentions a stack, or the branch is already in one. Load the `gh-stack` skill before you create a branch.
   - **Branch**: the ticket's `Branch:` line. Propose to create it from its base when the checkout sits on trunk. A stack layer branches from the layer below it.
   - **Worktree**: propose one when the checkout is dirty, sits on an unrelated branch, or another worktree already holds the target branch. Otherwise propose the current checkout.
   - **Conflicts**: name every place where the ticket header and the facts disagree.

3. Ask the user one question with `AskUserQuestion`. State the proposal in the question text, in this form: `Work in <path> on <branch> (<stack position or no stack>), <worktree or current checkout>.` Put "Proceed as proposed" first, marked recommended. Add one option for the worktree choice and one for a different branch or stack. Done when the user has answered. Read no code and edit no file before that.

4. Set up what the user confirmed: create or switch the branch, run `gh stack init` or `gh stack add` for a stack, or call `wt-switch-create` for a worktree. Done when `git branch --show-current` in the confirmed path prints the confirmed branch. Report the path, the branch, and the stack position in one line.
