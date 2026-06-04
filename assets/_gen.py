#!/usr/bin/env python3
"""Generate every self-hosted SVG panel for the profile, from one design
system. Deep black + scarlet, hairline borders, mono eyebrows, a recurring
spiral / scan motif. Outputs: banner.svg, divider.svg, pipeline.svg, work.svg."""
import math, os

# ---------- design tokens ----------
BLACK   = "#000000"
SURFACE = "#0A0A0D"
SURF2   = "#101015"
SCARLET = "#FF1500"
BRIGHT  = "#FF5340"
EMBER   = "#7A0A00"
INK     = "#FAFAFA"
INK2    = "#C8C8CC"
INK3    = "#8A8A8E"
INK4    = "#56565B"
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', 'JetBrains Mono', monospace"
HERE = os.path.dirname(__file__)

def write(name, body):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(body + "\n")
    print(f"wrote {name} ({len(body)} bytes)")

def svg(w, h, label, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" '
            f'role="img" aria-label="{label}">\n' + inner + '\n</svg>')

def eyebrow(x, y, text, anchor="start", fill=INK3, size=12, ls=6):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" '
            f'font-size="{size}" letter-spacing="{ls}" fill="{fill}">{text}</text>')

# ======================================================================
# 1. HERO — centered tilted spiral galaxy
# ======================================================================
def banner():
    W, H = 1200, 560
    CX, CY = 600.0, 232.0
    RMAX, RMIN, SQUASH = 208.0, 9.0, 0.46
    N_RINGS, N_ARMS, TURNS, STEPS = 7, 6, 2.45, 220

    def arm(off):
        pts, tmax = [], TURNS * 2 * math.pi
        for s in range(STEPS + 1):
            f = s / STEPS
            r = RMIN + (RMAX - RMIN) * (1 - f) ** 1.06
            a = tmax * f + off
            pts.append(f"{CX + r*math.cos(a):.1f},{CY + r*SQUASH*math.sin(a):.1f}")
        return " ".join(pts)

    o = []
    o.append('<defs>')
    o.append(f'<radialGradient id="core" cx="0.5" cy="0.5" r="0.5">'
             f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0.55"/>'
             f'<stop offset="45%" stop-color="{SCARLET}" stop-opacity="0.14"/>'
             f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></radialGradient>')
    o.append(f'<radialGradient id="vign" cx="0.5" cy="0.42" r="0.62">'
             f'<stop offset="0%" stop-color="{BLACK}" stop-opacity="0"/>'
             f'<stop offset="78%" stop-color="{BLACK}" stop-opacity="0"/>'
             f'<stop offset="100%" stop-color="{BLACK}" stop-opacity="0.9"/></radialGradient>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="{BLACK}"/>')
    for i in range(N_RINGS):
        f = i / (N_RINGS - 1)
        rx = RMIN + (RMAX - RMIN) * (1 - f); ry = max(2.0, rx * SQUASH)
        op = 0.05 + 0.10 * f
        o.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" '
                 f'stroke="#FFFFFF" stroke-opacity="{op:.3f}" stroke-width="0.8"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="70" fill="url(#core)">'
             f'<animate attributeName="opacity" values="0.7;1;0.7" dur="6s" repeatCount="indefinite"/></circle>')
    o.append('<g>')
    o.append(f'<animateTransform attributeName="transform" type="rotate" '
             f'from="0 {CX:.0f} {CY:.0f}" to="360 {CX:.0f} {CY:.0f}" dur="30s" repeatCount="indefinite"/>')
    for k in range(N_ARMS):
        off = k * 2 * math.pi / N_ARMS
        if k == 0:
            o.append(f'<polyline points="{arm(off)}" fill="none" stroke="{SCARLET}" stroke-width="1.5" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>')
        else:
            op = 0.16 if k % 2 else 0.10
            o.append(f'<polyline points="{arm(off)}" fill="none" stroke="#FFFFFF" stroke-opacity="{op:.2f}" '
                     f'stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="{SCARLET}"/>')
    o.append('</g>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')
    o.append(f'<text x="{CX:.0f}" y="476" text-anchor="middle" font-family="{SANS}" font-size="78" '
             f'font-weight="800" letter-spacing="-3" fill="{INK}">TossSky</text>')
    o.append(eyebrow(CX, 512, "SECURITY · BLOCKCHAIN · SYSTEMS", anchor="middle", ls=7, size=13))
    write("banner.svg", svg(W, H, "TossSky — a slow scarlet spiral on black.", "\n".join(o)))

# ======================================================================
# 2. DIVIDER — fading hairline with a pulsing scarlet node
# ======================================================================
def divider():
    W, H = 1200, 48
    cy = H / 2
    o = []
    o.append('<defs>'
             f'<linearGradient id="dl" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>'
             f'<stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.18"/>'
             f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient></defs>')
    o.append(f'<line x1="60" y1="{cy}" x2="{W-60}" y2="{cy}" stroke="url(#dl)" stroke-width="1"/>')
    o.append(f'<circle cx="{W/2}" cy="{cy}" r="16" fill="{SCARLET}" opacity="0.10">'
             f'<animate attributeName="r" values="10;20;10" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.04;0.16;0.04" dur="4s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="{W/2-4}" y="{cy-4}" width="8" height="8" transform="rotate(45 {W/2} {cy})" fill="{SCARLET}"/>')
    write("divider.svg", svg(W, H, "section divider", "\n".join(o)))

# ======================================================================
# 3. PIPELINE — how a scan runs, scarlet beam sweeping a hairline flow
# ======================================================================
def pipeline():
    W, H = 1200, 300
    o = []
    o.append('<defs>'
             f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0"/>'
             f'<stop offset="50%" stop-color="{BRIGHT}" stop-opacity="0.9"/>'
             f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></linearGradient>'
             f'<radialGradient id="bg" cx="0.5" cy="0.5" r="0.5">'
             f'<stop offset="0%" stop-color="{SCARLET}" stop-opacity="0.18"/>'
             f'<stop offset="100%" stop-color="{SCARLET}" stop-opacity="0"/></radialGradient></defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="{BLACK}"/>')
    o.append(eyebrow(40, 46, "HOW A SCAN RUNS"))
    o.append(eyebrow(W-40, 46, "≈ 60s · PUBLIC", anchor="end", fill=INK4, ls=4))

    baseline = 170
    # node specs: (cx, w, title, sub, scarlet)
    nodes = [
        (130, 150, "0x…", "address", False),
        (370, 196, "4 ENGINES", "parallel", False),
        (610, 150, "DEDUP", "ai cuts noise", False),
        (840, 156, "REPLAY", "fork exploit", False),
        (1075, 170, "REPORT", "public link", True),
    ]
    # connectors (under nodes) with flowing scarlet dashes
    o.append(f'<line x1="70" y1="{baseline}" x2="{W-70}" y2="{baseline}" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1"/>')
    o.append(f'<line x1="70" y1="{baseline}" x2="{W-70}" y2="{baseline}" stroke="{SCARLET}" stroke-opacity="0.5" '
             f'stroke-width="1.4" stroke-dasharray="2 12" stroke-linecap="round">'
             f'<animate attributeName="stroke-dashoffset" values="0;-140" dur="3s" repeatCount="indefinite"/></line>')

    for (cx, w, title, sub, red) in nodes:
        x = cx - w/2
        h = 64; y = baseline - h/2
        stroke = SCARLET if red else "#FFFFFF"
        sop = "0.5" if red else "0.14"
        fill = SURF2 if red else SURFACE
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="5" fill="{fill}" '
                 f'stroke="{stroke}" stroke-opacity="{sop}" stroke-width="1"/>')
        tcol = BRIGHT if red else INK
        o.append(f'<text x="{cx}" y="{baseline-4}" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="17" font-weight="600" letter-spacing="1" fill="{tcol}">{title}</text>')
        o.append(f'<text x="{cx}" y="{baseline+16}" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="10" letter-spacing="2" fill="{INK4}">{sub.upper()}</text>')
        if red:
            o.append(f'<circle cx="{x+14}" cy="{y+14}" r="3" fill="{SCARLET}">'
                     f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')

    # the four engine names floating above node 2
    engines = ["SLITHER", "ADERYN", "MYTHRIL", "CLAUDE"]
    for i, e in enumerate(engines):
        ex = 370 - 84 + i*56
        o.append(f'<text x="{ex}" y="92" text-anchor="middle" font-family="{MONO}" font-size="9.5" '
                 f'letter-spacing="1.5" fill="{INK3}">{e}</text>')
        o.append(f'<line x1="{ex}" y1="100" x2="370" y2="{baseline-34}" stroke="#FFFFFF" stroke-opacity="0.07" stroke-width="1"/>')

    # arrowheads between nodes
    for i in range(len(nodes)-1):
        ax = (nodes[i][0] + nodes[i][1]/2 + nodes[i+1][0] - nodes[i+1][1]/2)/2
        o.append(f'<path d="M{ax-3:.0f} {baseline-4} L{ax+3:.0f} {baseline} L{ax-3:.0f} {baseline+4}" '
                 f'fill="none" stroke="{INK3}" stroke-width="1" stroke-opacity="0.5"/>')

    # sweeping scan beam
    o.append(f'<g><rect x="-25" y="60" width="50" height="200" fill="url(#bg)"/>'
             f'<rect x="-0.8" y="70" width="1.6" height="180" fill="url(#beam)"/>'
             f'<animateTransform attributeName="transform" type="translate" values="80 0; {W-80} 0; 80 0" '
             f'dur="7s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
             f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></g>')
    write("pipeline.svg", svg(W, H, "ETorn scan pipeline: address, four engines, dedup, replay, report.", "\n".join(o)))

# ======================================================================
# 4. WORK — selected projects as hairline cards
# ======================================================================
def work():
    W = 1200
    eb_y = 46
    pad = 40; gap = 24
    cw = (W - 2*pad - gap) / 2
    ch = 132
    top = 74
    cards = [
        ("WEB3 · SECURITY", "ETorn", ["Pre-audit scanner for Solidity. Four engines,", "AI dedup, exploits replayed on a fork."], True),
        ("QUANT", "Bybit Trader", ["Algorithmic trading bot.", "Signals, risk, execution."], False),
        ("SYSTEMS", "StringOS", ["An operating-system kernel and bootloader,", "written down to x86 assembly."], False),
        ("PRODUCT", "ech0", ["Mobile-first social platform —", "curate your digital altar."], False),
    ]
    H = top + 2*ch + gap + 30
    o = [f'<rect width="{W}" height="{H}" fill="{BLACK}"/>']
    o.append(eyebrow(pad, eb_y, "SELECTED WORK"))
    o.append(eyebrow(W-pad, eb_y, "4 OF MANY", anchor="end", fill=INK4, ls=4))
    for idx, (cat, name, desc, live) in enumerate(cards):
        col = idx % 2; row = idx // 2
        x = pad + col*(cw+gap); y = top + row*(ch+gap)
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch}" rx="6" fill="{SURFACE}" '
                 f'stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>')
        # scarlet top-accent tick
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="40" height="2" rx="1" fill="{SCARLET}" opacity="0.9"/>')
        o.append(f'<text x="{x+26:.0f}" y="{y+34}" font-family="{MONO}" font-size="10.5" letter-spacing="2.5" '
                 f'fill="{INK3}">{cat}</text>')
        o.append(f'<text x="{x+24:.0f}" y="{y+70}" font-family="{SANS}" font-size="30" font-weight="700" '
                 f'letter-spacing="-1" fill="{INK}">{name}</text>')
        for j, line in enumerate(desc):
            o.append(f'<text x="{x+26:.0f}" y="{y+96+j*17}" font-family="{MONO}" font-size="11.5" '
                     f'fill="{INK2}">{line}</text>')
        if live:
            o.append(f'<circle cx="{x+cw-54:.0f}" cy="{y+28}" r="3.5" fill="{SCARLET}">'
                     f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')
            o.append(f'<text x="{x+cw-44:.0f}" y="{y+32}" font-family="{MONO}" font-size="10.5" '
                     f'letter-spacing="2" fill="{BRIGHT}">LIVE</text>')
    write("work.svg", svg(W, H, "Selected work: ETorn, Bybit Trader, StringOS, ech0.", "\n".join(o)))

# ======================================================================
# 5. STATS — a thin proof strip of real ETorn facts
# ======================================================================
def stats():
    W, H = 1200, 132
    tiles = [("4", "ENGINES"), ("~60s", "FREE SCAN"), ("7", "CHAINS"), ("0", "SIGNUP")]
    o = [f'<rect width="{W}" height="{H}" fill="{BLACK}"/>']
    o.append(f'<rect x="0" y="0" width="{W}" height="1" fill="{SCARLET}" opacity="0.5"/>')
    n = len(tiles); seg = W / n
    for i, (num, lab) in enumerate(tiles):
        cx = seg * (i + 0.5)
        if i:
            o.append(f'<line x1="{seg*i:.0f}" y1="28" x2="{seg*i:.0f}" y2="{H-28}" stroke="#FFFFFF" stroke-opacity="0.08"/>')
        o.append(f'<text x="{cx:.0f}" y="74" text-anchor="middle" font-family="{SANS}" font-size="42" '
                 f'font-weight="800" letter-spacing="-1.5" fill="{INK}">{num}</text>')
        o.append(f'<text x="{cx:.0f}" y="100" text-anchor="middle" font-family="{MONO}" font-size="11" '
                 f'letter-spacing="3" fill="{INK3}">{lab}</text>')
    write("stats.svg", svg(W, H, "ETorn at a glance: 4 engines, ~60s free scan, 7 chains, no signup.", "\n".join(o)))

if __name__ == "__main__":
    banner(); divider(); pipeline(); work(); stats()
    print("done")
