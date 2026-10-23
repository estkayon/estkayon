"""Build the static (but animated) profile visuals into assets/.

Run:  python scripts/build_static.py
Edit the PROFILE / FOCUS / QUOTE / HERO / CONTACT blocks below and re-run
whenever your details change.

Animation rule used everywhere: the element's own attributes describe the
finished picture, and SMIL only adds motion on top. A renderer that doesn't
play SVG animation still shows a complete, readable image.
"""
from __future__ import annotations

import math

from svgkit import C, ROOT, grow, icon, image_uri, panel, svg, t

OUT = ROOT / "assets"

HERO = {
    "name": "Ayon",
    "roles": "SOFTWARE ENGINEER  |  AI/ML ENGINEER  |  MLOPS ENGINEER",
    "taglines": [  # typed one after another, on a loop
        "// Building efficient models & reliable pipelines.",
        "// Forecasting • Deployment • Automation",
        "// Researching efficient AI for low-resource settings",
        "// The model is the start. The system is the mission.",
    ],
}
PROFILE = [
    ("user", "name", "Md. Estiak Rahman Ayon"),
    ("badge", "nickname", "Ayon / ER"),
    ("cap", "education", "AIUB (BSc CSE)"),
    ("cal", "graduation", "Aug 2026 (Completed)"),
    ("pin", "location", "Dhaka, Bangladesh"),
    ("clock", "timezone", "GMT +6"),
]
FOCUS = [
    "MLOps Engineer / AI Engineer",
    "Building real-world ML solutions",
    "Scalable systems & automation",
    "Open source & continuous learning",
]
QUOTE = {  # written word by word across the sunset-ship panel
    "lines": [["A", "small", "step"], ["each", "day"], ["builds", "a", "big", "dream."]],
    "gold": {"big", "dream."},
    "sign": "— Ayon",
}
CONTACT = [  # (icon, text) — drawn on the footer banner; None = gap over the captain's hat
    ("gh", "@estkayon"),
    ("in", "md-estiak-rahman-ayon"),
    None,
    ("web", "Portfolio"),
    ("mail", "estiakayon@gmail.com"),
]
# Live pipeline strip (Mission 01: Bangladesh electricity demand forecasting)
PIPELINE = [("data", "DVC", "versioned data"), ("train", "Train", "& evaluate"), ("track", "MLflow", "DagsHub"),
            ("serve", "FastAPI", "model API"), ("dash", "Streamlit", "dashboard"), ("ship", "Docker", "CI/CD · Render")]

DOCKER_PATH = "M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.954-5.43h2.118a.186.186 0 00.186-.186V3.574a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m0 2.716h2.118a.187.187 0 00.186-.186V6.29a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.887c0 .102.082.185.185.186m-2.93 0h2.12a.186.186 0 00.184-.186V6.29a.185.185 0 00-.185-.185H8.1a.185.185 0 00-.185.185v1.887c0 .102.083.185.185.186m-2.964 0h2.119a.186.186 0 00.185-.186V6.29a.185.185 0 00-.185-.185H5.136a.186.186 0 00-.186.185v1.887c0 .102.084.185.186.186m5.893 2.715h2.118a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m-2.93 0h2.12a.185.185 0 00.184-.185V9.006a.185.185 0 00-.184-.186h-2.12a.185.185 0 00-.184.185v1.888c0 .102.083.185.185.185m-2.964 0h2.119a.185.185 0 00.185-.185V9.006a.185.185 0 00-.184-.186h-2.12a.186.186 0 00-.186.186v1.887c0 .102.084.185.186.185m-2.92 0h2.12a.185.185 0 00.184-.185V9.006a.185.185 0 00-.184-.186h-2.12a.185.185 0 00-.184.185v1.888c0 .102.082.185.185.185M23.763 9.89c-.065-.051-.672-.51-1.954-.51-.338.001-.676.03-1.01.087-.248-1.7-1.653-2.53-1.716-2.566l-.344-.199-.226.327c-.284.438-.49.922-.612 1.43-.23.97-.09 1.882.403 2.661-.595.332-1.55.413-1.744.42H.751a.751.751 0 00-.75.748 11.376 11.376 0 00.692 4.062c.545 1.428 1.355 2.48 2.41 3.124 1.18.723 3.1 1.137 5.275 1.137.983.003 1.963-.086 2.93-.266a12.248 12.248 0 003.823-1.389c.98-.567 1.86-1.288 2.61-2.136 1.252-1.418 1.998-2.997 2.553-4.4h.221c1.372 0 2.215-.549 2.68-1.009.309-.293.55-.65.707-1.046l.098-.288Z"  # Simple Icons "docker", CC0

EASE = 'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote assets/{name}  ({len(content.encode())/1024:.0f} KB)")


def ken_burns(href: str, w: float, h: float, ox: float, oy: float, zoom: float, dur: float,
              x: float = 0, y: float = 0, par: str = "xMidYMid slice", pan=(0, 0), iid: str = "") -> str:
    """A slow zoom (and optional drift) around (ox, oy), eased in and out, looping forever."""
    px, py = pan
    return (
        f'<g transform="translate({ox} {oy})"><g>'
        f'<animateTransform attributeName="transform" type="scale" values="1;{zoom};1" dur="{dur}s" {EASE} repeatCount="indefinite"/>'
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{px} {py};0 0" dur="{dur*1.3:.1f}s" {EASE} repeatCount="indefinite"/>'
        f'<image{f' id="{iid}"' if iid else ""} href="{href}" x="{x-ox}" y="{y-oy}" width="{w}" height="{h}" preserveAspectRatio="{par}"/>'
        f'</g></g></g>'
    )


def blink(dur: float = 1.1) -> str:
    return f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="{dur}s" repeatCount="indefinite"/>'


def gull(y: float, scale: float, dur: float, begin: float) -> str:
    """Tiny seagull: two arcs that flap, gliding slowly across the sky."""
    return (
        f'<g opacity=".85"><animateTransform attributeName="transform" type="translate" '
        f'values="-60 {y};1090 {y-26}" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"/>'
        f'<g transform="scale({scale})">'
        f'<path d="M-9 0 Q-4.5 -5 0 0 Q4.5 -5 9 0" fill="none" stroke="#1a1426" stroke-width="1.8" stroke-linecap="round">'
        f'<animate attributeName="d" values="M-9 0 Q-4.5 -5 0 0 Q4.5 -5 9 0;M-9 -3 Q-4.5 1 0 0 Q4.5 1 9 -3;M-9 0 Q-4.5 -5 0 0 Q4.5 -5 9 0" '
        f'dur="1.4s" repeatCount="indefinite"/></path></g></g>'
    )


HAT_X = 232   # little straw hat that sits on the end of the name


def straw_hat(x: float, y: float) -> str:
    """A small generic straw hat (simple original shapes) that drops in, then rocks gently."""
    return (
        f'<g transform="translate({x} {y})"><g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 -40;0 -40;0 0" keyTimes="0;.55;1" dur="3.2s" '
        f'calcMode="spline" keySplines="0 0 1 1;.25 .1 .25 1" fill="freeze"/>'
        f'<g><animateTransform attributeName="transform" type="rotate" values="-8;6;-8" dur="5s" {EASE} repeatCount="indefinite" begin="3.2s"/>'
        f'<g transform="rotate(-14)">'
        f'<ellipse cx="0" cy="6" rx="27" ry="7.5" fill="#e8c46a" stroke="#9c7a2c" stroke-width="1.2"/>'
        f'<path d="M-14 6 C-14 -12 14 -12 14 6 Z" fill="#f0cf78" stroke="#9c7a2c" stroke-width="1.2"/>'
        f'<path d="M-14.2 1.5 C-8 4.5 8 4.5 14.2 1.5 L14 6 C8 8.6 -8 8.6 -14 6 Z" fill="#d63b2f"/>'
        f'</g></g></g></g>'
    )


# ------------------------------------------------------------------ hero (cover)
def hero() -> None:
    W, H = 1024, 345
    SUNX, SUNY = 690, 118               # where the sunset glow sits behind the ship

    stars = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".0">'
        f'<animate attributeName="opacity" values="0;.9;0" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/></circle>'
        for x, y, r, d, b in [(118, 62, 1.3, 4.2, 0), (262, 30, 1.1, 5.1, 1.2), (468, 22, 1.4, 4.6, .6),
                              (842, 92, 1.2, 5.4, 2.1), (980, 128, 1.1, 4.1, 1.6), (720, 40, 1.0, 6.0, .3),
                              (360, 70, 1.0, 5.6, 3.0), (930, 60, 1.2, 4.8, 2.6)]
    )
    rays = "".join(
        f'<path d="M0 0 L{560*math.cos(a):.1f} {560*math.sin(a)-16:.1f} L{560*math.cos(a):.1f} {560*math.sin(a)+16:.1f}Z"/>'
        for a in [i * 0.5236 + 0.2 for i in range(12)]
    )
    glints = "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="1.4" rx=".7" fill="#ffe1a0" opacity="0">'
        f'<animate attributeName="opacity" values="0;.85;0" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/></rect>'
        for x, y, w, d, b in [(600, 156, 14, 3.4, 0), (655, 162, 9, 4.1, 1.1), (742, 150, 12, 3.8, 2.0),
                              (520, 166, 10, 4.6, .7), (812, 160, 8, 3.2, 1.6), (700, 170, 11, 4.4, 2.6)]
    )
    embers = "".join(
        f'<circle cx="{x}" cy="{H+10}" r="{r}" fill="{C["gold2"]}" opacity="0">'
        f'<animate attributeName="cy" values="{H+10};{H-150}" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;.75;0" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cx" values="{x};{x+18};{x-6}" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/></circle>'
        for x, r, d, b in [(300, 1.6, 11, 0), (520, 1.2, 13, 4), (690, 1.8, 12, 7), (860, 1.3, 14, 2),
                           (960, 1.5, 10, 6), (410, 1.1, 15, 9), (760, 1.0, 12.5, 10.5)]
    )

    # ---- typed tagline loop
    lines = HERO["taglines"]
    slot = 4.5                      # seconds per line
    D = slot * len(lines)
    CW = 7.25                       # JetBrains Mono advance at 12px
    TX, TY = 66, 330
    typed = []
    for i, line in enumerate(lines):
        w = len(line) * CW
        a, b = i / len(lines), (i + 1) / len(lines)
        k1 = a + (b - a) * 0.42     # typing done
        k2 = a + (b - a) * 0.86     # start erasing
        k3 = b - 0.001
        kt = f"0;{a:.4f};{k1:.4f};{k2:.4f};{k3:.4f};1"
        vis = f"0;0;{w:.1f};{w:.1f};0;0"
        base_w = w if i == 0 else 0  # without animation, show the first line only
        typed.append(
            f'<clipPath id="ty{i}"><rect x="{TX}" y="{TY-12}" width="{base_w:.1f}" height="17">'
            f'<animate attributeName="width" values="{vis}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/></rect></clipPath>'
        )
        typed.append(f'<text x="{TX}" y="{TY}" class="m" font-size="12" fill="{C["cyan"]}" clip-path="url(#ty{i})">{t(line)}</text>')
    cur_x = ";".join(
        v for i, line in enumerate(lines) for v in
        (f"{TX}", f"{TX + len(line)*CW:.1f}", f"{TX + len(line)*CW:.1f}", f"{TX}")
    ) + f";{TX}"
    kts = []
    for i in range(len(lines)):
        a, b = i / len(lines), (i + 1) / len(lines)
        kts += [a, a + (b - a) * 0.42, a + (b - a) * 0.86, b - 0.001]
    kts.append(1)
    cursor = (
        f'<rect x="{TX + len(lines[0])*CW + 2:.1f}" y="{TY-11}" width="7" height="13" fill="{C["cyan"]}">'
        f'<animate attributeName="x" values="{cur_x}" keyTimes="{";".join(f"{k:.4f}" for k in kts)}" dur="{D}s" repeatCount="indefinite"/>'
        f'{blink()}</rect>'
    )

    name = t(HERO["name"])
    body = f"""
<defs>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#ffe3a8" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{C['gold']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{C['gold']}"/><stop offset="1" stop-color="{C['gold']}" stop-opacity="0"/></linearGradient>
  <radialGradient id="sun" cx="{SUNX/W}" cy="{SUNY/H}" r=".45" gradientTransform="translate({SUNX/W} {SUNY/H}) scale(1 2.97) translate({-SUNX/W} {-SUNY/H})">
    <stop offset="0" stop-color="#ffd27a" stop-opacity=".55"/><stop offset=".35" stop-color="#ff9a3c" stop-opacity=".18"/>
    <stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
  <radialGradient id="rayfade" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="raymask"><circle cx="{SUNX}" cy="{SUNY}" r="560" fill="url(#rayfade)"/></mask>
  <linearGradient id="readable" x1="0" y1="0" x2="0" y2="1"><stop offset=".5" stop-color="#050b18" stop-opacity="0"/>
    <stop offset="1" stop-color="#050b18" stop-opacity=".55"/></linearGradient>
  <linearGradient id="leftshade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050b18" stop-opacity=".62"/>
    <stop offset=".62" stop-color="#050b18" stop-opacity="0"/></linearGradient>
  <linearGradient id="leftfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".35" stop-color="#fff"/></linearGradient>
  <mask id="lowerhalf"><rect y="140" width="{W}" height="{H-140}" fill="url(#leftfade)"/></mask>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<g clip-path="url(#r)">
  <!-- 1. the cover itself: a slow, eased zoom + drift (26s loop) -->
  {ken_burns(image_uri('hero.jpg'), W, H, 512, 190, 1.06, 26, pan=(-9, -3))}

  <!-- 2. sunset light: breathing glow + slowly turning rays -->
  <rect width="{W}" height="{H}" fill="url(#sun)" style="mix-blend-mode:screen">
    <animate attributeName="opacity" values=".55;1;.55" dur="9s" {EASE} repeatCount="indefinite"/></rect>
  <g mask="url(#raymask)" style="mix-blend-mode:screen" opacity=".07" fill="#ffe2a6">
    <g transform="translate({SUNX} {SUNY})">{rays}
      <animateTransform attributeName="transform" type="rotate" values="0;360" dur="140s" repeatCount="indefinite" additive="sum"/></g>
  </g>
  {glints}
  {stars}
  {gull(58, 1.0, 46, 6)}{gull(84, .75, 58, 30)}{gull(40, .6, 64, 44)}
  {embers}
  <rect width="{W}" height="{H}" fill="url(#readable)"/>
  <rect width="{W}" height="{H}" fill="url(#leftshade)" mask="url(#lowerhalf)"/>
  <rect x="-300" y="0" width="240" height="{H}" fill="url(#sweep)" transform="skewX(-18)">
    <animate attributeName="x" values="-320;1400" dur="12s" {EASE.replace(';.45 0 .55 1','')} repeatCount="indefinite"/></rect>

  <!-- 4. corner labels (were baked into the art; now crisp and still) -->
  {icon('skull', 36, 18, 30, '#ffffff')}
  <text x="76" y="33" class="m" font-size="12.5" fill="#d6e4ff">Straw Hat Pirates</text>
  <text x="76" y="47" class="m" font-size="8.5" fill="#aebbd6">— Going to the Grand Line —</text>
  <g transform="rotate(-7 955 40)" class="b" fill="#fff" text-anchor="middle">
    <text x="952" y="34" font-size="14">Same Dream</text><text x="958" y="52" font-size="14">Bigger Horizons</text></g>
  <g transform="rotate(-12 935 295)" class="b" font-size="16" fill="#c9d4ff">
    {''.join(f'<text x="{906 + i*9}" y="{268 + i*19}">{w}<animate attributeName="opacity" values=".45;1;.45" dur="8s" begin="{i*2}s" {EASE} repeatCount="indefinite"/></text>' for i, w in enumerate(["Dream", "Build", "Ship", "Repeat"]))}
    <path d="M922 333 q28 0 62 -5" fill="none" stroke="#c9d4ff" stroke-width="1.4" stroke-linecap="round"/></g>

  <!-- 5. name, roles, typed tagline -->
  <text x="58" y="252" class="b" font-size="78" fill="#fff" stroke="#fff" stroke-width="1.4"
        stroke-dasharray="1200" stroke-dashoffset="0" fill-opacity="1">{name}
    {grow("stroke-dashoffset", 1200, 0, .2, 2.8)}{grow("fill-opacity", 0, 1, 1.7, 1.4)}</text>
  {straw_hat(HAT_X, 194)}
  <text x="64" y="306" class="mb" font-size="15" letter-spacing=".8" fill="#f4f6fb">{t(HERO['roles'])}
    {grow("opacity", 0, 1, 2.3, 1.2)}</text>
  {''.join(typed)}
  {cursor}
  <rect x="0" y="{H-2}" width="{W}" height="2" fill="url(#edge)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{C['line2']}"/>"""
    write("hero.svg", svg(W, H, body, fonts=("Brush", "JBM", "JBMB"),
                          title=f"{HERO['name']} — {HERO['roles']}"))


# ------------------------------------------------------------------ section header
def header(file: str, ico: str, title: str, sub: str) -> None:
    W, H = 1000, 66
    tw = len(title) * 18.2 + 16
    body = f"""
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{C['bg']}" stroke="{C['line']}"/>
<circle cx="40" cy="33" r="19" fill="none" stroke="{C['gold']}" stroke-opacity=".35"/>
<g><animateTransform attributeName="transform" type="rotate" values="0 40 33;360 40 33" dur="18s" repeatCount="indefinite"/>
  {icon(ico, 25, 18, 30, C['gold'])}</g>
<text x="74" y="43" class="s" font-size="25" fill="{C['text']}"><tspan textLength="{tw-16:.0f}" lengthAdjust="spacing">{t(title)}</tspan><tspan dx="16" dy="-1" class="m" font-weight="400" font-size="14" fill="{C['cyan']}">/ {t(sub)}</tspan></text>
<rect x="74" y="54" width="{tw-16:.0f}" height="2" rx="1" fill="{C['gold']}">
  <animate attributeName="width" values="0;{tw-16:.0f};{tw-16:.0f}" keyTimes="0;.25;1" dur="6s" repeatCount="indefinite"/>
</rect>"""
    write(file, svg(W, H, body, fonts=("Cinzel", "JBM"), title=f"{title} — {sub}"))


# ------------------------------------------------------------------ captain's log
def captains_log() -> None:
    W = 1000
    LW = 364
    rows = []
    for i, (ic, k, v) in enumerate(PROFILE):
        y = 37 + i * 26
        rows.append(
            f'<g>{grow("opacity", 0, 1, .15 * i, .5)}'
            f'{icon(ic, 20, y - 13, 16, C["text"])}'
            f'<text x="50" y="{y}" class="m" font-size="13" fill="{C["text"]}">{t(k)}</text>'
            f'<text x="142" y="{y}" class="m" font-size="13" fill="{C["muted"]}">:</text>'
            f'<text x="156" y="{y}" class="m" font-size="13" fill="{C["cyan"]}">{t(v)}</text></g>'
        )
    fy = 37 + len(PROFILE) * 26 - 4
    focus = [
        f'<line x1="20" x2="{LW-20}" y1="{fy}" y2="{fy}" stroke="{C["line2"]}"/>',
        icon("gear", 18, fy + 14, 20, C["gold"]),
        f'<text x="50" y="{fy+29}" class="mb" font-size="13" fill="{C["gold"]}">current focus :</text>',
    ]
    for j, f in enumerate(FOCUS):
        y = fy + 46 + j * 21
        focus.append(
            f'<text x="50" y="{y}" class="m" font-size="12.5" fill="{C["cyan"]}">'
            f'<tspan fill="{C["gold"]}">• </tspan>{t(f)}</text>'
        )
    cur_y = fy + 46 + (len(FOCUS) - 1) * 21
    cur_x = 50 + (len(FOCUS[-1]) + 2) * 7.55 + 6
    focus.append(f'<rect x="{cur_x:.0f}" y="{cur_y-11}" width="7" height="13" fill="{C["gold"]}">{blink()}</rect>')
    H = cur_y + 26

    RX, RW = LW + 16, W - LW - 16
    QX = RX + RW / 2
    D = 12.0                                   # one write → hold → fade loop
    words, idx = [], 0
    nlines = len(QUOTE["lines"])
    line_h = 58
    y0 = H / 2 - (nlines - 1) * line_h / 2 + 14
    hold_end, gone = 10.4, 11.2
    for li, line in enumerate(QUOTE["lines"]):
        spans = []
        for wi, w in enumerate(line):
            gap = " " if wi < len(line) - 1 else ""   # no trailing space, so lines stay centred
            t0 = 0.8 + idx * 0.42
            k0, k1, k2 = t0 / D, (t0 + .35) / D, (t0 + 1.1) / D
            final = C["gold2"] if w in QUOTE["gold"] else "#ffffff"
            spans.append(
                f'<tspan fill="{final}" fill-opacity="1">{t(w)}{gap}'
                f'<animate attributeName="fill-opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{k0:.4f};{k1:.4f};{hold_end/D:.4f};{gone/D:.4f};1" dur="{D}s" repeatCount="indefinite"/>'
                f'<animate attributeName="fill" values="{C["gold2"]};{C["gold2"]};{final};{final}" '
                f'keyTimes="0;{k1:.4f};{k2:.4f};1" dur="{D}s" repeatCount="indefinite"/></tspan>'
            )
            idx += 1
        words.append(f'<text x="{QX:.0f}" y="{y0 + li*line_h:.0f}" text-anchor="middle" class="b" font-size="46" '
                     f'filter="url(#qglow)">{"".join(spans)}</text>')
    t_done = 0.8 + idx * 0.42 + .2
    kd, kd2 = t_done / D, (t_done + .9) / D
    under_y = y0 + (nlines - 1) * line_h + 16
    fade = f'keyTimes="0;{kd:.4f};{kd2:.4f};{hold_end/D:.4f};{gone/D:.4f};1" dur="{D}s" repeatCount="indefinite"'
    shipimg = ken_burns(image_uri("ship.jpg"), RW, H, RX + RW * .3, H * .55, 1.06, 30, x=RX, par="xMinYMid slice", pan=(-8, 0))
    body = f"""
<defs>
  <clipPath id="ship"><rect x="{RX}" y="0" width="{RW}" height="{H}" rx="12"/></clipPath>
  <radialGradient id="shade" cx=".5" cy=".55" r=".75"><stop offset="0" stop-color="#030712" stop-opacity=".45"/>
    <stop offset=".7" stop-color="#030712" stop-opacity=".72"/><stop offset="1" stop-color="#030712" stop-opacity=".9"/></radialGradient>
  <filter id="qglow" x="-10%" y="-40%" width="120%" height="180%">
    <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#000" flood-opacity=".85"/></filter>
</defs>
{panel(.5, .5, LW - 1, H - 1, 12, C['panel'], C['line'])}
{''.join(rows)}
{''.join(focus)}
<g clip-path="url(#ship)">
  {shipimg}
  <rect x="{RX}" width="{RW}" height="{H}" fill="url(#shade)"/>
  <text x="{RX+24}" y="34" class="m" font-size="12" fill="{C['cyan']}">&gt;_ captain's motto
    <animate attributeName="opacity" values=".55;1;.55" dur="3s" repeatCount="indefinite"/></text>
  {''.join(words)}
  <line x1="{QX-150:.0f}" x2="{QX+150:.0f}" y1="{under_y:.0f}" y2="{under_y:.0f}" stroke="{C['gold']}" stroke-width="1.6"
        stroke-linecap="round" stroke-dasharray="300" stroke-dashoffset="0" opacity=".8">
    <animate attributeName="stroke-dashoffset" values="300;300;0;0;0;300" {fade}/></line>
  <text x="{RX+RW-30}" y="{H-24}" text-anchor="end" class="b" font-size="22" fill="{C['gold']}" fill-opacity="1">{t(QUOTE['sign'])}
    <animate attributeName="fill-opacity" values="0;0;1;1;0;0" {fade}/></text>
</g>
<rect x="{RX+.5}" y=".5" width="{RW-1}" height="{H-1}" rx="12" fill="none" stroke="{C['line2']}"/>"""
    write("captains-log.svg", svg(W, H, body, fonts=("JBM", "JBMB", "Brush"), title=f"Captain's log — about {HERO['name']}. Motto: A small step each day builds a big dream."))


# ------------------------------------------------------------------ MLOps pipeline strip
def pipeline() -> None:
    W, H = 1000, 124
    icons = {"data": "db", "train": "brain", "track": "chart", "serve": "bolt", "dash": "code", "ship": "box"}
    n = len(PIPELINE)
    x0, x1 = 24, W - 24
    gap = 26
    bw = (x1 - x0 - gap * (n - 1)) / n
    by, bh = 44, 62
    cyc = 9.0                                    # one full run through the pipeline
    parts = [panel(.5, .5, W - 1, H - 1, 12),
             f'<text x="24" y="27" class="mb" font-size="11.5" letter-spacing="1.5" fill="{C["gold"]}">MISSION 01 · DELIVERY PIPELINE</text>',
             f'<text x="{W-24}" y="27" text-anchor="end" class="m" font-size="11" fill="{C["muted"]}">Bangladesh electricity demand forecasting · holdout MAPE 5.68%</text>']
    for i, (key, label, sub) in enumerate(PIPELINE):
        bx = x0 + i * (bw + gap)
        k = i / n
        k2 = min(k + 1 / n, 1)
        glow = (f'<animate attributeName="stroke-opacity" values=".35;.35;1;.35;.35" '
                f'keyTimes="0;{k:.3f};{(k+k2)/2:.3f};{k2:.3f};1" dur="{cyc}s" repeatCount="indefinite"/>')
        parts.append(f'<rect x="{bx:.1f}" y="{by}" width="{bw:.1f}" height="{bh}" rx="10" fill="{C["panel2"]}" '
                     f'stroke="{C["gold"]}" stroke-opacity=".35" stroke-width="1.4">{glow}</rect>')
        if key == "ship":   # the real Docker whale (Simple Icons, CC0)
            parts.append(f'<path transform="translate({bx+13:.1f} {by+15}) scale(.95)" fill="#2496ED" d="{DOCKER_PATH}"/>')
        else:
            parts.append(icon(icons[key], bx + 14, by + 14, 22, C["cyan"]))
        parts.append(f'<text x="{bx+46:.1f}" y="{by+27}" class="mb" font-size="13" fill="{C["text"]}">{t(label)}</text>')
        parts.append(f'<text x="{bx+46:.1f}" y="{by+45}" class="m" font-size="10" fill="{C["muted"]}">{t(sub)}</text>')
        # status light: lights up while its stage runs, stays green afterwards in the cycle
        parts.append(f'<circle cx="{bx+bw-12:.1f}" cy="{by+12}" r="3.2" fill="{C["green"]}">'
                     f'<animate attributeName="opacity" values=".25;.25;1;1;.25" keyTimes="0;{k:.3f};{(k+k2)/2:.3f};.97;1" dur="{cyc}s" repeatCount="indefinite"/></circle>')
        if i < n - 1:
            cx0, cx1, cy = bx + bw + 2, bx + bw + gap - 2, by + bh / 2
            parts.append(f'<line x1="{cx0:.1f}" x2="{cx1:.1f}" y1="{cy}" y2="{cy}" stroke="{C["line2"]}" stroke-width="2" stroke-dasharray="3 3"/>')
            parts.append(f'<path d="M{cx1-5:.1f} {cy-4} L{cx1:.1f} {cy} L{cx1-5:.1f} {cy+4}" fill="none" stroke="{C["line2"]}" stroke-width="1.6"/>')
            parts.append(
                f'<circle cx="{cx0:.1f}" cy="{cy}" r="3.4" fill="{C["gold2"]}" opacity="0">'
                f'<animate attributeName="cx" values="{cx0:.1f};{cx0:.1f};{cx1:.1f};{cx1:.1f}" keyTimes="0;{k2-.04:.3f};{k2:.3f};1" dur="{cyc}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{k2-.04:.3f};{k2-.02:.3f};{k2:.3f};1" dur="{cyc}s" repeatCount="indefinite"/></circle>'
            )
    write("pipeline.svg", svg(W, H, "".join(parts), fonts=("JBM", "JBMB"),
                              title="Mission 01 delivery pipeline: DVC, training, MLflow/DagsHub, FastAPI, Streamlit, Docker and CI/CD"))


# ------------------------------------------------------------------ divider
def divider() -> None:
    W, H = 1000, 34
    body = f"""
<defs><linearGradient id="g"><stop offset="0" stop-color="{C['gold']}" stop-opacity="0"/>
<stop offset=".5" stop-color="{C['gold']}"/><stop offset="1" stop-color="{C['gold']}" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="16" width="{W}" height="1.6" fill="url(#g)"/>
<circle cx="500" cy="16.8" r="3" fill="{C['gold2']}"><animate attributeName="cx" values="60;940;60" dur="9s" {EASE} repeatCount="indefinite"/>
<animate attributeName="opacity" values=".2;1;.2" dur="9s" repeatCount="indefinite"/></circle>
<g transform="translate(500 17)">
  <circle r="13" fill="{C['bg']}" stroke="{C['gold']}" stroke-width="1.4"/>
  {icon('skull', -9, -9.5, 18, C['gold2'])}
</g>"""
    write("divider.svg", svg(W, H, body, fonts=(), title="divider"))


# ------------------------------------------------------------------ footer
def chip_icon(kind: str, x: float, y: float) -> str:
    """Small round contact icons (simple original glyphs, not brand logos)."""
    g = f'<circle cx="{x}" cy="{y}" r="11" fill="#13203a" stroke="{C["line2"]}"/>'
    if kind == "gh":
        g += (f'<path d="M{x-5} {y+4} q0-6 5-6 q5 0 5 6" fill="none" stroke="#fff" stroke-width="1.5"/>'
              f'<circle cx="{x}" cy="{y-3}" r="3.2" fill="none" stroke="#fff" stroke-width="1.5"/>')
    elif kind == "in":
        g += f'<text x="{x}" y="{y+4.5}" text-anchor="middle" class="mb" font-size="12" fill="#fff">in</text>'
    elif kind == "web":
        g += (f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="#fff" stroke-width="1.3"/>'
              f'<ellipse cx="{x}" cy="{y}" rx="2.6" ry="6" fill="none" stroke="#fff" stroke-width="1.1"/>'
              f'<line x1="{x-6}" x2="{x+6}" y1="{y}" y2="{y}" stroke="#fff" stroke-width="1.1"/>')
    elif kind == "x":
        g += (f'<path d="M{x-4.5} {y-4.5}L{x+4.5} {y+4.5}M{x+4.5} {y-4.5}L{x-4.5} {y+4.5}" '
              f'stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')
    elif kind == "mail":
        g += icon("mail", x - 7, y - 7, 14, "#fff")
    return g


FOOTER_QUOTE = ("“As long as I live, there are infinite chances!”", "— Monkey D. Luffy")


def footer() -> None:
    """Crew banner with only the quote on top: a light shadow over the art, a deeper soft shadow
    behind the quote, and the same slow zoom + light sweep as before."""
    W, H = 1024, 270
    quote, who = FOOTER_QUOTE
    QY = 196
    body = f"""
<defs><clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
<stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="qshade" cx="512" cy="{QY+10}" r="1" gradientUnits="userSpaceOnUse"
  gradientTransform="translate(512 {QY+10}) scale(420 92) translate(-512 {-(QY+10)})">
  <stop offset="0" stop-color="#030712" stop-opacity=".78"/><stop offset=".6" stop-color="#030712" stop-opacity=".45"/>
  <stop offset="1" stop-color="#030712" stop-opacity="0"/></radialGradient>
<linearGradient id="topfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050b18" stop-opacity=".5"/>
<stop offset=".42" stop-color="#050b18" stop-opacity="0"/></linearGradient>
<filter id="qs" x="-10%" y="-60%" width="120%" height="220%"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity=".9"/></filter>
</defs>
<g clip-path="url(#r)">
  {ken_burns(image_uri('footer.jpg'), W, H, 512, 200, 1.05, 28, pan=(8, 0))}
  <rect width="{W}" height="{H}" fill="#050b18" fill-opacity=".32"/>
  <rect width="{W}" height="{H}" fill="url(#topfade)"/>
  <rect width="{W}" height="{H}" fill="url(#qshade)"/>
  <rect x="-300" y="0" width="220" height="{H}" fill="url(#sweep)" transform="skewX(-18)">
    <animate attributeName="x" values="-320;1400" dur="14s" repeatCount="indefinite"/></rect>
  <rect x="0" y="0" width="{W}" height="2" fill="{C['gold']}" fill-opacity=".6"/>
  <text x="512" y="{QY}" text-anchor="middle" class="b" font-size="34" fill="#ffffff" filter="url(#qs)">{t(quote)}</text>
  <text x="512" y="{QY+34}" text-anchor="middle" class="b" font-size="19" fill="{C['gold2']}" filter="url(#qs)">{t(who)}</text>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{C['line2']}"/>"""
    write("footer.svg", svg(W, H, body, fonts=("Brush",), title=f"{quote} {who}"))


def docker_badge() -> None:
    """Self-hosted Docker badge, so the logo never depends on an outside badge service."""
    W, H = 74, 20
    body = (f'<rect width="{W}" height="{H}" fill="#0B1427"/>'
            f'<path transform="translate(6 3) scale(.58)" fill="#F4A63A" d="{DOCKER_PATH}"/>'
            f'<text x="26" y="14" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11" fill="#fff">Docker</text>')
    (OUT / "badge-docker.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" role="img" aria-label="Docker"><title>Docker</title>{body}</svg>',
        encoding="utf-8")
    print("wrote assets/badge-docker.svg")


if __name__ == "__main__":
    docker_badge()
    hero()
    captains_log()
    header("head-captains-log.svg", "helm", "CAPTAIN'S LOG", "about me")
    header("head-bounty-board.svg", "ship", "BOUNTY BOARD", "flagship missions")
    pipeline()
    header("head-voyage-log.svg", "compass", "VOYAGE LOG", "contributions & tech stack")
    divider()
    footer()
