#!/usr/bin/env python3
"""Generate the profile hero: cover.svg.

A single wide terminal/scanner banner. Pure-black OLED ground, blood-red
signal, JetBrains-Mono voice. Glitch-split wordmark, scanlines, a sweeping
scan beam, crosshair corner brackets, and one Bob-Ross creed at the bottom:
we don't make mistakes — just happy little accidents."""
import math, os

BLACK   = "#000000"
RED     = "#FF1500"   # primary scarlet
BLOOD   = "#E11D48"   # rose-blood
EMBER   = "#FF5340"   # bright ember
DEEPRED = "#C81029"   # dried blood (kept legible for the punchline)
INK     = "#FAFAFA"
INK3    = "#8A8A8E"
INK4    = "#56565B"
CYAN    = "#16E0E0"   # glitch ghost channel
MONO = "'JetBrains Mono', ui-monospace, 'SF Mono', 'Cascadia Code', monospace"
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
HERE = os.path.dirname(__file__)

W, H = 1200, 460


def scanlines():
    """Horizontal red scanlines across the whole canvas, very faint."""
    o = ['<g opacity="0.5">']
    y = 0
    while y < H:
        o.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{RED}" '
                 f'stroke-opacity="0.045" stroke-width="1"/>')
        y += 3
    o.append('</g>')
    return "\n".join(o)


def grid():
    """Faint vertical hairlines, blood-red, varying heights (a signal field)."""
    o = ['<g>']
    n = 60
    for i in range(n):
        x = 70 + i * ((W - 140) / (n - 1))
        hh = 10 + 26 * abs(math.sin(i * 0.55)) * abs(math.cos(i * 0.3))
        op = 0.05 + 0.05 * abs(math.sin(i * 0.9))
        o.append(f'<line x1="{x:.1f}" y1="{H-70-hh:.1f}" x2="{x:.1f}" y2="{H-70+hh:.1f}" '
                 f'stroke="{RED}" stroke-opacity="{op:.2f}" stroke-width="1"/>')
    o.append('</g>')
    return "\n".join(o)


def wordmark(cx, cy):
    """Glitch-split 'TossSky' — cyan + blood ghosts under the off-white core."""
    common = (f'text-anchor="middle" font-family="{SANS}" font-size="104" '
              f'font-weight="800" letter-spacing="-4"')
    o = ['<g>']
    # cyan ghost, nudged left, clipped jitter
    o.append(f'<text x="{cx-3}" y="{cy}" {common} fill="{CYAN}" opacity="0.55">TossSky'
             f'<animate attributeName="opacity" values="0;0.55;0.2;0.55;0" '
             f'dur="5.5s" begin="0s" repeatCount="indefinite"/>'
             f'<animate attributeName="x" values="{cx-3};{cx-7};{cx-3};{cx-1};{cx-3}" '
             f'dur="5.5s" repeatCount="indefinite"/></text>')
    # blood ghost, nudged right
    o.append(f'<text x="{cx+3}" y="{cy}" {common} fill="{BLOOD}" opacity="0.6">TossSky'
             f'<animate attributeName="opacity" values="0.2;0.6;0.1;0.6;0.2" '
             f'dur="4.2s" repeatCount="indefinite"/>'
             f'<animate attributeName="x" values="{cx+3};{cx+8};{cx+2};{cx+5};{cx+3}" '
             f'dur="4.2s" repeatCount="indefinite"/></text>')
    # solid core
    o.append(f'<text x="{cx}" y="{cy}" {common} fill="{INK}" '
             f'style="filter:url(#glow)">TossSky</text>')
    o.append('</g>')
    return "\n".join(o)


def crosshair(x, y, s, flip_x=1, flip_y=1):
    """L-shaped crosshair corner bracket, blood-red."""
    dx, dy = s * flip_x, s * flip_y
    return (f'<path d="M {x} {y+dy} L {x} {y} L {x+dx} {y}" fill="none" '
            f'stroke="{RED}" stroke-width="2" stroke-opacity="0.8"/>')


def main():
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none" '
             f'role="img" aria-label="TossSky — a blood-red security scanner banner on black.">')
    o.append('<defs>'
             f'<radialGradient id="core" cx="0.5" cy="0.42" r="0.62">'
             f'<stop offset="0%" stop-color="{RED}" stop-opacity="0.22"/>'
             f'<stop offset="55%" stop-color="{RED}" stop-opacity="0.06"/>'
             f'<stop offset="100%" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{RED}" stop-opacity="0"/>'
             f'<stop offset="50%" stop-color="{EMBER}" stop-opacity="0.9"/>'
             f'<stop offset="100%" stop-color="{RED}" stop-opacity="0"/></linearGradient>'
             f'<linearGradient id="beamhalo" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{RED}" stop-opacity="0"/>'
             f'<stop offset="50%" stop-color="{RED}" stop-opacity="0.16"/>'
             f'<stop offset="100%" stop-color="{RED}" stop-opacity="0"/></linearGradient>'
             f'<radialGradient id="vig" cx="0.5" cy="0.5" r="0.75">'
             f'<stop offset="60%" stop-color="{BLACK}" stop-opacity="0"/>'
             f'<stop offset="100%" stop-color="{BLACK}" stop-opacity="0.9"/></radialGradient>'
             f'<filter id="glow" x="-30%" y="-30%" width="160%" height="160%">'
             f'<feGaussianBlur stdDeviation="3.2" result="b"/>'
             f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
             f'</filter></defs>')

    o.append(f'<rect width="{W}" height="{H}" fill="{BLACK}"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#core)"/>')
    o.append(grid())
    o.append(scanlines())

    # sweeping scan beam (halo + bright line)
    o.append(f'<g><rect x="-60" y="0" width="120" height="{H}" fill="url(#beamhalo)"/>'
             f'<rect x="-1" y="0" width="2" height="{H}" fill="url(#beam)"/>'
             f'<animateTransform attributeName="transform" type="translate" '
             f'values="90 0; {W-90} 0; 90 0" dur="7s" repeatCount="indefinite" '
             f'calcMode="spline" keyTimes="0;0.5;1" '
             f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></g>')

    # top status line: terminal prompt
    o.append(f'<circle cx="74" cy="60" r="4" fill="{RED}"><animate attributeName="opacity" '
             f'values="1;0.25;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="90" y="65" font-family="{MONO}" font-size="14" letter-spacing="1" '
             f'fill="{INK3}">root@tossky:~# ./scan --target self --mode happy-accidents</text>')
    o.append(f'<text x="{W-70}" y="65" text-anchor="end" font-family="{MONO}" font-size="13" '
             f'letter-spacing="3" fill="{RED}" opacity="0.85">[ LIVE ]</text>')

    # crosshair corner brackets
    m, s = 40, 26
    o.append(crosshair(m, m, s, 1, 1))
    o.append(crosshair(W - m, m, s, -1, 1))
    o.append(crosshair(m, H - m, s, 1, -1))
    o.append(crosshair(W - m, H - m, s, -1, -1))

    # hero wordmark + subtitle
    o.append(wordmark(W // 2, 230))
    o.append(f'<text x="{W//2}" y="272" text-anchor="middle" font-family="{MONO}" '
             f'font-size="15" letter-spacing="9" fill="{INK3}">SECURITY · BLOCKCHAIN · SYSTEMS</text>')

    # thin red rule with end caps
    ry = 320
    o.append(f'<line x1="320" y1="{ry}" x2="{W-320}" y2="{ry}" stroke="{RED}" '
             f'stroke-opacity="0.5" stroke-width="1"/>')
    o.append(f'<circle cx="320" cy="{ry}" r="3" fill="{RED}"/>')
    o.append(f'<circle cx="{W-320}" cy="{ry}" r="3" fill="{RED}"/>')
    o.append(f'<rect x="{W//2-4}" y="{ry-4}" width="8" height="8" fill="{RED}" '
             f'transform="rotate(45 {W//2} {ry})"/>')

    # Bob Ross creed
    o.append(f'<text x="{W//2}" y="372" text-anchor="middle" font-family="{MONO}" '
             f'font-size="17" letter-spacing="1" fill="{INK}">'
             f'&quot;we don\'t make mistakes &#8212; just happy little accidents.&quot;</text>')
    o.append(f'<text x="{W//2}" y="398" text-anchor="middle" font-family="{MONO}" '
             f'font-size="12" letter-spacing="5" fill="{DEEPRED}">&#8212; BOB ROSS, RELUCTANT THREAT MODEL</text>')

    # blinking cursor block at the very bottom
    o.append(f'<rect x="{W//2-70}" y="416" width="11" height="18" fill="{RED}">'
             f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" '
             f'repeatCount="indefinite"/></rect>')
    o.append(f'<text x="{W//2-52}" y="431" font-family="{MONO}" font-size="13" '
             f'letter-spacing="2" fill="{INK4}">awaiting input</text>')

    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    # outer hairline frame
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" '
             f'stroke="{RED}" stroke-opacity="0.25" stroke-width="1"/>')

    o.append('</svg>')
    body = "\n".join(o)
    with open(os.path.join(HERE, "cover.svg"), "w", encoding="utf-8") as f:
        f.write(body + "\n")
    print(f"wrote cover.svg ({len(body)} bytes)")


if __name__ == "__main__":
    main()
