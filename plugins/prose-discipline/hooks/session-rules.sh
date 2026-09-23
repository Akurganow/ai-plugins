#!/bin/sh
# SessionStart hook for Claude Code and Codex. Prints the prose-discipline
# core rule (rules/prose-discipline.md) as JSON
# (hookSpecificOutput.additionalContext) for the host to inject as session
# context. Best-effort: ANY failure exits 0 with no stdout output so the
# session always starts. A diagnostic line goes to stderr so failures stay
# observable in host debug logs.
set -u

# Same precedence as hooks/hooks.json uses to invoke this script. If the two
# disagreed, the script would run from one plugin root and read its rule file
# from another.
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}}"
CORE="$PLUGIN_ROOT/rules/prose-discipline.md"

warn() { printf 'prose-discipline hook: %s\n' "$1" >&2; }

[ -f "$CORE" ] && [ -r "$CORE" ] || { warn "rule file missing or unreadable: $CORE"; exit 0; }
command -v node >/dev/null 2>&1 || { warn "node not found on PATH, skipping injection"; exit 0; }

# node builds the JSON with JSON.stringify, which escapes every control
# character (tabs, carriage returns, quotes) correctly. The frontmatter is
# stripped precisely: only when the file starts with a `---` line, and only
# the first such block. Body horizontal rules are never touched.
node - "$CORE" <<'EOF' || warn "node JSON encoding failed"
const fs = require("fs");
const raw = fs.readFileSync(process.argv[2], "utf8");
const lines = raw.split("\n");
let body = raw;
if (lines[0] === "---") {
    const close = lines.indexOf("---", 1);
    if (close !== -1) body = lines.slice(close + 1).join("\n");
}
process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: body },
}));
EOF

# Always succeed: the rule is best-effort context, never a gate.
exit 0