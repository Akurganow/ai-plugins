#!/usr/bin/env python3
"""Every release link in the published text names the tag binaries.json records.

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


def main() -> int:
    manifest = json.loads(BINARIES.read_text(encoding="utf-8"))
    tag = manifest["tag"]
    # Bases are derived from the manifest rather than hardcoded, so the check
    # follows wherever the release bot actually publishes. Every target is
    # read, not just the first: they share a base today, but a manifest that
    # ever carried two hosts would leave links to the second unscanned if this
    # keyed on targets[0].
    bases = sorted({t["url"].split("/releases/")[0] for t in manifest["targets"]})
    pattern = re.compile(
        "(?:" + "|".join(re.escape(b) for b in bases) + ")"
        # Match what a tag *is*, not what ends one. Markdown follows and
        # wraps a bare URL with punctuation -- a code span's backtick, a
        # sentence's full stop, a comma, a semicolon, bold's asterisks, a
        # '#' fragment, a '?' query -- and the first version of this
        # excluded only '/', the four bracketing characters, whitespace and
        # quotes, so each of those seven forms swallowed its punctuation
        # into the "tag" and made a *correct* link fail, which is the one
        # behaviour this check may never have. A positive class cannot fail
        # that way. It is narrower than git's own ref rules on purpose --
        # the tags here are howp-vX.Y.Z, so: an alphanumeric, then
        # alphanumerics, dots, hyphens and underscores. The trailing dot is
        # excluded in the class rather than stripped from the match
        # afterwards; git refuses a ref that ends in one, so a dot there is
        # never part of a tag, and keeping it here leaves the whole
        # definition of a tag in one place.
        + r"/releases/(?:tag|download)/([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9_-])?)"
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

    print(f"release-links OK: every release link names {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
