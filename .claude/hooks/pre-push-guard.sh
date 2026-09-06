#!/bin/bash
# PreToolUse hook (Bash): enforce "never push to main directly". The logic
# lives in pre-push-guard.py (shell-aware tokenising, refspec destination
# semantics, and a branch check that honours -C/--git-dir); this wrapper
# exists so settings.json and the tests keep one stable entry point.
# Exit 2 blocks the command and returns stderr to Claude as the reason.
exec python3 "$(dirname "$0")/pre-push-guard.py"
