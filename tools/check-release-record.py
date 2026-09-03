#!/usr/bin/env python3
"""The release record agrees with itself; nothing else here carries a version or a tag.

Three checks, and every one of them reads text a machine wrote or the
absence of text no machine writes, so no hit needs a reader's judgement:

1. `plugins/<name>/plugin.json`'s `version` equals the `version` in that
   package's `binaries.json`, and that file's `tag` is `<name>-v<version>`.
   All three are written by the release job in the repository the binaries
   are built in, in one commit, so a disagreement between them is not a
   drift: it is a version somebody moved by hand, which
   `.agents/rules/conformance.md` forbids outright.
2. No text under `plugins/` other than `binaries.json`, and nothing in
   `README.md`, contains a release URL with a tag segment
   (`/releases/tag/<tag>` or `/releases/download/<tag>`). The release
   rewrites `binaries.json` and cannot rewrite a sentence, so a tag written
   into prose is a claim the next release silently falsifies
   (`.agents/rules/claims.md`); `binaries.json` is exempt because it is the
   file the release writes.
3. `.claude-plugin/marketplace.json` carries no `version`: not at the top
   level, not under `metadata`, and not in a plugin entry. Nothing writes
   that file, so any version in it is one a person moves by hand -- and the
   top-level one had already drifted, reading 0.3.0 while the package it
   points at was at 0.3.1. Absence is the machine-checkable half of the
   same rule; the documentation this rests on is quoted in
   `.agents/rules/conformance.md` beside it.

It exists because each of the three has already failed here. The package once
shipped `howp-v0.2.0` while `README.md` still sent readers to the
`howp-v0.1.0` release page and its `SHA256SUMS` -- that is check 2. On
2026-09-02 the release job read this repository's `plugin.json` at
17:54:52.76Z and a hand bump of the same file to 0.2.1 merged six seconds
later, at 17:54:59Z; the release itself succeeded -- `howp-v0.2.1`, both
archives and `SHA256SUMS`, published at 18:03:49Z -- and its last step then
refused a package already at 0.2.1, so nothing here was ever pointed at it
and `binaries.json` stayed at `howp-v0.2.0`. That is check 1: the record has
to agree with itself, or the package names a release it is not on. Check 3
is the same defect in the one file no release touches at all -- the
marketplace index sat at 0.3.0 against a package the release had moved to
0.3.1, and it sat there because moving it was somebody's job to remember.

This script replaces `check-release-links.py`, which compared the tag in a
link against the tag `binaries.json` records. Comparing them is no longer a
question worth asking: prose may not name a tag at all, so the elaborate
definition of what a tag *is* -- which that check needed so that a correct
link could never be misread as stale -- is gone with the comparison it
served. Presence is the whole test now.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"
README = ROOT / "README.md"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
RULES = ".agents/rules/conformance.md"

# Text the repository publishes about itself. Only the suffixes a reader
# reads; symlinks are skipped so a vendor path is not scanned as a second
# copy of its target.
SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}

# A release URL that names a tag, under any host. Matched on the path shape
# alone rather than against the URLs binaries.json records: the objection is
# to a tag in a sentence, and a link to some other host's release page names
# a tag just as unrewritably. The trailing class stops at the delimiters
# markdown and HTML put after a URL, so the tag quoted back in the message
# is the tag and not the punctuation after it -- which is cosmetic here,
# because any match at all is a failure.
RELEASE_TAG_URL = re.compile(r"/releases/(?:tag|download)/([^\s/)\]\"'<>`,;*]+)")


def text_files(root: pathlib.Path) -> list[pathlib.Path]:
    return [
        p
        for p in sorted(root.rglob("*"))
        if p.is_file() and not p.is_symlink() and p.suffix in SUFFIXES
    ]


def check_versions() -> tuple[list[str], list[str]]:
    """The three machine-written strings of the release record agree."""
    problems: list[str] = []
    checked: list[str] = []
    for plugin_root in sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir()):
        binaries_path = plugin_root / "binaries.json"
        if not binaries_path.is_file():
            continue
        rel = plugin_root.relative_to(ROOT)
        manifest = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
        binaries = json.loads(binaries_path.read_text(encoding="utf-8"))
        name = manifest["name"]
        version = manifest["version"]
        # `<name>-v<version>` is this repository's convention rather than
        # anything the specification says, and it is the shape the release
        # builds: `tag="howp-v$version"` in how-possible's release.yml. It
        # holds for howp; a package released under some other scheme would
        # need this line to learn about it.
        expected_tag = f"{name}-v{version}"
        if binaries.get("version") != version or binaries.get("tag") != expected_tag:
            problems.append(
                f"{rel}: plugin.json records version {version!r} while "
                f"binaries.json records version {binaries.get('version')!r} "
                f"and tag {binaries.get('tag')!r} (expected {expected_tag!r}). "
                f"The release writes all three in one commit, so this is a "
                f"version moved by hand, which {RULES} forbids: restore the "
                f"version the release wrote and let the next release move it."
            )
        else:
            checked.append(f"{name} {version}, {expected_tag}")
    return problems, checked


def check_no_tag_in_prose() -> list[str]:
    """No release URL naming a tag in text the release path cannot rewrite."""
    problems: list[str] = []
    # `binaries.json` is the only exemption, and it stays the only one while
    # it is the only file under plugins/ a release writes. commands.md is not
    # machine-written yet: proposed in how-possible, not merged -- the rule
    # file .agents/rules/conformance.md carries the pull request.
    paths = [p for p in text_files(PLUGINS_DIR) if p.name != "binaries.json"]
    if README.is_file():
        paths.append(README)
    for path in paths:
        for n, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for found in RELEASE_TAG_URL.findall(line):
                problems.append(
                    f"{path.relative_to(ROOT)}:{n}: names the release tag "
                    f"{found!r} in a release URL. Nothing in the release path "
                    f"rewrites this text, so the next release falsifies it "
                    f"silently: point at plugins/*/binaries.json, which the "
                    f"release does rewrite."
                )
    return problems


def check_no_index_version() -> list[str]:
    """The catalogue index carries no version for anybody to move by hand."""
    if not MARKETPLACE.is_file():
        return []
    rel = MARKETPLACE.relative_to(ROOT)
    index = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    # Shape is check-conformance.py's business, not this script's: every
    # isinstance below is there so a hand-edited index of the wrong shape
    # reaches that check as a finding instead of ending this one in a
    # traceback.
    if not isinstance(index, dict):
        return []
    keys: list[str] = []
    if "version" in index:
        keys.append("version")
    metadata = index.get("metadata")
    if isinstance(metadata, dict) and "version" in metadata:
        keys.append("metadata.version")
    entries = index.get("plugins")
    if isinstance(entries, list):
        for n, entry in enumerate(entries):
            if isinstance(entry, dict) and "version" in entry:
                keys.append(f"plugins[{n}].version ({entry.get('name', '?')})")
    return [
        f"{rel}: carries `{key}`, a version no machine writes. The release "
        f"writes plugin.json and binaries.json; nothing writes this file, so "
        f"a version in it is one somebody moves by hand, which {RULES} "
        f"forbids. Delete the key -- Claude Code documents it as optional, "
        f"and plugin.json already carries the version the release wrote."
        for key in keys
    ]


def main() -> int:
    version_problems, checked = check_versions()
    problems = (
        version_problems + check_no_tag_in_prose() + check_no_index_version()
    )
    if problems:
        print(
            f"release-record: {len(problems)} problem(s):",
            file=sys.stderr,
        )
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    index = (
        ", and no hand-written version in .claude-plugin/marketplace.json"
        if MARKETPLACE.is_file()
        else ""
    )
    print(
        f"release-record OK: {len(checked)} package(s) at the version the "
        f"release wrote ({'; '.join(checked)}), no release URL naming a tag "
        f"in the text under plugins/ or in README.md{index}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
