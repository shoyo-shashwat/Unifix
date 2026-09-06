# UNIFIX brand assets

Vector marks and lockups for UNIFIX — the campus grievance &amp; infrastructure
platform for GL Bajaj Institute of Technology &amp; Management.

Open `preview.html` in a browser to see every asset at multiple sizes, on light
and dark, and over a mock QR code.

## The idea

The mark is a **map pin with a checkmark cut clean through its centre**.

- **Pin** — an issue always happens at a real place on campus.
- **Check as negative space** — the issue is resolved, and you can see the
  outcome right through the mark. Transparency is the product.
- **The loop** (`unifix-philosophy.svg`) — every report runs one path: Reported
  → In progress → Resolved, and the green segment closes it back to the start.
  Nothing gets dropped.

The wordmark is drawn, not typeset: monoline geometric strokes with rounded
ends, built on a grid — things made of parts, kept in repair.

## Files

| File | Use |
| --- | --- |
| `unifix-mark.svg` | Primary mark, navy, check knocked out. Favicons, small UI. |
| `unifix-mark-mono.svg` | Same shape in one colour via `currentColor`. Stamps, print, embroidery, dark grounds. |
| `unifix-tile.svg` | App icon — navy rounded square, white pin, green check. Home-screen, store listing. |
| `unifix-logo-horizontal.svg` | Mark + wordmark. Headers, letterhead, email signature. |
| `unifix-logo-stacked.svg` | Mark over wordmark + "Report it. Track it. Done." Posters, the QR sheet, splash. |
| `unifix-qr-badge.svg` | The mark on an opaque white disc, sized to drop into the centre of a QR code. |
| `unifix-philosophy.svg` | The report → resolve loop, for decks and onboarding. |

## Palette

| Token | Hex | Role |
| --- | --- | --- |
| ink-navy | `#0E2F5C` | Structure, the mark, primary text |
| signal-blue | `#1E5FBF` | An issue in motion / in progress |
| closed-green | `#12885A` | The fix — resolution, the closing loop segment |
| bright-green | `#47C68A` | The check on dark grounds (app tile) |
| mist | `#F4F7FB` | Background |
| slate | `#5B6B7F` | Secondary text |

## Putting the mark in a QR code

1. Generate the QR at error-correction level **H** (30%) — it tolerates a
   covered centre.
2. Overlay `unifix-qr-badge.svg` centred, at **18–22%** of the QR's width. Do
   not go bigger.
3. Keep the QR's own quiet zone (4 modules of white) around the outside.
4. Scan-test with two phones before printing.

The white disc in the badge is deliberate — it gives the scanner a clean break
and the pin a plain field to sit on.

## Clear space &amp; minimum size

- Clear space around any lockup = the height of the pin mark.
- Minimum: mark 16px, horizontal lockup 96px wide, stacked lockup 120px wide.

## Export to PNG

```bash
# ImageMagick
magick -background none -density 384 brand/unifix-tile.svg brand/unifix-tile-512.png

# or Inkscape
inkscape brand/unifix-logo-horizontal.svg --export-type=png -w 1200 -o unifix-logo.png
```

For raster app icons the project already has a generator at
`scripts/make_icons.py` — point it at a PNG export of `unifix-tile.svg`.

## Don't

- Recolour outside the palette, add shadows or gradients, or outline the mark.
- Rotate, stretch, or rebuild the pin.
- Place the check anywhere except inside the pin.
- Put the wordmark on a busy photo without a solid panel behind it.
