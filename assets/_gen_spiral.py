#!/usr/bin/env python3
"""Generate assets/banner.svg — a centered, refined spiral hero.

A tilted spiral-galaxy: faint concentric rings for depth + several thin
Archimedean arms winding into the core. Mostly white/grey hairlines, one
restrained scarlet arm, a small scarlet core. The arm group rotates slowly.
Deep black field, name set underneath. No bold squiggle, no glow blob."""
import math, os

BLACK   = "#000000"
SCARLET = "#FF1500"
INK     = "#FAFAFA"
GREY    = "#8A8A8E"

W, H = 1200, 560
CX, CY = 600.0, 232.0
RMAX = 208.0
RMIN = 9.0
SQUASH = 0.46          # disk tilt
N_RINGS = 7
N_ARMS = 6             # one scarlet, rest faint white
TURNS = 2.45
STEPS = 220

def arm_points(arm_offset):
    pts = []
    theta_max = TURNS * 2 * math.pi
    for s in range(STEPS + 1):
        f = s / STEPS                       # 0 outer -> 1 core
        theta = theta_max * f
        r = RMIN + (RMAX - RMIN) * (1 - f) ** 1.06
        a = theta + arm_offset
        x = CX + r * math.cos(a)
        y = CY + r * SQUASH * math.sin(a)
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)

out = []
out.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none" '
    f'role="img" aria-label="TossSky — a thin scarlet-and-white spiral turning slowly on a black field.">'
)

out.append('<defs>')
out.append(
    '<radialGradient id="core" cx="0.5" cy="0.5" r="0.5">'
    f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0.55"/>'
    f'<stop offset="45%" stop-color="{SCARLET}" stop-opacity="0.14"/>'
    f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></radialGradient>'
)
out.append(
    '<radialGradient id="vign" cx="0.5" cy="0.42" r="0.62">'
    f'<stop offset="0%" stop-color="{BLACK}" stop-opacity="0"/>'
    f'<stop offset="78%" stop-color="{BLACK}" stop-opacity="0"/>'
    f'<stop offset="100%" stop-color="{BLACK}" stop-opacity="0.9"/></radialGradient>'
)
out.append('</defs>')

out.append(f'<rect width="{W}" height="{H}" fill="{BLACK}"/>')

# faint concentric depth rings (static, calm)
for i in range(N_RINGS):
    f = i / (N_RINGS - 1)
    rx = RMIN + (RMAX - RMIN) * (1 - f)
    ry = max(2.0, rx * SQUASH)
    op = 0.05 + 0.10 * f                      # brighter toward core
    out.append(
        f'<ellipse cx="{CX:.1f}" cy="{CY:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
        f'fill="none" stroke="#FFFFFF" stroke-opacity="{op:.3f}" stroke-width="0.8"/>'
    )

# core glow (subtle, gentle breathing)
out.append(
    f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="70" fill="url(#core)">'
    f'<animate attributeName="opacity" values="0.7;1;0.7" dur="6s" repeatCount="indefinite"/></circle>'
)

# rotating arm group
out.append('<g>')
out.append(
    f'<animateTransform attributeName="transform" type="rotate" '
    f'from="0 {CX:.0f} {CY:.0f}" to="360 {CX:.0f} {CY:.0f}" dur="30s" repeatCount="indefinite"/>'
)
for k in range(N_ARMS):
    off = k * 2 * math.pi / N_ARMS
    if k == 0:
        out.append(
            f'<polyline points="{arm_points(off)}" fill="none" stroke="{SCARLET}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>'
        )
    else:
        op = 0.16 if k % 2 else 0.10
        out.append(
            f'<polyline points="{arm_points(off)}" fill="none" stroke="#FFFFFF" '
            f'stroke-opacity="{op:.2f}" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round"/>'
        )
# bright scarlet core dot rides with the arms
out.append(f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="3" fill="{SCARLET}"/>')
out.append('</g>')

# vignette to focus the center
out.append(f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')

# wordmark + eyebrow, centered beneath the spiral
sans = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
mono = "ui-monospace, 'SF Mono', 'Cascadia Code', 'JetBrains Mono', monospace"
out.append(
    f'<text x="{CX:.0f}" y="476" text-anchor="middle" font-family="{sans}" '
    f'font-size="78" font-weight="800" letter-spacing="-3" fill="{INK}">TossSky</text>'
)
out.append(
    f'<text x="{CX:.0f}" y="512" text-anchor="middle" font-family="{mono}" '
    f'font-size="13" letter-spacing="7" fill="{GREY}">SECURITY · BLOCKCHAIN · SYSTEMS</text>'
)

out.append('</svg>')

svg = "\n".join(out)
path = os.path.join(os.path.dirname(__file__), "banner.svg")
with open(path, "w", encoding="utf-8") as f:
    f.write(svg + "\n")
print(f"wrote {path} ({len(svg)} bytes, {N_ARMS} arms, {N_RINGS} rings)")
