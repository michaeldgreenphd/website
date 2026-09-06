#!/bin/bash
# PreToolUse hook (Bash): enforce "never push to main directly" for the
# forms the text-based deny rules cannot see. For every clause of the
# command that is `git [global options] push ...`, it blocks:
#   - a push whose arguments name main as a target: `main`, `HEAD:main`,
#     `x:main`, `+main` (forced), or fully qualified `refs/heads/main`;
#   - an all-ref push (`--all`, `--branches`, `--mirror`), which would
#     update origin/main without naming it;
#   - any push at all while main is the checked-out branch (a bare
#     `git push` would update origin/main).
# Global options between `git` and `push` (`-C dir`, `-c k=v`, `--git-dir`,
# `--no-pager`, ...) are skipped, and only the clause's own arguments are
# inspected, so `git fetch origin main && git push origin feature` and
# commit-message prose that mentions "git push" and "main" are not
# mistaken for a push to main. Exit 2 blocks the command and returns
# stderr to Claude as the reason.
#
# Scope: this guards against an agent pushing to main by accident or
# habit. It reads the command text, so a deliberate evasion (an alias,
# `eval`, `sh -c "..."`, a script that pushes) is out of scope; GitHub
# branch protection on main is the control for that.
cmd=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
case "$cmd" in *git*push*) ;; *) exit 0 ;; esac

# Git global options that take a separate argument (when not written =value).
takes_arg=' -C -c --git-dir --work-tree --namespace --exec-path --config-env --super-prefix --attr-source --list-cmds '

# Print one "PUSH <args>" line per clause that is `git [globals] push ...`.
push_clauses() {
  local clause i n
  local -a w
  printf '%s\n' "$cmd" | tr ';|&' '\n' | while IFS= read -r clause; do
    read -r -a w <<< "$clause"; n=${#w[@]}; i=0
    while [ "$i" -lt "$n" ]; do case "${w[$i]}" in *=*) i=$((i+1));; *) break;; esac; done  # VAR=value prefixes
    [ "$i" -lt "$n" ] && [ "${w[$i]}" = git ] || continue
    i=$((i+1))
    while [ "$i" -lt "$n" ]; do
      case "${w[$i]}" in
        --*=*) i=$((i+1)) ;;
        -*) case "$takes_arg" in *" ${w[$i]} "*) i=$((i+2)) ;; *) i=$((i+1)) ;; esac ;;
        *) break ;;
      esac
    done
    [ "$i" -lt "$n" ] && [ "${w[$i]}" = push ] || continue
    printf 'PUSH %s\n' "${w[*]:$((i+1))}"
  done
}

pushes=$(push_clauses)
[ -n "$pushes" ] || exit 0

if printf '%s\n' "$pushes" | grep -Eq '(^|[[:space:]]|:|\+|refs/heads/)main([[:space:]]|:|$)'; then
  echo "Blocked: this push targets main. Open a pull request instead (AGENTS.md, workflow step 1)." >&2
  exit 2
fi
if printf '%s\n' "$pushes" | grep -Eq '[[:space:]]--(all|branches|mirror)([[:space:]]|=|$)'; then
  echo "Blocked: an all-ref push (--all, --branches, --mirror) would update origin/main. Push one branch by name (AGENTS.md, workflow step 1)." >&2
  exit 2
fi

branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" symbolic-ref --short -q HEAD 2>/dev/null)
if [ "$branch" = "main" ]; then
  echo "Blocked: main is checked out, so this push would update origin/main. Create a branch first (AGENTS.md, workflow step 1)." >&2
  exit 2
fi
exit 0
