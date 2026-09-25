#!/usr/bin/env bash
# Regenerates every generated file in this repository from its source.
#
# Each generated file has one source, named in the step that writes it.
# CI runs this script, then fails when the tree differs from the commit.
# So a copy edited by hand, or a source edited without a rerun, does not
# merge. A second run changes nothing.
#
# A generated region inside a hand-written file sits between two lines,
# `<!-- NAME:start -->` and `<!-- NAME:end -->`. A file with neither marker
# is skipped, so a region takes effect once someone adds its markers. Any
# other mismatch stops the run: a lone marker, a duplicate, or the end
# before the start.
set -euo pipefail

die() {
  printf 'regenerate: %s\n' "$*" >&2
  exit 1
}

[ "$#" -eq 0 ] || die "takes no arguments"

for tool in jq node npm awk sed grep find sort wc cut tr cmp cat mktemp dirname; do
  command -v "$tool" >/dev/null 2>&1 ||
    die "$tool is not installed; install it and re-run bash tools/regenerate.sh"
done
if command -v shasum >/dev/null 2>&1; then
  sha256() { shasum -a 256; }
elif command -v sha256sum >/dev/null 2>&1; then
  sha256() { sha256sum; }
else
  die "neither shasum nor sha256sum is installed; install one and re-run bash tools/regenerate.sh"
fi

cd "$(dirname "$0")/.." || die "cannot enter the repository root above $0"

WORK=$(mktemp -d) || die "mktemp -d failed; check the temporary directory is writable"
trap 'rm -rf "$WORK"' EXIT

# write_if_changed SOURCE DEST: copy SOURCE over DEST unless they are equal.
# `cat >` keeps DEST's mode; a symlink at DEST is removed first, so the copy
# lands at DEST and not at the link's target.
write_if_changed() {
  if [ -L "$2" ]; then
    rm "$2"
  elif cmp -s "$1" "$2"; then
    return 0
  fi
  cat "$1" >"$2" || die "cannot write $2; check it and its directory are writable"
}

# replace_region FILE REGION CONTENT: put the lines of CONTENT between the
# REGION markers in FILE. Blank lines at both ends of CONTENT are dropped.
# One blank line follows the start marker and one precedes the end marker.
replace_region() {
  local file=$1 region=$2 content=$3
  local start="<!-- ${region}:start -->" end="<!-- ${region}:end -->"
  local starts ends status=0 out="$WORK/region"
  [ -f "$file" ] || return 0
  # A marker line ending in CR matches neither exact pattern below, so the
  # region would be skipped without a word.
  if grep -qxF -e "$start"$'\r' -e "$end"$'\r' -- "$file"; then
    die "$file: region '$region' has CRLF marker lines; convert the file to LF and re-run bash tools/regenerate.sh"
  fi
  # grep -c exits 1 when it counts zero; only a higher status is an error.
  starts=$(grep -cxF -- "$start" "$file") || [ "$?" -eq 1 ] || die "grep cannot read $file"
  ends=$(grep -cxF -- "$end" "$file") || [ "$?" -eq 1 ] || die "grep cannot read $file"
  [ "$starts" -eq 0 ] && [ "$ends" -eq 0 ] && return 0
  [ "$starts" -eq 1 ] && [ "$ends" -eq 1 ] ||
    die "$file: region '$region' needs one '$start' line and one '$end' line; found $starts and $ends; fix the markers and re-run bash tools/regenerate.sh"
  awk -v start="$start" -v end="$end" -v content="$content" '
    $0 == start {
      print
      n = 0
      while ((getline line < content) > 0) body[++n] = line
      close(content)
      first = 1
      while (first <= n && body[first] ~ /^[ \t]*$/) first++
      last = n
      while (last >= first && body[last] ~ /^[ \t]*$/) last--
      print ""
      for (i = first; i <= last; i++) print body[i]
      if (last >= first) print ""
      inside = 1
      next
    }
    $0 == end {
      if (!inside) exit 3
      inside = 0
    }
    !inside { print }
  ' "$file" >"$out" || status=$?
  case $status in
    0) ;;
    3) die "$file: '$end' comes before '$start'; swap the two lines and re-run bash tools/regenerate.sh" ;;
    *) die "$file: awk failed with status $status while filling region '$region'; its error is above" ;;
  esac
  write_if_changed "$out" "$file"
}

# render_template TEMPLATE NAME: TEMPLATE with every `{{name}}` replaced.
render_template() {
  sed -e "s|{{name}}|$2|g" "$1"
}

# strip_front_matter FILE: FILE without a leading `---` ... `---` block.
strip_front_matter() {
  awk '
    NR == 1 && /^---[ \t]*$/ { in_front = 1; next }
    in_front && /^---[ \t]*$/ { in_front = 0; next }
    !in_front { print }
  ' "$1"
}

# hermes_namespace NAME: the skill namespace Hermes gives a package that
# `hermes plugins install` placed, `agent-plugin-<slug>-<first 8 hex of
# sha256(NAME)>`. The documentation gives the form and not the hash:
# https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md
# The source gives both, in `_portable_skill_namespace` and `_portable_slug`:
# https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py
hermes_namespace() {
  local slug digest
  slug=$(printf '%s' "$1" | tr 'A-Z' 'a-z' | sed -e 's/[^a-z0-9_-]/-/g' -e 's/^[-_]*//' -e 's/[-_]*$//') ||
    die "tr or sed failed on the package name '$1'"
  digest=$(printf '%s' "$1" | sha256 | cut -c1-8) || die "sha256 failed on the package name '$1'"
  printf 'agent-plugin-%s-%s\n' "${slug:-plugin}" "$digest"
}

# doctoc_install_is_stale: true when tools/node_modules does not hold what
# tools/package-lock.json pins. npm ci records its install in
# tools/node_modules/.package-lock.json: the same packages, minus the root
# entry. A lockfile newer than that record, or listing other packages, means
# a bump the local install has not caught up with.
doctoc_install_is_stale() {
  local locked=tools/package-lock.json installed=tools/node_modules/.package-lock.json
  local want have
  [ -e tools/node_modules/.bin/doctoc ] && [ -f "$installed" ] || return 0
  [ "$locked" -nt "$installed" ] && return 0
  want=$(jq -cS '.packages | del(."")' "$locked") ||
    die "jq cannot read $locked; restore it with git checkout -- $locked"
  # An unreadable install record is only a reason to reinstall.
  have=$(jq -cS '.packages | del(."")' "$installed" 2>/dev/null) || return 0
  [ "$want" != "$have" ]
}

# run_doctoc ARGS...: doctoc from tools/package-lock.json, which pins its
# whole dependency tree. No locked package needs an install script, so npm
# runs none.
run_doctoc() {
  if doctoc_install_is_stale; then
    npm ci --prefix tools --ignore-scripts --no-audit --no-fund >/dev/null ||
      die "npm ci --prefix tools failed; check network access to registry.npmjs.org"
  fi
  tools/node_modules/.bin/doctoc --github --notitle "$@" >/dev/null ||
    die "doctoc failed on $*; its error is above, and deleting tools/node_modules forces a reinstall"
}

manifests=(plugins/*/plugin.json)

# 1. The catalogue index: the template's top-level fields plus one entry per
#    package manifest. A field a manifest lacks is left out, not set to null.
jq -n --slurpfile top tools/templates/marketplace.json '
  $top[0] + {
    plugins: ([inputs | {
      name,
      source: ("./" + (input_filename | rtrimstr("/plugin.json"))),
      description,
      homepage,
      category: .extensions["io.github.akurganow.ai-plugins"].category
    } | with_entries(select(.value != null))] | sort_by(.name))
  }
' "${manifests[@]}" >"$WORK/marketplace.json" ||
  die "jq cannot build the catalogue from plugins/*/plugin.json; the manifest it names above is not valid JSON"
write_if_changed "$WORK/marketplace.json" .claude-plugin/marketplace.json

# 2. The plugin table of the root README.
jq -rn '
  [inputs | {dir: (input_filename | rtrimstr("/plugin.json")), name, description}]
  | sort_by(.name)
  | ("| Plugin | What it does |", "| :-- | :-- |"),
    (.[] | "| [\(.name)](\(.dir)/README.md) | \(.description | gsub("\\|"; "\\|")) |")
' "${manifests[@]}" >"$WORK/plugins.md" ||
  die "jq cannot build the plugin table from plugins/*/plugin.json; the manifest it names above is not valid JSON"
replace_region README.md plugins "$WORK/plugins.md"

# 3. Per package: the description, install and hosts regions of its README,
#    its LICENSE, and the manifest copy at Claude Code's path. The hosts
#    region is filled only for a manifest that declares network hosts.
for manifest in "${manifests[@]}"; do
  dir=${manifest%/plugin.json}
  name=$(jq -r .name "$manifest") || die "jq cannot read .name from $manifest; fix its JSON"
  jq -r .description "$manifest" >"$WORK/description.md" ||
    die "jq cannot read .description from $manifest; fix its JSON"
  replace_region "$dir/README.md" description "$WORK/description.md"
  render_template tools/templates/install.md "$name" >"$WORK/install.md" ||
    die "sed cannot render tools/templates/install.md for $name"
  replace_region "$dir/README.md" install "$WORK/install.md"
  # jq -e inside `if` would read a broken manifest as "no hosts", so this
  # prints the same truth test as a value.
  has_hosts=$(jq '.extensions["io.github.akurganow.ai-plugins"].network.hosts | . != null and . != false' "$manifest") ||
    die "jq cannot read the network hosts of $manifest; fix its JSON"
  if [ "$has_hosts" = true ]; then
    jq -r '.extensions["io.github.akurganow.ai-plugins"].network.hosts[] | "- `\(.)`"' "$manifest" >"$WORK/hosts.md" ||
      die "jq cannot list the network hosts of $manifest; they must be an array of strings"
    replace_region "$dir/README.md" hosts "$WORK/hosts.md"
  fi
  write_if_changed LICENSE "$dir/LICENSE"
  mkdir -p "$dir/.claude-plugin" || die "cannot create $dir/.claude-plugin"
  write_if_changed "$manifest" "$dir/.claude-plugin/plugin.json"
done

# 4. The install region of the root README, for any package.
render_template tools/templates/install.md '<name>' >"$WORK/install.md" ||
  die "sed cannot render tools/templates/install.md for the root README"
replace_region README.md install "$WORK/install.md"

# 5. A table of contents at the top of every reference longer than 100 lines,
#    and of every reference that already has one. howp's commands.md is
#    excluded: its release job writes it. Then the root README's table of
#    contents, two levels deep, once the README carries doctoc's markers.
tocs=()
while IFS= read -r -d '' file; do
  case "$file" in plugins/howp/skills/*/references/commands.md) continue ;; esac
  if [ "$(wc -l <"$file")" -gt 100 ] || grep -q '^<!-- START doctoc ' "$file"; then
    tocs+=("$file")
  fi
done < <(find plugins/*/skills/*/references -type f -name '*.md' -print0 2>/dev/null | sort -z)
if [ "${#tocs[@]}" -gt 0 ]; then
  run_doctoc "${tocs[@]}"
fi
if grep -q '^<!-- START doctoc ' README.md; then
  run_doctoc --maxlevel 2 README.md
fi

# 6. prose-discipline: the rules in the house-style skill, because Hermes
#    loads nothing else from the package. Then the Hermes auto_load lines, in
#    the README and in the skill.
rules=plugins/prose-discipline/rules/prose-discipline.md
strip_front_matter "$rules" >"$WORK/rules.md" ||
  die "awk cannot strip the front matter of $rules; check the file exists"
replace_region plugins/prose-discipline/skills/house-style/SKILL.md rules "$WORK/rules.md"
pd_name=$(jq -r .name plugins/prose-discipline/plugin.json) ||
  die "jq cannot read .name from plugins/prose-discipline/plugin.json; fix its JSON"
namespace=$(hermes_namespace "$pd_name")
printf '```yaml\nskills:\n  auto_load:\n    - %s:house-style\n```\n' "$namespace" >"$WORK/auto-load.md" ||
  die "cannot write $WORK/auto-load.md"
replace_region plugins/prose-discipline/README.md hermes-auto-load "$WORK/auto-load.md"
replace_region plugins/prose-discipline/skills/house-style/SKILL.md hermes-auto-load "$WORK/auto-load.md"
