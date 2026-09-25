"""
GIRIH.EXE — generative NFT collection generator
10 unique 1024x1024 artworks derived from Persian girih geometry.

Deterministic: same SEED + token id => same artwork.
Outputs:
  output/<id>.png        artwork
  metadata/<id>.json     ERC-721 metadata (OpenSea-compatible)
  collection.json        trait census / rarity
"""

import json
import math
import os
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- config
SIZE = 1024
SS = 2                      # supersampling factor for crisp geometry
HI = SIZE * SS
TOTAL = 10
SEED = 20260926

COLLECTION_NAME = "GIRIH.EXE"
COLLECTION_DESC = (
    "Ten generative artworks built from Persian girih geometry - star rosettes, "
    "interlaced decagrams and khatam lattice - rendered as neon-lit digital tiles. "
    "Every line is computed from a seed; nothing is drawn by hand."
)

PALETTES = [
    dict(key="Midnight Gold",  bg1=(6, 10, 26),   bg2=(22, 30, 66),   line=(214, 176, 60),  line2=(255, 226, 150), glow=(255, 190, 70)),
    dict(key="Neon Bazaar",    bg1=(5, 4, 10),    bg2=(26, 6, 38),    line=(0, 226, 255),   line2=(255, 70, 205),  glow=(0, 220, 255)),
    dict(key="Emerald Prayer", bg1=(2, 15, 12),   bg2=(7, 44, 32),    line=(196, 164, 78),  line2=(120, 255, 205), glow=(70, 255, 190)),
    dict(key="Solar Tile",     bg1=(17, 8, 3),    bg2=(56, 24, 5),    line=(255, 168, 44),  line2=(255, 238, 170), glow=(255, 150, 20)),
    dict(key="Ice Mosque",     bg1=(4, 8, 24),    bg2=(12, 34, 68),   line=(174, 216, 255), line2=(255, 255, 255), glow=(130, 196, 255)),
]

PATTERNS = [
    "8-Point Star Rosette",
    "Interlaced 10-Star",
    "Hexagonal Lattice",
    "12-Point Khatam",
    "Radial Burst",
]
DENSITIES = ["Sparse", "Balanced", "Dense"]
AURAS = ["Bloom", "Grain", "Scanline"]


# ---------------------------------------------------------------- helpers
def star_pts(cx, cy, R, r, n, rot=0.0):
    """2n-gon star polygon."""
    pts = []
    for i in range(2 * n):
        a = rot + i * math.pi / n
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def poly_pts(cx, cy, R, n, rot=0.0):
    return [(cx + R * math.cos(rot + i * 2 * math.pi / n),
             cy + R * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def line(d, p, q, color, w):
    d.line([p, q], fill=color, width=w)


def polyline(d, pts, color, w, close=False):
    seq = list(pts) + ([pts[0]] if close else [])
    for i in range(len(seq) - 1):
        d.line([seq[i], seq[i + 1]], fill=color, width=w)


def font(size):
    for path in (
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ---------------------------------------------------------------- geometry
def draw_rosette8(d, c, dens, colA, colB):
    """Classic 8-point star rosette (two interlaced squares + octagram)."""
    S = {"Sparse": 1, "Balanced": 2, "Dense": 3}[dens]
    R = 350
    # two interlaced squares
    polyline(d, poly_pts(c, c, R, 4, 0), colA, 5, close=True)
    polyline(d, poly_pts(c, c, R, 4, math.pi / 4), colA, 5, close=True)
    # octagram outline
    polyline(d, star_pts(c, c, R * 0.98, R * 0.541, 8, math.pi / 8), colB, 4, close=True)
    # concentric rings
    for k, rr in enumerate((R * 1.09, R * 0.72, R * 0.40)):
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=colA if k % 2 == 0 else colB, width=3)
    # spokes
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        line(d, (c, c), (c + R * 1.09 * math.cos(a), c + R * 1.09 * math.sin(a)), colA, 3)
    # satellite stars
    count = {1: 4, 2: 8, 3: 12}[S]
    for i in range(count):
        a = i * 2 * math.pi / count + math.pi / count
        sx, sy = c + 358 * math.cos(a), c + 358 * math.sin(a)
        polyline(d, star_pts(sx, sy, 54, 27, 8, a), colB, 3, close=True)


def draw_decagram(d, c, dens, colA, colB):
    """Interlaced 10-point star."""
    S = {"Sparse": 1, "Balanced": 2, "Dense": 3}[dens]
    R = 400
    vs = poly_pts(c, c, R, 10, -math.pi / 2)
    n = len(vs)
    for k in (3, 4)[: S]:
        for i in range(n):
            line(d, vs[i], vs[(i + k) % n], colA if k == 3 else colB, 4)
    for rr, col, w in ((R * 1.06, colA, 4), (R * 0.66, colB, 3), (R * 0.34, colA, 3)):
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=col, width=w)
    inner = poly_pts(c, c, R * 0.66, 10, -math.pi / 2)
    for i in range(10):
        line(d, vs[i], inner[(i + 2) % 10], colB, 3)
    if S >= 2:
        cpts = poly_pts(c, c, R * 0.34, 5, -math.pi / 2)
        polyline(d, cpts, colB, 3, close=True)
        polyline(d, star_pts(c, c, R * 0.34, R * 0.13, 5, -math.pi / 2), colA, 3, close=True)


def draw_hexlattice(d, c, dens, colA, colB):
    """Hexagonal lattice with a dominant central hex cluster."""
    S = {"Sparse": 1, "Balanced": 2, "Dense": 3}[dens]
    R = 150
    dx = R * math.sqrt(3)
    dy = R * 1.5
    rings = {1: 1, 2: 2, 3: 3}[S]
    # grid of hexagons
    for row in range(-4, 5):
        for col in range(-4, 5):
            cx = c + col * dx + (dx / 2 if row % 2 else 0)
            cy = c + row * dy
            dist = math.hypot(cx - c, cy - c)
            if dist > 780:
                continue
            pts = poly_pts(cx, cy, R, 6, math.pi / 6)
            polyline(d, pts, colA if (row + col) % 2 == 0 else colB, 3, close=True)
            if dist < 330:
                polyline(d, poly_pts(cx, cy, R * 0.55, 6, math.pi / 6), colB, 2, close=True)
    # central emphasis
    for k in range(rings + 1):
        rr = 300 + k * 96
        polyline(d, poly_pts(c, c, rr, 6, math.pi / 6), colB if k % 2 else colA, 4, close=True)
    polyline(d, star_pts(c, c, 300, 150, 6, math.pi / 6), colA, 4, close=True)


def draw_khatam(d, c, dens, colA, colB):
    """12-point khatam star (layered polygons)."""
    S = {"Sparse": 1, "Balanced": 2, "Dense": 3}[dens]
    R = 410
    for k, rr in enumerate((R, R * 0.80, R * 0.60, R * 0.40, R * 0.20)):
        n = 12
        polyline(d, poly_pts(c, c, rr, n, k * math.pi / 12), colA if k % 2 == 0 else colB, 4, close=True)
    polyline(d, star_pts(c, c, R, R * 0.5, 12, 0), colB, 4, close=True)
    polyline(d, star_pts(c, c, R * 0.80, R * 0.40, 12, math.pi / 12), colA, 3, close=True)
    if S >= 2:
        polyline(d, star_pts(c, c, R * 0.5, R * 0.25, 6, 0), colB, 3, close=True)
    spokes = 12 if S == 1 else 24
    for i in range(spokes):
        a = i * 2 * math.pi / spokes
        line(d, (c + R * 0.20 * math.cos(a), c + R * 0.20 * math.sin(a)),
             (c + R * 1.06 * math.cos(a), c + R * 1.06 * math.sin(a)), colA, 2)
    if S == 3:
        for i in range(12):
            a = i * math.pi / 6 + math.pi / 12
            sx, sy = c + 366 * math.cos(a), c + 366 * math.sin(a)
            polyline(d, star_pts(sx, sy, 42, 20, 6, a), colB, 3, close=True)


def draw_burst(d, c, dens, colA, colB):
    """Radial burst with concentric polygons."""
    S = {"Sparse": 1, "Balanced": 2, "Dense": 3}[dens]
    rays = {1: 24, 2: 36, 3: 48}[S]
    for i in range(rays):
        a = i * 2 * math.pi / rays
        r0, r1 = (70, 420) if i % 2 == 0 else (110, 372)
        line(d, (c + r0 * math.cos(a), c + r0 * math.sin(a)),
             (c + r1 * math.cos(a), c + r1 * math.sin(a)),
             colA if i % 2 == 0 else colB, 3)
    for k, rr in enumerate((420, 372, 320, 244, 160, 78)):
        d.ellipse([c - rr, c - rr, c + rr, c + rr],
                  outline=colA if k % 2 == 0 else colB, width=4 if k < 3 else 3)
    for k, n in enumerate((12, 6, 3)):
        rr = 340 - k * 90
        polyline(d, poly_pts(c, c, rr, n, k * math.pi / n), colB, 3, close=True)
    polyline(d, star_pts(c, c, 160, 76, 6, 0), colA, 5, close=True)
    polyline(d, star_pts(c, c, 78, 34, 4, math.pi / 4), colB, 4, close=True)


PATTERN_FN = {
    PATTERNS[0]: draw_rosette8,
    PATTERNS[1]: draw_decagram,
    PATTERNS[2]: draw_hexlattice,
    PATTERNS[3]: draw_khatam,
    PATTERNS[4]: draw_burst,
}


def draw_frame(d, colA, colB):
    """Double border with corner star motifs."""
    for inset, w, col in ((46, 5, colA), (64, 3, colB), (74, 2, colA)):
        d.rectangle([inset, inset, SIZE - inset, SIZE - inset], outline=col, width=w)
    for (cx, cy) in ((110, 110), (SIZE - 110, 110), (110, SIZE - 110), (SIZE - 110, SIZE - 110)):
        polyline(d, star_pts(cx, cy, 40, 18, 4, math.pi / 4), colB, 3, close=True)
        polyline(d, poly_pts(cx, cy, 62, 4, 0), colA, 2, close=True)


# ---------------------------------------------------------------- background
def make_background(pal, c_off):
    h, w = SIZE, SIZE
    y = np.linspace(0, 1, h)[:, None]
    g = y[..., None]
    bg1 = np.array(pal["bg1"], float)[None, None, :]
    bg2 = np.array(pal["bg2"], float)[None, None, :]
    img = bg1 * (1 - g) + bg2 * g
    img = np.repeat(img, w, axis=1)

    # radial glow
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - c_off[0]) ** 2 + (yy - c_off[1]) ** 2) / (SIZE * 0.72)
    falloff = np.clip(1 - dist, 0, 1) ** 2.2
    glow = np.array(pal["glow"], float)[None, None, :]
    img = img + glow * falloff[..., None] * 0.30
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def add_vignette(img, strength=0.55):
    arr = np.asarray(img, float)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    d = np.sqrt((xx - SIZE / 2) ** 2 + (yy - SIZE / 2) ** 2) / (SIZE * 0.75)
    v = 1 - np.clip(d - 0.35, 0, 1) * strength
    arr *= v[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def add_grain(img, rng, amount=7):
    arr = np.asarray(img, float)
    nprng = np.random.default_rng(rng.randrange(1 << 30))
    noise = nprng.normal(0, amount, (SIZE, SIZE, 1))
    arr = arr + noise
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def add_scanlines(img):
    arr = np.asarray(img, float).copy()
    arr[::3] *= 0.86
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------- token
def build_token(tid, rng):
    pal = PALETTES[rng.randrange(len(PALETTES))]
    pattern = PATTERNS[rng.randrange(len(PATTERNS))]
    density = DENSITIES[rng.randrange(len(DENSITIES))]
    aura = AURAS[rng.randrange(len(AURAS))]
    accent = rng.choice(["Auric", "Pulse", "Frost", "Signal"])
    finish = rng.choice(["Matte", "Lacquer", "Metallic"])

    c_off = (SIZE / 2 + rng.uniform(-40, 40), SIZE / 2 + rng.uniform(-40, 40))
    base = make_background(pal, c_off)

    # --- geometry on supersampled RGBA canvas
    layer = Image.new("RGBA", (HI, HI), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    scale = lambda v: v * SS

    colA = pal["line"] + (255,)
    colB = pal["line2"] + (255,)

    class Proxy:  # draw in SIZE space, scale into HI space
        def __init__(self, dr):
            self.dr = dr

        def line(self, xy, fill, width):
            if xy and isinstance(xy[0], (tuple, list)):
                pts = [scale(v) for pt in xy for v in pt]
            else:
                pts = [scale(xy[0]), scale(xy[1]), scale(xy[2]), scale(xy[3])]
            self.dr.line(pts, fill=fill, width=max(1, width * SS))

        def ellipse(self, box, outline, width):
            self.dr.ellipse([scale(box[0]), scale(box[1]), scale(box[2]), scale(box[3])],
                            outline=outline, width=max(1, width * SS))

        def rectangle(self, box, outline, width):
            self.dr.rectangle([scale(box[0]), scale(box[1]), scale(box[2]), scale(box[3])],
                              outline=outline, width=max(1, width * SS))

    pd = Proxy(d)
    c = SIZE / 2
    PATTERN_FN[pattern](pd, c, density, colA, colB)

    # pattern geometry is clipped inside the frame so nothing bleeds past the border
    frame_layer = Image.new("RGBA", (HI, HI), (0, 0, 0, 0))
    draw_frame(Proxy(ImageDraw.Draw(frame_layer)), colA, colB)

    small = layer.resize((SIZE, SIZE), Image.LANCZOS)
    clip = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(clip).rectangle([80, 80, SIZE - 80, SIZE - 80], fill=255)
    geo_alpha = Image.composite(small.split()[3], Image.new("L", (SIZE, SIZE), 0), clip)

    frame_small = frame_layer.resize((SIZE, SIZE), Image.LANCZOS).split()[3]
    alpha = ImageChops.lighter(geo_alpha, frame_small)

    # --- glow
    glow_mask = alpha.filter(ImageFilter.GaussianBlur(11))
    glow_mask = glow_mask.point(lambda v: int(v * 0.85))
    glow_layer = Image.new("RGB", (SIZE, SIZE), pal["glow"])
    composed = Image.composite(Image.blend(base, glow_layer, 0.45), base, glow_mask)

    # softer second bloom
    soft = alpha.filter(ImageFilter.GaussianBlur(34)).point(lambda v: int(v * 0.35))
    composed = Image.composite(Image.blend(composed, glow_layer, 0.30), composed, soft)

    # --- sharp lines
    line_rgb = Image.new("RGB", (SIZE, SIZE), pal["line"])
    composed.paste(line_rgb, (0, 0), alpha)

    # --- finish / overlays
    composed = add_vignette(composed)
    if aura == "Grain":
        composed = add_grain(composed, rng, 8)
    elif aura == "Scanline":
        composed = add_scanlines(composed)
    else:
        composed = add_grain(composed, rng, 4)

    # --- labels
    dr = ImageDraw.Draw(composed)
    f1, f2 = font(26), font(18)
    label = f"{COLLECTION_NAME}  #{tid:03d}"
    dr.text((86, SIZE - 66), label, font=f1, fill=pal["line2"])
    dr.text((86, SIZE - 36), pal["key"].upper() + "  /  " + pattern.upper(),
            font=f2, fill=tuple(int(v * 0.75) for v in pal["line"]))
    dr.text((SIZE - 150, 34), "GIRIH", font=f2, fill=tuple(int(v * 0.6) for v in pal["line2"]))

    traits = [
        ("Pattern", pattern),
        ("Palette", pal["key"]),
        ("Density", density),
        ("Aura", aura),
        ("Accent", accent),
        ("Finish", finish),
    ]
    return composed, traits


# ---------------------------------------------------------------- main
def main():
    os.makedirs("output", exist_ok=True)
    os.makedirs("metadata", exist_ok=True)

    census = {}
    for tid in range(1, TOTAL + 1):
        rng = random.Random(SEED * 1000 + tid)
        img, traits = build_token(tid, rng)
        img.save(f"output/{tid}.png", "PNG", optimize=True)

        meta = {
            "name": f"{COLLECTION_NAME} #{tid:03d}",
            "description": COLLECTION_DESC,
            "image": f"ipfs://REPLACE_CID/{tid}.png",
            "external_url": "https://fyosamu.github.io/",
            "attributes": [{"trait_type": t, "value": v} for t, v in traits],
        }
        with open(f"metadata/{tid}.json", "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2, ensure_ascii=False)

        for t, v in traits:
            census.setdefault(t, {}).setdefault(v, []).append(tid)
        print(f"  #{tid:03d}  {traits[0][1]:<24} {traits[1][1]:<16} {traits[3][1]}")

    with open("collection.json", "w", encoding="utf-8") as fh:
        json.dump({
            "name": COLLECTION_NAME,
            "description": COLLECTION_DESC,
            "total": TOTAL,
            "seed": SEED,
            "traits": {t: {v: {"count": len(ids), "tokens": ids}
                           for v, ids in d.items()}
                       for t, d in census.items()},
        }, fh, indent=2, ensure_ascii=False)
    print("\ndone: 10 artworks + 10 metadata files + collection.json")


if __name__ == "__main__":
    main()
