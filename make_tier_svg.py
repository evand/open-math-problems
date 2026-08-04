#!/usr/bin/env python3
"""Generate tier-list.svg — a tier-list graphic of open problems in mathematics."""

TIERS = [
    ("S", "#ff7f7e", "Load-bearing pillars",
     ["Riemann Hypothesis", "P vs NP", "Langlands program"]),
    ("A", "#ffbf7f", "Field-defining",
     ["Birch–Swinnerton-Dyer", "Hodge", "Tate + Standard Conjectures", "Navier–Stokes regularity",
      "Yang–Mills mass gap", "abc", "Prime k-tuples (twin primes)", "Smooth 4D Poincaré",
      "Schanuel", "Bombieri–Lang", "One-way functions", "Fontaine–Mazur + Bloch–Kato",
      "Borel & Novikov", "Hilbert's 16th", "Cosmic censorship"]),
    ("B", "#ffdf80", "Major within their fields",
     ["Goldbach", "Lindelöf", "Zilber–Pink", "Inverse Galois", "Section conjecture",
      "Slice-ribbon", "L-space conjecture", "4D Schoenflies", "Mirror symmetry (SYZ/HMS)",
      "Restriction", "Invariant subspace", "Soliton resolution", "Kaplansky", "Thompson's F amenable?",
      "Hadwiger", "Erdős APs", "Sunflower", "Hadwiger–Nelson", "Inscribed square",
      "Sphere packing (general d)", "Erdős–Hajnal", "Continuum problem", "Unique Games",
      "ω = 2?", "VP vs VNP", "P = BPP", "KLS", "3D Ising", "KPZ",
      "Free group factors ('26 +)", "MLC ('26 +)", "+44 more ↓"]),
    ("C", "#7fff7f", "Famous but narrow",
     ["Odd perfect numbers", "∞ Mersenne primes", "Normality of π", "γ irrational?",
      "R(5,5)", "Frankl union-closed", "Beal", "Legendre", "Sendov", "Singmaster", "+4 more ↓"]),
    ("☠", "#b78aff", "Cursed: fame ≫ tractability",
     ["Collatz", "3×3 magic square of squares", "Perfect cuboid", "Brocard"]),
    ("🪦", "#9a9a9a", "Recently fell",
     ["Astra batch ×10 ('26 🤖)", "Jacobian conjecture ('26 ⭐)", "3D Kakeya ('25)", "Slicing problem ('25)", "Kervaire 126 ('24)",
      "Moving sofa ('24)", "McKay ('24)", "PFR ('23)", "Aperiodic monotile ('23)", "+more ↓"]),
]

W = 1280
LABEL_W = 150
PAD = 10
CHIP_H = 30
CHIP_GAP = 8
FONT = 13
TITLE_H = 74

def chip_w(text):
    # crude width estimate for a 13px sans font
    wide = sum(1 for c in text if c in "WMmw@⭐×∞")
    return int(len(text) * 6.9 + wide * 3 + 20)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

rows = []
y = TITLE_H
for name, color, sub, chips in TIERS:
    # lay out chips with wrapping
    lines, cur, curw = [], [], 0
    avail = W - LABEL_W - 2 * PAD
    for c in chips:
        w = chip_w(c)
        if curw + w + (CHIP_GAP if cur else 0) > avail and cur:
            lines.append(cur); cur, curw = [], 0
        cur.append((c, w)); curw += w + (CHIP_GAP if len(cur) > 1 else 0)
    if cur:
        lines.append(cur)
    h = max(len(lines) * (CHIP_H + CHIP_GAP) + PAD * 2 - CHIP_GAP + 2, 64)
    rows.append((name, color, sub, lines, y, h))
    y += h + 4

H = y + 34
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#131316"/>')
svg.append(f'<text x="{PAD+2}" y="30" fill="#f4f4f5" font-size="22" font-weight="bold">'
           'Open Problems in Mathematics — a tier list</text>')
svg.append(f'<text x="{PAD+2}" y="54" fill="#a1a1aa" font-size="14">ranked by structural centrality '
           '&#215; how much a proof would transform mathematics &#8212; not fame, not difficulty &#183; '
           'July 2026 &#183; full annotated list below</text>')

for name, color, sub, lines, ry, rh in rows:
    svg.append(f'<rect x="0" y="{ry}" width="{LABEL_W}" height="{rh}" fill="{color}"/>')
    svg.append(f'<rect x="{LABEL_W+2}" y="{ry}" width="{W-LABEL_W-2}" height="{rh}" fill="#1e1e22"/>')
    cy = ry + rh / 2
    svg.append(f'<text x="{LABEL_W/2}" y="{cy-2}" fill="#18181b" font-size="30" font-weight="bold" '
               f'text-anchor="middle" dominant-baseline="middle">{esc(name)}</text>')
    svg.append(f'<text x="{LABEL_W/2}" y="{cy+20}" fill="#18181b" font-size="10.5" font-weight="bold" '
               f'text-anchor="middle" dominant-baseline="middle">{esc(sub)}</text>')
    yy = ry + PAD
    for line in lines:
        xx = LABEL_W + 2 + PAD
        for text, w in line:
            svg.append(f'<rect x="{xx}" y="{yy}" width="{w}" height="{CHIP_H}" rx="6" fill="#2b2b31" '
                       f'stroke="#3f3f46" stroke-width="1"/>')
            svg.append(f'<text x="{xx+w/2}" y="{yy+CHIP_H/2+1}" fill="#e4e4e7" font-size="{FONT}" '
                       f'text-anchor="middle" dominant-baseline="middle">{esc(text)}</text>')
            xx += w + CHIP_GAP
        yy += CHIP_H + CHIP_GAP

svg.append(f'<text x="{PAD+2}" y="{H-12}" fill="#71717a" font-size="12">github.com/evand/open-math-problems '
           '&#183; inspired by the Jacobian conjecture counterexample (Alp&#246;ge + Claude, July 2026)</text>')
svg.append('</svg>')

with open("tier-list.svg", "w") as f:
    f.write("\n".join(svg))
print("wrote tier-list.svg", W, "x", H)
