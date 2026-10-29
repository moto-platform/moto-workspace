"""Build EAGLE/Fusion .lbr libraries from modules.py."""
import math
import sys
from collections import Counter, defaultdict
from xml.sax.saxutils import escape

import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from modules import M  # noqa: E402

P = 2.54
OUT = sys.argv[1] if len(sys.argv) > 1 else ".."

LIBS = {
    "core": ("moto-core", "Part 1 - Ana kontrolcu, guc zinciri, CAN, GPS/IMU, OBD2"),
    "anomaly": ("moto-anomaly", "Part 2 - Anomali / usta-mekanik sensorleri"),
    "safety": ("moto-safety", "Part 3 - Guvenlik: radar, viraj LED, NFC immobilizer, GSM, kamera"),
    "hud": ("moto-hud", "Part 4 - Kask HUD ve ses birimi"),
    "edge-hil": ("moto-edge-hil", "Part 5 - Raspberry Pi 5 kenar birimi ve HIL tezgahi"),
}

LAYERS = [(1, "Top", 4), (16, "Bottom", 1), (17, "Pads", 2), (18, "Vias", 2), (19, "Unrouted", 6),
          (20, "Dimension", 15), (21, "tPlace", 7), (22, "bPlace", 7), (23, "tOrigins", 15),
          (24, "bOrigins", 15), (25, "tNames", 7), (26, "bNames", 7), (27, "tValues", 7),
          (28, "bValues", 7), (29, "tStop", 7), (30, "bStop", 7), (31, "tCream", 7),
          (32, "bCream", 7), (35, "tGlue", 7), (36, "bGlue", 7), (39, "tKeepout", 4),
          (40, "bKeepout", 1), (41, "tRestrict", 4), (42, "bRestrict", 1), (43, "vRestrict", 2),
          (44, "Drills", 7), (45, "Holes", 7), (46, "Milling", 3), (47, "Measures", 7),
          (48, "Document", 7), (49, "Reference", 7), (51, "tDocu", 7), (52, "bDocu", 7),
          (91, "Nets", 2), (92, "Busses", 1), (93, "Pins", 2), (94, "Symbols", 4), (95, "Names", 7),
          (96, "Values", 7), (97, "Info", 7), (98, "Guide", 6)]


def f(v):
    return f"{v:.4f}".rstrip("0").rstrip(".") if v != 0 else "0"


def a(s):
    return escape(str(s), {'"': "&quot;"})


def pad_positions(h):
    """Yield (padname, pinname, x, y) for header h (board coords)."""
    out = []
    n = len(h["pins"])
    for i, pin in enumerate(h["pins"]):
        if h["rows"] == 2:
            k, row = divmod(i, 2)
        else:
            k, row = i, 0
        dx, dy = (h["pitch"] * k, 0) if h["dir"] == "h" else (0, h["pitch"] * k)
        x, y = h["x"] + dx, h["y"] + dy
        if row == 1:
            x += h["row_off"][0]
            y += h["row_off"][1]
        out.append((f"{h['name']}-{i + 1}", pin, x, y))
    return out


def gates_of(m):
    total = sum(len(h["pins"]) for h in m["hdrs"])
    if m["gates"] == "single" or (m["gates"] == "auto" and total <= 40) or len(m["hdrs"]) == 1:
        return [("G$1", m["hdrs"])]
    return [(h["name"], [h]) for h in m["hdrs"]]


def uniq_names(names):
    """EAGLE needs unique pin names per symbol; duplicates get @n (hidden suffix)."""
    cnt = Counter(n.split("@")[0] if "@" in n else n for n in names)
    seen = defaultdict(int)
    res = []
    for n in names:
        if "@" in n:
            res.append(n)
            continue
        if cnt[n] > 1:
            seen[n] += 1
            res.append(f"{n}@{seen[n]}")
        else:
            res.append(n)
    return res


# ------------------------------------------------------------------ package
def package_xml(m):
    w, h = m["w"], m["h"]
    cx, cy = w / 2, h / 2
    L = [f'<package name="{a(m["name"])}">',
         f'<description>{a(m["desc"])} | Kart: {w} x {h} mm | Guven: {m["conf"]}</description>']
    # outline (tDocu full, tPlace too) - centred on origin
    if m["outline"] == "circle":
        r = w / 2
        L.append(f'<circle x="0" y="0" radius="{f(r)}" width="0.2" layer="51"/>')
        L.append(f'<circle x="0" y="0" radius="{f(r)}" width="0.15" layer="21"/>')
    else:
        pts = [(-cx, -cy), (cx, -cy), (cx, cy), (-cx, cy)]
        for i in range(4):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % 4]
            L.append(f'<wire x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" width="0.2" layer="51"/>')
            L.append(f'<wire x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" width="0.15" layer="21"/>')
    # keepout on bottom side not needed; add body restrict for 3D clearance hint
    for hd in m["hdrs"]:
        for pname, pin, x, y in pad_positions(hd):
            X, Y = x - cx, y - cy
            if hd["drill"] == 0:  # SMD (FPC)
                L.append(f'<smd name="{a(pname)}" x="{f(X)}" y="{f(Y)}" dx="0.6" dy="2.0" layer="1"/>')
            else:
                first = pname.endswith("-1")
                shape = "square" if first else "round"
                L.append(f'<pad name="{a(pname)}" x="{f(X)}" y="{f(Y)}" drill="{f(hd["drill"])}" '
                         f'diameter="{f(hd["dia"])}" shape="{shape}"/>')
        # header label in tDocu
        px, py = hd["x"] - cx, hd["y"] - cy
        L.append(f'<text x="{f(px)}" y="{f(py + 1.6)}" size="0.8" layer="51">{a(hd["name"])}</text>')
    for (x, y, d) in m["holes"]:
        L.append(f'<hole x="{f(x - cx)}" y="{f(y - cy)}" drill="{f(d)}"/>')
    L.append(f'<text x="{f(-cx)}" y="{f(cy + 1.0)}" size="1.27" layer="25">&gt;NAME</text>')
    L.append(f'<text x="{f(-cx)}" y="{f(-cy - 2.3)}" size="1.27" layer="27">&gt;VALUE</text>')
    L.append("</package>")
    return "\n".join(L)


# ------------------------------------------------------------------ symbol
def symbol_xml(symname, title, pins):
    """pins: list of unique names. Left column = first half, right = second half."""
    n = len(pins)
    nl = math.ceil(n / 2)
    left, right = pins[:nl], pins[nl:]
    disp = lambda s: s.split("@")[0]
    longest = max((len(disp(p)) for p in pins), default=4)
    half_w = max(7.62, math.ceil((longest * 1.778 * 0.75 + 2.54) / P) * P)
    rows = max(len(left), len(right))
    top = (rows + 1) * P / 2
    top = math.ceil(top / P) * P
    bot = top - (rows + 1) * P
    L = [f'<symbol name="{a(symname)}">']
    for (x1, y1, x2, y2) in [(-half_w, top, half_w, top), (half_w, top, half_w, bot),
                             (half_w, bot, -half_w, bot), (-half_w, bot, -half_w, top)]:
        L.append(f'<wire x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" width="0.254" layer="94"/>')
    for i, p in enumerate(left):
        y = top - P * (i + 1)
        L.append(f'<pin name="{a(p)}" x="{f(-half_w - 5.08)}" y="{f(y)}" length="middle" direction="pas"/>')
    for i, p in enumerate(right):
        y = top - P * (i + 1)
        L.append(f'<pin name="{a(p)}" x="{f(half_w + 5.08)}" y="{f(y)}" length="middle" direction="pas" rot="R180"/>')
    L.append(f'<text x="{f(-half_w)}" y="{f(top + 1.0)}" size="1.778" layer="95">&gt;NAME</text>')
    L.append(f'<text x="{f(-half_w)}" y="{f(bot - 2.8)}" size="1.778" layer="96">&gt;VALUE</text>')
    L.append(f'<text x="0" y="{f(bot + 1.2)}" size="1.27" layer="97" align="bottom-center">{a(title)}</text>')
    L.append("</symbol>")
    return "\n".join(L)


def build_module(m):
    syms, connects, gates = [], [], []
    for gname, hds in gates_of(m):
        pads = [pp for hd in hds for pp in pad_positions(hd)]
        names = uniq_names([p[1] for p in pads])
        symname = m["name"] if gname == "G$1" else f'{m["name"]}_{gname}'
        title = m["name"] if gname == "G$1" else f'{m["name"]} {gname}'
        syms.append(symbol_xml(symname, title, names))
        gates.append((gname, symname))
        for (pname, _, _, _), pn in zip(pads, names):
            connects.append((gname, pn, pname))
    gx = []
    for i, (gname, symname) in enumerate(gates):
        gx.append(f'<gate name="{a(gname)}" symbol="{a(symname)}" x="{f((i % 3) * 50.8)}" y="{f(-(i // 3) * 76.2)}"/>')
    desc = (f'<b>{m["name"]}</b><br/>{m["desc"]}<br/>Kart: {m["w"]} x {m["h"]} mm - Guven: {m["conf"]}'
            f'<br/>STEP: {m["step"]}' + (f'<br/>NOT: {m["notes"]}' if m["notes"] else ""))
    ds = [f'<deviceset name="{a(m["name"])}" prefix="{a(m["prefix"])}">',
          f'<description>{escape(desc)}</description>',
          "<gates>", *gx, "</gates>", "<devices>",
          f'<device name="" package="{a(m["name"])}">', "<connects>"]
    for g, pn, pad in connects:
        ds.append(f'<connect gate="{a(g)}" pin="{a(pn)}" pad="{a(pad)}"/>')
    ds += ["</connects>", "<technologies>", '<technology name="">',
           f'<attribute name="BOARD_SIZE" value="{m["w"]}x{m["h"]}mm" constant="no"/>',
           f'<attribute name="CONFIDENCE" value="{m["conf"]}" constant="no"/>',
           "</technology>", "</technologies>", "</device>", "</devices>", "</deviceset>"]
    return package_xml(m), syms, "\n".join(ds)


def build_lib(key):
    fname, ldesc = LIBS[key]
    mods = [m for m in M if m["lib"] == key]
    pk, sy, ds = [], [], []
    for m in mods:
        p, s, d = build_module(m)
        pk.append(p)
        sy += s
        ds.append(d)
    layers = "\n".join(f'<layer number="{n}" name="{nm}" color="{c}" fill="1" visible="yes" active="yes"/>'
                       for n, nm, c in LAYERS)
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
{layers}
</layers>
<library>
<description>&lt;b&gt;{a(fname)}&lt;/b&gt; - moto-platform modul kutuphanesi. {a(ldesc)}. Footprint olculeri yaygin varyanttan alinmistir; fiziksel kartla dogrulayin (README).</description>
<packages>
{chr(10).join(pk)}
</packages>
<symbols>
{chr(10).join(sy)}
</symbols>
<devicesets>
{chr(10).join(ds)}
</devicesets>
</library>
</drawing>
</eagle>
'''
    return fname, xml, mods


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for key in LIBS:
        fname, xml, mods = build_lib(key)
        with open(os.path.join(OUT, fname + ".lbr"), "w", encoding="utf-8") as fh:
            fh.write(xml)
        print(fname, len(mods), "modul")
