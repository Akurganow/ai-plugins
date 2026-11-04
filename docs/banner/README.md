# The README banner

`docs/banner.svg` is the banner at the top of the root README: tools hanging on
a brown hardboard pegboard. Each tool stands for one package. This folder
holds its sources, and `scripts/compose-banner.py` writes the banner from them.

## Files

- `parts/<name>.svg` is one drawn part: the board, a tool, or the hooks.
- `parts/<name>.json` gives the part's size, its hang point and notes on how it
  was drawn.
- `layout.json` places each hook on the board and says which part hangs on it.
- `../banner.svg` is the output. Nothing edits it by hand.

| Part | Package |
| :-- | :-- |
| `wrench` | `triz-thinking` |
| `compass` | `design-review` |
| `ruler` | `prose-discipline` |
| `backpack` | `cognitive-load` |
| `bottle` | `toc-thinking` |

## How every part is drawn

- **Scale.** 17.3 px per cm, the same for every part. The board's hole pitch is
  25.4 mm, or 44 px, and a hole is 6.35 mm, or 11 px. A tool is drawn at its
  real size: the wrench is 25 cm long and the backpack about 40 × 30 cm.
- **View and light.** A straight-on front view of the board, lit from the
  upper left.
- **Style.** Cartoon-like but close to realistic: volume from gradients, a
  darker edge line, a light inner stroke on the lit side, highlights on metal,
  glass and plastic.
- **No cast shadow in a part.** The composer adds every cast shadow with one
  shared filter. Shading on the object itself belongs to the part.
- **Prefixed ids.** Every id in a part starts with the part's name, and the
  drawing sits in one `<g id="<name>-art">`. The composer stops on a
  duplicate id.
- **What GitHub renders.** GitHub shows the banner as an image under a Content
  Security Policy that blocks scripts and external resources. A part uses no
  `<script>`, `<text>`, `<foreignObject>` or external reference. Numerals are
  paths.

## How a tool hangs

A pegboard hook is bent wire. Its tab enters one hole and hooks behind the
board, a leg rests in the hole below, and a prong points at the viewer. A tool
hangs on the prong through its hole or loop. So `hooks.svg` splits each hook
into a `-back` group and a `-front` group, and the composer draws the hook's
back, then the tool, then the hook's front.

`parts/hooks.json` gives three kinds:

- `single`: one prong, for a tool with a hang hole or ring;
- `heavy`: two parallel prongs, for a loop at least 36.1 px wide inside;
- `shelf`: a small shelf on two brackets, for a tool that stands.

Each kind gives its anchor holes and its `hang` point: where the inside top
edge of a hole or loop rests, or where a standing tool's bottom stands.

## Add a tool

1. Draw `parts/<name>.svg` to the rules above, at the tool's real size.
2. Write `parts/<name>.json` with `width`, `height` and the hang point in the
   part's own units.
3. Add an entry to `layout.json`:
   - `object`: the part's name;
   - `kind`: the hook kind;
   - `i` and `j`: the column and row of the hook's upper-left anchor hole;
   - `hang`: the point on the tool that rests on the hook;
   - `shadow`: `flat` for a tool against the board, `far` for one that stands
     off it.

   Hole (i, j) is centred at (16 + 44i, 16 + 44j). Keep the arrangement
   irregular, with no two tools on one baseline, and keep every tool at least
   25 px inside the frame.
4. Run `python3 scripts/compose-banner.py`.
5. Render `docs/banner.svg` and look at it. Check each new hang point at 2× to
   see that the prong passes through the hole or loop.

An entry with `"object": null` draws an empty hook, room for the next tool.

## Where traced shapes come from

- The wrench's outline is traced from
  [Adjustable wrench - 15 x 2 cm - B2](https://commons.wikimedia.org/wiki/File:Adjustable_wrench_-_15_x_2_cm_-_B2.jpg),
  a CC0 photo by Fructibus on Wikimedia Commons.
- The hooks' bends and angles are traced from Fig. 3 of United States patent
  [US 4,750,700](https://patents.google.com/patent/US4750700A), a patent
  drawing.

Every other part is drawn without tracing.
