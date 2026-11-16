"""
sjsvg: a tiny SVG toolkit for Sayandip's black-and-gold liquid-glass profile cards.

Every card is a standalone animated SVG:
  * fonts are subset to the exact glyphs used and embedded as base64 WOFF2,
  * images are embedded as base64 (GitHub blocks external resources inside SVGs),
  * all motion is CSS keyframes / SMIL, so it runs inside GitHub's <img> sandbox,
  * prefers-reduced-motion turns the CSS motion off.
"""
import base64
import io
import math
import os
import random
from collections import defaultdict
from html import escape as _esc

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")

# ---------------------------------------------------------------- palette
BLACK = "#060504"
GOLD = "#D4AF37"
GOLD_L = "#F5D27A"
CHAMP = "#FFF1C9"
GOLD_D = "#9C7A1F"
INK = "#F4ECDD"      # warm white text
MUTED = "#C9BEA6"
DIM = "#8C826F"

VIOLET = "#8B5CF6"
ROSE = "#F43F5E"
AMBER = "#F59E0B"
TEAL = "#14B8A6"
CYAN = "#22D3EE"
EMERALD = "#10B981"
BLUE = "#3B82F6"
ORANGE = "#FB923C"
PINK = "#EC4899"
LIME = "#A3E635"

# ---------------------------------------------------------------- fonts
FAMILY = {"display": "SJDisplay", "sans": "SJSans", "mono": "SJMono"}
FALLBACK = {
    "display": "'Cinzel', 'Trajan Pro', Georgia, serif",
    "sans": "'Space Grotesk', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    "mono": "'JetBrains Mono', 'SF Mono', Consolas, monospace",
}
FONT_FILES = {
    ("display", 700): ["cinzel-700.woff2"],
    ("display", 900): ["cinzel-900.woff2"],
    ("sans", 400): ["spacegrotesk-400.woff2", "spacegrotesk-ext-400.woff2"],
    ("sans", 500): ["spacegrotesk-500.woff2", "spacegrotesk-ext-500.woff2"],
    ("sans", 700): ["spacegrotesk-700.woff2", "spacegrotesk-ext-700.woff2"],
    ("mono", 400): ["jetbrainsmono-400.woff2"],
    ("mono", 700): ["jetbrainsmono-700.woff2"],
}
_FONT_CACHE = {}


def _font(fname):
    if fname not in _FONT_CACHE:
        t = TTFont(os.path.join(FONT_DIR, fname))
        _FONT_CACHE[fname] = (t, t.getBestCmap(), t["hmtx"].metrics, t["head"].unitsPerEm)
    return _FONT_CACHE[fname]


def text_width(s, font="sans", weight=400, size=16, ls=0.0):
    """Advance width of a string in px using the embedded font's metrics."""
    total = 0.0
    files = FONT_FILES[(font, weight)]
    for ch in s:
        adv = None
        for fname in files:
            t, cmap, hmtx, upm = _font(fname)
            g = cmap.get(ord(ch))
            if g is not None:
                adv = hmtx[g][0] / upm
                break
        if adv is None:
            adv = 0.6  # system fallback glyph, rough average
        total += adv * size
    return total + ls * max(len(s) - 1, 0)


def _subset_b64(fname, chars):
    t = TTFont(os.path.join(FONT_DIR, fname))
    opts = ft_subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = ft_subset.Subsetter(opts)
    sub.populate(unicodes=[ord(c) for c in chars])
    sub.subset(t)
    buf = io.BytesIO()
    t.flavor = "woff2"
    t.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def _unicode_range(chars):
    cps = sorted(set(ord(c) for c in chars))
    return ",".join(f"U+{cp:04X}" for cp in cps)


def esc(s):
    return _esc(str(s), quote=True)


# ---------------------------------------------------------------- shared CSS
BASE_CSS = """
.bl{transform-box:fill-box;transform-origin:center}
.d1{animation:d1 26s ease-in-out infinite alternate}
.d2{animation:d2 31s ease-in-out infinite alternate}
.d3{animation:d3 23s ease-in-out infinite alternate}
.d4{animation:d4 35s ease-in-out infinite alternate}
@keyframes d1{0%{transform:translate(0,0) scale(1)}50%{transform:translate(70px,-40px) scale(1.12)}100%{transform:translate(-50px,30px) scale(.94)}}
@keyframes d2{0%{transform:translate(0,0) scale(1.05)}50%{transform:translate(-80px,35px) scale(.92)}100%{transform:translate(45px,-25px) scale(1.1)}}
@keyframes d3{0%{transform:translate(0,0) scale(.95)}50%{transform:translate(40px,50px) scale(1.15)}100%{transform:translate(-60px,-20px) scale(1)}}
@keyframes d4{0%{transform:translate(0,0) rotate(0deg)}100%{transform:translate(30px,-30px) rotate(25deg)}}
.dust{animation:rise linear infinite;opacity:0}
@keyframes rise{0%{transform:translateY(0);opacity:0}12%{opacity:.85}80%{opacity:.5}100%{transform:translateY(-240px);opacity:0}}
.sh{transform-box:fill-box;transform-origin:center;animation:sweep 9s cubic-bezier(.55,0,.35,1) infinite}
@keyframes sweep{0%{transform:translateX(-160%) skewX(-22deg)}45%,100%{transform:translateX(520%) skewX(-22deg)}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.85}100%{transform:scale(3.2);opacity:0}}
.fl{transform-box:fill-box;transform-origin:center;animation:fl 6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.spinr{transform-box:fill-box;transform-origin:center;animation:spin 22s linear infinite reverse}
.blink{animation:blink 1.05s steps(1) infinite}
@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:0}}
.glow{animation:glow 3.6s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}
.comet{animation:comet 7s linear infinite}
@keyframes comet{to{stroke-dashoffset:-2000}}
.breathe{transform-box:fill-box;transform-origin:center;animation:breathe 5s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}
.fadein{animation:fadein 1.2s ease-out both}
@keyframes fadein{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


class Card:
    """One animated SVG card."""

    def __init__(self, w, h, seed=1, rx=30, accents=(GOLD, VIOLET, ROSE), title="Sayandip Jana"):
        self.w, self.h, self.rx = w, h, rx
        self.rng = random.Random(seed)
        self.accents = accents
        self.title = title
        self.defs = []
        self.css = []
        self.layers = []  # drawn in order
        self.chars = defaultdict(set)
        self._uid = 0
        self._grads = {}
        self._common_defs()

    # ---------------------------------------------------------- utils
    def uid(self, p="i"):
        self._uid += 1
        return f"{p}{self._uid}"

    def add(self, s):
        self.layers.append(s)
        return s

    def grad_linear(self, stops, x1=0, y1=0, x2=1, y2=1, units=None, extra=""):
        key = ("L", tuple(stops), x1, y1, x2, y2, units, extra)
        if key in self._grads:
            return self._grads[key]
        gid = self.uid("g")
        u = f' gradientUnits="{units}"' if units else ""
        st = "".join(
            f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops
        )
        self.defs.append(
            f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}{extra}>{st}</linearGradient>'
        )
        self._grads[key] = gid
        return gid

    def grad_radial(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None):
        key = ("R", tuple(stops), cx, cy, r, fx, fy)
        if key in self._grads:
            return self._grads[key]
        gid = self.uid("r")
        f = (f' fx="{fx}" fy="{fy}"' if fx is not None else "")
        st = "".join(
            f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops
        )
        self.defs.append(f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}"{f}>{st}</radialGradient>')
        self._grads[key] = gid
        return gid

    def _common_defs(self):
        # moving liquid-gold text fill
        self.defs.append(
            '<linearGradient id="gold" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">'
            f'<stop offset="0" stop-color="{GOLD_D}"/><stop offset=".22" stop-color="{GOLD}"/>'
            f'<stop offset=".45" stop-color="{CHAMP}"/><stop offset=".62" stop-color="{GOLD_L}"/>'
            f'<stop offset="1" stop-color="{GOLD_D}"/>'
            '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="7s" repeatCount="indefinite"/>'
            "</linearGradient>"
        )
        self.defs.append(
            '<linearGradient id="goldv" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{CHAMP}"/><stop offset=".45" stop-color="{GOLD_L}"/>'
            f'<stop offset="1" stop-color="{GOLD_D}"/></linearGradient>'
        )
        # glass
        self.defs.append(
            '<linearGradient id="gfill" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".13"/>'
            '<stop offset=".45" stop-color="#FFFFFF" stop-opacity=".045"/>'
            '<stop offset="1" stop-color="#FFE9B0" stop-opacity=".075"/></linearGradient>'
        )
        self.defs.append(
            '<linearGradient id="gstroke" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{GOLD_L}" stop-opacity=".95"/>'
            '<stop offset=".3" stop-color="#FFFFFF" stop-opacity=".22"/>'
            '<stop offset=".65" stop-color="#FFFFFF" stop-opacity=".05"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity=".7"/></linearGradient>'
        )
        self.defs.append(
            '<linearGradient id="spec" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
            '<stop offset=".25" stop-color="#FFFFFF" stop-opacity=".55"/>'
            '<stop offset=".6" stop-color="#FFF4D6" stop-opacity=".25"/>'
            '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        )
        self.defs.append(
            '<linearGradient id="shim" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#FFF6DA" stop-opacity=".16"/>'
            '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        )
        self.defs.append(
            '<radialGradient id="sheen" cx=".18" cy="0" r="1">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".14"/>'
            '<stop offset=".5" stop-color="#FFFFFF" stop-opacity=".02"/>'
            '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
        )
        # film grain
        self.defs.append(
            '<filter id="grain" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" stitchTiles="stitch"/>'
            '<feColorMatrix type="saturate" values="0"/>'
            '<feComponentTransfer><feFuncA type="table" tableValues="0 .55"/></feComponentTransfer></filter>'
        )
        # soft glow for text / dots
        self.defs.append(
            '<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">'
            '<feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        )

    # ---------------------------------------------------------- text
    def text(self, x, y, s, font="sans", weight=400, size=16, fill=INK, anchor="start",
             ls=0, opacity=1, cls="", extra="", italic=False):
        self.chars[(font, weight)].update(str(s))
        fam = f"{FAMILY[font]}, {FALLBACK[font]}"
        c = f' class="{cls}"' if cls else ""
        o = f' opacity="{opacity}"' if opacity != 1 else ""
        it = ' font-style="italic"' if italic else ""
        ls_ = f' letter-spacing="{ls}"' if ls else ""
        return (
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(fam)}" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve"{ls_}{o}{it}{c} {extra}>{esc(s)}</text>'
        )

    def tw(self, s, font="sans", weight=400, size=16, ls=0):
        return text_width(str(s), font, weight, size, ls)

    def wrap(self, s, font, weight, size, maxw, ls=0):
        words, lines, cur = str(s).split(), [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if self.tw(t, font, weight, size, ls) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, font="sans", weight=400, size=15, fill=MUTED, maxw=400, lh=1.5,
             anchor="start", ls=0):
        out = []
        for i, line in enumerate(self.wrap(s, font, weight, size, maxw, ls)):
            out.append(self.text(x, y + i * size * lh, line, font, weight, size, fill, anchor, ls))
        n = len(self.wrap(s, font, weight, size, maxw, ls))
        return "".join(out), n * size * lh

    # ---------------------------------------------------------- background
    def background(self, blobs=None, dust=24, grid=False):
        w, h, rx = self.w, self.h, self.rx
        clip = self.uid("cc")
        self.defs.append(f'<clipPath id="{clip}"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>')
        base = self.grad_linear([(0, "#0E0B07", 1), (0.5, "#070605", 1), (1, "#030303", 1)], 0, 0, 0.3, 1)
        out = [f'<g clip-path="url(#{clip})">', f'<rect width="{w}" height="{h}" fill="url(#{base})"/>']
        if blobs is None:
            blobs = []
            acc = list(self.accents)
            spots = [(0.85, 0.1), (0.1, 0.9), (0.55, 0.55), (0.12, 0.15)]
            for i, col in enumerate(acc[:4]):
                sx, sy = spots[i % len(spots)]
                blobs.append((col, sx * w, sy * h, max(w, h) * (0.42 if i == 0 else 0.36), 0.55 if col == GOLD else 0.38))
        for i, (col, cx, cy, r, a) in enumerate(blobs):
            rg = self.grad_radial([(0, col, a), (0.45, col, a * 0.35), (1, col, 0)])
            out.append(f'<circle class="bl d{(i % 4) + 1}" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#{rg})"/>')
        if grid:
            gid = self.uid("pt")
            self.defs.append(
                f'<pattern id="{gid}" width="40" height="40" patternUnits="userSpaceOnUse">'
                f'<path d="M40 0H0V40" fill="none" stroke="{GOLD}" stroke-opacity=".05" stroke-width="1"/></pattern>'
            )
            out.append(f'<rect width="{w}" height="{h}" fill="url(#{gid})"/>')
        # gold dust rising
        for i in range(dust):
            x = self.rng.uniform(20, w - 20)
            y = self.rng.uniform(h * 0.35, h + 40)
            r = self.rng.choice([0.9, 1.2, 1.5, 2.0])
            dur = self.rng.uniform(9, 18)
            delay = -self.rng.uniform(0, dur)
            col = self.rng.choice([GOLD_L, CHAMP, GOLD])
            out.append(
                f'<circle class="dust" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" '
                f'style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>'
            )
        vig = self.grad_radial([(0, "#000", 0), (0.7, "#000", 0.15), (1, "#000", 0.6)], 0.5, 0.45, 0.75)
        out.append(f'<rect width="{w}" height="{h}" fill="url(#{vig})"/>')
        out.append(f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".06"/>')
        out.append("</g>")
        self.layers.insert(0, "".join(out))
        # frame drawn last (see render)
        self._frame = True

    def frame(self):
        w, h, rx = self.w, self.h, self.rx
        fs = self.grad_linear([(0, GOLD_L, 0.9), (0.3, GOLD, 0.25), (0.55, "#FFFFFF", 0.06), (0.8, GOLD, 0.3), (1, GOLD_L, 0.85)])
        out = [
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{rx}" fill="none" stroke="url(#{fs})" stroke-width="1.5"/>',
            f'<rect x="4.5" y="4.5" width="{w-9}" height="{h-9}" rx="{rx-4}" fill="none" stroke="#FFFFFF" stroke-opacity=".05"/>',
        ]
        # travelling comet on the frame
        per = 2 * (w + h)
        out.append(
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{rx}" fill="none" stroke="{CHAMP}" '
            f'stroke-width="2" stroke-linecap="round" stroke-dasharray="90 {per:.0f}" opacity=".9" filter="url(#softglow)">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-{per + 90:.0f}" dur="{per/260:.1f}s" repeatCount="indefinite"/></rect>'
        )
        # corner ornaments
        L = 18
        for (cx, cy, sx, sy) in [(18, 18, 1, 1), (w - 18, 18, -1, 1), (18, h - 18, 1, -1), (w - 18, h - 18, -1, -1)]:
            out.append(
                f'<path d="M{cx} {cy + sy*L} V{cy} H{cx + sx*L}" fill="none" stroke="{GOLD_L}" stroke-opacity=".55" stroke-width="1.2"/>'
            )
        return "".join(out)

    # ---------------------------------------------------------- glass
    def glass(self, x, y, w, h, r=20, tint=None, shimmer=True, delay=0.0, strong=False, glow=None):
        out = []
        if glow:
            gg = self.grad_radial([(0, glow, 0.35), (1, glow, 0)])
            out.append(f'<ellipse class="glow" cx="{x + w/2:.0f}" cy="{y + h/2:.0f}" rx="{w*0.62:.0f}" ry="{h*0.75:.0f}" fill="url(#{gg})"/>')
        # drop shadow
        out.append(f'<rect x="{x+4}" y="{y+10}" width="{w}" height="{h}" rx="{r}" fill="#000" opacity=".35"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#gfill)"/>')
        if tint:
            tg = self.grad_linear([(0, tint, 0.16), (0.6, tint, 0.03), (1, tint, 0.10)])
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{tg})"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#sheen)"/>')
        # refraction edge: inner bright line + coloured caustic
        out.append(
            f'<rect x="{x+1.2}" y="{y+1.2}" width="{w-2.4}" height="{h-2.4}" rx="{r-1}" fill="none" '
            f'stroke="#FFFFFF" stroke-opacity="{0.10 if not strong else 0.16}"/>'
        )
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="url(#gstroke)" stroke-width="{1.6 if strong else 1.2}"/>'
        )
        out.append(
            f'<path d="M{x + r*0.9:.1f} {y + 1.4:.1f} H{x + w*0.72:.1f}" stroke="url(#spec)" stroke-width="1.6" stroke-linecap="round"/>'
        )
        if shimmer:
            cid = self.uid("gc")
            self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>')
            out.append(
                f'<g clip-path="url(#{cid})"><rect class="sh" x="{x}" y="{y - 10}" width="{max(60, w*0.22):.0f}" height="{h + 20}" '
                f'fill="url(#shim)" style="animation-delay:{delay:.1f}s"/></g>'
            )
        return "".join(out)

    def pill(self, x, y, label, font="mono", weight=700, size=12, color=GOLD_L, h=30, ls=1.5,
             dot=None, pad=16, glassy=True, anchor="start", text_fill=None):
        tw = self.tw(label, font, weight, size, ls)
        dw = 18 if dot else 0
        w = tw + pad * 2 + dw
        if anchor == "middle":
            x = x - w / 2
        out = []
        if glassy:
            out.append(self.glass(x, y, w, h, r=h / 2, shimmer=False))
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity=".1" stroke="{color}" stroke-opacity=".45"/>')
        if dot:
            cx, cy = x + pad + 4, y + h / 2
            out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{dot}"/>')
            out.append(f'<circle class="pulse" cx="{cx}" cy="{cy}" r="4" fill="{dot}"/>')
        out.append(self.text(x + pad + dw, y + h / 2 + size * 0.36, label, font, weight, size, text_fill or color, ls=ls))
        return "".join(out), w

    def chip(self, x, y, label, color=GOLD, font="mono", weight=500, size=12, h=28, pad=12, ls=0.3):
        if (font, weight) not in FONT_FILES:
            weight = 400
        tw = self.tw(label, font, weight, size, ls)
        w = tw + pad * 2 + 14
        out = [
            f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity=".09" stroke="{color}" stroke-opacity=".5"/>',
            f'<rect x="{x+1}" y="{y+1}" width="{w-2:.1f}" height="{h/2-1}" rx="{h/2-1}" fill="#FFFFFF" fill-opacity=".05"/>',
            f'<circle cx="{x + pad + 3}" cy="{y + h/2}" r="3.2" fill="{color}"/>',
            self.text(x + pad + 12, y + h / 2 + size * 0.36, label, font, weight, size, INK, ls=ls),
        ]
        return "".join(out), w

    def chips_row(self, x, y, labels, maxw, colors=None, gap=8, h=28, size=12, font="mono", weight=500, rowgap=10, center=False):
        """Lays out chips with wrapping. Returns (svg, height)."""
        rows, cur, curw = [], [], 0
        widths = []
        for i, lab in enumerate(labels):
            w = self.tw(lab, font, weight if (font, weight) in FONT_FILES else 400, size, 0.3) + 12 * 2 + 14
            widths.append(w)
        for i, lab in enumerate(labels):
            w = widths[i]
            if cur and curw + gap + w > maxw:
                rows.append((cur, curw))
                cur, curw = [], 0
            cur.append(i)
            curw += (gap if curw else 0) + w
        if cur:
            rows.append((cur, curw))
        out = []
        for ri, (idxs, rw) in enumerate(rows):
            cx = x + ((maxw - rw) / 2 if center else 0)
            yy = y + ri * (h + rowgap)
            for k, i in enumerate(idxs):
                col = (colors[i] if colors else GOLD)
                svg, w = self.chip(cx, yy, labels[i], col, font, weight, size, h)
                delay = (i % 7) * 0.6
                out.append(f'<g class="fl" style="animation-delay:-{delay:.1f}s;animation-duration:{6 + (i % 3)}s">{svg}</g>')
                cx += w + gap
        return "".join(out), len(rows) * (h + rowgap) - rowgap

    def header(self, x, y, eyebrow, title, anchor="start", size=34, sub=None, maxw=None):
        out = []
        ew = self.tw(eyebrow, "mono", 700, 12, 3)
        if anchor == "middle":
            out.append(self.text(x, y, eyebrow, "mono", 700, 12, GOLD_L, "middle", ls=3))
            out.append(f'<path d="M{x - ew/2 - 46} {y-4} H{x - ew/2 - 12}" stroke="{GOLD}" stroke-opacity=".7"/>')
            out.append(f'<path d="M{x + ew/2 + 12} {y-4} H{x + ew/2 + 46}" stroke="{GOLD}" stroke-opacity=".7"/>')
        else:
            out.append(f'<path d="M{x} {y-4} H{x+28}" stroke="{GOLD}" stroke-width="1.5"/>')
            out.append(self.text(x + 38, y, eyebrow, "mono", 700, 12, GOLD_L, ls=3))
        out.append(self.text(x, y + size + 10, title, "display", 900, size, "url(#gold)", anchor, ls=1.5))
        h = size + 14
        if sub:
            body, bh = self.para(x, y + size + 40, sub, "sans", 400, 15, MUTED, maxw or 600, 1.5, anchor)
            out.append(body)
            h += 30 + bh
        return "".join(out), h

    # ---------------------------------------------------------- typing (SMIL, discrete)
    def typer(self, x, y, lines, font="mono", weight=500, size=18, fill=INK, cursor=GOLD_L,
              tc=0.055, hold=2.2, td=0.022, gap=0.35):
        if (font, weight) not in FONT_FILES:
            weight = 400
        slots, t = [], 0.0
        for s in lines:
            n = len(s)
            dur = n * tc + hold + n * td + gap
            slots.append((t, dur))
            t += dur
        T = t
        out = []
        for (start, dur), s in zip(slots, lines):
            prefix = [self.tw(s[:k], font, weight, size) for k in range(len(s) + 1)]
            n = len(s)
            pts = [(0.0, 0.0)]
            for k in range(1, n + 1):
                pts.append((start + k * tc, prefix[k]))
            t_del = start + n * tc + hold
            for j in range(1, n + 1):
                pts.append((t_del + j * td, prefix[n - j]))
            # visibility window of the cursor
            vis = [(0.0, 0), (start, 1), (start + dur - gap, 0)]
            if start == 0:
                vis = [(0.0, 1), (dur - gap, 0)]
            def anim(attr, ptsv, fmt="{:.1f}"):
                kt = ";".join(f"{min(max(p[0] / T, 0), 1):.5f}" for p in ptsv)
                vals = ";".join(fmt.format(p[1]) for p in ptsv)
                return (f'<animate attributeName="{attr}" calcMode="discrete" dur="{T:.2f}s" '
                        f'repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/>')
            cid = self.uid("tc")
            maxw = prefix[-1] + 4
            self.defs.append(
                f'<clipPath id="{cid}"><rect x="{x}" y="{y - size}" width="0" height="{size * 1.5}">'
                f'{anim("width", pts)}</rect></clipPath>'
            )
            out.append(f'<g clip-path="url(#{cid})">{self.text(x, y, s, font, weight, size, fill)}</g>')
            # cursor follows
            cur_pts = [(p[0], x + p[1] + 2) for p in pts]
            out.append(
                f'<rect x="{x}" y="{y - size * 0.82:.1f}" width="{size*0.55:.1f}" height="{size*1.02:.1f}" fill="{cursor}" opacity="0">'
                f'{anim("x", cur_pts)}{anim("opacity", vis, "{}")}</rect>'
            )
        return "".join(out)

    # ---------------------------------------------------------- misc
    def divider_line(self, x1, x2, y, color=GOLD):
        g = self.grad_linear([(0, color, 0), (0.5, color, 0.8), (1, color, 0)], 0, 0, 1, 0)
        span = x2 - x1
        return (
            f'<path d="M{x1} {y} H{x2}" stroke="url(#{g})" stroke-width="1"/>'
            f'<circle r="3" fill="{CHAMP}" filter="url(#softglow)"><animateMotion dur="5s" repeatCount="indefinite" '
            f'path="M{x1 + span*0.08} {y} H{x2 - span*0.08}" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1"/></circle>'
        )

    def embed_image(self, path, mime="image/jpeg"):
        with open(path, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

    # ---------------------------------------------------------- render
    def render(self):
        faces = []
        for (font, weight), chars in sorted(self.chars.items()):
            chars = set(chars) | {" "}
            files = FONT_FILES[(font, weight)]
            remaining = set(chars)
            for fname in files:
                _, cmap, _, _ = _font(fname)
                here = {c for c in remaining if ord(c) in cmap}
                if not here:
                    continue
                remaining -= here
                b64 = _subset_b64(fname, here)
                faces.append(
                    f"@font-face{{font-family:{FAMILY[font]};font-weight:{weight};font-style:normal;"
                    f"src:url(data:font/woff2;base64,{b64}) format('woff2');unicode-range:{_unicode_range(here)}}}"
                )
        css = "\n".join(faces) + BASE_CSS + "\n".join(self.css)
        body = "".join(self.layers)
        frame = self.frame() if getattr(self, "_frame", False) else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.title)}">'
            f"<title>{esc(self.title)}</title><defs><style>{css}</style>{''.join(self.defs)}</defs>"
            f"{body}{frame}</svg>"
        )

    def save(self, path):
        svg = self.render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        return len(svg.encode())
