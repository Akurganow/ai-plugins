#!/usr/bin/env bash
# Writes the two builds and the four catalogues from src/.
#
#   bundles/<name>/   the install shared by Claude Code, Codex, Cursor and Oh-My-Pi
#   plugins/<name>/   the Agent Plugins 1.0.0 package
#   .claude-plugin/marketplace.json, .agents/plugins/marketplace.json,
#   .cursor-plugin/marketplace.json, .omp-plugin/marketplace.json
#
# Each package's two builds are deleted and written whole, so a file removed
# from src/<name>/ leaves no copy. Nothing is deleted before every source has
# been read and the prose-discipline short form has passed its limits. CI runs
# this script and fails when the tree differs from the commit. A second run
# changes nothing. It needs jq and POSIX tools, no node.
set -euo pipefail

die() {
  printf 'build: %s\n' "$*" >&2
  exit 1
}

[ "$#" -eq 0 ] || die "takes no arguments"

for tool in jq awk grep mkdir rm cp cmp cat mktemp dirname wc; do
  command -v "$tool" >/dev/null 2>&1 ||
    die "$tool is not installed; install it and re-run bash tools/build.sh"
done

. "$(dirname "$0")/regions.sh" || die "cannot read regions.sh next to $0"

cd "$(dirname "$0")/.." || die "cannot enter the repository root above $0"

WORK=$(mktemp -d) || die "mktemp -d failed; check the temporary directory is writable"
trap 'rm -rf "$WORK"' EXIT

RULES=src/prose-discipline/rules/prose-discipline.md
SCHEMA_ID=https://agent-plugins.org/schemas/1.0.0/plugin.schema.json

# windows_command TEXT: one `echo` per line, joined by `&`, with `echo:` for a
# blank line. cmd.exe runs it as one command line.
windows_command() {
  printf '%s\n' "$1" | awk '{ printf "%s%s", (NR > 1 ? "&" : ""), ($0 == "" ? "echo:" : "echo " $0) }'
}

# check_short_form TEXT WINDOWS: stop on a short form that breaks a limit. The
# hooks print TEXT through sh, PowerShell and cmd.exe, and each limit names the
# failure it prevents: a text that one of them reads as something other than
# plain text, or a text that never reaches the session whole.
check_short_form() {
  local text=$1 win=$2 hit size
  # Single quotes delimit the text in sh and PowerShell. The plugin directory
  # forbids variables, command substitution and wildcards in a hook command.
  if hit=$(printf '%s\n' "$text" | LC_ALL=C grep -n -m1 '[^A-Za-z0-9 .,:_/#-]'); then
    die "short form line ${hit%%:*} holds a character outside letters, digits, space and . , : - _ / # (line: '${hit#*:}'); a quote or a backslash changes what sh and PowerShell print, and cmd.exe runs & | < > ^ % as operators; edit the hook-text region of $RULES"
  fi
  # cmd.exe runs `echo /?` as a request for help and prints no text.
  if hit=$(printf '%s\n' "$text" | LC_ALL=C grep -n -m1 -v -e '^$' -e '^[A-Za-z0-9#]' -e '^- '); then
    die "short form line ${hit%%:*} starts with something other than a letter, digit, # or '- ' (line: '${hit#*:}'); cmd.exe prints help for 'echo /?' instead of the line, and every line keeps one safe opening; edit the hook-text region of $RULES"
  fi
  # Codex moves hook context over 2500 tokens to a file, and Claude Code caps
  # hook output at 10,000 characters. The size is what echo prints, with its
  # final line feed.
  size=$(($(printf '%s\n' "$text" | wc -c)))
  if [ "$size" -ge 8000 ]; then
    die "short form prints as $size bytes; the limit is under 8000, because Codex moves hook context over 2500 tokens to a file and Claude Code caps hook output at 10,000 characters, so a longer text does not reach the session whole; shorten the hook-text region of $RULES"
  fi
  # Each line adds `echo ` or `echo:` and a `&` to its text.
  if [ "${#win}" -ge 8191 ]; then
    die "the Windows command is ${#win} characters; the limit is under 8191, the command-line limit of cmd.exe, and each line adds 'echo' and '&' to its text, so a short form under 8000 bytes can still exceed it; merge lines in the hook-text region of $RULES"
  fi
}

# hook_files SHORT WINDOWS: write both hooks files into $WORK. The commands
# read no file and name no variable. printf '%s' carries the JSON of
# SubagentStart because echo is implementation-defined on its backslash-n.
hook_files() {
  local say='def say: "echo " + $q + $t + $q;
    def cmd($c): {type: "command", command: $c};'
  jq -n --arg t "$1" --arg q "'" "$say"'
    {hooks: {
      SessionStart: [{hooks: [cmd(say)]}],
      SubagentStart: [{hooks: [cmd("printf " + $q + "%s" + $q + " " + $q
        + ({hookSpecificOutput: {hookEventName: "SubagentStart", additionalContext: $t}} | tojson)
        + $q)]}]
    }}' >"$WORK/hooks.json" || die "jq cannot build the Claude Code hooks file from the short form"
  jq -n --arg t "$1" --arg q "'" --arg w "$2" "$say"'
    def hook: {hooks: [cmd(say) + {commandWindows: $w}]};
    {description: "Print the prose-discipline core rules into every session and every subagent.",
     hooks: {SessionStart: [hook], SubagentStart: [hook]}}' >"$WORK/codex.json" ||
    die "jq cannot build the Codex hooks file from the short form"
}

# prepare_rules: read the full rules, check the short form, and write the
# files built from them into $WORK. Runs before any deletion.
prepare_rules() {
  local short win
  [ -f "$RULES" ] || die "$RULES is missing; restore it from git"
  short=$(short_form "$RULES")
  win=$(windows_command "$short")
  check_short_form "$short" "$win"
  full_text "$RULES" >"$WORK/rules.mdc"
  hook_files "$short" "$win"
}

# project SOURCE DEST FILTER [JQ_ARG...]: DEST is FILTER applied to SOURCE.
project() {
  local from=$1 dest=$2 filter=$3
  shift 3
  jq "$@" "$filter" "$from" >"$dest" ||
    die "jq cannot write $dest from $from; fix the file and re-run bash tools/build.sh"
}

# copy_into SOURCE DEST: cp -R that stops with a message.
copy_into() {
  cp -R "$1" "$2" || die "cannot copy $1 to $2"
}

# build_bundle NAME: the install every client except Agent Plugins reads. It
# has no root plugin.json, because next to one Codex drops a package's hooks.
build_bundle() {
  local from="src/$1/source.json" out="bundles/$1" skills=0 hooks=0
  [ -d "src/$1/skills" ] && skills=1
  [ "$1" = prose-discipline ] && hooks=1
  mkdir -p "$out/.claude-plugin" "$out/.codex-plugin" "$out/.cursor-plugin" ||
    die "cannot create $out"
  project "$from" "$out/.claude-plugin/plugin.json" \
    '{name, version, description, author, homepage, repository, license, keywords}'
  project "$from" "$out/.codex-plugin/plugin.json" \
    '{name, version, description, keywords}
     + (if $skills == "1" then {skills: "./skills/"} else {} end)
     + (if $hooks == "1" then {hooks: "./hooks/codex.json"} else {} end)' \
    --arg skills "$skills" --arg hooks "$hooks"
  project "$from" "$out/.cursor-plugin/plugin.json" \
    '{name, description, version, author: {name: .author.name}, homepage, repository, license, keywords}'
  copy_into "src/$1/README.md" "$out/README.md"
  copy_into LICENSE "$out/LICENSE"
  if [ "$skills" = 1 ]; then
    copy_into "src/$1/skills" "$out/skills"
  fi
  if [ "$hooks" = 1 ]; then
    mkdir -p "$out/hooks" "$out/rules" || die "cannot create $out/hooks and $out/rules"
    copy_into "$WORK/hooks.json" "$out/hooks/hooks.json"
    copy_into "$WORK/codex.json" "$out/hooks/codex.json"
    copy_into "$WORK/rules.mdc" "$out/rules/prose-discipline.mdc"
  fi
}

# build_agent_plugin NAME: the Agent Plugins 1.0.0 package, with the core
# fields and nothing a client reads outside them.
build_agent_plugin() {
  local out="plugins/$1"
  mkdir -p "$out" || die "cannot create $out"
  project "src/$1/source.json" "$out/plugin.json" \
    '{"$schema": $schema, name, version, description, author, homepage, repository, license, keywords}' \
    --arg schema "$SCHEMA_ID"
  copy_into "src/$1/README.md" "$out/README.md"
  copy_into LICENSE "$out/LICENSE"
  if [ -d "src/$1/skills" ]; then
    copy_into "src/$1/skills" "$out/skills"
  fi
}

# write_catalogue DEST FILTER: FILTER over the catalogue template ($top) and
# every source.json, sorted by name ($all), written when it differs. Every
# entry points at ./bundles/<name> and carries no version.
write_catalogue() {
  jq -n --slurpfile top tools/templates/marketplace.json --slurpfile all "$WORK/all.json" "$2" \
    >"$WORK/catalogue.json" || die "jq cannot build $1 from tools/templates/marketplace.json and src/*/source.json"
  write_if_changed "$WORK/catalogue.json" "$1"
}

write_catalogues() {
  write_catalogue .claude-plugin/marketplace.json '
    $top[0] + {plugins: [$all[0][] | {name, source: ("./bundles/" + .name), description, homepage, category}]}'
  write_catalogue .agents/plugins/marketplace.json '
    {name: $top[0].name, plugins: [$all[0][] | {name,
      source: {source: "local", path: ("./bundles/" + .name)},
      policy: {installation: "AVAILABLE", authentication: "ON_INSTALL"}, category}]}'
  write_catalogue .cursor-plugin/marketplace.json '
    {name: $top[0].name, owner: {name: $top[0].owner.name}, metadata: {description: $top[0].description},
     plugins: [$all[0][] | {name, source: ("./bundles/" + .name), description, category}]}'
  write_catalogue .omp-plugin/marketplace.json '
    {name: $top[0].name, owner: {name: $top[0].owner.name}, metadata: {description: $top[0].description},
     plugins: [$all[0][] | {name, source: ("./bundles/" + .name), description}]}'
}

# Read phase. Bash globs skip dot-folders, and a glob with no match stays
# literal, which the -d test skips.
sources=()
for dir in src/*/; do
  if [ -d "$dir" ]; then
    dir=${dir#src/}
    sources+=("${dir%/}")
  fi
done
[ "${#sources[@]}" -gt 0 ] || die "src/ holds no package folder; restore it from git"

files=()
for name in "${sources[@]}"; do
  jq -e 'type == "object"' "src/$name/source.json" >/dev/null ||
    die "src/$name/source.json is missing or is not a JSON object; fix it and re-run bash tools/build.sh"
  files+=("src/$name/source.json")
done
jq -s 'sort_by(.name)' "${files[@]}" >"$WORK/all.json" || die "jq cannot combine the source.json files"
prepare_rules

# Delete phase. A name from a glob holds no slash and no leading dot, so no
# path below leaves bundles/ or plugins/.
for name in "${sources[@]}"; do
  rm -rf "bundles/$name" "plugins/$name"
done
for dir in bundles/*/ plugins/*/; do
  if [ -d "$dir" ]; then
    name=${dir#*/}
    name=${name%/}
    [ -d "src/$name" ] || rm -rf "${dir%/}"
  fi
done

# Write phase.
for name in "${sources[@]}"; do
  build_bundle "$name"
  build_agent_plugin "$name"
done
write_catalogues
