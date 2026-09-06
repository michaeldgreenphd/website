#!/bin/bash
# Regression test for pre-push-guard.sh / pre-push-guard.py. Run from the
# repository root:
#   bash .claude/hooks/pre-push-guard.test.sh
# Builds two throwaway repositories (the "project" the hook sees through
# CLAUDE_PROJECT_DIR, and a second worktree reached only via `git -C`),
# feeds each command to the hook as Claude Code would (JSON on stdin), and
# checks the exit code: 0 = allowed, 2 = blocked. Exits non-zero if any
# case disagrees.
set -u
HOOK="$(cd "$(dirname "$0")" && pwd)/pre-push-guard.sh"
T=$(mktemp -d); T2=$(mktemp -d)
trap 'rm -rf "$T" "$T2"' EXIT
for R in "$T" "$T2"; do
  git -C "$R" init -q -b main
  git -C "$R" -c user.email=t@t -c user.name=t commit -q --allow-empty -m init
done

fail=0; total=0
check() { # check <want-exit> <command>
  local want="$1" cmd="$2" got
  printf '{"tool_input":{"command":%s}}' \
    "$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$cmd")" \
    | CLAUDE_PROJECT_DIR="$T" bash "$HOOK" 2>/dev/null
  got=$?; total=$((total+1))
  if [ "$got" = "$want" ]; then printf 'ok    '; else printf 'FAIL  '; fail=1; fi
  printf 'want=%s got=%s  %s\n' "$want" "$got" "$cmd"
}

git -C "$T" checkout -q -b feature          # project on feature
echo "-- project on feature: allowed --"
check 0 "git push"
check 0 "git push -u origin feature"
check 0 "git push --force-with-lease origin feature"
check 0 "git push --tags origin"
check 0 "git -C /repo push origin feature"
check 0 "git -c core.x=1 push origin feature"
check 0 "git fetch origin main && git push origin feature"
check 0 "git push origin feature-main"
check 0 "git push origin HEAD:refs/heads/feature"
check 0 "git push origin refs/heads/maintenance"
check 0 "git commit -m 'a bare git push with main checked out' && git push -u origin feature"
check 0 "git -C x commit -m 'push --all to main'"
check 0 "echo git pushed"
check 0 "git log --oneline"
check 0 "git push origin main:feature"
check 0 "git push origin \"HEAD:feature\""
check 0 "git push -o ci.skip origin feature"
check 0 "git push origin HEAD"
check 0 "git -C $T2 push origin feature"
echo "-- project on feature: blocked (destination is main) --"
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
check 2 "git push origin --delete main"
check 2 "git push origin :main"
check 2 "FOO=1 git push origin main"
check 2 "env FOO=1 git push origin main"
check 2 "git push origin \"HEAD:main\""
check 2 "git push origin 'main'"
check 2 "git push -o ci.skip origin main"
check 2 "git push --repo=origin main"
check 2 "git push origin feature main"
echo "-- project on feature: blocked (global options before push) --"
check 2 "git -C \"\$CLAUDE_PROJECT_DIR\" push origin HEAD:main"
check 2 "git -C /repo push origin main"
check 2 "git -c core.x=1 push origin main"
check 2 "git --no-pager push origin main"
check 2 "git --git-dir=/repo/.git push origin main"
echo "-- project on feature: blocked (all-ref modes) --"
check 2 "git push --all origin"
check 2 "git push origin --all"
check 2 "git push --branches origin"
check 2 "git push --mirror origin"
check 2 "git -C /repo push --mirror origin"
echo "-- project on feature, second worktree on main: blocked via -C --"
check 2 "git -C $T2 push"
check 2 "git -C $T2 push origin HEAD"

git -C "$T" checkout -q main                # project on main
git -C "$T2" checkout -q -b feature         # second worktree on feature
echo "-- project on main: blocked (would update origin/main) --"
check 2 "git push"
check 2 "git push origin"
check 2 "git -C \"\$CLAUDE_PROJECT_DIR\" push"
check 2 "git push origin HEAD"
echo "-- project on main: allowed (another branch by name, or another worktree) --"
check 0 "git commit -m 'mention git push here' && git push origin feature"
check 0 "git push origin HEAD:feature"
check 0 "git push origin main:feature"
check 0 "git -C $T2 push"
check 0 "git status"

if [ "$fail" = 0 ]; then echo "ALL $total CASES PASS"; else echo "SOME OF $total CASES FAILED"; exit 1; fi
