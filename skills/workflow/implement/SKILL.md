---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

First, call the Skill tool with "preflight". Read no code and edit no file until the user has confirmed the repo, branch, worktree, and stack.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly and single test files regularly. Run the full test suite once at the end, in the background. The suite has passed only when you have read its exit code and its summary line. A run that ends without a summary has not passed. Say so, then rerun it in smaller sets.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the branch that preflight confirmed. In a stack, that is the layer that owns the change. Push or submit only when the user asks.
