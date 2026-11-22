#!/usr/bin/env python3
"""Generate trace-light.svg and trace-dark.svg for github.com/sinonchum.

Restrained institutional palette (navy / slate / neutral gray, zero neon or gradients).
"""

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": dict(
        surface="#fafbfc",
        stroke="#d8dee6",
        ink="#0f172a",
        ink2="#475569",
        ink3="#64748b",
        base="#cbd5e1",
        series=["#64748b", "#1e3a5f", "#2563eb"],
        prompt="#64748b",
    ),
    "dark": dict(
        surface="#0d1117",
        stroke="#262c36",
        ink="#f0f6fc",
        ink2="#9ca3af",
        ink3="#6e7681",
        base="#30363d",
        series=["#6e7681", "#3b82f6", "#60a5fa"],
        prompt="#6e7681",
    ),
}

# (label, duration_note, start_year, end_year, series_index or None for neutral base)
SPANS = [
    ("Logistics & Mobile Info Eng.", "4 yr",    2013.7, 2017.5, None),
    ("Management & Strategy",        "3 yr",    2017.7, 2020.5, 0),
    ("IP & LegalTech Workflows",     "active",  2020.5, 2026.9, 1),
    ("AI Agents, Mobile & Comp. ML", "active",  2024.0, 2026.9, 2),
]

W, H = 780, 268
X0, X1 = 276, 704
T0, T1 = 2013.5, 2027.2
ROW0, ROWH, BARH = 76, 30, 13


def x(t: float) -> float:
    return X0 + (t - T0) / (T1 - T0) * (X1 - X0)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(mode: str) -> str:
    t = THEMES[mode]
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{MONO}" role="img" '
        f'aria-label="Career trajectory of Simon Qin rendered as execution spans: '
        f'Logistics and Mobile Information Engineering 2013 to 2017, Management and Strategy 2017 to 2020, '
        f'IP and LegalTech Workflows 2020 to present, AI Agents, Mobile and Competitive ML 2024 to present.">',
        f'<rect width="{W}" height="{H}" rx="8" fill="{t["surface"]}" stroke="{t["stroke"]}"/>',
        f'<text x="24" y="36" font-size="13" fill="{t["prompt"]}">$</text>',
        f'<text x="38" y="36" font-size="13" fill="{t["ink2"]}">'
        f'trace <tspan fill="{t["ink3"]}">--actor</tspan> simon-qin '
        f'<tspan fill="{t["ink3"]}">--view</tspan> spans</text>',
    ]

    for year in (2014, 2016, 2018, 2020, 2022, 2024, 2026):
        gx = x(year)
        o.append(
            f'<line x1="{gx:.1f}" y1="58" x2="{gx:.1f}" y2="{ROW0 + len(SPANS) * ROWH - 12}" '
            f'stroke="{t["stroke"]}" stroke-width="1"/>'
        )
        o.append(
            f'<text x="{gx:.1f}" y="{ROW0 + len(SPANS) * ROWH + 4}" font-size="10" '
            f'fill="{t["ink3"]}" text-anchor="middle">{year}</text>'
        )

    for i, (label, dur, a, b, ci) in enumerate(SPANS):
        y = ROW0 + i * ROWH
        fill = t["base"] if ci is None else t["series"][ci]
        bx, bw = x(a), max(4.0, x(b) - x(a))
        o.append(f'<text x="24" y="{y + 4}" font-size="12.5" fill="{t["ink"]}">{esc(label)}</text>')
        o.append(
            f'<rect x="{bx:.1f}" y="{y - BARH + 4:.1f}" width="{bw:.1f}" height="{BARH}" '
            f'rx="3" fill="{fill}"/>'
        )
        if dur:
            o.append(
                f'<text x="{bx + bw + 8:.1f}" y="{y + 4}" font-size="10.5" '
                f'fill="{t["ink3"]}">{esc(dur)}</text>'
            )

    fy = H - 34
    o.append(
        f'<text x="24" y="{fy}" font-size="12.5" fill="{t["ink"]}">'
        f'simon qin <tspan fill="{t["ink3"]}">·</tspan> '
        f'ai systems &amp; product builder <tspan fill="{t["ink3"]}">·</tspan> paris</text>'
    )
    o.append(
        f'<text x="24" y="{fy + 17}" font-size="11.5" fill="{t["ink2"]}">'
        f'non-linear path, same compilation target: systems that hold up when actually run.</text>'
    )
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    import pathlib

    out_dir = pathlib.Path(__file__).resolve().parent
    for mode in ("light", "dark"):
        p = out_dir / f"trace-{mode}.svg"
        p.write_text(build(mode), encoding="utf-8")
        print(f"wrote {p}")
