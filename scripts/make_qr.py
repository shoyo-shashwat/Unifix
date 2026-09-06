"""Generate the printable UNIFIX install QR code.

    py -3.13 scripts/make_qr.py https://your-host/get

Writes brand/qr-unifix-install.svg — a QR at error-correction level H with the
UNIFIX pin badge sitting in the middle. Level H tolerates ~30% loss, which is
what buys us the covered centre.

Not part of the app. `segno` is a build-time tool only and is deliberately NOT
in requirements.txt:  py -3.13 -m pip install segno
"""
import os
import sys

import segno

NAVY = "#0E2F5C"
GREEN = "#12885A"
QUIET = 4          # modules of margin the spec requires around every QR
# Badge diameter as a fraction of the QR body. A centred disc of diameter d
# hides pi*(d/2)^2 of the area, so 0.27 costs ~5.7% — well inside level H's 30%
# budget. Verified decoding up to 0.40; keep well under that for print wear.
BADGE = 0.27


def build(url: str) -> str:
    qr = segno.make(url, error="h")
    matrix = [list(row) for row in qr.matrix]
    n = len(matrix)
    size = n + QUIET * 2

    # One path for every dark module. Cheaper than n^2 <rect> elements and it
    # keeps the file small enough to drop straight into a print layout.
    parts = []
    for y, row in enumerate(matrix):
        for x, dark in enumerate(row):
            if dark:
                parts.append(f"M{x + QUIET} {y + QUIET}h1v1h-1z")
    modules = "".join(parts)

    c = size / 2
    r = n * BADGE / 2                     # badge radius, in modules
    pin = r * 2 / 48 * 0.80               # scale factor for the 48-unit mark
    # The mark's ink sits in y 4..46, not the full 48-unit box, so centre on its
    # visual middle (24, 25) or it reads as floating high in the disc.
    px = c - 24 * pin
    py = c - 25 * pin

    # An intrinsic width/height keeps Word, Docs and print layouts from placing
    # the QR at some arbitrary size; the viewBox still lets it scale cleanly.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"
     width="420" height="420" role="img" aria-labelledby="qr-title">
  <title id="qr-title">Scan to install UNIFIX — {url}</title>
  <mask id="pin-check">
    <rect width="48" height="48" fill="#fff"/>
    <path d="M16 18 L21.5 24 L31.5 12.5" fill="none" stroke="#000"
          stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
  </mask>
  <rect width="{size}" height="{size}" fill="#FFFFFF"/>
  <path d="{modules}" fill="{NAVY}" shape-rendering="crispEdges"/>
  <circle cx="{c}" cy="{c}" r="{r:.3f}" fill="#FFFFFF"/>
  <circle cx="{c}" cy="{c}" r="{r:.3f}" fill="none" stroke="{NAVY}"
          stroke-opacity="0.14" stroke-width="{r * 0.045:.3f}"/>
  <g transform="translate({px:.3f} {py:.3f}) scale({pin:.4f})">
    <path d="M24 46 C 16 34 9 27 9 19 A 15 15 0 1 1 39 19 C 39 27 32 34 24 46 Z"
          fill="{NAVY}" mask="url(#pin-check)"/>
  </g>
</svg>
"""


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    url = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "brand", "qr-unifix-install.svg")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build(url))
    print(f"{out}\n  -> {url}\n  scan-test on two phones before printing")


if __name__ == "__main__":
    main()
