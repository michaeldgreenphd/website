#!/bin/bash
# Regression test for pre-push-guard.sh. Run from the repository root:
#   bash .claude/hooks/pre-push-guard.test.sh
# Builds a throwaway repository, feeds each command to the hook as Claude
# Code would (JSON on stdin, CLAUDE_PROJECT_DIR set), and checks the exit
# code: 0 = allowed, 2 = blocked. Exits non-zero if any case disagrees.
set -u
HOOK="$(cd "$(dirname "$0")" && pwd)/pre-push-guard.sh"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
git -C "$T" init -q -b main
git -C "$T" -c user.email=t@t -c user.name=t commit -q --allow-empty -m init

fail=0
check() { # check <want-exit> <command>
  local want="$1" cmd="$2" got
  printf '{"tool_input":{"command":%s}}' \
    "$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$cmd")" \
    | CLAUDE_PROJECT_DIR="$T" bash "$HOOK" 2>/dev/null
  got=$?
  if [ "$got" = "$want" ]; then printf 'ok    '; else printf 'FAIL  '; fail=1; fi
  printf 'want=%s got=%s  %s\n' "$want" "$got" "$cmd"
}

git -C "$T" checkout -q -b feature
echo "-- feature branch checked out: allowed --"
check 0 "git push"
check 0 "git push -u origin feature"
check 0 "git push --force-with-lease origin feature"
check 0 "git fetch origin main && git push origin feature"
check 0 "git push origin feature-main"
check 0 "git push origin HEAD:refs/heads/feature"
check 0 "git push origin refs/heads/maintenance"
check 0 "git commit -m 'a bare git push with main checked out' && git push -u origin feature"
check 0 "echo git pushed"
check 0 "git log --oneline"
echo "-- feature branch checked out: blocked (targets main) --"
check 2 "git push origin main"
check 2 "git push origin HEAD:main"
check 2 "cd /repo && git push origin main"
check 2 "  git push origin feature:main"
check 2 "git push origin HEAD:refs/heads/main"
check 2 "git push origin refs/heads/main"
check 2 "git push origin feature:refs/heads/main"
check 2 "git push origin +main"
check 2 "git push origin +HEAD:main"
check 2 "git push -f origin +feature:refs/heads/main"

git -C "$T" checkout -q main
echo "-- main checked out: every push blocked --"
check 2 "git push"
check 2 "git push origin"
check 2 "git commit -m 'mention git push here' && git push origin feature"
check 0 "git status"

if [ "$fail" = 0 ]; then echo "ALL 24 CASES PASS"; else echo "SOME CASES FAILED"; exit 1; fi
