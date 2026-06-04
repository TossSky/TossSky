#!/usr/bin/env python3
"""Generate one composed canvas for the profile: cover.svg.

Not a stack of boxes — a single tall composition. Deep black, scarlet
accent, a recurring spiral / signal motif, lots of negative space.
Content is abstract; the only concrete bit is a two-line work list."""
import math, os

BLACK   = "#000000"
SCARLET = "#FF1500"
BRIGHT  = "#FF5340"
INK     = "#FAFAFA"
INK2    = "#C8C8CC"
INK3    = "#8A8A8E"
INK4    = "#56565B"
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', 'JetBrains Mono', monospace"
HERE = os.path.dirname(__file__)

W, H = 1200, 1480

def spiral(cx, cy, rmax, arms=6, turns=2.45, squash=0.46, steps=200, dur=30):
    rmin = rmax * 0.045
    def arm(off):
        pts, tmax = [], turns * 2 * math.pi
        for s in range(steps + 1):
            f = s / steps
            r = rmin + (rmax - rmin) * (1 - f) ** 1.06
            a = tmax * f + off
            pts.append(f"{cx + r*math.cos(a):.1f},{cy + r*squash*math.sin(a):.1f}")
        return " ".join(pts)
    o = [f'<circle cx="{cx}" cy="{cy}" r="{rmax*0.34:.0f}" fill="url(#core)">'
         f'<animate attributeName="opacity" values="0.7;1;0.7" dur="6s" repeatCount="indefinite"/></circle>']
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" '
             f'from="0 {cx:.0f} {cy:.0f}" to="360 {cx:.0f} {cy:.0f}" dur="{dur}s" repeatCount="indefinite"/>')
    for k in range(arms):
        off = k * 2 * math.pi / arms
        if k == 0:
            o.append(f'<polyline points="{arm(off)}" fill="none" stroke="{SCARLET}" stroke-width="1.5" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>')
        else:
            op = 0.15 if k % 2 else 0.09
            o.append(f'<polyline points="{arm(off)}" fill="none" stroke="#FFFFFF" stroke-opacity="{op:.2f}" '
                     f'stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{SCARLET}"/></g>')
    return "\n".join(o)

def sine(y0, amp, freq, phase, x0, x1, stroke, op, sw, steps=240):
    pts = []
    for s in range(steps + 1):
        x = x0 + (x1 - x0) * s / steps
        t = (x - x0) / (x1 - x0)
        # taper amplitude at the ends so the curve fades into space
        env = math.sin(math.pi * t)
        yv = y0 + amp * env * math.sin(freq * 2 * math.pi * t + phase)
        pts.append(f"{x:.1f},{yv:.1f}")
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{stroke}" '
            f'stroke-opacity="{op}" stroke-width="{sw}" stroke-linecap="round"/>')

def main():
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none" '
             f'role="img" aria-label="TossSky — a scarlet spiral and abstract signal field on black.">')
    o.append('<defs>'
             f'<radialGradient id="core" cx="0.5" cy="0.5" r="0.5">'
             f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0.5"/>'
             f'<stop offset="45%" stop-color="{SCARLET}" stop-opacity="0.12"/>'
             f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="hv" cx="0.5" cy="0.18" r="0.7">'
             f'<stop offset="0%" stop-color="{BLACK}" stop-opacity="0"/>'
             f'<stop offset="72%" stop-color="{BLACK}" stop-opacity="0"/>'
             f'<stop offset="100%" stop-color="{BLACK}" stop-opacity="0.92"/></radialGradient>'
             f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0"/>'
             f'<stop offset="50%" stop-color="{BRIGHT}" stop-opacity="0.85"/>'
             f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></linearGradient>'
             f'<radialGradient id="bg2" cx="0.5" cy="0.5" r="0.5">'
             f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0.14"/>'
             f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></radialGradient></defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="{BLACK}"/>')

    # ---------- A · hero spiral ----------
    o.append(spiral(600, 250, 196))
    o.append(f'<rect y="0" width="{W}" height="560" fill="url(#hv)"/>')
    o.append(f'<text x="600" y="470" text-anchor="middle" font-family="{SANS}" font-size="76" '
             f'font-weight="800" letter-spacing="-3" fill="{INK}">TossSky</text>')
    o.append(f'<text x="600" y="506" text-anchor="middle" font-family="{MONO}" font-size="13" '
             f'letter-spacing="7" fill="{INK3}">SECURITY · BLOCKCHAIN · SYSTEMS</text>')

    # ---------- B · abstract signal field ----------
    fy = 760
    o.append(f'<text x="80" y="650" font-family="{MONO}" font-size="11" letter-spacing="6" fill="{INK4}">FIELD</text>')
    # faint vertical hairline grid, varying heights
    for i in range(49):
        x = 80 + i * (1040/48)
        hh = 26 + 70 * abs(math.sin(i*0.6))*abs(math.cos(i*0.27))
        o.append(f'<line x1="{x:.1f}" y1="{fy-hh:.1f}" x2="{x:.1f}" y2="{fy+hh:.1f}" '
                 f'stroke="#FFFFFF" stroke-opacity="0.05" stroke-width="1"/>')
    # layered sine curves, one scarlet
    o.append(sine(fy, 86, 2.1, 0.0, 80, 1120, "#FFFFFF", "0.10", 1.0))
    o.append(sine(fy, 64, 3.3, 1.7, 80, 1120, "#FFFFFF", "0.08", 1.0))
    o.append(sine(fy, 104, 1.5, 0.6, 80, 1120, SCARLET, "0.85", 1.6))
    # sweeping scan beam across the field
    o.append(f'<g><rect x="-25" y="{fy-150}" width="50" height="300" fill="url(#bg2)"/>'
             f'<rect x="-0.8" y="{fy-140}" width="1.6" height="280" fill="url(#beam)"/>'
             f'<animateTransform attributeName="transform" type="translate" values="120 0; {W-120} 0; 120 0" '
             f'dur="8s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
             f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></g>')

    # ---------- C · selected work (editorial list, 2 entries) ----------
    wy = 1010
    o.append(f'<text x="80" y="{wy}" font-family="{MONO}" font-size="11" letter-spacing="6" fill="{INK3}">SELECTED WORK</text>')
    o.append(f'<line x1="80" y1="{wy+26}" x2="{W-80}" y2="{wy+26}" stroke="#FFFFFF" stroke-opacity="0.10"/>')
    rows = [("ETorn", "security · web3"), ("OmegaClaw-Core", "autonomous agents")]
    for i, (name, tag) in enumerate(rows):
        ry = wy + 26 + 64 + i * 84
        o.append(f'<rect x="80" y="{ry-44}" width="3" height="30" fill="{SCARLET}" opacity="0.9"/>')
        o.append(f'<text x="104" y="{ry-18}" font-family="{SANS}" font-size="34" font-weight="700" '
                 f'letter-spacing="-1" fill="{INK}">{name}</text>')
        o.append(f'<text x="{W-80}" y="{ry-22}" text-anchor="end" font-family="{MONO}" font-size="12" '
                 f'letter-spacing="3" fill="{INK3}">{tag.upper()}</text>')
        o.append(f'<line x1="80" y1="{ry+18}" x2="{W-80}" y2="{ry+18}" stroke="#FFFFFF" stroke-opacity="0.07"/>')

    # ---------- D · closing flourish ----------
    o.append(spiral(600, 1330, 70, arms=5, turns=2.0, dur=44))
    o.append(f'<rect y="1230" width="{W}" height="250" fill="url(#hv)" opacity="0"/>')

    o.append('</svg>')
    body = "\n".join(o)
    with open(os.path.join(HERE, "cover.svg"), "w", encoding="utf-8") as f:
        f.write(body + "\n")
    print(f"wrote cover.svg ({len(body)} bytes)")

if __name__ == "__main__":
    main()
