#!/bin/bash
# PreToolUse hook (Bash): enforce "never push to main directly". The logic
# lives in pre-push-guard.py (shell-aware tokenising, refspec destination
# semantics, and a branch check that honours -C/--git-dir); this wrapper
# exists so settings.json and the tests keep one stable entry point.
# Exit 2 blocks the command and returns stderr to Claude as the reason.
#
# Only exit 2 blocks a PreToolUse call, so a missing or broken python3, or
# an uncaught error in the checker, would otherwise let a push through
# unchecked. Any other exit status blocks the command if it mentions a push.
input=$(cat)
printf '%s' "$input" | python3 "$(dirname "$0")/pre-push-guard.py"
rc=$?
case $rc in 0|2) exit $rc ;; esac
case $input in
  *push*)
    echo "Blocked: the push guard could not run (python3 exit $rc), so this command was not checked. Fix python3, or run the push yourself." >&2
    exit 2 ;;
esac
exit 0
