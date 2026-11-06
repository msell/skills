---
name: herdr
description: "Control Herdr Core (the `hc` CLI) to run commands and coding agents in long-lived terminals, and to read, prompt, wait on, or stop other terminals. Use only when the user mentions Herdr, herdr-core, or hc, or asks to run or control another terminal or agent through it. Do not use merely because a task could benefit from a background terminal, delegation, or parallel work. Requires HC_TERMINAL_ID."
---

# Herdr Core (`hc`)

Herdr Core keeps programs and coding agents alive in terminals. The `hc` command controls them. `herdr-core` is the same binary, and `hc` is a symlink to it.

The old `herdr` CLI (workspaces, tabs, panes, `HERDR_ENV`) is gone. Do not run `herdr`. Use `hc`.

## Check that you are inside Herdr

Before any control command, run this check:

```bash
test -n "${HC_TERMINAL_ID:-}"
```

If it fails, say that you are not running inside a Herdr terminal and stop. Do not control other terminals from outside Herdr.

Herdr sets these variables in each terminal:

- `HC_TERMINAL_ID` is your own address, for example `t1c`.
- `HC_TERMINAL_SOCKET` is the socket of the core.
- `HC_SCOPE` identifies your scope.

## Learn the current CLI

The installed binary is the authority for syntax. Run these first:

```bash
hc --help
hc <command> --help
```

Do not run bare `hc` for discovery. It opens a picker and attaches your terminal. Do not run `hc attach`, which takes over the terminal.

Add `--json` for output you must parse. Read addresses and state from responses. Do not guess them.

## Terminals and addresses

Each program runs in a flat terminal. There are no workspaces, tabs, or panes.

- A terminal address looks like `t7`.
- A terminal on another machine looks like `mini-me-tailscale/t7`.
- You can also address a terminal by its name. A name uses `a-z`, `0-9`, `-`, `_`, 1 to 32 characters, and is unique among live terminals.

List what is running:

```bash
hc ls --json
hc get <t> --json
```

`hc ls` shows each terminal's address, program (`agent`), `cwd`, `state`, and, for agents, `status`. Agent status is `idle`, `working`, or `blocked`. `hc ls --all` also shows finished terminals.

## Run a command or an agent

`hc run` starts a program, or a template by name with its task. By default it waits like a shell and returns the exit code.

```bash
hc run just test
hc run --bg --name api -- yarn start
hc run reviewer "review the current diff"
```

Useful options:

- `--bg` starts it and returns at once. Use it for servers and workers.
- `--name <n>` sets a unique name.
- `--cwd <dir>` sets the working directory. The default is where `hc` runs.
- `--on <machine>` runs it on another machine.
- `--label k=v` tags it. Filter with `hc ls --label k=v`.
- `--rm` removes the terminal after it exits.
- `--outlive-parent` keeps it running after your program ends. By default a child ends with its parent.

A terminal you start becomes your child. When a child blocks, errors, or finishes, Herdr types a note into your terminal. Use `--no-notify` or `--no-parent` to change that.

Run `hc templates` to list templates. The list may be empty.

For one command that needs no terminal, use `hc exec`. It prints exactly what the program wrote and exits with its code. It runs without a shell.

```bash
hc exec --timeout 120 -- git status
hc exec --on <machine> -- uname -a
```

## Talk to a program or agent

Send text and press Enter:

```bash
hc send <t> "Review the current diff and report only actionable findings." --wait --timeout 120
```

- `--wait` waits for the turn that this send started.
- `--if idle` sends only when the agent is idle.
- `hc send` refuses a blocked program. `--force` types anyway and may answer its dialog. Read the screen first. Ask the user before you answer a dialog.

Press keys with `hc keys <t> esc`, `hc keys <t> ctrl+c`, and so on. Use `hc interrupt <t>` to press the stop key and see what happened.

Send a local file next to a terminal with `hc put <t> <file>`. It prints where the file landed.

## Wait, then read

Use `hc wait` instead of `sleep` or polling.

```bash
hc wait <t>                       # until the agent stops working
hc wait <t> --output "test result" # for programs: until this text prints
hc wait --children all            # until none of your children is working
hc wait --children any            # until the next child news or message
```

All waits take `--timeout <seconds>`. The default is the configured `wait_timeout`, else 180. A timeout means the wait checked in. The program keeps running.

Read output with:

```bash
hc read <t> --lines 200
```

`--lines` adds lines of history above the screen. The default is 0, which prints the screen only.

If a wait returns blocked, an error, or a timeout, read the screen before you decide what to send. A timeout does not prove that a prompt was never delivered. Do not send the same prompt again blindly.

## Stop and clean up

- `hc kill <t>` ends a program. It hangs up first, then escalates.
- `hc rm <t>` removes a finished terminal.
- `hc label <t> k=v` sets a label. `k=` removes it.
- `hc keep <t>` replaces a lost program with a shell. `--off` disables it.

## Other machines

```bash
hc machine ls
hc --help        # see `machine add|login|update|rename|rm`
```

Pass `--on <machine>` to `run` and `exec`. Address existing terminals as `machine/t7`. Only add, remove, or log in a machine when the user asks.

## Safety rules

- Use an explicit address or name. Do not rely on a picker or on another client's selection.
- Parse addresses from `--json` output. Do not derive them from examples.
- Do not `kill` or `rm` terminals you did not start unless the user asks.
- Never run `hc server stop` or `hc server restart` from an active session unless the user explicitly asks. Stopping parks kept terminals, and restarting is only for updates.
- Do not run `hc update` unless the user asks.
- Use `hc events` to follow changes live. It streams until you stop it, so run it in the background or with a bound.
