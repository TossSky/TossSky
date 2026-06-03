#!/usr/bin/env python3
"""Generate assets/banner.svg — an animated scarlet vortex/spiral for the
profile hero. Echoes the etorn.ee 'tornado' wireframe (stacked, twisted
elliptical rings + helix struts) but recoloured deep-black + scarlet."""
import math, os

# ---- palette ----
BLACK   = "#000000"
SCARLET = "#FF1500"   # алый — pure scarlet, no blue (kills the pink cast)
HI      = "#FF5340"   # bright tip (light scarlet, warm not pink)
EMBER   = "#7A0A00"   # deep ember red
INK     = "#FAFAFA"
GREY    = "#8A8A8E"

W, H = 1200, 360
# vortex axis (right side, like the landing)
CX = 880.0
TOP, BOT = 28.0, 332.0
N_RINGS = 17
N_STRANDS = 7
RX_MAX = 230.0
SQUASH = 0.20         # ellipse vertical squash (perspective)
TWIST = 2.35 * math.pi  # total phase rotation top->bottom => coil

def funnel(t):
    # wide at top, pinched ~70%, tiny flare at the very bottom (vortex throat)
    return RX_MAX * (0.18 + 0.82 * (1.0 - t) ** 1.35 + 0.06 * t ** 3)

def ring_geom(i):
    t = i / (N_RINGS - 1)
    cy = TOP + (BOT - TOP) * t
    rx = funnel(t)
    ry = max(2.0, rx * SQUASH)
    phi = t * TWIST
    return t, cy, rx, ry, phi

def pt(cx, cy, rx, ry, ang):
    return cx + rx * math.cos(ang), cy + ry * math.sin(ang)

out = []
out.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none" '
    f'role="img" aria-label="TossSky — a scarlet wireframe vortex turning over a black field; '
    f'a horizontal scan line descends through it.">'
)

# ---- defs ----
out.append('<defs>')
out.append(
    '<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0"/>'
    f'<stop offset="50%" stop-color="{HI}" stop-opacity="1"/>'
    f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></linearGradient>'
)
out.append(
    '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
    f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0.42"/>'
    f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></radialGradient>'
)
out.append(
    '<linearGradient id="strand" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0%" stop-color="{HI}"/>'
    f'<stop offset="55%" stop-color="{SCARLET}"/>'
    f'<stop offset="100%" stop-color="{EMBER}"/></linearGradient>'
)
out.append(
    '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
    f'<path d="M40 0 H0 V40" fill="none" stroke="#FFFFFF" stroke-opacity="0.04" stroke-width="1"/></pattern>'
)
out.append(
    '<linearGradient id="vignette" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0%" stop-color="{BLACK}" stop-opacity="0.96"/>'
    f'<stop offset="50%" stop-color="{BLACK}" stop-opacity="0.0"/></linearGradient>'
)
out.append('</defs>')

# ---- ground ----
out.append(f'<rect width="{W}" height="{H}" fill="{BLACK}"/>')
out.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

# ---- vortex group (gentle continuous spin via skew oscillation) ----
out.append(f'<g transform="translate({CX} 0)">')
out.append(
    '<animateTransform attributeName="transform" type="rotate" additive="sum" '
    f'values="-1.6 0 {(TOP+BOT)/2}; 1.6 0 {(TOP+BOT)/2}; -1.6 0 {(TOP+BOT)/2}" '
    'dur="11s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
    'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>'
)
out.append(f'<g transform="translate({-CX} 0)">')

# ambient glow behind the throat
out.append(f'<circle cx="{CX}" cy="{TOP+(BOT-TOP)*0.62:.0f}" r="150" fill="url(#glow)">'
           '<animate attributeName="opacity" values="0.55;1;0.55" dur="6s" repeatCount="indefinite"/></circle>')

# rings
for i in range(N_RINGS):
    t, cy, rx, ry, phi = ring_geom(i)
    op = 0.10 + 0.30 * (1.0 - t)          # top rings brighter
    sw = 1.0 + 0.6 * (1.0 - t)
    out.append(
        f'<ellipse cx="{CX:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
        f'fill="none" stroke="#FFFFFF" stroke-opacity="{op:.3f}" stroke-width="{sw:.2f}">'
        f'<animate attributeName="stroke-opacity" values="{op:.3f};{min(op+0.12,0.6):.3f};{op:.3f}" '
        f'dur="6s" begin="{t*1.2:.2f}s" repeatCount="indefinite"/></ellipse>'
    )

# helix strands (the 'spiral' read): connect the same angular seam across rings
for k in range(N_STRANDS):
    base = k * 2 * math.pi / N_STRANDS
    pts = []
    for i in range(N_RINGS):
        t, cy, rx, ry, phi = ring_geom(i)
        x, y = pt(CX, cy, rx, ry, base + phi)
        pts.append(f'{x:.1f},{y:.1f}')
    scarlet_strand = (k == 0)   # one strand glows scarlet — the live coil
    if scarlet_strand:
        out.append(
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="url(#strand)" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>'
        )
    else:
        out.append(
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="#FFFFFF" '
            f'stroke-opacity="0.10" stroke-width="1" stroke-linejoin="round">'
            f'<animate attributeName="stroke-opacity" values="0.05;0.16;0.05" dur="7s" '
            f'begin="{k*0.5:.2f}s" repeatCount="indefinite"/></polyline>'
        )

# scarlet finding markers riding the scarlet strand
for (i, dur, beg) in [(4, 4.5, 0.0), (9, 4.5, 1.4), (13, 4.5, 2.8)]:
    t, cy, rx, ry, phi = ring_geom(i)
    x, y = pt(CX, cy, rx, ry, 0 + phi)
    out.append(
        f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" rx="1.5" '
        f'transform="rotate(45 {x:.1f} {y:.1f})" fill="{SCARLET}">'
        f'<animate attributeName="opacity" values="0;1;0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></rect>'
    )

out.append('</g>')  # un-translate
out.append('</g>')  # vortex spin group

# descending scan beam across the vortex region
out.append(
    f'<g><rect x="{CX-RX_MAX-20:.0f}" y="-4" width="{2*(RX_MAX+20):.0f}" height="40" fill="url(#glow)" opacity="0.5"/>'
    f'<rect x="{CX-RX_MAX-20:.0f}" y="14" width="{2*(RX_MAX+20):.0f}" height="2" fill="url(#beam)"/>'
    f'<animateTransform attributeName="transform" type="translate" values="0 {TOP-10:.0f}; 0 {BOT-10:.0f}; 0 {TOP-10:.0f}" '
    f'dur="9s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
    f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></g>'
)

# left vignette so wordmark stays legible over the vortex
out.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

# frame hairlines
out.append(f'<line x1="0" y1="1" x2="{W}" y2="1" stroke="#FFFFFF" stroke-opacity="0.10"/>')
out.append(f'<line x1="0" y1="{H-1}" x2="{W}" y2="{H-1}" stroke="#FFFFFF" stroke-opacity="0.10"/>')

# ---- wordmark + manifesto (left) ----
mono = "ui-monospace, 'SF Mono', 'Cascadia Code', 'JetBrains Mono', monospace"
sans = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

out.append(f'<circle cx="68" cy="103" r="5" fill="{SCARLET}">'
           '<animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite"/></circle>')
out.append(f'<text x="86" y="108" font-family="{mono}" font-size="14" letter-spacing="6" '
           f'fill="{GREY}">SECURITY · BLOCKCHAIN · SYSTEMS</text>')
out.append(f'<text x="62" y="196" font-family="{sans}" font-size="92" font-weight="800" '
           f'letter-spacing="-3.5" fill="{INK}">TossSky</text>')
out.append(f'<text x="66" y="240" font-family="{mono}" font-size="16" letter-spacing="0.4" '
           f'fill="{SCARLET}">scan first. trust later.</text>')

out.append('</svg>')

svg = "\n".join(out)
path = os.path.join(os.path.dirname(__file__), "banner.svg")
with open(path, "w", encoding="utf-8") as f:
    f.write(svg + "\n")
print(f"wrote {path} ({len(svg)} bytes, {N_RINGS} rings, {N_STRANDS} strands)")
