#!/usr/bin/env bash
# Regenerates every generated file in this repository from its source.
#
# Each generated file has one source, named in the step that writes it.
# CI runs this script, then fails when the tree differs from the commit.
# So a copy edited by hand, or a source edited without a rerun, does not
# merge. A second run changes nothing.
#
# A generated region inside a hand-written file sits between two marker
# lines. tools/regions.sh owns the markers and the rules for them. The last
# step runs tools/build.sh, which writes bundles/, plugins/ and the
# catalogues from src/.
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

. "$(dirname "$0")/regions.sh" || die "cannot read regions.sh next to $0"

cd "$(dirname "$0")/.." || die "cannot enter the repository root above $0"

WORK=$(mktemp -d) || die "mktemp -d failed; check the temporary directory is writable"
trap 'rm -rf "$WORK"' EXIT

# render_template TEMPLATE NAME: TEMPLATE with every `{{name}}` replaced.
render_template() {
  sed -e "s|{{name}}|$2|g" "$1"
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

sources=(src/*/source.json)

# 1. The plugin table of the root README.
jq -rn '
  [inputs | {name, description}]
  | sort_by(.name)
  | ("| Plugin | What it does |", "| :-- | :-- |"),
    (.[] | "| [\(.name)](plugins/\(.name)/README.md) | \(.description | gsub("\\|"; "\\|")) |")
' "${sources[@]}" >"$WORK/plugins.md" ||
  die "jq cannot build the plugin table from src/*/source.json; the file it names above is not valid JSON"
replace_region README.md plugins "$WORK/plugins.md"

# 2. Per package: the description and install regions of its README.
for source in "${sources[@]}"; do
  dir=${source%/source.json}
  name=$(jq -r .name "$source") || die "jq cannot read .name from $source; fix its JSON"
  jq -r .description "$source" >"$WORK/description.md" ||
    die "jq cannot read .description from $source; fix its JSON"
  replace_region "$dir/README.md" description "$WORK/description.md"
  render_template tools/templates/install.md "$name" >"$WORK/install.md" ||
    die "sed cannot render tools/templates/install.md for $name"
  replace_region "$dir/README.md" install "$WORK/install.md"
done

# 3. The install region of the root README, for any package.
render_template tools/templates/install.md '<name>' >"$WORK/install.md" ||
  die "sed cannot render tools/templates/install.md for the root README"
replace_region README.md install "$WORK/install.md"

# 4. A table of contents at the top of every reference longer than 100 lines,
#    and of every reference that already has one. Then the root README's table
#    of contents, two levels deep, once the README carries doctoc's markers.
tocs=()
while IFS= read -r -d '' file; do
  if [ "$(wc -l <"$file")" -gt 100 ] || grep -q '^<!-- START doctoc ' "$file"; then
    tocs+=("$file")
  fi
done < <(find src/*/skills/*/references -type f -name '*.md' -print0 2>/dev/null | sort -z)
if [ "${#tocs[@]}" -gt 0 ]; then
  run_doctoc "${tocs[@]}"
fi
if grep -q '^<!-- START doctoc ' README.md; then
  run_doctoc --maxlevel 2 README.md
fi

# 5. prose-discipline: the full rules in the house-style skill, because Hermes
#    loads nothing else from the package. Then the Hermes auto_load lines, in
#    the README and in the skill.
rules=src/prose-discipline/rules/prose-discipline.md
full_text "$rules" >"$WORK/full-rules.md"
strip_front_matter "$WORK/full-rules.md" >"$WORK/rules.md" ||
  die "awk cannot strip the front matter of $rules; check the file exists"
replace_region src/prose-discipline/skills/house-style/SKILL.md rules "$WORK/rules.md"
pd_name=$(jq -r .name src/prose-discipline/source.json) ||
  die "jq cannot read .name from src/prose-discipline/source.json; fix its JSON"
namespace=$(hermes_namespace "$pd_name")
printf '```yaml\nskills:\n  auto_load:\n    - %s:house-style\n```\n' "$namespace" >"$WORK/auto-load.md" ||
  die "cannot write $WORK/auto-load.md"
replace_region src/prose-discipline/README.md hermes-auto-load "$WORK/auto-load.md"
replace_region src/prose-discipline/skills/house-style/SKILL.md hermes-auto-load "$WORK/auto-load.md"

# 6. The builds and the catalogues, from the files above.
bash tools/build.sh
