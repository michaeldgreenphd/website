#!/bin/bash
# PostToolUse hook (Edit / MultiEdit / Write): after a Python file is edited,
# compile-check it; after a workflow file is edited, parse it with PyYAML.
# Exit 2 sends stderr back to Claude as feedback; anything else is silent.
f=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
[ -n "$f" ] && [ -f "$f" ] || exit 0
case "$f" in
  *.py)
    python3 -m py_compile "$f" || { echo "py_compile failed: $f" >&2; exit 2; } ;;
  */.github/workflows/*.yml|*/.github/workflows/*.yaml)
    python3 -c 'import sys, yaml
try:
    yaml.safe_load(open(sys.argv[1]))
except yaml.YAMLError as e:
    sys.exit(f"YAML parse failed: {sys.argv[1]}\n{e}")' "$f" || exit 2 ;;
esac
exit 0
