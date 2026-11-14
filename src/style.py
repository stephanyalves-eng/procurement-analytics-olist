"""Stephany Alves Design System (tokens v1.1.0) applied to Plotly charts.

Import once per notebook: `from src.style import C, finish, save`.
Rules kept from the design system: rows-only gridlines, zero baseline,
one highlighted series with the rest in context grey, color by business
meaning (favorable / unfavorable), mono labels for axes and sources.
"""
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

C = {
    "ink": "#101714",          # sa-near-black, text primary
    "ink_2": "#454C48",        # sa-gray-700, text secondary
    "page": "#F5F4EC",         # sa-ivory, surface page
    "forest_900": "#0B302B",   # Deep Forest, key mark
    "forest_700": "#1E5246",   # primary series (dv-cat-1)
    "forest_500": "#4A8574",
    "sage_500": "#8FA99D",     # secondary series (dv-cat-2)
    "context": "#D6D8D2",      # dv-context, greyed series
    "grid": "#E8E9E5",         # dv-gridline
    "axis": "#5E6561",         # dv-axis
    "baseline": "#BDC1BB",     # dv-baseline
    "favorable": "#1F7A4F",    # dv-favorable
    "unfavorable": "#A63A2A",  # dv-unfavorable
    "neutral": "#858B86",      # dv-neutral
}
SEQ = ["#EEF3EF", "#D2DED7", "#A9C1B5", "#7A9E8E", "#4A8574", "#2F6B5B", "#0B302B"]

SANS = "IBM Plex Sans, Arial, sans-serif"
MONO = "IBM Plex Mono, Consolas, monospace"
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
    title=dict(x=0, xanchor="left", y=0.95, font=dict(family=SANS, size=20, color=C["ink"])),
    margin=dict(l=80, r=40, t=110, b=110),
    xaxis=dict(showgrid=False, zeroline=False, **_axis),
    yaxis=dict(showgrid=True, gridcolor=C["grid"], zeroline=True,
               zerolinecolor=C["baseline"], **_axis),
    colorway=[C["forest_700"], C["sage_500"], "#4F6D8A", "#C49A45", "#B4694A"],
    legend=dict(orientation="h", x=1, xanchor="right", y=1.02, yanchor="bottom",
                font=dict(size=12, color=C["ink_2"])),
    hoverlabel=dict(font=dict(family=SANS)),
))
pio.templates.default = "sa"


def finish(fig, title, subtitle, source=SOURCE):
    """Title states the finding; subtitle gives metric, unit and period."""
    fig.update_layout(title=dict(
        text=f"{title}<br><span style='font-size:13px;color:{C['ink_2']}'>{subtitle}</span>"))
    fig.add_annotation(text=source, xref="paper", yref="paper", x=0, y=-0.2,
                       xanchor="left", yanchor="top", showarrow=False,
                       font=dict(family=MONO, size=10, color=C["axis"]))
    return fig


FIG_DIR = Path(__file__).resolve().parents[1] / "reports" / "figures"


def save(fig, name, width=1200, height=675):
    """PNG at 2x for README, LinkedIn carousel and articles."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_image(FIG_DIR / f"{name}.png", width=width, height=height, scale=2)
    return FIG_DIR / f"{name}.png"
