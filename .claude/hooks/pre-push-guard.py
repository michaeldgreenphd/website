#!/usr/bin/env python3
"""PreToolUse hook (Bash): enforce "never push to main directly".

Reads the Bash tool call from stdin (JSON with tool_input.command), splits
the command into clauses with shell-aware tokenising (quotes removed, so
`git push origin "HEAD:main"` reads the same as the unquoted form), and
for every clause that is `git [global options] push ...` blocks:

  - a refspec whose *destination* is main: `main`, `HEAD:main`, `x:main`,
    `:main`, `+main`, or fully qualified `refs/heads/main`. The source
    half is ignored, so `main:feature` is allowed. With `--delete` every
    refspec is a destination;
  - an all-ref push (`--all`, `--branches`, `--mirror`, or the
    matching-branches refspec `:`), which would update origin/main
    without naming it;
  - a push that would update main because main is the checked-out branch
    of the repository the command selects: a bare push with no refspec,
    or a `HEAD` (or `@`) refspec. The repository is the one git would use,
    honouring `-C`, `--git-dir`, `--work-tree`, `GIT_DIR`/`GIT_WORK_TREE`
    assignments, `env -C`, and any earlier `cd`/`pushd` clause in the same
    command (a `cd` to a directory that does not exist leaves the shell
    where it was, and is treated the same). Pushing another branch by
    name from a main checkout is allowed.

Transparent prefixes are skipped to find the command: `VAR=value`
assignments and the wrappers env (with its options), command, exec,
nohup, time and nice. Global options between `git` and `push` (`-C dir`,
`-c k=v`, `--git-dir=…`, `--no-pager`, …) are skipped to find the
subcommand, and only the clause's own arguments are inspected, so
`git fetch origin main && git push origin feature` and commit-message
prose that mentions "git push" and "main" are not mistaken for a push to
main. Exit 2 blocks the command and returns stderr to Claude as the
reason; exit 0 allows it.

Scope: this guards against an agent pushing to main by accident or habit.
It reads the command text, so a deliberate evasion (an alias, `eval`,
`sh -c "..."`, a script that pushes, or a push.default of `matching`)
is out of scope; GitHub branch protection on main is the control for that.
"""
import json
import os
import shlex
import subprocess
import sys

# git global options that take a separate argument (when not written =value)
GIT_GLOBAL_WITH_ARG = {
    "-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path",
    "--config-env", "--super-prefix", "--attr-source", "--list-cmds",
}
# git push options that take a separate argument (when not written =value)
PUSH_OPT_WITH_ARG = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}
ALL_REF_OPTS = {"--all", "--branches", "--mirror"}
MAIN_REFS = {"main", "refs/heads/main"}
HEAD_ALIASES = {"HEAD", "@"}
# wrappers that run the command that follows them, and their options that
# take a separate argument (when not written =value)
WRAPPER_OPT_WITH_ARG = {
    "env": {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"},
    "command": set(),
    "exec": {"-a"},
    "nohup": set(),
    "time": set(),
    "nice": {"-n", "--adjustment"},
}
RULE = "(AGENTS.md, workflow step 1)"


def block(reason):
    sys.stderr.write(f"Blocked: {reason}. Open a pull request instead {RULE}.\n")
    sys.exit(2)


def clauses(cmd):
    """Yield the command's clauses as lists of unquoted words."""
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError:  # unbalanced quotes: fall back to a plain split
        tokens = []
        for piece in cmd.replace("&&", " ; ").replace("||", " ; ").replace("|", " ; ").replace("&", " ; ").split(";"):
            tokens += piece.split() + [";"]
    current = []
    for tok in tokens:
        if tok and all(ch in ";&|()" for ch in tok):
            if current:
                yield current
            current = []
        else:
            current.append(tok)
    if current:
        yield current


def expand(value):
    return os.path.expanduser(os.path.expandvars(value))


def resolve_dir(target, cwd):
    """The directory a `cd`/`env -C` selects. A target that cannot be
    entered leaves the shell where it was, so the previous directory is
    kept in that case."""
    if not target:
        return cwd
    base = cwd or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    path = os.path.normpath(os.path.join(base, expand(target)))
    return path if os.path.isdir(path) else cwd


def strip_prefix(words, cwd):
    """Skip VAR=value assignments and transparent wrappers with their
    options. Returns (index of the command word or None, effective cwd,
    GIT_* environment overrides: value, or None for `env -u`)."""
    i = 0
    env_over = {}

    def assign(word):
        name, _, value = word.partition("=")
        if name.startswith("GIT_"):
            env_over[name] = expand(value)

    while i < len(words):
        w = words[i]
        if "=" in w and not w.startswith("-"):
            assign(w)
            i += 1
            continue
        if w not in WRAPPER_OPT_WITH_ARG:
            break
        name, i = w, i + 1
        with_arg = WRAPPER_OPT_WITH_ARG[name]
        while i < len(words):
            w = words[i]
            if w == "--":
                i += 1
                break
            if w.startswith("-"):
                opt, has_value, value = w.partition("=")
                if not has_value and opt in with_arg and i + 1 < len(words):
                    value = words[i + 1]
                if name == "command" and opt in ("-v", "-V"):
                    return None, cwd, env_over  # prints a path; runs nothing
                if name == "env" and opt in ("-C", "--chdir"):
                    cwd = resolve_dir(value, cwd)
                if name == "env" and opt in ("-u", "--unset") and value.startswith("GIT_"):
                    env_over[value] = None
                i += 2 if (opt in with_arg and not has_value and i + 1 < len(words)) else 1
            elif name == "env" and "=" in w:
                assign(w)
                i += 1
            else:
                break
    return (i if i < len(words) else None), cwd, env_over


def parse_push(words, cwd):
    """Return (global_options, push_options, positionals, cwd, env_over) if
    the clause is `[prefixes] git [globals] push [args]`, else None."""
    i, cwd, env_over = strip_prefix(words, cwd)
    if i is None or os.path.basename(words[i]) != "git":
        return None
    i += 1
    globals_ = []
    while i < len(words):
        w = words[i]
        if w.startswith("--") and "=" in w:
            globals_.append(w)
            i += 1
        elif w.startswith("-"):
            if w in GIT_GLOBAL_WITH_ARG and i + 1 < len(words):
                globals_ += [w, words[i + 1]]
                i += 2
            else:
                globals_.append(w)
                i += 1
        else:
            break
    if i >= len(words) or words[i] != "push":
        return None
    args = words[i + 1:]
    opts, positionals = [], []
    j = 0
    while j < len(args):
        a = args[j]
        if a == "--":
            positionals += args[j + 1:]
            break
        if a.startswith("-"):
            opts.append(a)
            j += 2 if (a in PUSH_OPT_WITH_ARG and j + 1 < len(args)) else 1
        else:
            positionals.append(a)
            j += 1
    return globals_, opts, positionals, cwd, env_over


def current_branch(globals_, cwd, env_over):
    """The checked-out branch of the repository the command selects."""
    env = dict(os.environ)
    for name, value in env_over.items():
        if value is None:
            env.pop(name, None)
        else:
            env[name] = value
    try:
        out = subprocess.run(
            ["git", *(expand(g) for g in globals_), "symbolic-ref", "--short", "-q", "HEAD"],
            cwd=cwd or os.environ.get("CLAUDE_PROJECT_DIR") or None,
            env=env, capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def main():
    try:
        cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except (ValueError, AttributeError):
        return 0
    if not isinstance(cmd, str) or "push" not in cmd:
        return 0
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or None
    previous = None  # where `cd -` would go back to
    for words in clauses(cmd):
        if words and words[0] in ("cd", "pushd"):
            targets = [w for w in words[1:] if w == "-" or not w.startswith("-")] or ["~"]
            if targets[-1] == "-":
                cwd, previous = previous, cwd
            else:
                new = resolve_dir(targets[-1], cwd)
                if new != cwd:  # a failed cd changes neither PWD nor OLDPWD
                    cwd, previous = new, cwd
            continue
        parsed = parse_push(words, cwd)
        if not parsed:
            continue
        globals_, opts, positionals, clause_cwd, env_over = parsed
        if any(o.split("=", 1)[0] in ALL_REF_OPTS for o in opts):
            block("an all-ref push (--all, --branches, --mirror) would update origin/main; push one branch by name")
        delete = any(o in ("-d", "--delete") for o in opts)
        # `--repo=<repo>` supplies the repository, so every positional is a refspec.
        if any(o.startswith("--repo=") for o in opts) or not positionals:
            refspecs = positionals
        else:
            refspecs = positionals[1:]
        dests = []
        for spec in refspecs:
            spec = spec.lstrip("+")
            if spec == ":":
                block("the matching-branches refspec ':' would update origin/main; push one branch by name")
            dests.append(spec if delete or ":" not in spec else spec.split(":", 1)[1])
        if any(d in MAIN_REFS for d in dests):
            block("this push targets main")
        if (not refspecs or any(d in HEAD_ALIASES for d in dests)) and current_branch(globals_, clause_cwd, env_over) == "main":
            if not refspecs:
                block("main is checked out, so a push with no refspec would update origin/main; create a branch first")
            block("main is checked out, so pushing HEAD would update origin/main; create a branch first")
    return 0


if __name__ == "__main__":
    sys.exit(main())
