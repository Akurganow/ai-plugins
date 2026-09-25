#!/bin/sh
# Prints the body of rules/prose-discipline.md for a hook to inject.
#
# Without an argument the output is plain text starting with the H1.
# Claude Code adds plain SessionStart stdout to the context, but it would
# parse output starting with "{" as JSON instead.
# With --json the output is one SubagentStart hook object, because a
# subagent receives only hookSpecificOutput.additionalContext.
#
# Every failure prints one line to stderr and exits 0 with empty stdout.
# A non-zero exit would surface as a hook error, and the rules are context,
# never a gate on the session.

fail() {
  printf 'prose-discipline print-rules.sh: %s\n' "$1" >&2
  exit 0
}

case $# in
  0) mode=plain ;;
  1) [ "$1" = --json ] || fail "unknown argument $1. Pass no argument, or --json."; mode=json ;;
  *) fail "got $# arguments, but it takes at most one. Pass no argument, or --json." ;;
esac

# The script's own path locates the plugin root, so it reads the rules file
# of the package it belongs to whichever client ran it.
case $0 in
  */*) hooks_dir=${0%/*} ;;
  *) hooks_dir=. ;;
esac
rules=$hooks_dir/../rules/prose-discipline.md

[ -f "$rules" ] && [ -r "$rules" ] || fail "cannot read $rules. Reinstall the prose-discipline plugin."

# The command substitution holds the whole output until awk has succeeded,
# so a failure midway leaves stdout empty.
out=$(awk -v mode="$mode" '
  BEGIN {
    # Escapes are applied one character at a time. gsub replacement strings
    # treat backslashes differently in mawk, gawk and BWK awk.
    for (i = 1; i < 32; i++) esc[sprintf("%c", i)] = sprintf("\\u%04x", i)
    esc["\t"] = "\\t"
    esc["\r"] = "\\r"
    esc["\\"] = "\\\\"
    esc["\""] = "\\\""
    code = 0
  }
  NR == 1 && $0 == "---" { in_front = 1; next }
  in_front { if ($0 == "---") in_front = 0; next }
  !started && $0 == "" { next }
  !started {
    if (substr($0, 1, 2) != "# ") { code = 4; exit code }
    started = 1
  }
  { line[++n] = $0 }
  END {
    if (code) exit code
    if (in_front) exit 3
    if (!started) exit 4
    # The enclosing command substitution strips trailing blank lines from
    # the plain output. Dropping them here keeps both modes the same text.
    while (line[n] == "") n--
    if (mode == "plain") {
      for (i = 1; i <= n; i++) print line[i]
      exit 0
    }
    text = ""
    for (i = 1; i <= n; i++) {
      if (i > 1) text = text "\\n"
      s = line[i]
      len = length(s)
      for (j = 1; j <= len; j++) {
        c = substr(s, j, 1)
        text = text ((c in esc) ? esc[c] : c)
      }
    }
    printf "{\"hookSpecificOutput\":{\"hookEventName\":\"SubagentStart\",\"additionalContext\":\"%s\"}}\n", text
  }
' "$rules" 2>/dev/null)
status=$?

case $status in
  0) printf '%s\n' "$out" ;;
  3) fail "$rules has front matter with no closing --- line. Close it, or reinstall the plugin." ;;
  4) fail "$rules has no level-1 heading where its body starts. Start the body with a '# ' heading, or reinstall the plugin." ;;
  *) fail "awk exited with status $status while reading $rules. Check that the awk on PATH is POSIX awk." ;;
esac
