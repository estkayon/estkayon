"""Shared helpers for the Straw Hat profile SVGs.

Every SVG embeds its own fonts and images as data URIs, because GitHub shows
README images through <img>, and an SVG loaded that way cannot fetch anything
external.
"""
from __future__ import annotations

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
IMG = ROOT / "assets" / "img"

# Palette taken from the design mock-up
C = {
    "bg": "#070d1a",
    "panel": "#0b1427",
    "panel2": "#0e1930",
    "line": "#1d2b4a",
    "line2": "#2a3d63",
    "gold": "#f4a63a",
    "gold2": "#ffcf6e",
    "text": "#e8edf7",
    "muted": "#8a97b4",
    "cyan": "#7cc8ff",
    "violet": "#c3a6ff",
    "green": "#2fd27a",
    "green_d": "#0f5132",
}

FONT_FILES = {
    "Cinzel": ("cinzel-latin-700-normal.woff2", 700),
    "JBM": ("jetbrains-mono-latin-400-normal.woff2", 400),
    "JBMB": ("jetbrains-mono-latin-700-normal.woff2", 700),
    "Brush": ("kaushan-script-latin-400-normal.woff2", 400),
}

MONO = "'JBM','JetBrains Mono',Consolas,'DejaVu Sans Mono',monospace"
MONOB = "'JBMB','JetBrains Mono',Consolas,'DejaVu Sans Mono',monospace"
SERIF = "'Cinzel',Georgia,'Times New Roman',serif"
BRUSH = "'Brush','Segoe Script','Brush Script MT',cursive"


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def font_css(*names: str) -> str:
    out = []
    for n in names:
        file, weight = FONT_FILES[n]
        out.append(
            f"@font-face{{font-family:'{n}';font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64(FONTS / file)}) format('woff2');}}"
        )
    return "".join(out)


def image_uri(name: str) -> str:
    p = IMG / name
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64(p)}"


def t(s) -> str:
    return escape(str(s))


def svg(w: int, h: int, body: str, fonts=("JBM",), extra_css: str = "", title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{t(title)}">'
        f"<title>{t(title)}</title>"
        f"<style>{font_css(*fonts)}"
        f".m{{font-family:{MONO}}}.mb{{font-family:{MONOB};font-weight:700}}"
        f".s{{font-family:{SERIF};font-weight:700}}.b{{font-family:{BRUSH}}}"
        f"{extra_css}</style>{body}</svg>"
    )


# ---------- small icons (simple original line art, 24x24 grid) ----------

def icon(name: str, x: float, y: float, size: float = 18, color: str = C["gold"]) -> str:
    s = size / 24
    paths = {
        "helm": '<circle cx="12" cy="12" r="5.2"/><circle cx="12" cy="12" r="1.8"/>'
                + "".join(
                    f'<line x1="{12+5.2*cs:.2f}" y1="{12+5.2*sn:.2f}" x2="{12+10.5*cs:.2f}" y2="{12+10.5*sn:.2f}"/>'
                    for cs, sn in [(1, 0), (.7071, .7071), (0, 1), (-.7071, .7071), (-1, 0), (-.7071, -.7071), (0, -1), (.7071, -.7071)]
                ),
        "compass": '<circle cx="12" cy="12" r="10"/><path d="M12 3.5l2.4 6.1L20.5 12l-6.1 2.4L12 20.5l-2.4-6.1L3.5 12l6.1-2.4z"/><circle cx="12" cy="12" r="1.3"/>',
        "flame": '<path d="M12 2.5c1 3.4 5.5 5.6 5.5 10.6a5.5 5.5 0 0 1-11 0c0-2.4 1.2-3.9 2.4-5 .1 1.7.9 2.8 2 3.2C11 8.7 10.6 5.6 12 2.5z"/>',
        "code": '<path d="M8 6l-6 6 6 6M16 6l6 6-6 6M14 4l-4 16"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.4 4.2-6.5 8-6.5s7 2.1 8 6.5"/>',
        "badge": '<rect x="4" y="6" width="16" height="15" rx="2"/><path d="M9 6V3h6v3M8 13h8M8 17h5"/>',
        "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c2.5 2.2 9.5 2.2 12 0v-5M22 9v6"/>',
        "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
        "pin": '<path d="M12 22s7-6.6 7-12a7 7 0 0 0-14 0c0 5.4 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/><circle cx="12" cy="12" r="6.3"/>',
        "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
        "ship": '<path d="M3 16h18l-2.5 4.5h-13z"/><path d="M12 3v13M12 4l6 9h-6M12 6l-5 7h5"/>',
        "skull": '<path d="M12 3a7 7 0 0 0-7 7c0 2.3 1.1 3.8 2.5 4.8V18h9v-3.2C17.9 13.8 19 12.3 19 10a7 7 0 0 0-7-7z"/><circle cx="9.3" cy="10.5" r="1.4"/><circle cx="14.7" cy="10.5" r="1.4"/><path d="M10 18v2.5M14 18v2.5M12 18v2.5"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "snake": '<path d="M3 17c2.5 0 3.2-1.6 3.6-3.4C7.1 11.4 8 9.5 10.5 9.5s3.4 1.9 3.9 4.1c.4 1.8 1.1 3.4 3.6 3.4 2 0 3-1.3 3-3"/><path d="M14.8 6.5c0-1.6 1.3-2.5 2.7-2.5s2.7.9 2.7 2.5-1.3 2.5-2.7 2.5"/><circle cx="18.2" cy="5.8" r=".5"/>',
        "db": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
        "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a2.5 2.5 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
        "trophy": '<path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 14v4M8 21h8M9 18h6"/>',
    }
    return (
        f'<g transform="translate({x} {y}) scale({s:.4f})" fill="none" stroke="{color}" '
        f'stroke-width="{1.8/ max(s,0.5):.2f}" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</g>'
    )


def panel(x, y, w, h, r=10, fill=None, stroke=None, op=1.0) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or C["panel"]}" '
        f'fill-opacity="{op}" stroke="{stroke or C["line"]}" stroke-width="1"/>'
    )


def grow(attr: str, start, end, delay: float, dur: float) -> str:
    """Entrance animation that starts at t=0, so the element never flashes and
    renderers without SMIL simply show the final state (set on the element itself)."""
    total = delay + dur
    k = delay / total if total else 0
    return (f'<animate attributeName="{attr}" values="{start};{start};{end}" '
            f'keyTimes="0;{k:.3f};1" dur="{total:.2f}s" fill="freeze"/>')
