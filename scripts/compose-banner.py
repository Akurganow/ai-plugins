"""Write docs/banner.svg, the README banner, from the parts in docs/banner/.

docs/banner/README.md says how a part is drawn and how to add one. Run with
no arguments from anywhere; it prints the output path and size.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANNER = ROOT / "docs" / "banner"
PARTS = BANNER / "parts"
OUT = ROOT / "docs" / "banner.svg"

HOOKS = json.loads((PARTS / "hooks.json").read_text())["hooks"]
HOOK_ID = {"single": "hook-single", "heavy": "hook-heavy", "shelf": "shelf"}

# Shadow opacity along the board's own light falloff (centre (420, 90),
# r 1650): darker board, denser shadow, so shadows read on the right too.
SHADOW_OPACITY = [(0, 0.5), (0.4, 0.52), (0.72, 0.62), (1, 0.74)]


def hole(i, j):
    """Centre of the board hole in column i, row j (docs/banner/parts/board.json)."""
    return 16 + 44 * i, 16 + 44 * j


def split(name):
    svg = (PARTS / f"{name}.svg").read_text()
    defs = svg[svg.index("<defs>") + 6 : svg.index("</defs>")]
    body = svg[svg.index("</defs>") + 7 : svg.rindex("</svg>")]
    return defs, body


def shadow(fid, std, dx, dy, opacity, region):
    # The alpha boost lets glass, which is mostly transparent, still cast a shadow.
    x, y, w, h = region
    return (f'<filter id="{fid}" x="{x}" y="{y}" width="{w}" height="{h}" color-interpolation-filters="sRGB">'
            '<feComponentTransfer in="SourceAlpha"><feFuncA type="linear" slope="3"/></feComponentTransfer>'
            f'<feGaussianBlur stdDeviation="{std}"/><feOffset dx="{dx}" dy="{dy}" result="a"/>'
            f'<feFlood flood-color="#22110a" flood-opacity="{opacity}"/><feComposite in2="a" operator="in"/></filter>')


def main():
    layout = json.loads((BANNER / "layout.json").read_text())
    board_defs, board_body = split("board")
    defs = [board_defs]
    for name in [it["object"] for it in layout if it.get("object")]:
        part_defs, body = split(name)
        defs += [part_defs, body[body.index(f'<g id="{name}-art"'):]]
    defs.append(split("hooks")[0])
    defs += [shadow("banner-sh-flat", 5, 13, 18, 1, ("-60%", "-20%", "220%", "150%")),
             shadow("banner-sh-far", 6.5, 16, 21, 0.92, ("-30%", "-15%", "160%", "135%")),
             shadow("banner-sh-hook", 2, 5, 7, 1, ("-60%", "-40%", "220%", "180%")),
             '<radialGradient id="banner-sh-falloff" gradientUnits="userSpaceOnUse" cx="420" cy="90" r="1650">'
             + "".join(f'<stop offset="{o}" stop-color="#fff" stop-opacity="{a}"/>' for o, a in SHADOW_OPACITY)
             + '</radialGradient><mask id="banner-sh-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="2100" height="900">'
             '<rect width="2100" height="900" fill="url(#banner-sh-falloff)"/></mask>']

    # Each hook is drawn in two layers, so the object hangs between its base
    # and the prong tip that passes in front of it.
    shadows, items = [], []
    for it in layout:
        hid = HOOK_ID[it["kind"]]
        hx, hy = hole(it["i"], it["j"])
        at = f"translate({hx},{hy})"
        shadows.append(f'<g transform="{at}" filter="url(#banner-sh-hook)"><use href="#{hid}-back"/><use href="#{hid}-front"/></g>')
        items.append(f'<use href="#{hid}-back" transform="{at}"/>')
        if it.get("object"):
            name, (px, py) = it["object"], it["hang"]
            hang = HOOKS[hid]["hang"]
            at_obj = f'translate({round(hx + hang["x"] - px, 2)},{round(hy + hang["y"] - py, 2)})'
            shadows.append(f'<use href="#{name}-art" transform="{at_obj}" filter="url(#banner-sh-{it["shadow"]})"/>')
            items.append(f'<use href="#{name}-art" transform="{at_obj}"/>')
        items.append(f'<use href="#{hid}-front" transform="{at}"/>')

    svg = "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                     'viewBox="0 0 2100 900" width="2100" height="900">',
                     "<defs>", *defs, "</defs>", board_body.strip(),
                     '<g clip-path="url(#board-clip)" mask="url(#banner-sh-mask)">', *shadows, "</g>",
                     *items, "</svg>"])
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\n\s*\n", "\n", svg)
    ids = re.findall(r'\bid="([^"]+)"', svg)
    clashes = sorted({i for i in ids if ids.count(i) > 1})
    if clashes:
        raise SystemExit(f"compose-banner: duplicate ids {clashes}; prefix every id in a part with the part's name.")
    OUT.write_text(svg + "\n")
    print(OUT.relative_to(ROOT), len(svg.encode()), "bytes")


if __name__ == "__main__":
    main()
