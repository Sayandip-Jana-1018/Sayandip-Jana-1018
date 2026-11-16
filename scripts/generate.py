"""Builds every profile card in assets/cards/ from data/stats.json."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sjsvg import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "cards")
S = json.load(open(os.path.join(ROOT, "data", "stats.json")))


def fmt(n):
    return f"{n:,}"


# ======================================================================= icons
def icon(kind, x, y, s=18, color=GOLD_L, sw=1.6):
    """Tiny line icons drawn in a s*s box at (x, y)."""
    k = s / 24.0
    T = f'transform="translate({x},{y}) scale({k})"'
    a = f'fill="none" stroke="{color}" stroke-width="{sw / k:.2f}" stroke-linecap="round" stroke-linejoin="round"'
    p = {
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5 12 13l8.5-6.5"/>',
        "phone": '<path d="M5 3.5h3.5l1.7 4.3-2.2 1.4a11 11 0 0 0 6.8 6.8l1.4-2.2 4.3 1.7V19a1.5 1.5 0 0 1-1.6 1.5A17 17 0 0 1 3.5 5.1 1.5 1.5 0 0 1 5 3.5z"/>',
        "pin": '<path d="M12 21s-6.5-6.1-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.9 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.4"/>',
        "cap": '<path d="M2.5 9 12 4.5 21.5 9 12 13.5z"/><path d="M6.5 11v4.5c1.6 1.6 3.6 2.4 5.5 2.4s3.9-.8 5.5-2.4V11"/><path d="M21.5 9v5"/>',
        "trophy": '<path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4v1.5A3.5 3.5 0 0 0 7.5 11M17 6h3v1.5a3.5 3.5 0 0 1-3.5 3.5"/><path d="M12 14v3.5M8.5 20.5h7M9.5 17.5h5v3h-5z"/>',
        "code": '<path d="M8.5 7 3.5 12l5 5M15.5 7l5 5-5 5M13.5 4.5l-3 15"/>',
        "bolt": '<path d="M13 2.5 4.5 13.5H11l-1 8 8.5-11H12z"/>',
        "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
        "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
        "brain": '<path d="M9 4.5a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 2.5V4.5zM15 4.5a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 2.5V4.5z"/>',
        "cloud": '<path d="M7 18.5h10a4.5 4.5 0 0 0 .5-9A6 6 0 0 0 6 10.5a4 4 0 0 0 1 8z"/>',
        "db": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
        "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="m2.5 12.5 9.5 5 9.5-5M2.5 16.5l9.5 5 9.5-5"/>',
        "rocket": '<path d="M12 2.5c3.5 2.5 5.5 6 5.5 10.5l-2.5 3h-6l-2.5-3C6.5 8.5 8.5 5 12 2.5z"/><circle cx="12" cy="9.5" r="1.8"/><path d="M9 16.5 7 21l3-1.5M15 16.5l2 4.5-3-1.5"/>',
        "flame": '<path d="M12 21.5a6.5 6.5 0 0 1-6.5-6.5c0-4 3.5-6 4-10 2.5 1.5 3 4 3 5.5 1-.8 1.8-2.2 2-3.5 1.8 1.8 4 4.6 4 8a6.5 6.5 0 0 1-6.5 6.5z"/>',
        "scroll": '<path d="M7 3.5h11a2 2 0 0 1 2 2V8h-4M7 3.5a2.5 2.5 0 0 0-2.5 2.5v12.5a2.5 2.5 0 0 0 2.5 2.5h9.5a2 2 0 0 0 2-2v-11"/><path d="M8.5 9h6M8.5 12.5h6M8.5 16h4"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-7M21.5 20.5h-19"/>',
        "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3.1-3.1a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2M14 10a4.5 4.5 0 0 0-6.4 0l-3.1 3.1a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2"/>',
        "gem": '<path d="M6.5 3.5h11L21.5 9 12 21 2.5 9z"/><path d="M2.5 9h19M9 3.5 12 21l3-17.5"/>',
        "quote": '<path d="M9.5 6.5C6 7.5 4.5 10 4.5 13.5V18h5v-5H7c0-2.5 1-4 3-4.8zM19.5 6.5c-3.5 1-5 3.5-5 7V18h5v-5H17c0-2.5 1-4 3-4.8z"/>',
        "gamepad": '<rect x="2.5" y="7" width="19" height="11" rx="5.5"/><path d="M7 11v3.5M5.25 12.75h3.5"/><circle cx="15.5" cy="11.5" r="1"/><circle cx="18" cy="14" r="1"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
        "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8.5 7V5.5A1.5 1.5 0 0 1 10 4h4a1.5 1.5 0 0 1 1.5 1.5V7M3 12.5h18"/>',
        "school": '<path d="M3 21h18M5 21V10l7-5 7 5v11M9.5 21v-5h5v5"/><path d="M12 9.5v2"/>',
        "medal": '<path d="M8 2.5h8l-2.5 6h-3z"/><circle cx="12" cy="15" r="6"/><path d="m12 12 .9 1.9 2 .3-1.5 1.4.4 2-1.8-1-1.8 1 .4-2-1.5-1.4 2-.3z"/>',
    }.get(kind)
    if p is None:
        f = f'fill="{color}" stroke="none"'
        p = {
            "github": '<path d="M12 1C5.92 1 1 5.92 1 12c0 4.87 3.15 8.98 7.52 10.44.55.1.76-.24.76-.53v-1.86c-3.06.67-3.71-1.3-3.71-1.3-.5-1.27-1.22-1.61-1.22-1.61-1-.68.08-.67.08-.67 1.1.08 1.68 1.13 1.68 1.13.98 1.69 2.58 1.2 3.2.92.1-.71.39-1.2.7-1.47-2.44-.28-5.01-1.22-5.01-5.43 0-1.2.43-2.18 1.13-2.95-.11-.28-.49-1.4.11-2.91 0 0 .92-.3 3.02 1.13a10.4 10.4 0 0 1 5.5 0c2.1-1.43 3.02-1.13 3.02-1.13.6 1.51.22 2.63.11 2.91.7.77 1.13 1.75 1.13 2.95 0 4.22-2.57 5.15-5.02 5.42.4.34.74 1 .74 2.03v3.01c0 .29.2.63.76.52A11 11 0 0 0 23 12c0-6.08-4.92-11-11-11z"/>',
            "linkedin": '<path d="M4.5 2.5h15a2 2 0 0 1 2 2v15a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2v-15a2 2 0 0 1 2-2zM6.2 9.6v8.2h2.6V9.6zM7.5 5.4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm3.4 4.2v8.2h2.6v-4.3c0-1.2.4-2.1 1.6-2.1 1.1 0 1.3.9 1.3 2v4.4h2.6v-4.8c0-2.4-.9-3.6-3-3.6-1.2 0-2 .6-2.4 1.2V9.6z" fill-rule="evenodd"/>',
            "x": '<path d="M3 3h5.2l4.3 5.9L17.6 3h2.6l-6.5 7.5L21 21h-5.2l-4.7-6.4L5.5 21H2.9l7-8z"/>',
        }[kind]
        return f'<g {T} {f}>{p}</g>'
    return f'<g {T} {a}>{p}</g>'


# ======================================================================= HERO
def hero():
    W, H = 1000, 772
    c = Card(W, H, seed=11, accents=(GOLD, VIOLET, ROSE, AMBER), title="Sayandip Jana — SDE Intern @ Broadridge")
    c.background(blobs=[
        (GOLD, 800, 210, 420, 0.55),
        (VIOLET, 110, 640, 380, 0.42),
        (ROSE, 470, 360, 250, 0.20),
        (AMBER, 40, 30, 260, 0.30),
    ], dust=30)

    # ---------------- right column: poster in a liquid-gold frame
    px, py, pw, ph = 616, 62, 324, 432
    cx, cy = px + pw / 2, py + ph / 2
    # orbit rings behind the photo
    c.add(f'<g class="spin"><circle cx="{cx}" cy="{cy}" r="262" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="2 9"/></g>')
    c.add(f'<g class="spinr"><circle cx="{cx}" cy="{cy}" r="238" fill="none" stroke="{GOLD_L}" stroke-opacity=".18" stroke-dasharray="60 18 4 18"/></g>')
    c.add(f'<circle r="4.5" fill="{CHAMP}" filter="url(#softglow)"><animateMotion dur="16s" repeatCount="indefinite" path="M{cx-262} {cy} a262 262 0 1 0 524 0 a262 262 0 1 0 -524 0"/></circle>')
    c.add(f'<circle r="3" fill="{VIOLET}" filter="url(#softglow)"><animateMotion dur="11s" repeatCount="indefinite" path="M{cx+238} {cy} a238 238 0 1 1 -476 0 a238 238 0 1 1 476 0"/></circle>')
    gg = c.grad_radial([(0, GOLD, 0.55), (0.5, GOLD, 0.15), (1, GOLD, 0)])
    c.add(f'<ellipse class="glow" cx="{cx}" cy="{cy}" rx="{pw*0.75}" ry="{ph*0.62}" fill="url(#{gg})"/>')
    clip = c.uid("ph")
    c.defs.append(f'<clipPath id="{clip}"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="24"/></clipPath>')
    img = c.embed_image(os.path.join(ROOT, "assets", "img", "poster.jpg"))
    fade = c.grad_linear([(0, "#000", 0), (0.62, "#000", 0), (1, "#000", 0.55)], 0, 0, 0, 1)
    photo = (
        f'<rect x="{px+6}" y="{py+16}" width="{pw}" height="{ph}" rx="24" fill="#000" opacity=".5"/>'
        f'<g clip-path="url(#{clip})">'
        f'<image href="{img}" x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid slice"/>'
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#{fade})"/>'
        f'<rect class="sh" x="{px}" y="{py-20}" width="90" height="{ph+40}" fill="url(#shim)" style="animation-duration:7s"/>'
        f'</g>'
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="24" fill="none" stroke="url(#gstroke)" stroke-width="2.4"/>'
        f'<rect x="{px+5}" y="{py+5}" width="{pw-10}" height="{ph-10}" rx="20" fill="none" stroke="#FFFFFF" stroke-opacity=".18"/>'
    )
    per = 2 * (pw + ph)
    photo += (
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="24" fill="none" stroke="{CHAMP}" stroke-width="3" '
        f'stroke-linecap="round" stroke-dasharray="120 {per:.0f}" filter="url(#softglow)">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-{per+120:.0f}" dur="6s" repeatCount="indefinite"/></rect>'
    )
    c.add(f'<g class="breathe" style="animation-duration:9s">{photo}</g>')
    # floating tags around the photo
    for (tx, ty, lab, col, d) in [(584, 112, "GenAI · Agents", VIOLET, 0), (862, 236, "Java", ORANGE, 1.5),
                                  (588, 318, "Cloud · DevOps", TEAL, 3), (858, 452, "DSA 650+", GOLD, 2)]:
        svg, w = c.chip(tx, ty, lab, col, "mono", 700, 11.5, 28)
        c.add(f'<g class="fl" style="animation-delay:-{d}s">{svg}</g>')
    cap, _ = c.pill(cx, py + ph + 22, "B.TECH CSE · LPU · 2023–27", "mono", 700, 11.5, GOLD_L, 30, 1.6, anchor="middle")
    c.add(cap)

    # "currently" glass card
    c.add(c.glass(px, 574, pw, 92, r=18, tint=VIOLET, delay=2))
    c.add(icon("spark", px + 18, 590, 18, GOLD_L))
    c.add(c.text(px + 44, 604, "CURRENTLY", "mono", 700, 11, GOLD_L, ls=2.5))
    c.add(c.text(px + 18, 634, "LangGraph agents · Spring Boot", "sans", 500, 15, INK))
    c.add(c.text(px + 18, 654, "Daily DSA in Java across 4 judges", "sans", 400, 13.5, MUTED))

    # ---------------- left column
    x0 = 60
    pill, pw_ = c.pill(x0, 58, "SDE INTERN @ BROADRIDGE · JOINING 11 JAN 2027", "mono", 700, 11.5, GOLD_L, 32, 1.4, dot=EMERALD)
    c.add(pill)
    c.add(c.text(x0, 140, "HELLO, I'M", "mono", 700, 13, GOLD_L, ls=5, opacity=0.9))
    # name with soft glow underlay
    c.add(c.text(x0, 222, "SAYANDIP", "display", 900, 78, GOLD, opacity=0.35, extra='filter="url(#softglow)"'))
    c.add(c.text(x0, 222, "SAYANDIP", "display", 900, 78, "url(#gold)"))
    c.add(c.text(x0, 300, "JANA", "display", 900, 78, GOLD, opacity=0.35, extra='filter="url(#softglow)"'))
    c.add(c.text(x0, 300, "JANA", "display", 900, 78, "url(#gold)"))
    jw = c.tw("JANA", "display", 900, 78)
    c.add(f'<path d="M{x0 + jw + 24} 276 H{x0 + 500}" stroke="{GOLD}" stroke-opacity=".5"/>')
    c.add(f'<circle cx="{x0 + jw + 24}" cy="276" r="3" fill="{GOLD_L}"/>')
    c.add(c.text(x0, 346, "Full-Stack Engineer · GenAI & Agentic Systems", "sans", 500, 18, INK))
    c.add(c.text(x0, 372, "Java · Spring Boot · FastAPI · Next.js · Cloud-Native DevOps", "sans", 400, 14.5, MUTED))

    # terminal typing bar
    c.add(c.glass(x0, 394, 514, 52, r=14, tint=GOLD, delay=1))
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        c.add(f'<circle cx="{x0 + 20 + i*14}" cy="{394 + 26}" r="4.2" fill="{col}" opacity=".9"/>')
    c.add(c.text(x0 + 70, 426, "›", "mono", 700, 20, GOLD_L))
    c.add(c.typer(x0 + 90, 426, [
        "Full-Stack & GenAI Engineer",
        "Autonomous agentic systems builder",
        "653 LeetCode problems solved",
        "₹6L+ national hackathon winner",
        "14+ industry-level projects shipped",
        "Incoming SDE Intern @ Broadridge",
    ], "mono", 500, 16.5, INK))

    # stat tiles
    lc = S["leetcode"]["solved"]
    tiles = [
        ("9.11", "CGPA · B.TECH CSE · LPU", VIOLET, "cap"),
        (fmt(lc), "LEETCODE PROBLEMS SOLVED", ORANGE, "code"),
        ("₹6L+", "HACKATHON PRIZES WON", AMBER, "trophy"),
        ("14+", "INDUSTRY-LEVEL PROJECTS", ROSE, "layers"),
    ]
    tw_, th_ = 249, 92
    for i, (val, lab, col, ic) in enumerate(tiles):
        tx = x0 + (i % 2) * (tw_ + 16)
        ty = 466 + (i // 2) * (th_ + 16)
        c.add(c.glass(tx, ty, tw_, th_, r=18, tint=col, delay=i * 1.3, glow=None))
        c.add(c.text(tx + 20, ty + 50, val, "sans", 700, 36, "url(#gold)"))
        c.add(c.text(tx + 20, ty + 74, lab, "mono", 700, 10.5, MUTED, ls=1.2))
        c.add(f'<circle cx="{tx + tw_ - 34}" cy="{ty + 32}" r="17" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55"/>')
        c.add(icon(ic, tx + tw_ - 44, ty + 22, 20, CHAMP))

    # contact ribbon
    c.add(c.glass(x0, 692, 880, 52, r=26, tint=GOLD, delay=4))
    items = [("mail", "sayandip.jana24@gmail.com"), ("phone", "+91-8617005893"), ("pin", "Contai, WB · Punjab, India")]
    widths = [25 + c.tw(lab, "sans", 500, 14.5) for _, lab in items]
    gap = (880 - 2 * 28 - sum(widths)) / (len(items) - 1)
    xx = x0 + 28
    for i, ((ic, lab), w) in enumerate(zip(items, widths)):
        c.add(icon(ic, xx, 709, 17, GOLD_L))
        c.add(c.text(xx + 25, 723, lab, "sans", 500, 14.5, INK))
        xx += w + gap
        if i < len(items) - 1:
            c.add(f'<circle cx="{xx - gap/2:.0f}" cy="718" r="2" fill="{GOLD}" opacity=".7"/>')
    return c


# ======================================================================= shared helpers
def base(W, H, seed, accents, title, blobs=None, grid=True, dust=22):
    c = Card(W, H, seed=seed, accents=accents, title=title)
    c.background(blobs=blobs, dust=dust, grid=grid)
    return c


def head(c, y, eyebrow, title, sub=None, size=38, maxw=720):
    svg, h = c.header(c.w / 2, y, eyebrow, title, "middle", size, sub, maxw)
    c.add(svg)
    return y + h


def fit(c, s, font, weight, maxw, size, ls=0):
    while c.tw(s, font, weight, size, ls) > maxw and size > 10:
        size -= 0.5
    return size


def seg(c, x, y, parts, font="mono", size=13.5, cls="", style=""):
    """Multi-colour single line. parts = [(text, colour, weight), ...]."""
    out = []
    for t, col, wt in parts:
        out.append(c.text(x, y, t, font, wt, size, col))
        x += c.tw(t, font, wt, size)
    attr = (f' class="{cls}"' if cls else "") + (f' style="{style}"' if style else "")
    return f"<g{attr}>{''.join(out)}</g>", x


def icon_badge(c, cx, cy, r, kind, color, spin=True, isize=None):
    isize = isize or r * 1.05
    out = [
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".6"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 4}" fill="none" stroke="#FFFFFF" stroke-opacity=".08"/>',
    ]
    if spin:
        out.append(
            f'<g class="spin" style="animation-duration:{10 + (cx % 7):.0f}s"><circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="none" '
            f'stroke="{color}" stroke-opacity=".55" stroke-dasharray="3 7"/></g>'
        )
    out.append(icon(kind, cx - isize / 2, cy - isize / 2, isize, CHAMP))
    return "".join(out)


def soft_frame(c, color=GOLD_L):
    w, h, rx = c.w, c.h, c.rx
    per = 2 * (w + h)
    return (f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{rx}" fill="none" stroke="url(#gstroke)" stroke-width="1.5"/>'
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{rx}" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-dasharray="70 {per:.0f}" filter="url(#softglow)">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-{per+70:.0f}" dur="{per/220:.1f}s" repeatCount="indefinite"/></rect>')


def date_pill(c, x, y, label, color, h=24, size=10.5, anchor="start"):
    w = c.tw(label, "mono", 700, size, 1.4) + 24
    if anchor == "end":
        x -= w
    if anchor == "middle":
        x -= w / 2
    return (
        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity=".16" stroke="{color}" stroke-opacity=".6"/>'
        + c.text(x + 12, y + h / 2 + size * 0.36, label, "mono", 700, size, CHAMP, ls=1.4)
    ), w


def cycle(attr, n, k, dur, on="1", off="0"):
    """Discrete SMIL animation that is `on` only in slot k of n."""
    vals = [on if i == k else off for i in range(n)] + [off if k != 0 else on]
    kt = ";".join(f"{i / n:.4f}" for i in range(n)) + ";1"
    return (f'<animate attributeName="{attr}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite" '
            f'keyTimes="{kt}" values="{";".join(vals)}"/>')


def packet(path, dur, delay=0.0, color=CHAMP, r=3):
    return (f'<circle r="{r}" fill="{color}" filter="url(#softglow)" opacity="0">'
            f'<animateMotion dur="{dur}s" begin="-{delay:.2f}s" repeatCount="indefinite" path="{path}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.85;1" dur="{dur}s" begin="-{delay:.2f}s" repeatCount="indefinite"/></circle>')


# ======================================================================= DIVIDER
def divider():
    c = Card(1000, 64, seed=3, title="section divider")
    g = c.grad_linear([(0, GOLD, 0), (0.5, GOLD, 0.95), (1, GOLD, 0)], 60, 0, 940, 0, units="userSpaceOnUse")
    c.add(f'<path d="M60 32 H468 M532 32 H940" stroke="url(#{g})" stroke-width="1.3"/>')
    c.add(f'<g class="spin" style="animation-duration:8s"><path d="M500 14 L518 32 L500 50 L482 32Z" fill="none" stroke="{GOLD_L}" stroke-width="1.4"/></g>')
    c.add(f'<path class="glow" d="M500 23 L509 32 L500 41 L491 32Z" fill="url(#goldv)"/>')
    for i, (a, b) in enumerate([(468, 60), (532, 940)]):
        c.add(packet(f"M{a} 32 H{b}", 3.8, i * 1.9, CHAMP, 2.6))
    return c


# ======================================================================= ABOUT
def about():
    W, H = 1000, 600
    c = base(W, H, 21, (VIOLET, GOLD, TEAL, ROSE), "About Sayandip Jana",
             blobs=[(VIOLET, 120, 160, 380, .42), (GOLD, 900, 520, 400, .45), (TEAL, 560, 330, 260, .16), (ROSE, 950, 60, 220, .2)])
    head(c, 62, "01 · ABOUT", "WHO I AM")
    tx, ty, tw_, th = 50, 150, 560, 410
    c.add(c.glass(tx, ty, tw_, th, r=18, tint=VIOLET, strong=True))
    c.add(f'<path d="M{tx+1} {ty+42} H{tx+tw_-1}" stroke="#FFFFFF" stroke-opacity=".09"/>')
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        c.add(f'<circle cx="{tx + 22 + i*16}" cy="{ty + 21}" r="5" fill="{col}"/>')
    c.add(c.text(tx + tw_ / 2, ty + 26, "sayandip@sj: ~/profile — zsh", "mono", 400, 12, DIM, "middle"))
    P = lambda t, col=MUTED, w=400: (t, col, w)
    cmd = lambda verb, arg=None: [P("$ ", EMERALD, 700), P(verb, GOLD_L, 700)] + ([P(arg, CYAN)] if arg else [])
    lines = [
        cmd("whoami"),
        [P("sayandip_jana", INK, 700), P("   # full-stack · genai · devops", DIM)],
        cmd("cat ", "education.txt"),
        [P("B.Tech CSE", INK, 700), P(" · Lovely Professional University")],
        [P("CGPA "), P("9.11", AMBER, 700), P("  ·  ISC "), P("94.75%", AMBER, 700), P("  ·  ICSE "), P("96.20%", AMBER, 700)],
        cmd("cat ", "now.txt"),
        [P("» ", ROSE, 700), P("joining "), P("Broadridge", INK, 700), P(" as SDE Intern on "), P("11 Jan 2027", GOLD_L, 700)],
        [P("» ", ROSE, 700), P("shipping agentic systems with LangGraph & CrewAI")],
        [P("» ", ROSE, 700), P("one DSA problem a day on 4 judges, in Java")],
        cmd("echo ", "$MOTTO"),
        [P('"Code. Learn. Build. Solve real problems. Make an impact."', PINK, 400)],
    ]
    c.css.append(".tl{opacity:0;animation:tl 16s ease-out infinite}"
                 "@keyframes tl{0%{opacity:0;transform:translateX(-6px)}3%,90%{opacity:1;transform:none}94%,100%{opacity:0}}")
    y = ty + 78
    for i, parts in enumerate(lines):
        svg, _ = seg(c, tx + 26, y, parts, size=13.5, cls="tl", style=f"animation-delay:{i*0.32:.2f}s")
        c.add(svg)
        y += 27 if i not in (1, 4, 8) else 34
    svg, xe = seg(c, tx + 26, y, [P("$ ", EMERALD, 700)], size=13.5)
    c.add(svg)
    c.add(f'<rect class="blink" x="{xe+1:.0f}" y="{y-12}" width="8" height="15" fill="{GOLD_L}"/>')

    facts = [
        ("pin", TEAL, "BASED IN", "Contai, West Bengal", "Studying in Punjab, India"),
        ("briefcase", GOLD, "NEXT STOP", "SDE Intern @ Broadridge", "Joining on 11 Jan 2027"),
        ("brain", VIOLET, "FOCUS", "Agentic AI · Backend", "Spring Boot · FastAPI · DevOps"),
        ("code", ORANGE, "DAILY RITUAL", "1 problem × 4 judges", "LeetCode · CF · AtCoder · CodeChef"),
    ]
    fx, fw, fh, gap = 640, 310, 91, 15
    for i, (ic, col, eb, t1, t2) in enumerate(facts):
        yy = ty + i * (fh + gap)
        c.add(f'<g class="fl" style="animation-delay:-{i*1.4:.1f}s;animation-duration:{7+i}s">'
              + c.glass(fx, yy, fw, fh, r=18, tint=col, delay=i * 1.7)
              + icon_badge(c, fx + 42, yy + fh / 2, 22, ic, col)
              + c.text(fx + 80, yy + 28, eb, "mono", 700, 10.5, col if col != GOLD else GOLD_L, ls=2)
              + c.text(fx + 80, yy + 52, t1, "sans", 700, 16.5, INK)
              + c.text(fx + 80, yy + 73, t2, "sans", 400, 13, MUTED)
              + "</g>")
    return c


# ======================================================================= JOURNEY
def journey():
    nodes = [
        ("SCHOOL", "Contai Public School", "ICSE 96.20% and ISC 94.75% in Contai, West Bengal.", TEAL, "school", False),
        ("2023", "B.Tech CSE @ LPU", "Began Computer Science at Lovely Professional University, Punjab. CGPA 9.11.", VIOLET, "cap", False),
        ("APR 2024", "Inter-University Hackathons", "Multiple podium finishes for rapid MVPs, RAG pipelines and cloud-native builds.", CYAN, "medal", False),
        ("JUN 2024", "DSA in Java · Apna College", "Locked in Java and DSA, the base for 650+ LeetCode solves.", ORANGE, "code", False),
        ("FEB 2025", "Web-A-Thon Champion", "1st place and ₹1,00,000 for HygieiaAI, a multi-agent healthcare system.", GOLD, "trophy", False),
        ("JUL 2025", "TechForge '25 · 2nd Runner-Up", "₹5,00,000 seed backing for a high-concurrency cloud architecture.", AMBER, "rocket", False),
        ("JUL 2025", "ML Made Easy · LPU", "Tuned a multi-disease prediction model to about 94% accuracy.", LIME, "brain", False),
        ("SEP 2025", "NPTEL · IIT Guwahati", "Certified in Machine Learning and Deep Learning.", PINK, "spark", False),
        ("NOV 2026", "Placed at Broadridge", "Cleared every round of the on-campus drive for the SDE role.", EMERALD, "star", False),
        ("11 JAN 2027", "Joining Broadridge · SDE Intern", "Day one of the internship. The next chapter starts here.", GOLD, "briefcase", True),
        ("2027", "B.Tech CSE Graduation", "Class of 2027, Lovely Professional University.", BLUE, "cap", False),
    ]
    top, step, ch, cw = 200, 98, 116, 410
    W = 1000
    H = top + step * (len(nodes) - 1) + ch + 60
    c = base(W, H, 31, (GOLD, VIOLET, TEAL, ROSE), "Journey timeline",
             blobs=[(VIOLET, 120, 300, 380, .38), (GOLD, 880, H * 0.45, 420, .42), (TEAL, 150, H * 0.8, 340, .26), (ROSE, 860, H - 120, 300, .24)])
    head(c, 62, "02 · JOURNEY", "THE ROAD SO FAR", "From Contai to Broadridge, one milestone at a time.")
    sx, y0, y1 = 500, top - 10, H - 50
    c.add(f'<path d="M{sx} {y0} V{y1}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="2"/>')
    L = y1 - y0
    c.add(f'<path d="M{sx} {y0} V{y1}" stroke="{CHAMP}" stroke-width="3" stroke-linecap="round" stroke-dasharray="120 {L:.0f}" filter="url(#softglow)">'
          f'<animate attributeName="stroke-dashoffset" from="120" to="-{L:.0f}" dur="7s" repeatCount="indefinite"/></path>')
    for i, (date, title, desc, col, ic, hi) in enumerate(nodes):
        cy = top + ch / 2 + i * step
        left = i % 2 == 0
        x = sx - 40 - cw if left else sx + 40
        yy = cy - ch / 2
        e1, e2 = (x + cw, sx) if left else (sx, x)
        c.add(f'<path d="M{e1} {cy} H{e2}" stroke="{col}" stroke-opacity=".7" stroke-dasharray="3 4"/>')
        g = c.glass(x, yy, cw, ch, r=18, tint=col, delay=i * 0.8, strong=hi, glow=GOLD if hi else None)
        pill, pw = date_pill(c, x + 22, yy + 18, date, col)
        tf = "url(#gold)" if hi else INK
        body, _ = c.para(x + 22, yy + 86, desc, "sans", 400, 13.5, MUTED, cw - 44, 1.45)
        inner = g + pill + c.text(x + 22, yy + 66, title, "sans", 700, fit(c, title, "sans", 700, cw - 70, 18.5), tf) + body
        inner += icon(ic, x + cw - 44, yy + 16, 22, col if col != GOLD else GOLD_L)
        if hi:
            nb, _ = date_pill(c, x + 30 + pw, yy + 18, "NEXT", ROSE)
            inner += f'<g class="glow">{nb}</g>'
        c.add(f'<g class="fl" style="animation-delay:-{i*0.9:.1f}s;animation-duration:{8 + i % 3}s">{inner}</g>')
        c.add(f'<circle cx="{sx}" cy="{cy}" r="11" fill="{BLACK}" stroke="{col}" stroke-width="2"/>')
        c.add(f'<circle cx="{sx}" cy="{cy}" r="5" fill="{col}"/>')
        c.add(f'<circle class="pulse" cx="{sx}" cy="{cy}" r="5" fill="{col}" style="animation-delay:{i*0.3:.1f}s"/>')
    return c


# ======================================================================= HALL OF FAME
def hall_of_fame():
    W, H = 1000, 744
    c = base(W, H, 41, (GOLD, AMBER, ROSE, VIOLET), "Hall of Fame",
             blobs=[(GOLD, 500, 340, 420, .5), (AMBER, 120, 560, 300, .3), (ROSE, 900, 200, 280, .25), (VIOLET, 860, 640, 300, .3)], dust=40)
    head(c, 62, "03 · HALL OF FAME", "TROPHIES & HONORS", "₹6,00,000+ in prizes and seed funding across national hackathons.")
    cards = [
        (50, 214, 280, 356, AMBER, "rocket", "2ND RUNNER-UP", "TechForge '25", "₹5,00,000", "SEED INVESTMENT", "JUL 2025",
         "Seed backing in SMG for a high-concurrency cloud architecture."),
        (360, 184, 280, 386, GOLD, "trophy", "1ST PLACE · CHAMPION", "Web-A-Thon by OnDemand", "₹1,00,000", "WINNING PRIZE", "FEB 2025",
         "HygieiaAI: multi-agent healthcare on Gemini 2.0 Flash, under 2 s per request."),
        (670, 214, 280, 356, CYAN, "medal", "MULTIPLE PODIUMS", "Inter-University Hackathons", "Multiple", "PODIUM FINISHES", "APR 2024",
         "Rapid MVPs, autonomous RAG pipelines and cloud-native reliability."),
    ]
    for i, (x, y, w, h, col, ic, rank, ev, prize, plab, date, desc) in enumerate(cards):
        champ = col == GOLD
        cx = x + w / 2
        out = c.glass(x, y, w, h, r=24, tint=col, delay=i * 1.5, strong=champ, glow=GOLD if champ else None)
        out += icon_badge(c, cx, y + 70, 38 if champ else 34, ic, col if not champ else GOLD_L, isize=38 if champ else 34)
        out += c.text(cx, y + 136, rank, "mono", 700, 11, col if not champ else GOLD_L, "middle", ls=2.2)
        out += c.text(cx, y + 164, ev, "sans", 700, fit(c, ev, "sans", 700, w - 40, 19), INK, "middle")
        out += c.text(cx, y + 212, prize, "sans", 700, fit(c, prize, "sans", 700, w - 40, 38), "url(#gold)", "middle")
        out += c.text(cx, y + 234, plab, "mono", 700, 10, DIM, "middle", ls=2)
        body, _ = c.para(cx, y + 266, desc, "sans", 400, 13, MUTED, w - 44, 1.45, "middle")
        out += body
        pill, _ = date_pill(c, cx, y + h - 40, date, col, anchor="middle")
        out += pill
        c.add(f'<g class="fl" style="animation-delay:-{i*2:.0f}s;animation-duration:{7+i}s">{out}</g>')
    # sparkles around the champion
    rng = c.rng
    for k in range(9):
        sx_ = rng.uniform(340, 660)
        sy_ = rng.uniform(170, 300)
        s_ = rng.uniform(5, 9)
        c.add(f'<path class="glow" style="animation-delay:-{rng.uniform(0,3.6):.1f}s;animation-duration:{rng.uniform(2.4,4.2):.1f}s" '
              f'd="M{sx_} {sy_-s_} L{sx_+s_*0.25} {sy_-s_*0.25} L{sx_+s_} {sy_} L{sx_+s_*0.25} {sy_+s_*0.25} L{sx_} {sy_+s_} '
              f'L{sx_-s_*0.25} {sy_+s_*0.25} L{sx_-s_} {sy_} L{sx_-s_*0.25} {sy_-s_*0.25}Z" fill="{CHAMP}"/>')
    # ribbon
    ry = 616
    c.add(c.glass(50, ry, 900, 86, r=43, tint=GOLD, delay=3))
    stats = [("₹6L+", "PRIZES & SEED FUNDING", "trophy", GOLD_L), ("14+", "INDUSTRY-LEVEL PROJECTS", "layers", VIOLET),
             (f"{S['leetcode']['solved']}", "LEETCODE PROBLEMS SOLVED", "code", ORANGE)]
    for i, (v, lab, ic, col) in enumerate(stats):
        x = 50 + i * 300
        c.add(icon_badge(c, x + 58, ry + 43, 22, ic, col, spin=False))
        c.add(c.text(x + 94, ry + 46, v, "sans", 700, 26, "url(#gold)"))
        c.add(c.text(x + 94, ry + 66, lab, "mono", 700, 9.5, MUTED, ls=1.2))
        if i:
            c.add(f'<path d="M{x} {ry+20} V{ry+66}" stroke="{GOLD}" stroke-opacity=".35"/>')
    return c


# ======================================================================= CERTIFICATIONS
def certs():
    W, H = 1000, 400
    c = base(W, H, 51, (VIOLET, ORANGE, TEAL, GOLD), "Certifications",
             blobs=[(VIOLET, 180, 260, 300, .38), (ORANGE, 500, 360, 260, .25), (TEAL, 840, 240, 300, .3), (GOLD, 500, 40, 300, .3)])
    head(c, 58, "04 · CREDENTIALS", "CERTIFICATIONS")
    items = [
        ("IITG", VIOLET, "Machine Learning & Deep Learning", "IIT GUWAHATI · NPTEL", "SEP 2025", None),
        ("AC", ORANGE, "Data Structures & Algorithms in Java", "APNA COLLEGE", "JUN 2024", None),
        ("LPU", TEAL, "Machine Learning Made Easy", "LOVELY PROFESSIONAL UNIVERSITY", "JUL 2025", "Multi-disease model · ~94% accuracy"),
    ]
    for i, (mono_, col, title, issuer, date, note) in enumerate(items):
        x, y, w, h = 50 + i * 310, 150, 280, 210
        out = c.glass(x, y, w, h, r=22, tint=col, delay=i * 1.2)
        cx, cy = x + 56, y + 58
        out += f'<circle cx="{cx}" cy="{cy}" r="32" fill="{col}" fill-opacity=".15" stroke="{col}" stroke-opacity=".7"/>'
        out += f'<g class="spin" style="animation-duration:{12+i*3}s"><circle cx="{cx}" cy="{cy}" r="39" fill="none" stroke="{GOLD_L}" stroke-opacity=".6" stroke-dasharray="1.5 5"/></g>'
        out += c.text(cx, cy + 6, mono_, "display", 700, fit(c, mono_, "display", 700, 46, 17), "url(#gold)", "middle")
        pill, _ = date_pill(c, x + w - 20, y + 24, date, col, anchor="end")
        out += pill
        lines = c.wrap(title, "sans", 700, 17, w - 44)
        for k, ln in enumerate(lines):
            out += c.text(x + 22, y + 124 + k * 23, ln, "sans", 700, 17, INK)
        yb = y + 124 + len(lines) * 23
        out += c.text(x + 22, yb + 2, issuer, "mono", 700, fit(c, issuer, "mono", 700, w - 44, 10, 1.2), col if col != VIOLET else "#B79CFF", ls=1.2)
        if note:
            out += c.text(x + 22, yb + 24, note, "sans", 400, 12.5, MUTED)
        c.add(f'<g class="fl" style="animation-delay:-{i*1.6:.1f}s;animation-duration:{7+i}s">{out}</g>')
    return c


# ======================================================================= FLAGSHIP PROJECTS
def _project_text(c, x, colw, eyebrow, title, sub, bullets, chips, chip_cols, cta):
    c.add(f'<path d="M{x} 66 H{x+28}" stroke="{GOLD}" stroke-width="1.5"/>')
    c.add(c.text(x + 38, 70, eyebrow, "mono", 700, 11.5, GOLD_L, ls=2.6))
    ts = fit(c, title, "display", 900, colw, 40, 1.5)
    c.add(c.text(x, 70 + ts + 14, title, "display", 900, ts, "url(#gold)", ls=1.5))
    y = 70 + ts + 46
    body, h = c.para(x, y, sub, "sans", 500, 16, INK, colw, 1.45)
    c.add(body)
    y += h + 18
    for i, (ic, col, bt, bd) in enumerate(bullets):
        c.add(icon_badge(c, x + 20, y + 4, 19, ic, col, spin=False, isize=19))
        c.add(c.text(x + 52, y, bt, "sans", 700, 15.5, INK))
        b, bh = c.para(x + 52, y + 21, bd, "sans", 400, 13.5, MUTED, colw - 52, 1.45)
        c.add(b)
        y += 21 + bh + 14
    y += 4
    svg, ch = c.chips_row(x, y, chips, colw, chip_cols, size=11.5, h=27, rowgap=8)
    c.add(svg)
    y += ch + 22
    pill, pw = c.pill(x, y, cta, "mono", 700, 11.5, GOLD_L, 34, 1.6)
    c.add(f'<g class="fl" style="animation-duration:5s">{pill}</g>')
    return y + 34


def _window(c, x, y, w, h, title, tint):
    c.add(c.glass(x, y, w, h, r=22, tint=tint, strong=True, delay=1))
    c.add(f'<path d="M{x+1} {y+42} H{x+w-1}" stroke="#FFFFFF" stroke-opacity=".09"/>')
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        c.add(f'<circle cx="{x + 22 + i*16}" cy="{y + 21}" r="5" fill="{col}"/>')
    c.add(c.text(x + w / 2, y + 26, title, "mono", 400, 12, DIM, "middle"))
    live, _ = c.pill(x + w - 16, y + 9, "LIVE", "mono", 700, 9.5, EMERALD, 24, 1.4, dot=EMERALD, pad=10, glassy=False)
    # right-align: re-render at computed x
    lw = c.tw("LIVE", "mono", 700, 9.5, 1.4) + 20 + 18
    live, _ = c.pill(x + w - 16 - lw, y + 9, "LIVE", "mono", 700, 9.5, EMERALD, 24, 1.4, dot=EMERALD, pad=10, glassy=False)
    c.add(live)


def autoforge():
    W, H = 1000, 640
    c = base(W, H, 61, (CYAN, VIOLET, GOLD, EMERALD), "AutoForge ML Studio",
             blobs=[(CYAN, 860, 160, 380, .32), (VIOLET, 120, 560, 360, .36), (GOLD, 250, 80, 300, .32), (EMERALD, 780, 600, 280, .22)])
    bullets = [
        ("bolt", CYAN, "Decoupled AutoML architecture", "Sub-1-minute cloud deployments through Google Vertex AI pipelines."),
        ("brain", VIOLET, "Multi-LLM dataset profiler", "Automated EDA and hyperparameter tuning with GPT-4, Claude 3.5 and Gemini 2.0."),
        ("chart", EMERALD, "Observability & 3D visuals", "GitHub Actions CI/CD, live training lineage and Three.js 3D model views."),
    ]
    chips = ["Next.js 15", "React 19", "TypeScript", "Vertex AI", "LangChain", "GPT-4", "Claude 3.5", "Gemini 2.0", "Firebase", "Three.js"]
    cols = [INK, CYAN, BLUE, BLUE, EMERALD, TEAL, AMBER, VIOLET, AMBER, INK]
    _project_text(c, 50, 450, "05 · FLAGSHIP BUILD · 01", "AUTOFORGE ML STUDIO",
                  "Low-code cloud AutoML on Google Vertex AI, tuned by a team of LLM agents.",
                  bullets, chips, cols, "TAP TO OPEN THE REPO  ›")
    # visual: pipeline window
    vx, vy, vw, vh = 540, 50, 410, 540
    _window(c, vx, vy, vw, vh, "autoforge · pipeline", CYAN)
    steps = [("db", CYAN, "Dataset upload", "CSV · Parquet · Firestore"),
             ("brain", VIOLET, "LLM profiler", "GPT-4 · Claude 3.5 · Gemini 2.0"),
             ("cloud", BLUE, "AutoML training", "Google Vertex AI pipelines"),
             ("rocket", EMERALD, "Deploy endpoint", "Live in under a minute")]
    n = len(steps)
    sx, sw, sh = vx + 30, vw - 60, 58
    for k, (ic, col, t1, t2) in enumerate(steps):
        yy = vy + 66 + k * 84
        c.add(f'<rect x="{sx}" y="{yy}" width="{sw}" height="{sh}" rx="14" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".35"/>')
        c.add(f'<rect x="{sx}" y="{yy}" width="{sw}" height="{sh}" rx="14" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.6" opacity="0">{cycle("opacity", n, k, 8)}</rect>')
        c.add(icon_badge(c, sx + 30, yy + sh / 2, 17, ic, col, spin=False, isize=17))
        c.add(c.text(sx + 58, yy + 25, t1, "sans", 700, 14.5, INK))
        c.add(c.text(sx + 58, yy + 44, t2, "mono", 400, 11, MUTED))
        # status: spinner while active, tick otherwise
        ccx, ccy = sx + sw - 26, yy + sh / 2
        c.add(f'<g opacity="0">{cycle("opacity", n, k, 8)}<g class="spin" style="animation-duration:1.2s">'
              f'<circle cx="{ccx}" cy="{ccy}" r="9" fill="none" stroke="{col}" stroke-width="2.4" stroke-dasharray="14 40" stroke-linecap="round"/></g></g>')
        c.add(f'<g opacity="1">{cycle("opacity", n, k, 8, on="0", off="1")}'
              f'<circle cx="{ccx}" cy="{ccy}" r="9" fill="{EMERALD}" fill-opacity=".18" stroke="{EMERALD}" stroke-opacity=".7"/>'
              f'<path d="M{ccx-4} {ccy} l3 3 l5.5 -6" fill="none" stroke="{EMERALD}" stroke-width="2" stroke-linecap="round"/></g>')
        if k < n - 1:
            px = sx + 30
            c.add(f'<path d="M{px} {yy+sh} V{yy+84}" stroke="{col}" stroke-opacity=".5" stroke-dasharray="2 4"/>')
            c.add(packet(f"M{px} {yy+sh} V{yy+84}", 2.0, k * 0.5, col, 2.6))
    # accuracy chart
    cx0, cy0, cw0, chh = vx + 30, vy + 412, vw - 60, 100
    c.add(f'<rect x="{cx0}" y="{cy0}" width="{cw0}" height="{chh}" rx="14" fill="#000" fill-opacity=".25" stroke="#FFFFFF" stroke-opacity=".08"/>')
    c.add(c.text(cx0 + 16, cy0 + 22, "VALIDATION ACCURACY", "mono", 700, 9.5, DIM, ls=1.6))
    c.add(c.text(cx0 + cw0 - 16, cy0 + 22, "best run", "mono", 400, 10, EMERALD, "end"))
    pts = [0.30, 0.42, 0.40, 0.55, 0.61, 0.66, 0.70, 0.74, 0.79, 0.83, 0.86, 0.90, 0.92, 0.94]
    px_ = lambda i: cx0 + 16 + i * (cw0 - 32) / (len(pts) - 1)
    py_ = lambda v: cy0 + chh - 14 - v * (chh - 44)
    d = "M" + " L".join(f"{px_(i):.1f} {py_(v):.1f}" for i, v in enumerate(pts))
    area = d + f" L{px_(len(pts)-1):.1f} {cy0+chh-12} L{px_(0):.1f} {cy0+chh-12}Z"
    ag = c.grad_linear([(0, EMERALD, 0.35), (1, EMERALD, 0)], 0, 0, 0, 1)
    c.add(f'<path d="{area}" fill="url(#{ag})"/>')
    c.add(f'<path d="{d}" fill="none" stroke="{EMERALD}" stroke-width="2.2" stroke-dasharray="600" stroke-linejoin="round">'
          f'<animate attributeName="stroke-dashoffset" values="600;0;0" keyTimes="0;.45;1" dur="8s" repeatCount="indefinite"/></path>')
    c.add(f'<circle r="4" fill="{CHAMP}" filter="url(#softglow)"><animateMotion dur="8s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.45;1" calcMode="linear" path="{d}"/></circle>')
    # floating model chips
    for i, (lab, col, xx, yy) in enumerate([("GPT-4", TEAL, vx + vw - 116, vy + 125), ("Claude 3.5", AMBER, vx + vw - 150, vy + 209), ("Gemini 2.0", VIOLET, vx + vw - 166, vy + 293)]):
        svg, _ = c.chip(xx, yy, lab, col, "mono", 700, 11, 26)
        c.add(f'<g class="fl" style="animation-delay:-{i*1.7:.1f}s">{svg}</g>')
    return c


def splitit():
    W, H = 1000, 660
    c = base(W, H, 71, (AMBER, PINK, BLUE, GOLD), "SplitIT",
             blobs=[(AMBER, 160, 160, 360, .32), (PINK, 860, 560, 340, .3), (BLUE, 120, 600, 300, .26), (GOLD, 820, 80, 320, .34)])
    bullets = [
        ("layers", AMBER, "Dual-algorithm settlement engine", "Greedy netting plus exact-match pruning keeps group payments to a minimum."),
        ("scroll", PINK, "Vision receipt OCR & agent", "Sub-2-second receipt ingestion with GPT-4o-mini Vision and a CrewAI spending assistant."),
        ("cloud", BLUE, "GitOps infrastructure", "Production Kubernetes with Prometheus custom metrics and Grafana dashboards."),
    ]
    chips = ["Next.js 16", "React 19", "TypeScript", "Prisma", "PostgreSQL (Neon)", "CrewAI", "LangGraph", "GPT-4o Vision", "Docker", "Kubernetes", "Grafana"]
    cols = [INK, CYAN, BLUE, TEAL, BLUE, ROSE, EMERALD, TEAL, BLUE, BLUE, ORANGE]
    _project_text(c, 500, 450, "05 · FLAGSHIP BUILD · 02", "SPLITIT",
                  "Smart expense splitting and settlement, with a multi-agent financial AI. Live at splitsj.vercel.app.",
                  bullets, chips, cols, "TAP FOR REPO · LIVE APP BELOW  ›")
    vx, vy, vw, vh = 50, 50, 410, 560
    _window(c, vx, vy, vw, vh, "splitit · settle up", AMBER)
    # settlement graph
    gcx, gcy, R = vx + vw / 2, vy + 190, 112
    names = ["A", "B", "C", "D", "E"]
    pos = [(gcx + R * math.cos(-math.pi / 2 + i * 2 * math.pi / 5), gcy + R * math.sin(-math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    before = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 0), (4, 1), (1, 2), (3, 4)]
    after = [(1, 0), (3, 2), (4, 0)]
    T = 9
    bg = "".join(f'<path d="M{pos[a][0]:.1f} {pos[a][1]:.1f} L{pos[b][0]:.1f} {pos[b][1]:.1f}" stroke="{ROSE}" stroke-opacity=".55" stroke-dasharray="4 5"/>' for a, b in before)
    c.add(f'<g opacity="1"><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.42;.5;.92;1" dur="{T}s" repeatCount="indefinite"/>{bg}</g>')
    ag_ = ""
    for j, (a, b) in enumerate(after):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ag_ += f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{GOLD_L}" stroke-width="2.6" stroke-linecap="round"/>'
        ag_ += packet(f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}", 1.6, j * 0.5, CHAMP, 3.2)
    c.add(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.42;.5;.92;1" dur="{T}s" repeatCount="indefinite"/>{ag_}</g>')
    cols5 = [VIOLET, CYAN, EMERALD, PINK, AMBER]
    for i, (px, py) in enumerate(pos):
        c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="21" fill="{BLACK}" stroke="{cols5[i]}" stroke-width="2"/>')
        c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="21" fill="{cols5[i]}" fill-opacity=".16"/>')
        c.add(c.text(px, py + 6, names[i], "sans", 700, 16, INK, "middle"))
    lab_b = c.text(gcx, vy + 340, "BEFORE · 8 PAYMENTS", "mono", 700, 11, ROSE, "middle", ls=2)
    lab_a = c.text(gcx, vy + 340, "AFTER NETTING · 3 PAYMENTS", "mono", 700, 11, GOLD_L, "middle", ls=2)
    c.add(f'<g><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.42;.5;.92;1" dur="{T}s" repeatCount="indefinite"/>{lab_b}</g>')
    c.add(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.42;.5;.92;1" dur="{T}s" repeatCount="indefinite"/>{lab_a}</g>')
    # receipt scanner
    rx_, ry_, rw_, rh_ = vx + 30, vy + 372, 150, 160
    c.add(f'<rect x="{rx_}" y="{ry_}" width="{rw_}" height="{rh_}" rx="12" fill="{INK}" fill-opacity=".9"/>')
    c.add(c.text(rx_ + 14, ry_ + 24, "RECEIPT", "mono", 700, 10, BLACK, ls=2))
    for k in range(6):
        ww = [96, 70, 110, 84, 60, 100][k]
        c.add(f'<rect x="{rx_+14}" y="{ry_ + 38 + k*16}" width="{ww}" height="5" rx="2.5" fill="{BLACK}" fill-opacity=".28"/>')
    c.add(f'<rect x="{rx_+14}" y="{ry_+rh_-22}" width="56" height="7" rx="3" fill="{BLACK}" fill-opacity=".6"/>')
    sg = c.grad_linear([(0, AMBER, 0), (0.5, AMBER, 0.9), (1, AMBER, 0)], 0, 0, 1, 0)
    c.add(f'<rect x="{rx_-6}" y="{ry_}" width="{rw_+12}" height="3" rx="1.5" fill="url(#{sg})" filter="url(#softglow)">'
          f'<animate attributeName="y" values="{ry_};{ry_+rh_-3};{ry_}" dur="3s" repeatCount="indefinite"/></rect>')
    # extracted fields
    fx = rx_ + rw_ + 22
    fields = [("MERCHANT", "detected", TEAL), ("TOTAL", "parsed", AMBER), ("SPLIT", "4 ways", PINK), ("TIME", "< 2 s", EMERALD)]
    for k, (a, b, col) in enumerate(fields):
        yy = ry_ + 4 + k * 40
        c.add(f'<rect x="{fx}" y="{yy}" width="178" height="32" rx="10" fill="{col}" fill-opacity=".09" stroke="{col}" stroke-opacity=".45">'
              f'<animate attributeName="fill-opacity" values=".05;.22;.05" dur="3s" begin="{k*0.4}s" repeatCount="indefinite"/></rect>')
        c.add(c.text(fx + 12, yy + 21, a, "mono", 700, 10, col, ls=1.4))
        c.add(c.text(fx + 166, yy + 21, b, "sans", 500, 12.5, INK, "end"))
    return c


# ======================================================================= BUTTONS / TILES / BANNERS
def button(label, sub, ic, color, seed=5, w=460, h=84):
    c = Card(w, h, seed=seed, rx=h / 2, title=label)
    c.background(blobs=[(color, w * 0.15, h / 2, 160, .45), (GOLD, w * 0.85, h / 2, 160, .3)], dust=6, grid=False)
    c._frame = False
    c.add(c.glass(6, 6, w - 12, h - 12, r=(h - 12) / 2, tint=color, delay=1, strong=True))
    c.add(icon_badge(c, 48, h / 2, 22, ic, color, spin=True, isize=22))
    c.add(c.text(86, h / 2 - 3, label, "sans", 700, 18, INK))
    c.add(c.text(86, h / 2 + 18, sub, "mono", 400, fit(c, sub, "mono", 400, w - 160, 12), MUTED))
    ax = w - 50
    c.add(f'<g class="fl" style="animation-duration:2.4s"><circle cx="{ax}" cy="{h/2}" r="17" fill="{GOLD}" fill-opacity=".14" stroke="{GOLD_L}" stroke-opacity=".6"/>'
          f'<path d="M{ax-6} {h/2} H{ax+6} M{ax+1} {h/2-5} L{ax+6} {h/2} L{ax+1} {h/2+5}" fill="none" stroke="{GOLD_L}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return c


def tile(name, desc, lang, lang_col, metric, ic, accent, seed):
    w, h = 480, 214
    c = Card(w, h, seed=seed, rx=26, title=name)
    c.background(blobs=[(accent, 60, 40, 220, .45), (GOLD, 440, 200, 200, .3)], dust=8, grid=False)
    c._frame = False
    c.add(icon_badge(c, 56, 62, 26, ic, accent, isize=25))
    c.add(c.text(98, 56, name, "sans", 700, fit(c, name, "sans", 700, w - 200, 22), INK))
    c.add(c.text(98, 78, "github.com/Sayandip-Jana-1018", "mono", 400, 10.5, DIM))
    mw = c.tw(metric, "mono", 700, 10, 1.4) + 24
    pill, _ = date_pill(c, w - 26, 34, metric, accent, anchor="end")
    c.add(f'<g class="glow" style="animation-duration:4s">{pill}</g>')
    body, _ = c.para(30, 122, desc, "sans", 400, 14.5, MUTED, w - 60, 1.5)
    c.add(body)
    c.add(f'<circle cx="38" cy="{h-34}" r="6" fill="{lang_col}"/>')
    c.add(c.text(52, h - 29, lang, "mono", 700, 12, INK))
    c.add(c.text(w - 30, h - 29, "open repo ›", "mono", 700, 12, GOLD_L, "end"))
    c.add(soft_frame(c, accent))
    return c


def banner(eyebrow, title, sub, accents, seed):
    W, H = 1000, 170
    c = base(W, H, seed, accents, title, blobs=[(accents[0], 200, 90, 260, .38), (accents[1], 800, 80, 260, .34)], dust=10)
    head(c, 52, eyebrow, title, sub, size=34)
    return c


# ======================================================================= ARSENAL
def arsenal():
    W = 1000
    groups = [
        ("Languages & Core CS", "code", ORANGE,
         [("Java", ORANGE), ("Python", BLUE), ("TypeScript", BLUE), ("JavaScript", LIME), ("SQL", CYAN),
          ("Data Structures & Algorithms", GOLD), ("System Design", GOLD), ("OOPs", GOLD), ("DBMS", GOLD),
          ("Operating Systems", GOLD), ("Computer Networks", GOLD)]),
        ("GenAI & Autonomous Agents", "brain", VIOLET,
         [("LangChain", EMERALD), ("LangGraph", EMERALD), ("CrewAI", ROSE), ("RAG Pipelines", CYAN), ("Chroma DB", PINK),
          ("OpenAI GPT-4o", TEAL), ("Gemini 2.0", VIOLET), ("Claude 3.5 Sonnet", AMBER)]),
        ("Full-Stack & Backend", "layers", CYAN,
         [("Spring Boot", LIME), ("Next.js 15/16", INK), ("React 19", CYAN), ("FastAPI", TEAL), ("Node.js", EMERALD),
          ("Prisma", BLUE), ("Tailwind CSS", CYAN), ("Three.js", INK), ("REST APIs", GOLD)]),
        ("Databases, Cloud & Big Data", "db", EMERALD,
         [("PostgreSQL", BLUE), ("MongoDB", EMERALD), ("Firebase", AMBER), ("Supabase", EMERALD), ("MySQL", BLUE),
          ("AWS", ORANGE), ("Google Vertex AI", BLUE), ("Apache Spark", ORANGE), ("Apache Hadoop", CYAN)]),
        ("DevOps, CI/CD & Observability", "cloud", ROSE,
         [("Docker", BLUE), ("Kubernetes", BLUE), ("GitHub Actions", INK), ("Jenkins", ROSE), ("Terraform", VIOLET),
          ("Prometheus", ORANGE), ("Grafana", ORANGE), ("Git", ORANGE), ("Linux", AMBER)]),
    ]
    # measure panels
    pw2, gap = 440, 20
    tmp = Card(10, 10)
    def ph(items, w):
        _, hh = tmp.chips_row(0, 0, [t for t, _ in items], w - 48, None, size=12, h=28, rowgap=9)
        return 86 + hh + 26
    rows = [(groups[0], groups[1]), (groups[2], groups[3]), (groups[4],)]
    oy = 345           # orbit centre
    top = 560
    heights = []
    for r in rows:
        if len(r) == 2:
            heights.append(max(ph(g[3], pw2) for g in r))
        else:
            heights.append(ph(r[0][3], 900))
    H = top + sum(heights) + gap * (len(rows) - 1) + 50
    c = base(W, H, 81, (VIOLET, GOLD, CYAN, ROSE), "Technical arsenal",
             blobs=[(VIOLET, 500, oy, 420, .38), (GOLD, 120, H * 0.6, 360, .34), (CYAN, 880, H * 0.7, 340, .26), (ROSE, 500, H - 80, 320, .22)])
    head(c, 62, "07 · ARSENAL", "TECHNICAL ARSENAL", "The tools I reach for, from the first commit to the Grafana dashboard.")
    # ---- orbit system
    cx = 500
    orbits = [
        (120, 0.40, 26, ["Java", "Python", "TypeScript", "SQL"], [ORANGE, BLUE, BLUE, CYAN]),
        (240, 0.40, 40, ["Spring Boot", "FastAPI", "Next.js", "React", "Node.js", "Prisma"], [LIME, TEAL, INK, CYAN, EMERALD, BLUE]),
        (370, 0.36, 58, ["LangGraph", "CrewAI", "Docker", "Kubernetes", "AWS", "PostgreSQL", "Vertex AI", "Grafana"],
         [EMERALD, ROSE, BLUE, BLUE, ORANGE, BLUE, VIOLET, ORANGE]),
    ]
    for k, (rx, f, dur, labels, cols) in enumerate(orbits):
        ry = rx * f
        c.add(f'<ellipse cx="{cx}" cy="{oy}" rx="{rx}" ry="{ry:.1f}" fill="none" stroke="{GOLD}" stroke-opacity="{.4 - k*0.08:.2f}" stroke-dasharray="{"2 6" if k % 2 else "1 0"}"/>')
        path = f"M{cx - rx} {oy} a{rx} {ry:.1f} 0 1 {'1' if k % 2 == 0 else '0'} {2*rx} 0 a{rx} {ry:.1f} 0 1 {'1' if k % 2 == 0 else '0'} {-2*rx} 0"
        for i, (lab, col) in enumerate(zip(labels, cols)):
            w = c.tw(lab, "mono", 700, 11.5, 0.3) + 38
            chip, _ = c.chip(-w / 2, -14, lab, col, "mono", 700, 11.5, 28)
            begin = -dur * i / len(labels)
            c.add(f'<g>{chip}<animateMotion dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite" path="{path}"/></g>')
    # core
    cg = c.grad_radial([(0, GOLD, .55), (1, GOLD, 0)])
    c.add(f'<circle class="glow" cx="{cx}" cy="{oy}" r="96" fill="url(#{cg})"/>')
    c.add(c.glass(cx - 54, oy - 54, 108, 108, r=54, tint=GOLD, strong=True))
    c.add(f'<g class="spin" style="animation-duration:12s"><circle cx="{cx}" cy="{oy}" r="66" fill="none" stroke="{GOLD_L}" stroke-opacity=".7" stroke-dasharray="40 14 4 14"/></g>')
    c.add(c.text(cx, oy + 12, "SJ", "display", 900, 36, "url(#gold)", "middle", ls=2))
    # ---- panels
    y = top
    for ri, r in enumerate(rows):
        hh = heights[ri]
        for j, (title, ic, col, items) in enumerate(r):
            pw = pw2 if len(r) == 2 else 900
            x = 50 + j * (pw2 + gap)
            c.add(c.glass(x, y, pw, hh, r=22, tint=col, delay=ri * 1.3 + j))
            c.add(icon_badge(c, x + 44, y + 44, 21, ic, col, isize=21))
            c.add(c.text(x + 80, y + 40, title, "sans", 700, 18, INK))
            c.add(c.text(x + 80, y + 60, f"{len(items)} TOOLS", "mono", 700, 10, col if col not in (VIOLET,) else "#B79CFF", ls=2))
            svg, _ = c.chips_row(x + 24, y + 86, [t for t, _ in items], pw - 48, [cc for _, cc in items], size=12, h=28, rowgap=9)
            c.add(svg)
        y += hh + gap
    return c


# ======================================================================= ARCHITECTURE
def architecture():
    W = 1000
    layers = [
        ("L1", "CLIENT & INTERACTIVE LAYER", CYAN, ["Next.js 16 · App Router", "React 19", "Tailwind CSS", "Three.js 3D"]),
        ("L2", "API & ROUTING MIDDLEWARE", VIOLET, ["FastAPI", "Spring Boot", "Node.js / Express", "Next.js Server Actions"]),
        ("L3", None, None, None),
        ("L4", "DATA PERSISTENCE & ANALYTICS", EMERALD, ["PostgreSQL · Neon / Supabase", "MongoDB", "Firestore", "MySQL", "Apache Spark", "Hadoop"]),
        ("L5", "GITOPS & CLOUD AUTOMATION", ROSE, ["Docker", "Kubernetes", "Jenkins", "GitHub Actions", "AWS", "Vertex AI", "Prometheus", "Grafana"]),
    ]
    split = [("AGENTIC & GENAI PIPELINES", PINK, ["LangGraph workflows", "CrewAI", "RAG", "Chroma DB", "GPT-4o", "Gemini 2.0"]),
             ("CORE SYSTEM ENGINES", AMBER, ["Greedy netting engine", "Async handlers", "Prisma ORM", "Type-safe schemas"])]
    top, bh, bh3, gap = 196, 94, 128, 42
    H = top + bh * 4 + bh3 + gap * 4 + 70
    c = base(W, H, 91, (CYAN, VIOLET, PINK, EMERALD), "System architecture blueprint",
             blobs=[(CYAN, 150, 220, 320, .3), (PINK, 850, 430, 320, .3), (EMERALD, 160, 720, 320, .26), (ROSE, 860, H - 120, 300, .26)])
    head(c, 62, "08 · ARCHITECTURE", "SYSTEM BLUEPRINT", "How my production builds are layered, from pixels to pods.")
    y = top
    ys = []
    for li, (tag, title, col, items) in enumerate(layers):
        if title is None:
            hw = (900 - 24) / 2
            for j, (t2, c2, it2) in enumerate(split):
                x = 50 + j * (hw + 24)
                c.add(c.glass(x, y, hw, bh3, r=18, tint=c2, delay=li + j))
                c.add(f'<rect x="{x}" y="{y+18}" width="4" height="{bh3-36}" rx="2" fill="{c2}"/>')
                c.add(c.text(x + 24, y + 32, f"L3{'ab'[j]}", "mono", 700, 11, c2, ls=1))
                c.add(c.text(x + 62, y + 32, t2, "mono", 700, 12.5, INK, ls=2))
                svg, _ = c.chips_row(x + 24, y + 52, it2, hw - 44, [c2] * len(it2), size=11.5, h=27, rowgap=8)
                c.add(svg)
            ys.append((y, bh3))
            y += bh3 + gap
            continue
        c.add(c.glass(50, y, 900, bh, r=18, tint=col, delay=li))
        c.add(f'<rect x="50" y="{y+18}" width="4" height="{bh-36}" rx="2" fill="{col}"/>')
        c.add(c.text(74, y + 32, tag, "mono", 700, 11, col, ls=1))
        c.add(c.text(108, y + 32, title, "mono", 700, 12.5, INK, ls=2))
        svg, _ = c.chips_row(74, y + 52, items, 850, [col] * len(items), size=11.5, h=27, rowgap=8)
        c.add(svg)
        c.add(f'<g class="spin" style="animation-duration:6s"><circle cx="{920}" cy="{y+28}" r="7" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="10 30"/></g>')
        ys.append((y, bh))
        y += bh + gap
    # connectors with travelling packets
    for k in range(len(ys) - 1):
        y1 = ys[k][0] + ys[k][1]
        y2 = ys[k + 1][0]
        for j, xx in enumerate([250, 500, 750]):
            col = [CYAN, GOLD_L, PINK][j]
            c.add(f'<path d="M{xx} {y1} V{y2}" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="2 4"/>')
            down = (j + k) % 2 == 0
            p = f"M{xx} {y1} V{y2}" if down else f"M{xx} {y2} V{y1}"
            c.add(packet(p, 1.6, (k * 0.37 + j * 0.53) % 1.6, col, 3))
        c.add(f'<path d="M{486} {(y1+y2)/2} h28" stroke="none"/>')
    return c


# ======================================================================= CP ARENA
def cp_arena():
    W, H = 1000, 720
    lc = S["leetcode"]
    rp = S["repos"]
    c = base(W, H, 101, (ORANGE, GOLD, TEAL, ROSE), "Algorithm arena",
             blobs=[(ORANGE, 220, 360, 360, .38), (GOLD, 820, 200, 360, .34), (TEAL, 760, 600, 300, .24), (ROSE, 120, 660, 260, .22)])
    head(c, 62, "09 · ALGORITHM ARENA", "PROBLEM SOLVING",
         f"{lc['solved']} problems on LeetCode, plus a fresh problem every day on four judges. All in Java.", maxw=760)
    # ring panel
    px, py, pw, ph_ = 50, 200, 430, 340
    c.add(c.glass(px, py, pw, ph_, r=24, tint=ORANGE, strong=True))
    rcx, rcy, R = px + 150, py + 170, 108
    C = 2 * math.pi * R
    c.add(f'<circle cx="{rcx}" cy="{rcy}" r="{R}" fill="none" stroke="#FFFFFF" stroke-opacity=".07" stroke-width="18"/>')
    parts = [(lc["easy"], TEAL), (lc["medium"], AMBER), (lc["hard"], ROSE)]
    tot = sum(p for p, _ in parts) or 1
    off = 0.0
    for val, col in parts:
        L = C * val / tot - 4
        c.add(f'<circle cx="{rcx}" cy="{rcy}" r="{R}" fill="none" stroke="{col}" stroke-width="18" stroke-linecap="butt" '
              f'transform="rotate({-90 + 360 * off / C:.2f} {rcx} {rcy})" stroke-dasharray="0 {C:.1f}">'
              f'<animate attributeName="stroke-dasharray" values="0 {C:.1f};{L:.1f} {C:.1f};{L:.1f} {C:.1f}" keyTimes="0;.18;1" dur="12s" repeatCount="indefinite"/></circle>')
        off += C * val / tot
    c.add(f'<g class="spin" style="animation-duration:5s"><circle cx="{rcx}" cy="{rcy}" r="{R+16}" fill="none" stroke="{GOLD_L}" stroke-opacity=".6" stroke-dasharray="30 {2*math.pi*(R+16)-30:.0f}" stroke-linecap="round"/></g>')
    c.add(c.text(rcx, rcy + 10, fmt(lc["solved"]), "display", 900, 46, "url(#gold)", "middle"))
    c.add(c.text(rcx, rcy + 34, "SOLVED", "mono", 700, 11, MUTED, "middle", ls=3))
    lx = px + 290
    for i, (lab, val, col) in enumerate([("EASY", lc["easy"], TEAL), ("MEDIUM", lc["medium"], AMBER), ("HARD", lc["hard"], ROSE)]):
        yy = py + 96 + i * 66
        c.add(c.text(lx, yy, lab, "mono", 700, 10.5, col, ls=2))
        c.add(c.text(lx, yy + 26, fmt(val), "sans", 700, 24, INK))
        bw = 110 * val / max(p for p, _ in parts)
        c.add(f'<rect x="{lx}" y="{yy+36}" width="110" height="4" rx="2" fill="#FFFFFF" fill-opacity=".08"/>')
        c.add(f'<rect x="{lx}" y="{yy+36}" width="{bw:.0f}" height="4" rx="2" fill="{col}"/>')
    # stat tiles
    stats = [("flame", ORANGE, str(lc["streak"]), "DAY STREAK"), ("chart", VIOLET, str(lc["active_days"]), "ACTIVE DAYS"),
             ("globe", CYAN, fmt(lc["ranking"]), "GLOBAL RANK")]
    for i, (ic, col, v, lab) in enumerate(stats):
        x = 500 + i * 153
        c.add(c.glass(x, py, 140, 120, r=20, tint=col, delay=i))
        c.add(icon_badge(c, x + 34, py + 36, 17, ic, col, spin=False, isize=17))
        c.add(c.text(x + 18, py + 88, v, "sans", 700, fit(c, v, "sans", 700, 108, 26), "url(#gold)"))
        c.add(c.text(x + 18, py + 106, lab, "mono", 700, 9.5, MUTED, ls=1.4))
    # daily arena
    c.add(c.text(500, py + 158, "DAILY ARENA", "mono", 700, 12, GOLD_L, ls=3))
    jp, jw = date_pill(c, 950, py + 142, "JAVA ONLY", ORANGE, anchor="end")
    c.add(f'<g class="glow">{jp}</g>')
    plats = [("LeetCode", ORANGE, "Daily problem · submitted twice", f"{rp['LeetCodeSj']} solutions"),
             ("Codeforces", BLUE, "One rated problem a day", f"{rp['CodeforcesSj']} pushed"),
             ("AtCoder", EMERALD, "ABC C / D level", f"{rp['AtCoderSj']} pushed"),
             ("CodeChef", AMBER, "Rated 1200–1400 band", f"{rp['CodeChefSj']} pushed")]
    for i, (nm, col, sub, cnt) in enumerate(plats):
        x = 500 + (i % 2) * 230
        yy = py + 176 + (i // 2) * 84
        c.add(c.glass(x, yy, 220, 74, r=16, tint=col, delay=i * 0.9))
        c.add(f'<circle cx="{x+22}" cy="{yy+26}" r="5" fill="{col}"/><circle class="pulse" cx="{x+22}" cy="{yy+26}" r="5" fill="{col}" style="animation-delay:{i*0.5}s"/>')
        c.add(c.text(x + 36, yy + 31, nm, "sans", 700, 15.5, INK))
        c.add(c.text(x + 204, yy + 31, cnt, "mono", 700, 10, col if col != BLUE else "#8DB8FF", "end"))
        c.add(c.text(x + 22, yy + 56, sub, "sans", 400, 12.5, MUTED))
    # ritual pipeline
    ry = 590
    c.add(c.glass(50, ry, 900, 92, r=46, tint=GOLD, delay=2))
    c.add(c.text(84, ry + 52, "EVERY DAY", "mono", 700, 11, GOLD_L, ls=2.4))
    steps = [("Read", CYAN), ("Brute force", VIOLET), ("Optimal", EMERALD), ("Dry run", AMBER), ("Push guide", ROSE)]
    sx0, span = 200, 720
    xs = [sx0 + i * span / (len(steps) - 1) for i in range(len(steps))]
    c.add(f'<path d="M{xs[0]} {ry+46} H{xs[-1]}" stroke="{GOLD}" stroke-opacity=".4" stroke-dasharray="3 5"/>')
    c.add(packet(f"M{xs[0]} {ry+46} H{xs[-1]}", 5, 0, CHAMP, 3.4))
    for i, ((lab, col), x) in enumerate(zip(steps, xs)):
        c.add(f'<circle cx="{x}" cy="{ry+46}" r="9" fill="{BLACK}" stroke="{col}" stroke-width="2"/>')
        c.add(f'<circle cx="{x}" cy="{ry+46}" r="4" fill="{col}"><animate attributeName="r" values="3;6;3" dur="5s" begin="{i*1.0}s" repeatCount="indefinite"/></circle>')
        c.add(c.text(x, ry + 28, f"0{i+1}", "mono", 700, 9.5, DIM, "middle", ls=1))
        c.add(c.text(x, ry + 76, lab, "sans", 700, 13, INK, "middle"))
    return c


# ======================================================================= GITHUB TELEMETRY
def telemetry():
    import datetime as dt
    g = S["github"]
    W, H = 1000, 700
    c = base(W, H, 111, (GOLD, EMERALD, VIOLET, CYAN), "GitHub telemetry",
             blobs=[(GOLD, 500, 420, 460, .36), (EMERALD, 140, 220, 300, .24), (VIOLET, 880, 640, 320, .3), (CYAN, 880, 160, 260, .2)])
    head(c, 62, "10 · GITHUB TELEMETRY", "COMMIT ENERGY", "Contributions across the last twelve months, refreshed every day.")
    tiles = [(fmt(g["contrib_year"]), "CONTRIBUTIONS · 1 YR", "chart", GOLD_L), (f"{g['current_streak']}d", "CURRENT STREAK", "flame", ORANGE),
             (f"{g['longest_streak']}d", "LONGEST STREAK", "bolt", VIOLET), (str(g["public_repos"]), "PUBLIC REPOS", "layers", CYAN)]
    for i, (v, lab, ic, col) in enumerate(tiles):
        x = 50 + i * 230
        c.add(c.glass(x, 190, 210, 96, r=20, tint=col if col != GOLD_L else GOLD, delay=i))
        c.add(icon_badge(c, x + 170, 222, 17, ic, col, spin=False, isize=17))
        c.add(c.text(x + 20, 240, v, "sans", 700, 30, "url(#gold)"))
        c.add(c.text(x + 20, 266, lab, "mono", 700, 9.5, MUTED, ls=1.3))
    # heatmap
    lv = g["levels"]
    start = dt.date.fromisoformat(g["levels_start"])
    pad = (start.weekday() + 1) % 7            # Sunday = 0 row
    weeks = (pad + len(lv) + 6) // 7
    cell, gp = 13, 3
    gw = weeks * (cell + gp) - gp
    hx = (W - gw) / 2 + 14
    hy = 350
    c.add(c.glass(50, 312, 900, 210, r=22, tint=GOLD, delay=2))
    pal = ["#1C1810", "#5A4515", "#9C7A1F", "#D4AF37", "#FFE08A"]
    cells = []
    last_m = None
    for i, ch in enumerate(lv):
        idx = pad + i
        wk, dw = divmod(idx, 7)
        d = start + dt.timedelta(days=i)
        x = hx + wk * (cell + gp)
        y = hy + dw * (cell + gp)
        k = int(ch)
        cls = ' class="glow"' if k >= 3 else ""
        st = f' style="animation-delay:-{(i % 11) * 0.3:.1f}s"' if k >= 3 else ""
        cells.append(f'<rect{cls}{st} x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" rx="3" fill="{pal[k]}"'
                     + ((' stroke="%s" stroke-opacity=".35"' % GOLD_L) if k else "") + "/>")
        if d.day <= 7 and dw == 0 or (i == 0):
            if d.month != last_m:
                c.add(c.text(x, hy - 10, d.strftime("%b"), "mono", 400, 10, DIM))
                last_m = d.month
    c.add("".join(cells))
    for dw, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        c.add(c.text(hx - 10, hy + dw * (cell + gp) + 10, lab, "mono", 400, 9.5, DIM, "end"))
    # scanning beam
    bg = c.grad_linear([(0, CHAMP, 0), (0.5, CHAMP, 0.35), (1, CHAMP, 0)], 0, 0, 1, 0)
    c.add(f'<rect x="{hx-30}" y="{hy-6}" width="30" height="{7*(cell+gp)+6}" fill="url(#{bg})">'
          f'<animate attributeName="x" values="{hx-30};{hx+gw};{hx+gw}" keyTimes="0;.7;1" dur="6s" repeatCount="indefinite"/></rect>')
    # legend
    lx = hx + gw - 5 * 16 - 70
    c.add(c.text(lx - 8, hy + 7 * (cell + gp) + 18, "Less", "mono", 400, 9.5, DIM, "end"))
    for k in range(5):
        c.add(f'<rect x="{lx + k*16}" y="{hy + 7*(cell+gp) + 8}" width="12" height="12" rx="3" fill="{pal[k]}"/>')
    c.add(c.text(lx + 5 * 16 + 4, hy + 7 * (cell + gp) + 18, "More", "mono", 400, 9.5, DIM))
    c.add(c.text(hx, hy + 7 * (cell + gp) + 18, f"peak day · {g['max_day']} contributions", "mono", 400, 9.5, MUTED))
    # languages
    langs = g["languages"]
    lcol = {"TypeScript": BLUE, "Python": AMBER, "Jupyter Notebook": ORANGE, "JavaScript": LIME, "Java": ROSE}
    tot = sum(langs.values())
    ly = 556
    c.add(c.text(50, ly, "TOP LANGUAGES · BY REPOSITORY", "mono", 700, 11, GOLD_L, ls=2.4))
    bx, bw_ = 50, 900
    x = bx
    clip = c.uid("lb")
    c.defs.append(f'<clipPath id="{clip}"><rect x="{bx}" y="{ly+16}" width="{bw_}" height="14" rx="7"/></clipPath>')
    segs = []
    for name, n in langs.items():
        w = bw_ * n / tot
        segs.append(f'<rect x="{x:.1f}" y="{ly+16}" width="{w:.1f}" height="14" fill="{lcol.get(name, GOLD)}"/>')
        x += w
    c.add(f'<g clip-path="url(#{clip})">{"".join(segs)}<rect class="sh" x="{bx}" y="{ly+10}" width="120" height="26" fill="url(#shim)"/></g>')
    x = bx
    for name, n in langs.items():
        col = lcol.get(name, GOLD)
        lab = f"{name} · {round(100*n/tot)}%"
        c.add(f'<circle cx="{x+6}" cy="{ly+58}" r="5" fill="{col}"/>')
        c.add(c.text(x + 18, ly + 63, lab, "sans", 500, 13.5, INK))
        x += c.tw(lab, "sans", 500, 13.5) + 46
    c.add(c.text(950, ly + 100, f"followers {g['followers']}  ·  stars {g['stars']}  ·  synced {S['updated']}", "mono", 400, 10.5, DIM, "end"))
    return c


# ======================================================================= QUEST LOG
QUESTS = [
    ("QUEST 01", "Generative AI & Autonomous Agentic Systems", "brain", VIOLET, 4, 5, "LangGraph · CrewAI · RAG · Multi-LLM"),
    ("QUEST 02", "Full-Stack Web Architecture & Performance", "globe", CYAN, 4, 5, "Next.js · React 19 · FastAPI · Prisma"),
    ("QUEST 03", "Cloud-Native DevOps, Kubernetes & GitOps", "cloud", EMERALD, 4, 5, "Docker · K8s · CI/CD · Prometheus"),
    ("QUEST 04", "Algorithmic Mastery & 650+ LeetCode Milestone", "code", ORANGE, 4, 5, "DP · Graphs · Trees · 4 daily judges"),
]


def quest_log():
    W, H = 1000, 650
    c = base(W, H, 121, (VIOLET, CYAN, EMERALD, ORANGE), "Engineering quest log",
             blobs=[(VIOLET, 200, 280, 320, .34), (CYAN, 820, 280, 320, .26), (EMERALD, 200, 520, 300, .24), (ORANGE, 820, 520, 320, .28)])
    head(c, 62, "11 · QUEST LOG", "ENGINEERING QUESTS", "Four campaigns, one character sheet. 16 of 20 objectives cleared, and counting.")
    for i, (qn, title, ic, col, done, total, tags) in enumerate(QUESTS):
        x = 50 + (i % 2) * 460
        y = 196 + (i // 2) * 186
        w, h = 440, 168
        out = c.glass(x, y, w, h, r=22, tint=col, delay=i * 1.1)
        out += icon_badge(c, x + 44, y + 46, 22, ic, col, isize=22)
        out += c.text(x + 82, y + 38, qn, "mono", 700, 10.5, col if col != VIOLET else "#B79CFF", ls=2.4)
        lines = c.wrap(title, "sans", 700, 16.5, w - 110)
        for k, ln in enumerate(lines[:2]):
            out += c.text(x + 82, y + 60 + k * 21, ln, "sans", 700, 16.5, INK)
        out += c.text(x + 24, y + 116, tags, "mono", 400, 11, MUTED)
        pct = done / total
        bx, by, bw = x + 24, y + 134, w - 120
        out += f'<rect x="{bx}" y="{by}" width="{bw}" height="10" rx="5" fill="#FFFFFF" fill-opacity=".08"/>'
        fg = c.grad_linear([(0, col, .9), (1, GOLD_L, 1)], 0, 0, 1, 0)
        cid = c.uid("qb")
        c.defs.append(f'<clipPath id="{cid}"><rect x="{bx}" y="{by}" width="{bw*pct:.0f}" height="10" rx="5"/></clipPath>')
        out += (f'<g clip-path="url(#{cid})"><rect x="{bx}" y="{by}" width="{bw*pct:.0f}" height="10" fill="url(#{fg})">'
                f'<animate attributeName="width" values="0;{bw*pct:.0f};{bw*pct:.0f}" keyTimes="0;.25;1" dur="10s" repeatCount="indefinite"/></rect>'
                f'<rect class="sh" x="{bx}" y="{by-4}" width="40" height="18" fill="url(#shim)" style="animation-duration:3.5s"/></g>')
        out += c.text(x + w - 24, by + 10, f"{done}/{total} · {round(pct*100)}%", "mono", 700, 11, GOLD_L, "end")
        c.add(f'<g class="fl" style="animation-delay:-{i*1.5:.1f}s;animation-duration:{7+i%2}s">{out}</g>')
    # character sheet ribbon
    ry = 572
    c.add(c.glass(50, ry, 900, 56, r=28, tint=GOLD, delay=3, strong=True))
    xp, _ = c.pill(70, ry + 13, "+5000 XP", "mono", 700, 11, CHAMP, 30, 1.6, dot=GOLD, glassy=False)
    c.add(f'<g class="glow">{xp}</g>')
    c.add(c.text(500, ry + 34, "CLASS · FULL-STACK ARCHITECT   ·   LEVEL MAX ENGINEER", "mono", 700, 12, GOLD_L, "middle", ls=2))
    c.add(c.text(930, ry + 34, "16 / 20 objectives", "sans", 500, 13, MUTED, "end"))
    return c


def vault():
    W, H = 1000, 280
    c = base(W, H, 131, (GOLD, VIOLET, ROSE, AMBER), "Secret developer vault",
             blobs=[(GOLD, 180, 140, 260, .5), (VIOLET, 760, 140, 320, .32)], dust=26)
    cx, cy = 180, 140
    c.add(f'<circle cx="{cx}" cy="{cy}" r="92" fill="#000" fill-opacity=".35" stroke="url(#gstroke)" stroke-width="3"/>')
    c.add(f'<g class="spin" style="animation-duration:18s"><circle cx="{cx}" cy="{cy}" r="78" fill="none" stroke="{GOLD}" stroke-width="6" stroke-dasharray="3 9" stroke-opacity=".8"/></g>')
    c.add(f'<g class="spinr" style="animation-duration:9s"><circle cx="{cx}" cy="{cy}" r="56" fill="none" stroke="{GOLD_L}" stroke-width="2" stroke-dasharray="26 10"/>'
          + "".join(f'<path d="M{cx} {cy-56} V{cy-40}" stroke="{GOLD_L}" stroke-width="3" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 45))
          + "</g>")
    c.add(f'<circle cx="{cx}" cy="{cy}" r="32" fill="url(#goldv)"/>')
    c.add(icon("gem", cx - 15, cy - 15, 30, BLACK, 2.2))
    c.add(f'<path d="M370 52 V228" stroke="{GOLD}" stroke-opacity=".35"/>')
    c.add(c.text(410, 84, "SECRET VAULT · UNLOCKED", "mono", 700, 12, GOLD_L, ls=3))
    c.add(c.text(410, 124, "You found the loot.", "display", 900, 32, "url(#gold)"))
    c.add(c.text(410, 160, "“Any sufficiently advanced technology is", "sans", 500, 17, INK, italic=True))
    c.add(c.text(410, 184, "indistinguishable from magic.”  — Arthur C. Clarke", "sans", 500, 17, INK, italic=True))
    loot = [("+5000 XP", GOLD), ("LEGENDARY", VIOLET), ("BUILDER BADGE", ROSE), ("∞ CURIOSITY", TEAL)]
    x = 410
    for i, (lab, col) in enumerate(loot):
        svg, w = c.chip(x, 222, lab, col, "mono", 700, 11, 28)
        c.add(f'<g class="fl" style="animation-delay:-{i*0.8:.1f}s">{svg}</g>')
        x += w + 10
    return c


# ======================================================================= PHILOSOPHY
def philosophy():
    W, H = 1000, 676
    c = base(W, H, 141, (GOLD, VIOLET, CYAN, EMERALD), "Engineering philosophy",
             blobs=[(GOLD, 500, 300, 460, .42), (VIOLET, 120, 600, 320, .3), (CYAN, 880, 620, 300, .24), (EMERALD, 500, 660, 260, .2)])
    head(c, 62, "12 · PHILOSOPHY", "ENGINEERING CREED")
    qx, qy, qw, qh = 80, 180, 840, 270
    c.add(c.glass(qx, qy, qw, qh, r=28, tint=GOLD, strong=True, glow=GOLD))
    c.add(f'<g class="glow">{icon("quote", qx + 30, qy + 26, 46, GOLD_L, 1.4)}</g>')
    c.add(f'<g class="glow" style="animation-delay:-1.8s" transform="rotate(180 {qx+qw-53} {qy+qh-49})">{icon("quote", qx + qw - 76, qy + qh - 72, 46, GOLD_L, 1.4)}</g>')
    quote = "Architecture is not just about writing code that works today; it is about crafting systems that remain resilient, observable, and extensible tomorrow."
    lines = c.wrap(quote, "display", 700, 26, 660)
    y0 = qy + qh / 2 - (len(lines) - 1) * 40 / 2 + 2
    for k, ln in enumerate(lines):
        c.add(c.text(500, y0 + k * 40, ln, "display", 700, 26, "url(#gold)", "middle"))
    c.add(c.text(500, qy + qh - 26, "— SAYANDIP JANA", "mono", 700, 11, MUTED, "middle", ls=3))
    princ = [("rocket", CYAN, "THINK BIG", "Build Bigger", "Design for the 10× version from day one."),
             ("code", VIOLET, "CODE", "Clean & Scalable", "Readable today, extensible tomorrow."),
             ("bolt", EMERALD, "SHIP", "Continuously", "Small commits, green pipelines, observable releases.")]
    for i, (ic, col, k1, k2, d) in enumerate(princ):
        x, y, w, h = 50 + i * 310, 484, 280, 150
        out = c.glass(x, y, w, h, r=22, tint=col, delay=i * 1.3)
        out += icon_badge(c, x + 44, y + 46, 22, ic, col, isize=22)
        out += c.text(x + 82, y + 40, k1, "mono", 700, 11.5, col if col != VIOLET else "#B79CFF", ls=3)
        out += c.text(x + 82, y + 64, k2, "sans", 700, 19, INK)
        body, _ = c.para(x + 24, y + 104, d, "sans", 400, 14, MUTED, w - 48, 1.45)
        out += body
        c.add(f'<g class="fl" style="animation-delay:-{i*1.2:.1f}s;animation-duration:{6+i}s">{out}</g>')
    return c


# ======================================================================= FOOTER
def footer():
    W, H = 1000, 300
    c = base(W, H, 151, (GOLD, VIOLET, ROSE, TEAL), "Thanks for visiting",
             blobs=[(GOLD, 500, 300, 460, .45), (VIOLET, 120, 60, 260, .3), (TEAL, 880, 60, 260, .22)], dust=34)
    # waves
    c.css.append(".wv{animation:wv 9s linear infinite}.wv2{animation:wv 14s linear infinite reverse}@keyframes wv{to{transform:translateX(-400px)}}")
    for k, (amp, yb, col, op, cls) in enumerate([(14, 236, GOLD, .55, "wv"), (10, 250, GOLD_L, .35, "wv2"), (18, 262, VIOLET, .35, "wv")]):
        d = f"M-400 {yb}"
        for i in range(0, 1800, 100):
            d += f" Q{-400 + i + 50} {yb - amp if (i//100) % 2 == 0 else yb + amp} {-400 + i + 100} {yb}"
        c.add(f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="1.6"/>')
    c.add(c.text(500, 92, "THANK YOU FOR SCROLLING", "display", 900, 38, "url(#gold)", "middle", ls=2))
    c.add(c.text(500, 132, "Always up for building GenAI systems, distributed platforms and high-impact software together.", "sans", 500, 16, INK, "middle"))
    c.add(c.text(500, 162, "sayandip.jana24@gmail.com   ·   +91-8617005893", "mono", 700, 13, GOLD_L, "middle", ls=0.5))
    c.add(c.text(500, 200, f"Hand-built SVG · animated · auto-refreshed daily · last sync {S['updated']}", "mono", 400, 10.5, DIM, "middle"))
    return c


# ======================================================================= REGISTRY
PROJECT_TILES = [
    ("ChitChat", "Liquid-glass real-time chat app with a polished, glassy UI.", "Python", "#3776AB", "REALTIME", "quote", CYAN),
    ("ScamRadar", "AI job-scam detector: multi-agent pipeline, ML classifier, retrieval and live domain checks.", "Multi-agent AI · ML", ROSE, "AGENTIC AI", "spark", ROSE),
    ("LeetCodeSj", "LeetCode solutions in Java, with a full study guide for every daily problem.", "Java", "#ED8B00", "{LeetCodeSj} SOLUTIONS", "code", ORANGE),
    ("CodeforcesSj", "One Codeforces problem a day in Java, explained from brute force to optimal.", "Java", "#ED8B00", "{CodeforcesSj} SOLVED · DAILY", "chart", BLUE),
    ("AtCoderSj", "Daily AtCoder ABC problems in Java, with dry runs and complexity notes.", "Java", "#ED8B00", "{AtCoderSj} SOLVED · DAILY", "bolt", EMERALD),
    ("CodeChefSj", "Daily rated CodeChef problems in Java, with edge cases called out.", "Java", "#ED8B00", "{CodeChefSj} SOLVED · DAILY", "flame", AMBER),
    ("MyDSASheet", "A DSA interview-prep handbook, organised topic by topic.", "JavaScript", "#F7DF1E", "PREP SHEET", "scroll", LIME),
    ("PortFolio-SJ", "My personal portfolio site, live at sayandipjana.vercel.app.", "Live website", VIOLET, "PORTFOLIO", "globe", VIOLET),
]

CONNECT = [
    ("linkedin", "LinkedIn", "in/jsayandip2003", "linkedin", "#0A66C2"),
    ("github", "GitHub", "Sayandip-Jana-1018", "github", GOLD),
    ("x", "X · Twitter", "@51Sayandip", "x", INK),
    ("leetcode", "LeetCode", "u/sayandip_jana", "code", ORANGE),
    ("email", "Email", "sayandip.jana24@gmail.com", "mail", ROSE),
    ("phone", "Phone", "+91-8617005893", "phone", EMERALD),
    ("portfolio", "Portfolio", "sayandipjana.vercel.app", "globe", VIOLET),
    ("splitit_live", "SplitIT live", "splitsj.vercel.app", "rocket", AMBER),
]


def build_all():
    out = {"hero": hero, "divider": divider, "about": about, "journey": journey, "hall_of_fame": hall_of_fame,
           "certs": certs, "autoforge": autoforge, "splitit": splitit, "arsenal": arsenal, "architecture": architecture,
           "cp_arena": cp_arena, "telemetry": telemetry, "quest_log": quest_log, "vault": vault, "philosophy": philosophy,
           "footer": footer}
    out["btn_autoforge_repo"] = lambda: button("View repository", "github.com/Sayandip-Jana-1018/AutoML", "github", CYAN, 6)
    out["btn_splitit_repo"] = lambda: button("View repository", "github.com/Sayandip-Jana-1018/SplitIT", "github", AMBER, 7)
    out["btn_splitit_live"] = lambda: button("Open the live app", "splitsj.vercel.app", "rocket", PINK, 8)
    out["banner_builds"] = lambda: banner("06 · MORE BUILDS", "THE OPEN-SOURCE SHELF", "Every tile below opens its repository.", (TEAL, ROSE, GOLD, VIOLET), 161)
    out["banner_connect"] = lambda: banner("13 · CONNECT", "LET'S BUILD TOGETHER", "Tap any card to reach me.", (VIOLET, GOLD, ROSE, TEAL), 171)
    for i, (nm, desc, lang, lc_, metric, ic, acc) in enumerate(PROJECT_TILES):
        m = metric.format(**S["repos"])
        out[f"tile_{nm.lower()}"] = (lambda nm=nm, desc=desc, lang=lang, lc_=lc_, m=m, ic=ic, acc=acc, i=i:
                                     tile(nm, desc, lang, lc_, m, ic, acc, 200 + i))
    for i, (key, label, handle, ic, col) in enumerate(CONNECT):
        out[f"connect_{key}"] = lambda label=label, handle=handle, ic=ic, col=col, i=i: button(label, handle, ic, col, 300 + i)
    return out


CARDS = build_all()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:] or list(CARDS)
    for name in only:
        card = CARDS[name]()
        n = card.save(os.path.join(OUT, f"{name}.svg"))
        print(f"{name}.svg  {n/1024:.0f} KB")
