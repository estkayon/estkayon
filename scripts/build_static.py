"""Build the static profile visuals into assets/.

Run:  python scripts/build_static.py
Edit PROFILE / FOCUS / CONTACT below and re-run whenever your details change.
"""
from __future__ import annotations

from svgkit import C, ROOT, grow, icon, image_uri, panel, svg, t

OUT = ROOT / "assets"

PROFILE = [
    ("user", "name", "Md. Estiak Rahman Ayon"),
    ("badge", "nickname", "Ayon / ER"),
    ("cap", "education", "AIUB (BSc CSE)"),
    ("cal", "graduation", "Aug 2026 (Completed)"),
    ("star", "cgpa", "3.54 / 4.00"),
    ("pin", "location", "Dhaka, Bangladesh"),
    ("clock", "timezone", "GMT +6"),
]
FOCUS = [
    "MLOps Engineer / AI Engineer",
    "Building real-world ML solutions",
    "Scalable systems & automation",
    "Open source & continuous learning",
]
CONTACT = [  # (icon, text) — drawn on the footer banner
    ("gh", "@estkayon"),
    ("in", "md-estiak-rahman-ayon"),
    ("web", "Portfolio"),
    ("mail", "estiakayon@gmail.com"),
]


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote assets/{name}  ({len(content.encode())/1024:.0f} KB)")


# ------------------------------------------------------------------ hero
def hero() -> None:
    W, H = 1024, 345
    stars = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"><animate attributeName="opacity" '
        f'values="0;.9;0" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for x, y, r, d, b in [(118, 62, 1.3, 3.2, 0), (262, 30, 1.1, 4.1, 1.2), (468, 22, 1.4, 3.6, .6),
                              (842, 92, 1.2, 4.4, 2.1), (980, 128, 1.1, 3.1, 1.6), (720, 40, 1.0, 5.0, .3)]
    )
    body = f"""
<defs>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <linearGradient id="sweep" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#ffe3a8" stop-opacity=".22"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{C['gold']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{C['gold']}"/><stop offset="1" stop-color="{C['gold']}" stop-opacity="0"/></linearGradient>
</defs>
<g clip-path="url(#r)">
  <image href="{image_uri('hero.jpg')}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
  {stars}
  <rect x="-260" y="0" width="220" height="{H}" fill="url(#sweep)" transform="skewX(-18)">
    <animate attributeName="x" values="-300;1300" dur="7s" repeatCount="indefinite"/>
  </rect>
  <rect x="571" y="304" width="7" height="13" fill="{C['cyan']}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
  <rect x="0" y="{H-2}" width="{W}" height="2" fill="url(#edge)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{C['line2']}"/>"""
    write("hero.svg", svg(W, H, body, fonts=(), title="Ayon — Software, AI/ML and MLOps Engineer"))


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
    W, H = 1000, 322
    LW = 364
    rows = []
    for i, (ic, k, v) in enumerate(PROFILE):
        y = 36 + i * 24
        d = .15 * i
        rows.append(
            f'<g>{grow("opacity", 0, 1, d, .5)}'
            f'{icon(ic, 20, y - 13, 16, C["text"])}'
            f'<text x="50" y="{y}" class="m" font-size="13" fill="{C["text"]}">{t(k)}</text>'
            f'<text x="142" y="{y}" class="m" font-size="13" fill="{C["muted"]}">:</text>'
            f'<text x="156" y="{y}" class="m" font-size="13" fill="{C["cyan"]}">{t(v)}</text></g>'
        )
    fy = 36 + len(PROFILE) * 24 - 4
    focus = [
        f'<line x1="20" x2="{LW-20}" y1="{fy}" y2="{fy}" stroke="{C["line2"]}"/>',
        icon("gear", 18, fy + 14, 20, C["gold"]),
        f'<text x="50" y="{fy+29}" class="mb" font-size="13" fill="{C["gold"]}">current focus :</text>',
    ]
    for j, f in enumerate(FOCUS):
        y = fy + 48 + j * 20
        focus.append(
            f'<text x="50" y="{y}" class="m" font-size="12.5" fill="{C["cyan"]}">'
            f'<tspan fill="{C["gold"]}">• </tspan>{t(f)}</text>'
        )
    cur_y = fy + 48 + (len(FOCUS) - 1) * 20
    cur_x = 50 + (len(FOCUS[-1]) + 2) * 7.55 + 6
    focus.append(
        f'<rect x="{cur_x:.0f}" y="{cur_y-11}" width="7" height="13" fill="{C["gold"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )
    RX = LW + 16
    RW = W - RX
    body = f"""
<defs><clipPath id="ship"><rect x="{RX}" y="0" width="{RW}" height="{H}" rx="12"/></clipPath></defs>
{panel(.5, .5, LW - 1, H - 1, 12, C['panel'], C['line'])}
{''.join(rows)}
{''.join(focus)}
<g clip-path="url(#ship)">
  <image href="{image_uri('ship.jpg')}" x="{RX}" y="0" width="{RW}" height="{H}" preserveAspectRatio="xMaxYMid slice"/>
</g>
<rect x="{RX+.5}" y=".5" width="{RW-1}" height="{H-1}" rx="12" fill="none" stroke="{C['line2']}"/>"""
    write("captains-log.svg", svg(W, H, body, fonts=("JBM", "JBMB"), title="Captain's log — about Ayon"))


# ------------------------------------------------------------------ divider
def divider() -> None:
    W, H = 1000, 34
    body = f"""
<defs><linearGradient id="g"><stop offset="0" stop-color="{C['gold']}" stop-opacity="0"/>
<stop offset=".5" stop-color="{C['gold']}"/><stop offset="1" stop-color="{C['gold']}" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="16" width="{W}" height="1.6" fill="url(#g)"/>
<circle cy="16.8" r="3" fill="{C['gold2']}"><animate attributeName="cx" values="60;940;60" dur="9s" repeatCount="indefinite"/>
<animate attributeName="opacity" values=".2;1;.2" dur="9s" repeatCount="indefinite"/></circle>
<g transform="translate(500 17)">
  <circle r="13" fill="{C['bg']}" stroke="{C['gold']}" stroke-width="1.4"/>
  {icon('skull', -9, -9.5, 18, C['gold2'])}
</g>"""
    write("divider.svg", svg(W, H, body, fonts=(), title="divider"))


# ------------------------------------------------------------------ footer
def chip_icon(kind: str, x: float, y: float) -> str:
    """Small round contact icons (original simple glyphs, not brand logos)."""
    g = f'<circle cx="{x}" cy="{y}" r="11" fill="#13203a" stroke="{C["line2"]}"/>'
    if kind == "gh":
        g += f'<path d="M{x-5} {y+4} q0-6 5-6 q5 0 5 6" fill="none" stroke="#fff" stroke-width="1.5"/><circle cx="{x}" cy="{y-3}" r="3.2" fill="none" stroke="#fff" stroke-width="1.5"/>'
    elif kind == "in":
        g += f'<text x="{x}" y="{y+4.5}" text-anchor="middle" class="mb" font-size="12" fill="#fff">in</text>'
    elif kind == "web":
        g += (f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="#fff" stroke-width="1.3"/>'
              f'<ellipse cx="{x}" cy="{y}" rx="2.6" ry="6" fill="none" stroke="#fff" stroke-width="1.1"/>'
              f'<line x1="{x-6}" x2="{x+6}" y1="{y}" y2="{y}" stroke="#fff" stroke-width="1.1"/>')
    elif kind == "mail":
        g += icon("mail", x - 7, y - 7, 14, "#fff")
    return g


def footer() -> None:
    W, H = 1024, 270
    # Two chips left and two right, leaving the gap above the captain's hat clear.
    slots = [84, None, 488, None]
    chips, x = [], 0
    for i, (kind, text) in enumerate(CONTACT):
        x = slots[i] if slots[i] is not None else x
        w = 34 + len(text) * 7.0 + 12
        chips.append(
            f'<g><rect x="{x}" y="57" width="{w:.0f}" height="30" rx="15" fill="#08101f" fill-opacity=".93" stroke="{C["line2"]}"/>'
            f'{chip_icon(kind, x + 16, 72)}'
            f'<text x="{x+33}" y="76.5" class="m" font-size="11.5" fill="{C["text"]}">{t(text)}</text></g>'
        )
        x += w + 6
    body = f"""
<defs><clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050b18" stop-opacity=".7"/>
<stop offset=".22" stop-color="#050b18" stop-opacity="0"/></linearGradient></defs>
<g clip-path="url(#r)">
  <image href="{image_uri('footer.jpg')}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
  <rect width="{W}" height="{H}" fill="url(#top)"/>
  <rect x="0" y="0" width="{W}" height="2" fill="{C['gold']}" fill-opacity=".6"/>
  <rect x="24" y="9" width="392" height="42" rx="21" fill="#08101f" fill-opacity=".93" stroke="{C['line2']}"/>
  {icon('skull', 38, 15, 30, '#ffffff')}
  <text x="80" y="39" class="s" font-size="22" fill="#fff"><tspan textLength="196" lengthAdjust="spacing">OPEN CHANNEL</tspan><tspan dx="12" dy="-1" class="m" font-weight="400" font-size="13" fill="{C['cyan']}">/ let's connect</tspan></text>
  {''.join(chips)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{C['line2']}"/>"""
    write("footer.svg", svg(W, H, body, fonts=("Cinzel", "JBM", "JBMB"), title="Open channel — let's connect"))


if __name__ == "__main__":
    hero()
    captains_log()
    header("head-captains-log.svg", "helm", "CAPTAIN'S LOG", "about me")
    header("head-bounty-board.svg", "ship", "BOUNTY BOARD", "flagship missions")
    header("head-voyage-log.svg", "compass", "VOYAGE LOG", "contributions & tech stack")
    divider()
    footer()
