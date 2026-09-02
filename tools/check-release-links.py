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
        # The delimiter set matters: a markdown autolink <URL> and a link
        # [t](URL) both end the tag with a character that is not part of
        # it. Getting this wrong makes a *correct* link fail, which is the
        # one behaviour this check may never have.
        + r"/releases/(?:tag|download)/([^/)\]>\s\"']+)"
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
