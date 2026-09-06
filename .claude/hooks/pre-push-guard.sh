#!/bin/bash
# PreToolUse hook (Bash): enforce "never push to main directly" for the
# forms the text-based deny rules cannot see. Blocks any `git push` that
# names main as its target, and any `git push` at all while main is the
# checked-out branch (a bare `git push` would update origin/main).
# Exit 2 blocks the command and returns stderr to Claude as the reason.
cmd=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
printf '%s' "$cmd" | grep -Eq '(^|[^[:alnum:]_])git[[:space:]]+push([[:space:]]|$)' || exit 0

# Look only at clauses that *start* with `git push` (after splitting a
# compound command on ; | &), so neither `git fetch origin main && git push
# origin feature` nor prose in a commit message that mentions "git push"
# and "main" is mistaken for a push to main.
if printf '%s\n' "$cmd" | tr ';|&' '\n' | grep -E '^[[:space:]]*git[[:space:]]+push' \
   | grep -Eq '(^|[[:space:]]|:)main([[:space:]]|:|$)'; then
  echo "Blocked: this push targets main. Open a pull request instead (AGENTS.md, workflow step 1)." >&2
  exit 2
fi

branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" symbolic-ref --short -q HEAD 2>/dev/null)
if [ "$branch" = "main" ]; then
  echo "Blocked: main is checked out, so this push would update origin/main. Create a branch first (AGENTS.md, workflow step 1)." >&2
  exit 2
fi
exit 0
