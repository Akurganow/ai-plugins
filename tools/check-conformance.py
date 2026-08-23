#!/usr/bin/env python3
"""Check that this repository's plugins still conform to Agent Plugins 1.0.0.

Run it by hand (`python3 tools/check-conformance.py`) or let CI run it; it
exits non-zero and prints one line per problem.

Why this script exists instead of a ready-made tool. The specification
publishes a machine-readable manifest schema (`schemas/1.0.0/
plugin.schema.json`) but no validator: the agent-plugins-spec repository
contains the spec text, the two JSON schemas, and governance files, and
nothing executable. The Agent Skills project does publish a reference
validator, `skills-ref`, but its own README says "This library is intended
for demonstration purposes only. It is not meant to be used in production",
and it is distributed from a source tree rather than a package index, so it
is not something to pin a CI job to (it is still the right thing to run by
hand when changing a skill).

So the split here is: everything the official schema can decide is decided
by the official schema, through `jsonschema` — the schema file in
tools/schemas/ is a verbatim copy of the published one, and the copy is
authenticated by sha256 against the digest recorded below before it is used
for anything. The digest is what makes a schema edited in place — same
`$id`, a `pattern` or a `maxLength` quietly removed — fail instead of
silently widening every manifest check. The `$id` check that follows it can
only fire once the digest has been updated as well, which is the case where
a different published version was vendored in deliberately and this script
was not moved to it. Only the rules a JSON Schema cannot express — where
files sit on disk, what symlinks resolve to, what the skill frontmatter
says — are implemented below, against the spec text quoted at each check.

Out of scope, recorded so it is a decision and not an oversight: a hard link
whose target lies outside the plugin root is not detected. Git cannot
represent a hard link, so one cannot arrive through a commit; it could only
be created in a working tree after checkout, which is outside what a check on
the repository's contents can speak to.

Vendored schema provenance: https://agent-plugins.org/schemas/1.0.0/
plugin.schema.json, published in github.com/agentplugins/agent-plugins-spec
at schemas/1.0.0/plugin.schema.json, licensed Apache-2.0 by the Agent
Plugins project. Copied verbatim; the digest is `SCHEMA_SHA256` below and it
is checked at every run.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
SCHEMA_PATH = REPO_ROOT / "tools/schemas/agent-plugins/1.0.0/plugin.schema.json"

# Agent Plugins 1.0.0 §5.2: for this version the value of `$schema` MUST be
# this exact identifier.
CANONICAL_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"

# sha256 of the published 1.0.0 manifest schema, as vendored in tools/schemas/.
# Recompute after deliberately revendoring, and never to make a failure go
# away: a mismatch means the local copy is not the published schema.
SCHEMA_SHA256 = "0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883"

# Agent Plugins 1.0.0 §5.2: the manifest schema is closed.
MANIFEST_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}

# Agent Skills specification: the frontmatter fields a skill may carry.
SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILL_COMPATIBILITY_MAX = 500
# A frontmatter delimiter is a whole line, never a substring of a value.
FRONTMATTER_DELIMITER = re.compile(r"---[ \t]*")
SKILL_DESCRIPTION_MAX = 1024

problems: list[str] = []


def fail(where: str, message: str) -> None:
    problems.append(f"{where}: {message}")


def resolved_inside(path: Path, root: Path) -> bool:
    """True when `path` resolves inside the resolved `root`.

    Agent Plugins 1.0.0 §4.1(3): "When a client discovers, reads, or executes
    a file or directory supplied by the plugin package, the filesystem-
    resolved path MUST remain within the filesystem-resolved plugin root."
    """
    try:
        real_root = root.resolve(strict=True)
        path.resolve(strict=False).relative_to(real_root)
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def load_schema_validator():
    try:
        import jsonschema
    except ImportError:
        print(
            "This check needs the `jsonschema` and `pyyaml` packages:\n"
            "    pip install jsonschema pyyaml",
            file=sys.stderr,
        )
        raise SystemExit(2)

    raw = SCHEMA_PATH.read_bytes()
    # The vendored copy is only trustworthy if it is byte for byte the
    # published schema for this version, so authenticate it before validating
    # anything with it. `$id` alone would not: it is a field inside the file,
    # so any edit that keeps it — dropping `pattern` from `name`, opening up
    # `author` — would leave the check passing while the rules it enforces got
    # weaker.
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SCHEMA_SHA256:
        fail(
            str(SCHEMA_PATH.relative_to(REPO_ROOT)),
            f"vendored schema sha256 is {digest}, expected {SCHEMA_SHA256}; "
            "the copy is not the published schema",
        )
        raise SystemExit(report())
    schema = json.loads(raw.decode("utf-8"))
    if schema.get("$id") != CANONICAL_SCHEMA_ID:
        fail(
            str(SCHEMA_PATH.relative_to(REPO_ROOT)),
            f"vendored schema declares $id {schema.get('$id')!r}, "
            f"expected {CANONICAL_SCHEMA_ID!r}",
        )
        raise SystemExit(report())
    return jsonschema.Draft202012Validator(schema)


def parse_frontmatter(text: str):
    """Return the YAML frontmatter of a SKILL.md as a dict, or None.

    The block ends at the first *line* that is `---`, which is how a client
    finds it: Hermes reads the closer with `re.search(r"\n---\s*\n", ...)`
    (`hermes_cli/agent_plugins.py`), and YAML itself treats `---` at the start
    of a line as a document marker.

    Splitting on the substring `---` instead — which is what the Agent Skills
    reference validator `skills-ref` does at `src/skills_ref/parser.py:45`,
    and what this function did until it was tested — ends the block at the
    first occurrence anywhere, including inside a quoted or folded value. Then
    every rule below runs on a partial document that no client ever sees, and
    whatever the author wrote after the truncation point is invisible: a
    `SKILL.md` carrying an em dash and `---` in its folded `description`, an
    unknown frontmatter field, and a `name` that does not match its directory
    passed this check with `conformance OK` and exit 0.
    """
    import yaml

    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or not FRONTMATTER_DELIMITER.fullmatch(lines[0]):
        return None
    for index in range(1, len(lines)):
        if FRONTMATTER_DELIMITER.fullmatch(lines[index]):
            block = "\n".join(lines[1:index])
            break
    else:
        return None
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def check_manifest(plugin_root: Path, validator) -> dict | None:
    """§4.1(2), §5.1, §5.2, §5.3, §5.5 — the manifest at the plugin root."""
    where = str(plugin_root.relative_to(REPO_ROOT))
    manifest_path = plugin_root / "plugin.json"

    # §4.1(2): "A plugin MUST include a manifest at `plugin.json` in the
    # plugin root."
    if not manifest_path.exists():
        fail(where, "no plugin.json at the plugin root (§4.1, §5.1)")
        return None
    # Not a spec rule but a loader reality and a repository rule: the root
    # manifest is the real file that vendor paths point at, never a link.
    # Codex's loader refuses a symlinked root manifest outright --
    # find_plugin_manifest_path() calls symlink_metadata() and returns None
    # for a symlink, pinned by rejects_symlinked_root_plugin_manifest:
    # https://github.com/openai/codex/blob/main/codex-rs/utils/plugins/src/plugin_namespace.rs
    if manifest_path.is_symlink():
        fail(where, "plugin.json at the plugin root is a symlink; it must be the real file")
        return None
    if not manifest_path.is_file():
        fail(where, "plugin.json is not a regular file (§5.1)")
        return None

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(where, f"plugin.json does not parse: {exc}")
        return None
    # §5.2: "The manifest MUST be JSON and MUST contain a top-level object."
    if not isinstance(manifest, dict):
        fail(where, "plugin.json does not contain a top-level object (§5.2)")
        return None

    # §5.2/§5.3: `$schema` is required and its value is fixed for 1.0.0.
    # Checked explicitly as well as by the schema, so the failure names the
    # reason instead of reading as a generic `const` mismatch.
    if manifest.get("$schema") != CANONICAL_SCHEMA_ID:
        fail(
            where,
            f"plugin.json $schema is {manifest.get('$schema')!r}, "
            f"must be {CANONICAL_SCHEMA_ID!r} (§5.2)",
        )

    # §5.2: the top-level schema is closed.
    for field in sorted(set(manifest) - MANIFEST_FIELDS):
        fail(where, f"plugin.json has top-level field {field!r}, outside the closed set (§5.2)")

    # Everything else the published schema decides: required fields (§5.3),
    # the name constraints (§5.5), field types (§5.4), the closed `author`
    # object, `extensions` shape (§8.1).
    for error in sorted(validator.iter_errors(manifest), key=lambda e: list(e.path)):
        location = ".".join(str(p) for p in error.path) or "(root)"
        fail(where, f"plugin.json fails the published schema at {location}: {error.message}")

    return manifest


def check_skills(plugin_root: Path) -> None:
    """§6.1, §6.2, §7.1 — skills live in `skills/`, one level deep."""
    where = str(plugin_root.relative_to(REPO_ROOT))
    skills_dir = plugin_root / "skills"
    # §6.2: "If a fixed component location is absent, the client MUST NOT
    # treat that as an error." A plugin with no skills is fine.
    if not skills_dir.exists():
        return
    # §6.2: present but not the expected filesystem kind is invalid.
    if not skills_dir.is_dir():
        fail(where, "skills/ exists but is not a directory (§6.2)")
        return

    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        # §7.1: "Each immediate child directory containing a path named
        # exactly `SKILL.md` that resolves to a regular file is treated as
        # one skill."
        if not skill_md.exists():
            fail(f"{where}/skills/{child.name}", "directory has no SKILL.md (§7.1)")
            continue
        if not skill_md.is_file():
            fail(f"{where}/skills/{child.name}", "SKILL.md does not resolve to a regular file (§7.1)")
            continue
        # §4.1(3) with the failure boundary of §4.1: "If a discovered
        # `SKILL.md` does not resolve within the plugin root, the client MUST
        # skip that skill under §7.1."
        if not resolved_inside(skill_md, plugin_root):
            fail(f"{where}/skills/{child.name}", "SKILL.md resolves outside the plugin root (§4.1)")
            continue
        check_skill_frontmatter(child, skill_md)


def check_skill_frontmatter(skill_dir: Path, skill_md: Path) -> None:
    """§7.1 defers the format to the Agent Skills specification.

    Only the rules that decide whether a client loads or skips the skill are
    checked here; `skills-ref validate` is the full reference check.
    """
    where = str(skill_dir.relative_to(REPO_ROOT))
    data = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if data is None:
        fail(where, "SKILL.md has no parseable YAML frontmatter")
        return

    for field in sorted(set(data) - SKILL_FIELDS):
        fail(where, f"SKILL.md frontmatter has unknown field {field!r}")

    name = data.get("name")
    if not isinstance(name, str) or not name:
        fail(where, "SKILL.md frontmatter has no `name`")
    else:
        if len(name) > 64 or not SKILL_NAME_RE.fullmatch(name):
            fail(where, f"skill name {name!r} breaks the Agent Skills name constraints")
        if name != skill_dir.name:
            fail(where, f"skill name {name!r} does not match its directory {skill_dir.name!r}")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        fail(where, "SKILL.md frontmatter has no `description`")
    elif len(description) > SKILL_DESCRIPTION_MAX:
        fail(where, f"skill description is {len(description)} characters, over the 1024 limit")

    # The optional fields decide load-or-skip just as the required ones do: a
    # client that type-checks them skips the skill when one is the wrong
    # shape. Hermes is the worked example — `_valid_skill_frontmatter` in
    # `hermes_cli/agent_plugins.py` returns an error for each of these and the
    # skill is dropped with a diagnostic while its siblings still load — so a
    # check that verifies only `name` and `description` passes packages that
    # the mandatory client silently loads short of a skill.
    if "license" in data and not isinstance(data["license"], str):
        # Agent Skills: `license` is "License name or reference to a bundled
        # license file".
        fail(where, "SKILL.md frontmatter `license` is not a string")

    if "compatibility" in data:
        # Agent Skills: `compatibility` "Must be 1-500 characters if provided".
        compatibility = data["compatibility"]
        if not isinstance(compatibility, str) or not compatibility.strip():
            fail(where, "SKILL.md frontmatter `compatibility` is not a non-empty string")
        elif len(compatibility) > SKILL_COMPATIBILITY_MAX:
            fail(
                where,
                f"skill compatibility is {len(compatibility)} characters, "
                f"over the {SKILL_COMPATIBILITY_MAX} limit",
            )

    if "metadata" in data:
        # Agent Skills: `metadata` is "A map from string keys to string values".
        metadata = data["metadata"]
        if not isinstance(metadata, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        ):
            fail(where, "SKILL.md frontmatter `metadata` is not a map of string to string")

    if "allowed-tools" in data and not isinstance(data["allowed-tools"], str):
        # Agent Skills: `allowed-tools` is "A space-separated string of tools".
        fail(where, "SKILL.md frontmatter `allowed-tools` is not a string")


def check_containment(plugin_root: Path) -> None:
    """§4.1(3) — nothing in the package may resolve outside the plugin root."""
    where = str(plugin_root.relative_to(REPO_ROOT))
    for dirpath, dirnames, filenames in os.walk(plugin_root):
        for entry in list(dirnames) + list(filenames):
            path = Path(dirpath) / entry
            if not path.is_symlink():
                continue
            rel = path.relative_to(REPO_ROOT)
            if not path.exists():
                fail(str(rel), "symlink target does not exist")
                continue
            if not resolved_inside(path, plugin_root):
                fail(
                    str(rel),
                    f"symlink resolves to {os.path.realpath(path)}, outside the plugin root (§4.1)",
                )


def materialised_symlink_hint(path: Path, expected_target: Path) -> str:
    """Name the Windows checkout case instead of misreporting it.

    A checkout with `core.symlinks=false` — git's default on Windows — writes
    a symlink as a small text file holding its target path. The repository
    still records mode 120000, so this is a property of the checkout and not
    of the commit, and saying "second copy of the manifest" about it would
    send a contributor looking for a defect that is not there.
    """
    try:
        if path.stat().st_size > 4096:
            return ""
        content = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError):
        return ""
    if not content or "\n" in content:
        return ""
    if (path.parent / content).resolve(strict=False) != expected_target:
        return ""
    return (
        f" — the file holds {content!r} and nothing else, so this checkout "
        "materialised the symlink as text (git core.symlinks=false, the "
        "default on Windows); re-clone with `-c core.symlinks=true`"
    )


def check_no_duplicate_manifest(plugin_root: Path) -> None:
    """Repository rule: a vendor path may point at the manifest, not hold one.

    A second `plugin.json` anywhere below the plugin root is only acceptable
    as a symlink to the root manifest; a real file there would be a copy that
    drifts, and §5.1 is explicit that "No other file can replace, supplement,
    or override the core fields in root `plugin.json`."
    """
    root_manifest = (plugin_root / "plugin.json").resolve(strict=False)
    for dirpath, _dirnames, filenames in os.walk(plugin_root):
        if Path(dirpath) == plugin_root:
            continue
        if "plugin.json" not in filenames:
            continue
        path = Path(dirpath) / "plugin.json"
        rel = path.relative_to(REPO_ROOT)
        if not path.is_symlink():
            fail(
                str(rel),
                "second copy of the manifest; a vendor path may only be a "
                "symlink to ../plugin.json"
                + materialised_symlink_hint(path, root_manifest),
            )
        elif path.resolve(strict=False) != root_manifest:
            fail(str(rel), f"symlink points at {path.resolve(strict=False)}, not the plugin's own manifest")


def check_marketplace_index(manifests: dict[str, dict]) -> None:
    """Cross-check Claude's vendor index against the conforming manifests.

    Agent Plugins 1.0.0 defines no repository-level index, so this file is
    outside the standard; it is checked only for pointing at real plugin
    roots under the names those plugins actually declare.
    """
    index_path = REPO_ROOT / ".claude-plugin/marketplace.json"
    if not index_path.exists():
        return
    where = ".claude-plugin/marketplace.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(where, f"does not parse: {exc}")
        return
    # Shape before content, twice over. A hand-edited index can be a JSON
    # array, or carry `plugins` as a string, or hold strings where entries
    # belong; each of those used to reach `.get` on something that has none
    # and end the run in an AttributeError traceback instead of a finding.
    if not isinstance(index, dict):
        fail(where, "does not contain a top-level object")
        return
    entries = index.get("plugins", [])
    if not isinstance(entries, list):
        fail(where, f"`plugins` is {type(entries).__name__}, must be an array")
        return

    listed = set()
    for entry in entries:
        if not isinstance(entry, dict):
            fail(where, f"entry {entry!r} is not an object")
            continue
        name, source = entry.get("name"), entry.get("source")
        if not isinstance(name, str) or not isinstance(source, str):
            fail(where, f"entry {entry!r} needs a string `name` and `source`")
            continue
        listed.add(name)
        target = (REPO_ROOT / source).resolve(strict=False)
        # An entry may point anywhere the filesystem allows, including out of
        # the repository (`../elsewhere`, or an absolute path). That is a
        # finding, not a crash: reported here rather than left to raise out of
        # the `relative_to` below.
        try:
            relative_target = target.relative_to(REPO_ROOT)
        except ValueError:
            fail(
                where,
                f"entry {name!r} points at {source}, which resolves outside the "
                f"repository ({target})",
            )
            continue
        if not (target / "plugin.json").is_file():
            fail(where, f"entry {name!r} points at {source}, which is not a plugin root")
            continue
        declared = manifests.get(str(relative_target), {}).get("name")
        if declared is not None and declared != name:
            fail(where, f"entry {name!r} points at a plugin whose manifest name is {declared!r}")

    for plugin_path, manifest in manifests.items():
        if manifest.get("name") not in listed:
            fail(where, f"plugin {plugin_path} is not listed in the index")


def report() -> int:
    if problems:
        print(f"{len(problems)} conformance problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    return 0


def main() -> int:
    validator = load_schema_validator()

    if not PLUGINS_DIR.is_dir():
        print("no plugins/ directory, nothing to check")
        return 0

    manifests: dict[str, dict] = {}
    plugin_roots = sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir())
    for plugin_root in plugin_roots:
        manifest = check_manifest(plugin_root, validator)
        if manifest is not None:
            manifests[str(plugin_root.relative_to(REPO_ROOT))] = manifest
        check_skills(plugin_root)
        check_containment(plugin_root)
        check_no_duplicate_manifest(plugin_root)

    check_marketplace_index(manifests)

    exit_code = report()
    if exit_code == 0:
        names = ", ".join(sorted(m.get("name", "?") for m in manifests.values()))
        print(f"conformance OK: {len(plugin_roots)} plugin(s) checked ({names})")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
