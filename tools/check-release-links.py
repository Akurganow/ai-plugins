#!/usr/bin/env python3
"""Every release link under plugins/ and in README.md names the tag binaries.json records.

Not a check on prose. Both sides are machine-written: the tag segment of a
release URL, and the `tag` field the release bot writes into
plugins/howp/binaries.json. A mismatch is arithmetic, not a judgement call,
which is what separates this from a grep that hunts stale claims -- every hit
of one of those needs a human, and a check whose hits need a human is a check
its readers learn to skip.

It exists because the package shipped howp-v0.2.0 while README.md still sent
readers to the howp-v0.1.0 release page and its SHA256SUMS.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BINARIES = ROOT / "plugins" / "howp" / "binaries.json"
# Text the package publishes. binaries.json is included deliberately: it is
# machine-written, so its own URLs must agree with its own tag.
SEARCH = ["plugins", "README.md"]
SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}

# What a tag is: an alphanumeric, then any run of alphanumerics, dots,
# hyphens and underscores, ending on an alphanumeric. One definition, used
# twice -- to match the tag segment of a URL, and to check the tag
# binaries.json records -- so the two ends of the comparison cannot drift
# apart.
#
# It describes what a tag *is* rather than what ends one, because the first
# version of this check ended the tag at a negated class naming only '/',
# the four bracketing characters, whitespace and quotes, and markdown puts
# far more than that after a URL. Eight ordinary ways of writing a *correct*
# release link swallowed their punctuation into the "tag" and failed: a code
# span's backtick, a sentence's full stop, a comma, a semicolon, bold's
# asterisks, a '#' fragment, a '?' query, and -- surviving the first
# correction, whose class still admitted '_' and '-' as terminal characters
# -- markdown's underscore emphasis, `_URL_` and `__URL__`. Making a correct
# link fail is the one behaviour this check may never have.
#
# What it refuses by design is three shapes, which the refusal message
# below states as the one rule they break -- a tag must begin and end with a
# letter or a digit, with letters, digits, dots, hyphens and underscores
# between. So: a tag whose *first* character is not alphanumeric, a tag whose
# *last* character is not alphanumeric, and a tag carrying any character
# outside `[A-Za-z0-9._-]` -- a semver '+' among them. git accepts all three:
# `git check-ref-format --allow-onelevel` accepts `refs/tags/_howp`,
# `refs/tags/howp-v0.2.0-`, `refs/tags/howp-v0.2.0_`, `refs/tags/howp+build.5`
# and `refs/tags/howp@1`, and this class matches none of them, so under such a
# tag every correct link in the tree would look stale. That is why the
# recorded tag is asserted against this same class before anything is
# scanned: one loud refusal naming the tag beats a page of hits that are all
# wrong.
TAG_FORM = r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?"


def main() -> int:
    manifest = json.loads(BINARIES.read_text(encoding="utf-8"))
    tag = manifest["tag"]
    if not re.fullmatch(TAG_FORM, tag):
        print(
            f"release-links: plugins/howp/binaries.json records the tag "
            f"{tag!r}, which this check cannot match: a tag must begin and "
            f"end with a letter or a digit, with letters, digits, dots, "
            f"hyphens and underscores between (/{TAG_FORM}/). Nothing was "
            f"scanned. Widen TAG_FORM in this file and re-run it, rather "
            f"than reading the links as stale.",
            file=sys.stderr,
        )
        return 1
    # Bases are derived from the manifest rather than hardcoded, so the check
    # follows wherever the release bot actually publishes. Every target is
    # read, not just the first: they share a base today, but a manifest that
    # ever carried two hosts would leave links to the second unscanned if this
    # keyed on targets[0].
    bases = sorted({t["url"].split("/releases/")[0] for t in manifest["targets"]})
    pattern = re.compile(
        "(?:" + "|".join(re.escape(b) for b in bases) + ")"
        + r"/releases/(?:tag|download)/(" + TAG_FORM + ")"
    )

    paths = []
    for entry in SEARCH:
        p = ROOT / entry
        if p.is_file():
            paths.append(p)
        else:
            paths.extend(
                q for q in sorted(p.rglob("*"))
                if q.is_file() and not q.is_symlink() and q.suffix in SUFFIXES
            )

    bad = []
    for path in paths:
        for n, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for found in pattern.findall(line):
                if found != tag:
                    bad.append((path.relative_to(ROOT), n, found))

    if bad:
        print(
            f"release-links: {len(bad)} link(s) name a tag that is not "
            f"{tag!r}, which is what plugins/howp/binaries.json records:",
            file=sys.stderr,
        )
        for rel, n, found in bad:
            print(f"  {rel}:{n}: names {found!r}, expected {tag!r}", file=sys.stderr)
        return 1

    print(
        f"release-links OK: every release link under plugins/ and in "
        f"README.md names {tag}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
