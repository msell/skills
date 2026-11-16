#!/usr/bin/env python3
"""Print the repo, branch, worktree, stack, and ticket facts that preflight needs.

Usage: facts.py [TICKET_FILE] [--repo PATH]
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HEADER_KEYS = ("Repo", "Branch", "Stack", "Worktree", "Blocked by", "Linear", "Status")
GH_FALLBACKS = ("/opt/homebrew/bin/gh", "/usr/local/bin/gh")


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def git(args, cwd):
    return run(["git", *args], cwd)


def read_ticket(path):
    text = Path(path).read_text()
    header = {}
    for line in text.splitlines():
        match = re.match(r"^(%s):\s*(.*)$" % "|".join(HEADER_KEYS), line)
        if match and match.group(1) not in header:
            header[match.group(1)] = match.group(2).strip()
    return header, bool(re.search(r"\bstack\b", text, re.IGNORECASE))


def resolve_repo(args, header):
    if args.repo:
        return Path(args.repo).expanduser().resolve()
    named = header.get("Repo")
    if named:
        candidate = Path("~/cocam").expanduser() / named
        if candidate.is_dir():
            return candidate
    return Path.cwd()


def default_branch(repo):
    code, out, _ = git(["symbolic-ref", "--short", "refs/remotes/origin/HEAD"], repo)
    if code == 0 and out:
        return out.split("/", 1)[1]
    for name in ("master", "main"):
        if git(["rev-parse", "--verify", "--quiet", name], repo)[0] == 0:
            return name
    return "unknown"


def gh_stack(repo):
    candidates = [shutil.which("gh"), *GH_FALLBACKS]
    last_error = "gh is not installed"
    for gh in [c for c in candidates if c]:
        code, out, err = run([gh, "stack", "view", "--json"], repo)
        if code == 0:
            return parse_stack(out)
        if code == 2:
            return "not in a stack"
        last_error = (err.splitlines() or ["gh stack failed"])[0]
    return "unavailable: %s" % last_error


def parse_stack(raw):
    data = json.loads(raw)
    names = []
    for branch in data.get("branches", []):
        label = branch["name"]
        if branch.get("isMerged"):
            label += " (merged)"
        names.append(label)
    chain = " <- ".join(["(%s)" % data.get("trunk", "?"), *names])
    return "%s; current: %s" % (chain, data.get("currentBranch", "?"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket", nargs="?")
    parser.add_argument("--repo")
    args = parser.parse_args()

    header, mentions_stack = {}, False
    if args.ticket:
        header, mentions_stack = read_ticket(args.ticket)

    repo = resolve_repo(args, header)
    if git(["rev-parse", "--show-toplevel"], repo)[0] != 0:
        print("repo: %s is not a git repository" % repo)
        return 1

    trunk = default_branch(repo)
    branch = git(["branch", "--show-current"], repo)[1] or "(detached HEAD)"
    dirty = [l for l in git(["status", "--porcelain"], repo)[1].splitlines() if l]
    _, counts, _ = git(["rev-list", "--left-right", "--count", "%s...HEAD" % trunk], repo)
    behind, ahead = (counts.split() + ["?", "?"])[:2]
    _, upstream, _ = git(["rev-parse", "--abbrev-ref", "@{upstream}"], repo)

    print("repo: %s" % repo)
    print("branch: %s" % branch)
    print("trunk: %s" % trunk)
    print("ahead/behind trunk: %s/%s" % (ahead, behind))
    print("upstream: %s" % (upstream or "none"))
    print("dirty files: %d" % len(dirty))
    print("worktrees:")
    for line in git(["worktree", "list"], repo)[1].splitlines():
        print("  %s" % line)
    print("stack: %s" % gh_stack(repo))
    if args.ticket:
        print("ticket: %s" % args.ticket)
        for key in HEADER_KEYS:
            if key in header:
                print("  %s: %s" % (key, header[key]))
        missing = [k for k in ("Repo", "Branch", "Stack", "Worktree") if k not in header]
        if missing:
            print("  header lines missing: %s" % ", ".join(missing))
        print("  text mentions a stack: %s" % ("yes" if mentions_stack else "no"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
