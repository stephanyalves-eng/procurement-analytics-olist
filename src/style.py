"""SA Design System 2.0 applied to Plotly charts.

Import once per notebook: `from src.style import C, finish, save`.
Palette from the 2.0 tokens (sa.css): Deep Forest, Graphite, Ivory 2, Stone,
Mist, Muted Sage, Mineral Bronze, plus the derived text and status colors.
Rules: rows-only gridlines, zero baseline, one highlighted series with the
rest in context grey, color by business meaning (favorable / unfavorable),
mono labels for axes and sources. Mineral Bronze is a brand accent, never a
status color, so it stays out of the data marks.
"""
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

# Keys are kept from v1 so the notebooks do not change; values follow 2.0.
C = {
    "ink": "#2B2F2E",              # Graphite, text primary
    "ink_2": "#4F615A",            # text muted (derived)
    "page": "#FBF9F4",             # Ivory 2, canvas
    "forest_900": "#06402B",       # Deep Forest, key mark
    "forest_700": "#06402B",       # Deep Forest, primary series
    "forest_500": "#6F857A",       # border strong (derived), secondary structure
    "sage_500": "#8FAF9E",         # Muted Sage, secondary series
    "context": "#A6B0A9",          # Mist, greyed series
    "grid": "#E7E2D9",             # Stone, gridlines
    "axis": "#4F615A",             # text muted, axis labels
    "baseline": "#A6B0A9",         # Mist, reference lines
    "favorable": "#235F46",        # success
    "unfavorable": "#9B3434",      # error
    "unfavorable_light": "#CB9690",  # error at 50% on Ivory 2 (secondary negative)
    "neutral": "#A6B0A9",          # Mist
    "accent": "#C97A3A",           # Mineral Bronze, decoration only
}
SEQ = ["#FBF9F4", "#E7E2D9", "#C5D3CB", "#8FAF9E", "#6F857A", "#4F615A", "#06402B"]

SANS = "IBM Plex Sans, Arial, sans-serif"
MONO = "IBM Plex Mono, Consolas, monospace"
SERIF = "Newsreader, Georgia, serif"
SOURCE = ("SOURCE · OLIST BRAZILIAN E-COMMERCE DATASET (KAGGLE, CC BY-NC-SA 4.0) · "
          "WINDOW JAN 2017 TO AUG 2018")

_axis = dict(
    linecolor=C["baseline"], tickcolor=C["baseline"], ticks="outside",
    tickfont=dict(family=MONO, size=11, color=C["axis"]),
    title=dict(font=dict(family=SANS, size=12, color=C["axis"])),
)

pio.templates["sa"] = go.layout.Template(layout=dict(
    font=dict(family=SANS, size=13, color=C["ink"]),
    paper_bgcolor=C["page"], plot_bgcolor=C["page"],
    title=dict(x=0, xref="paper", xanchor="left", y=0.93, font=dict(family=SERIF, size=24, color=C["forest_900"])),
    margin=dict(l=80, r=40, t=110, b=110),
    xaxis=dict(showgrid=False, zeroline=False, **_axis),
    yaxis=dict(showgrid=True, gridcolor=C["grid"], zeroline=True,
               zerolinecolor=C["baseline"], **_axis),
    colorway=[C["forest_700"], C["sage_500"], "#376C8C", "#705477", C["forest_500"]],
    legend=dict(orientation="h", x=1, xanchor="right", y=1.02, yanchor="bottom",
                font=dict(size=12, color=C["ink_2"])),
    hoverlabel=dict(font=dict(family=SANS)),
))
pio.templates.default = "sa"


def finish(fig, title, subtitle, source=SOURCE):
    """Title states the finding (Newsreader); subtitle gives metric, unit and period."""
    fig.update_layout(title=dict(
        text=f"{title}<br><span style='font-family:{SANS};font-size:13px;color:{C['ink_2']}'>{subtitle}</span>"))
    fig.add_annotation(text=source, xref="paper", yref="paper", x=0, y=-0.2,
                       xanchor="left", yanchor="top", showarrow=False,
                       font=dict(family=MONO, size=10, color=C["axis"]))
    # Mineral Bronze rule above the title: the 2.0 section marker, decoration only
    fig.add_shape(type="line", xref="paper", yref="paper", x0=0, x1=0.05, y0=1.2, y1=1.2,
                  line=dict(color=C["accent"], width=2))
    return fig


FIG_DIR = Path(__file__).resolve().parents[1] / "reports" / "figures"


def save(fig, name, width=1200, height=675):
    """PNG at 2x for README, LinkedIn carousel and articles."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_image(FIG_DIR / f"{name}.png", width=width, height=height, scale=2)
    return FIG_DIR / f"{name}.png"
