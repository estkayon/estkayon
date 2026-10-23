"""Generate the live "Voyage Log" cards from real GitHub data.

Outputs (written to --out, default ./dist):
  voyage-log.svg      contribution heatmap + tech-stack usage + monthly bars
  voyage-bestday.svg  night-city banner with your best day and streaks

Data sources, in order:
  1. GitHub GraphQL API   (needs a token: GITHUB_TOKEN in Actions, or a PAT
                           in GH_STATS_TOKEN to include private contributions)
  2. Public fallback      contribution calendar page + REST repo languages

Usage:
  python scripts/generate_voyage.py --user estkayon --out dist
  python scripts/generate_voyage.py --demo        # sample data, for previews
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import sys
import urllib.request
from collections import OrderedDict

from svgkit import C, grow, icon, image_uri, panel, svg, t

MONTHS_SHOWN = 8
TOP_LANGS = 8
# Languages that would distort a "what I write" chart. Override with EXCLUDE_LANGS="A,B".
EXCLUDE_DEFAULT = {"Jupyter Notebook", "HTML", "CSS", "SCSS", "Procfile", "Makefile", "Batchfile"}

FALLBACK_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "PHP": "#4F5D95",
    "C#": "#178600", "C++": "#f34b7d", "C": "#555555", "Java": "#b07219", "R": "#198CE7",
    "Blade": "#f7523f", "Shell": "#89e051", "Dockerfile": "#384d54", "SQL": "#e38c00",
    "Go": "#00ADD8", "Rust": "#dea584", "Kotlin": "#A97BFF", "Dart": "#00B4AB", "TSQL": "#e38c00",
}


# ------------------------------------------------------------------ fetching
def http(url: str, token: str | None = None, data: bytes | None = None) -> bytes:
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "straw-hat-voyage-log"})
    if token:
        req.add_header("Authorization", f"bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


GQL = """
query($login:String!, $from:DateTime!, $to:DateTime!, $after:String) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations:OWNER, isFork:false, first:100, after:$after) {
      pageInfo { hasNextPage endCursor }
      nodes { languages(first:25) { edges { size node { name color } } } }
    }
  }
}"""


def fetch_graphql(user: str, token: str):
    to = dt.datetime.now(dt.timezone.utc)
    frm = to - dt.timedelta(days=364)
    days, langs, colors, after, first = {}, {}, {}, None, True
    while True:
        payload = json.dumps({"query": GQL, "variables": {
            "login": user, "from": frm.isoformat(), "to": to.isoformat(), "after": after}}).encode()
        res = json.loads(http("https://api.github.com/graphql", token, payload))
        if "errors" in res:
            raise RuntimeError(res["errors"])
        u = res["data"]["user"]
        if first:
            for w in u["contributionsCollection"]["contributionCalendar"]["weeks"]:
                for d in w["contributionDays"]:
                    days[d["date"]] = d["contributionCount"]
            first = False
        for repo in u["repositories"]["nodes"]:
            for e in repo["languages"]["edges"]:
                n = e["node"]["name"]
                langs[n] = langs.get(n, 0) + e["size"]
                colors[n] = e["node"]["color"] or colors.get(n)
        pi = u["repositories"]["pageInfo"]
        if not pi["hasNextPage"]:
            break
        after = pi["endCursor"]
    return days, langs, colors


def fetch_public(user: str, token: str | None):
    html = http(f"https://github.com/users/{user}/contributions").decode("utf-8", "replace")
    id_date = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?id="([^"]+)"', html))
    id_date = {v: k for k, v in id_date.items()} if id_date else {}
    if not id_date:  # attribute order differs between page versions
        id_date = {i: d for i, d in re.findall(r'id="([^"]+)"[^>]*?data-date="(\d{4}-\d\d-\d\d)"', html)}
    days = {d: 0 for d in id_date.values()}
    for fid, txt in re.findall(r'<tool-tip[^>]*?for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        m = re.match(r"\s*(\d+)\s+contribution", txt)
        if fid in id_date:
            days[id_date[fid]] = int(m.group(1)) if m else 0
    langs, colors, page = {}, {}, 1
    while True:
        repos = json.loads(http(f"https://api.github.com/users/{user}/repos?per_page=100&page={page}", token))
        if not repos:
            break
        for r in repos:
            if r.get("fork"):
                continue
            for n, size in json.loads(http(r["languages_url"], token)).items():
                langs[n] = langs.get(n, 0) + size
        page += 1
    return days, langs, colors


def demo_data():
    rnd = random.Random(7)
    today = dt.date.today()
    days = {}
    for i in range(365):
        d = today - dt.timedelta(days=364 - i)
        active = rnd.random() < (0.62 if d.weekday() < 5 else 0.38)
        days[d.isoformat()] = rnd.choice([1, 2, 3, 4, 5, 6, 8, 11]) if active else 0
    best = today - dt.timedelta(days=97)
    days[best.isoformat()] = 24
    langs = {"Python": 2_800_000, "JavaScript": 1_400_000, "TypeScript": 1_000_000, "PHP": 800_000,
             "Blade": 520_000, "C#": 600_000, "Java": 500_000, "R": 400_000, "Dockerfile": 120_000,
             "Shell": 90_000, "C++": 300_000, "Jupyter Notebook": 9_000_000}
    return days, langs, {}


# ------------------------------------------------------------------ stats
def month_start(d: dt.date, back: int) -> dt.date:
    y, m = d.year, d.month - back
    while m <= 0:
        m += 12
        y -= 1
    return dt.date(y, m, 1)


def compute(days_raw: dict[str, int]):
    days = OrderedDict(sorted((dt.date.fromisoformat(k), v) for k, v in days_raw.items()))
    today = max(days) if days else dt.date.today()
    start = month_start(today, MONTHS_SHOWN - 1)
    window = OrderedDict((d, c) for d, c in days.items() if d >= start)

    total = sum(window.values())
    active = sum(1 for c in window.values() if c > 0)
    longest = run = 0
    for c in window.values():
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    # current streak: today may still be empty, so start counting from yesterday then
    cur, seq = 0, list(days.items())
    if seq and seq[-1][1] == 0:
        seq = seq[:-1]
    for _, c in reversed(seq):
        if c == 0:
            break
        cur += 1

    months = OrderedDict()
    for i in range(MONTHS_SHOWN - 1, -1, -1):
        ms = month_start(today, i)
        months[ms] = 0
    for d, c in window.items():
        months[dt.date(d.year, d.month, 1)] += c

    best_d, best_c = (max(window.items(), key=lambda kv: (kv[1], kv[0])) if window else (today, 0))
    return {
        "window": window, "start": start, "today": today, "total": total, "active": active,
        "span": len(window), "longest": longest, "current": cur, "months": months,
        "best_day": best_d, "best_count": best_c,
    }


def lang_share(langs: dict[str, int], colors: dict[str, str]):
    excl = set(filter(None, os.environ.get("EXCLUDE_LANGS", "").split(","))) or EXCLUDE_DEFAULT
    items = sorted(((n, s) for n, s in langs.items() if n not in excl), key=lambda x: -x[1])
    total = sum(s for _, s in items) or 1
    top = items[:TOP_LANGS]
    rest = sum(s for _, s in items[TOP_LANGS:])
    rows = [(n, s / total * 100, colors.get(n) or FALLBACK_COLORS.get(n, "#8a97b4")) for n, s in top]
    if rest:
        rows.append(("Others", rest / total * 100, "#5b6b8c"))
    return rows


# ------------------------------------------------------------------ drawing
LEVELS = ["#121c31", "#0e4429", "#006d32", "#26a641", "#39d353"]


def quartiles(values) -> list[int]:
    nz = sorted(v for v in values if v > 0)
    if not nz:
        return [1, 1, 1]
    return [nz[int(len(nz) * q)] for q in (.25, .5, .75)]


def level(c: int, qs: list[int]) -> int:
    """GitHub-style shading: quartiles of the non-zero days, so one huge day doesn't wash out the rest."""
    if c <= 0:
        return 0
    return 1 if c < qs[0] else 2 if c < qs[1] else 3 if c < qs[2] else 4


def days_word(n: int) -> str:
    return f"{n} day" if n == 1 else f"{n} days"


def card_contrib(s, x0: int, y0: int, w: int, h: int) -> str:
    out = [panel(x0 + .5, y0 + .5, w - 1, h - 1, 12)]
    out.append(icon("flame", x0 + 18, y0 + 17, 20, C["gold"]))
    out.append(f'<text x="{x0+48}" y="{y0+32}" class="mb" font-size="14" fill="{C["text"]}">My Contributions</text>')
    stats = [("Total", f"{s['total']:,}"), ("Active Days", f"{s['active']} / {s['span']}"),
             ("Best Streak", days_word(s['longest'])), ("Current", days_word(s['current']))]
    offs = [0, .21, .52, .78]
    for i, (k, v) in enumerate(stats):
        x = x0 + 18 + offs[i] * (w - 36)
        out.append(f'<text x="{x:.0f}" y="{y0+64}" class="m" font-size="9.5" fill="{C["muted"]}">{k}</text>')
        out.append(f'<text x="{x:.0f}" y="{y0+86}" class="mb" font-size="14" fill="{C["green"]}">{t(v)}</text>')

    # heatmap: columns = weeks (Sun..Sat rows)
    win = s["window"]
    first = s["start"] - dt.timedelta(days=(s["start"].weekday() + 1) % 7)
    n_weeks = ((s["today"] - first).days // 7) + 1
    gap = 1.8
    cell = min(((w - 36) - gap * (n_weeks - 1)) / n_weeks, 11)
    gx = x0 + 18 + ((w - 36) - (cell * n_weeks + gap * (n_weeks - 1))) / 2
    gy = y0 + 136
    qs = quartiles(win.values())
    cells, labels, seen = [], [], set()
    for wk in range(n_weeks):
        for dy in range(7):
            d = first + dt.timedelta(days=wk * 7 + dy)
            if d < s["start"] or d > s["today"]:
                continue
            c = win.get(d, 0)
            cx = gx + wk * (cell + gap)
            cy = gy + dy * (cell + gap)
            delay = wk * 0.035
            cells.append(
                f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell:.1f}" height="{cell:.1f}" rx="1.6" fill="{LEVELS[level(c, qs)]}">'
                f'{grow("opacity", 0, 1, delay, .4)}</rect>'
            )
        wk_start = first + dt.timedelta(days=wk * 7)
        for dd in range(7):
            d = wk_start + dt.timedelta(days=dd)
            if d.day == 1 and d >= s["start"] and (d.year, d.month) not in seen:
                seen.add((d.year, d.month))
                labels.append(f'<text x="{gx + wk*(cell+gap):.0f}" y="{gy-9}" class="m" font-size="9.5" fill="{C["text"]}">{d.strftime("%b")}</text>')
    out += labels + cells
    ly = y0 + h - 18
    out.append(f'<text x="{x0+18}" y="{ly}" class="m" font-size="9" fill="{C["muted"]}">Last {MONTHS_SHOWN} months</text>')
    lx = x0 + w - 18 - 5 * 15 - 30
    out.append(f'<text x="{lx-6}" y="{ly}" text-anchor="end" class="m" font-size="9" fill="{C["muted"]}">Less</text>')
    for i, col in enumerate(LEVELS):
        out.append(f'<rect x="{lx + i*15}" y="{ly-9}" width="11" height="11" rx="2" fill="{col}"/>')
    out.append(f'<text x="{lx + 5*15 + 2}" y="{ly}" class="m" font-size="9" fill="{C["muted"]}">More</text>')
    return "".join(out)


def card_langs(rows, x0, y0, w, h) -> str:
    out = [panel(x0 + .5, y0 + .5, w - 1, h - 1, 12)]
    out.append(icon("code", x0 + 18, y0 + 17, 20, C["gold"]))
    out.append(f'<text x="{x0+48}" y="{y0+32}" class="mb" font-size="14" fill="{C["text"]}">Tech Stack Usage</text>')
    out.append(f'<line x1="{x0+18}" x2="{x0+w-18}" y1="{y0+46}" y2="{y0+46}" stroke="{C["line"]}"/>')
    n = max(len(rows), 1)
    step = min(21.5, (h - 74) / n)
    bx, bw = x0 + 112, w - 112 - 62
    mxp = max((p for _, p, _ in rows), default=1)
    for i, (name, pct, col) in enumerate(rows):
        y = y0 + 68 + i * step
        abbr = "".join(ch for ch in name if ch.isalnum())[:2].upper() if name != "Others" else "··"
        out.append(f'<rect x="{x0+18}" y="{y-11}" width="15" height="15" rx="3.5" fill="{col}"/>')
        out.append(f'<text x="{x0+25.5}" y="{y-0.8}" text-anchor="middle" class="mb" font-size="6.8" fill="#0b1427">{t(abbr)}</text>')
        out.append(f'<text x="{x0+40}" y="{y}" class="m" font-size="10.5" fill="{C["text"]}">{t(name[:11])}</text>')
        out.append(f'<rect x="{bx}" y="{y-8.5}" width="{bw}" height="9" rx="4.5" fill="#16223b"/>')
        fw = max(bw * pct / mxp, 4)
        out.append(
            f'<rect x="{bx}" y="{y-8.5}" width="{fw:.1f}" height="9" rx="4.5" fill="{col}">'
            f'{grow("width", 0, round(fw, 1), 0.08 * i, .9)}</rect>'
        )
        out.append(f'<text x="{x0+w-18}" y="{y}" text-anchor="end" class="m" font-size="10.5" fill="{C["text"]}">{pct:.0f}%</text>')
    if not rows:
        out.append(f'<text x="{x0+w/2}" y="{y0+h/2}" text-anchor="middle" class="m" font-size="11" fill="{C["muted"]}">no language data yet</text>')
    return "".join(out)


def card_monthly(s, x0, y0, w, h) -> str:
    out = [panel(x0 + .5, y0 + .5, w - 1, h - 1, 12)]
    out.append(icon("chart", x0 + 18, y0 + 17, 20, C["green"]))
    out.append(f'<text x="{x0+48}" y="{y0+32}" class="mb" font-size="14" fill="{C["text"]}">Monthly Contributions</text>')
    out.append('<defs><linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3ee58c"/>'
               '<stop offset="1" stop-color="#0f7a45"/></linearGradient></defs>')
    months = list(s["months"].items())
    mx = max((v for _, v in months), default=1) or 1
    area_top, area_bot = y0 + 78, y0 + h - 40
    slot = (w - 36) / len(months)
    bw = slot * 0.6
    for i, (m, v) in enumerate(months):
        bh = (area_bot - area_top) * v / mx if v else 2
        x = x0 + 18 + i * slot + (slot - bw) / 2
        out.append(
            f'<rect x="{x:.1f}" y="{area_bot-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="2" fill="url(#bar)">'
            f'{grow("height", 0, round(bh, 1), 0.07 * i, .8)}{grow("y", area_bot, round(area_bot - bh, 1), 0.07 * i, .8)}</rect>'
        )
        out.append(f'<text x="{x+bw/2:.1f}" y="{area_bot-bh-7:.1f}" text-anchor="middle" class="mb" font-size="10" fill="{C["text"]}">{v}</text>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{area_bot+20}" text-anchor="middle" class="m" font-size="10" fill="{C["muted"]}">{m.strftime("%b")}</text>')
    out.append(f'<line x1="{x0+18}" x2="{x0+w-18}" y1="{area_bot+.5}" y2="{area_bot+.5}" stroke="{C["line2"]}"/>')
    return "".join(out)


def voyage_log(s, rows, stamp: str) -> str:
    W, CH = 1000, 262
    H = CH + 18
    body = (card_contrib(s, 0, 0, 380, CH) + card_langs(rows, 392, 0, 284, CH) +
            card_monthly(s, 688, 0, 312, CH))
    body += f'<text x="{W-4}" y="{H-4}" text-anchor="end" class="m" font-size="9" fill="{C["muted"]}">{t(stamp)}</text>'
    return svg(W, H, body, fonts=("JBM", "JBMB"), title="Voyage log — contributions and tech stack")


def best_day(s, stamp: str) -> str:
    W, H = 1000, 190
    IW = round(772 * H / 183)
    bd = s["best_day"]
    side = [("star", "Active Days", f"{s['active']} / {s['span']}"),
            ("flame", "Longest Streak", days_word(s['longest'])),
            ("bolt", "Current Streak", days_word(s['current']))]
    sx = IW + 14
    sw = W - sx
    side_svg = [panel(sx + .5, .5, sw - 1, H - 1, 12)]
    for i, (ic, k, v) in enumerate(side):
        y = 22 + i * 56
        side_svg.append(icon(ic, sx + 16, y + 4, 20, C["cyan"]))
        side_svg.append(f'<text x="{sx+48}" y="{y+12}" class="m" font-size="10.5" fill="{C["cyan"]}">{k}</text>')
        side_svg.append(f'<text x="{sx+48}" y="{y+33}" class="mb" font-size="14" fill="{C["text"]}">{t(v)}</text>')
    count_word = "contribution" if s["best_count"] == 1 else "contributions"
    body = f"""
<defs><clipPath id="city"><rect width="{IW}" height="{H}" rx="12"/></clipPath></defs>
<g clip-path="url(#city)">
  <image href="{image_uri('city.jpg')}" width="{IW}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
  <g fill="#fff">
    <circle cx="120" cy="40" r="1.2"><animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/></circle>
    <circle cx="560" cy="30" r="1.2"><animate attributeName="opacity" values="0;1;0" dur="4s" begin="1s" repeatCount="indefinite"/></circle>
    <circle cx="700" cy="58" r="1"><animate attributeName="opacity" values="0;1;0" dur="3.4s" begin=".5s" repeatCount="indefinite"/></circle>
  </g>
  <rect x="388" y="16" width="160" height="80" rx="9" fill="#070d1a" fill-opacity=".94" stroke="{C['gold']}" stroke-opacity=".55"/>
  {icon('trophy', 400, 25, 16, C['gold'])}
  <text x="422" y="38" class="mb" font-size="12.5" fill="{C['gold']}">Best Day</text>
  <text x="400" y="62" class="mb" font-size="15" fill="{C['text']}">{s['best_count']} <tspan class="m" font-weight="400" font-size="12">{count_word}</tspan></text>
  <text x="400" y="83" class="m" font-size="10.5" fill="{C['muted']}">{bd.strftime('%b %d, %Y')}</text>
</g>
<rect x=".5" y=".5" width="{IW-1}" height="{H-1}" rx="12" fill="none" stroke="{C['line2']}"/>
{''.join(side_svg)}"""
    return svg(W, H, body, fonts=("JBM", "JBMB"), title="Best day and streaks")


# ------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=os.environ.get("GITHUB_USER", "estkayon"))
    ap.add_argument("--out", default="dist")
    ap.add_argument("--demo", action="store_true", help="use sample data (no network)")
    a = ap.parse_args()

    token = os.environ.get("GH_STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if a.demo:
        days, langs, colors = demo_data()
        src = "sample data"
    else:
        try:
            if not token:
                raise RuntimeError("no token")
            days, langs, colors = fetch_graphql(a.user, token)
            src = "GitHub GraphQL"
        except Exception as e:  # noqa: BLE001
            print(f"GraphQL unavailable ({e}); using public pages", file=sys.stderr)
            days, langs, colors = fetch_public(a.user, token)
            src = "GitHub public data"

    s = compute(days)
    rows = lang_share(langs, colors)
    stamp = f"updated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC · {src}"
    os.makedirs(a.out, exist_ok=True)
    for name, content in (("voyage-log.svg", voyage_log(s, rows, stamp)), ("voyage-bestday.svg", best_day(s, stamp))):
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote {a.out}/{name}")
    print(json.dumps({k: (str(v) if not isinstance(v, (int, float)) else v) for k, v in s.items()
                      if k not in ("window", "months")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
