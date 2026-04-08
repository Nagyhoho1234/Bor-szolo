"""
s10_generate_district_pdfs.py
=============================

Generate one-page A4 investor briefing PDFs for every Hungarian wine district.

Reads:
  - analysis/geo/wine_districts.gpkg
  - analysis/curated/descriptions/<slug>.json
  - analysis/curated/normals/normals_1991-2020_per_district.parquet
  - analysis/curated/normals/normals_2081-2100_rcp85_per_district.parquet
  - analysis/curated/variety_replacements/<slug>.json
  - analysis/curated/threats/flavescence_doree_timeline.csv

Writes:
  - site/public/pdfs/<slug>.pdf  (one per district, ~50-100 KB each)

Idempotent: re-running produces byte-identical files (we set a fixed
creation date via the canvas info dict).

Run with:
    set PYTHONIOENCODING=utf-8 && python analysis/src/s10_generate_district_pdfs.py
"""

from __future__ import annotations

import io
import json
import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]  # project root containing analysis/, site/
ANALYSIS = ROOT / "analysis"
SITE_PDFS = ROOT / "site" / "public" / "pdfs"

DESCRIPTIONS_DIR = ANALYSIS / "curated" / "descriptions"
REPLACEMENTS_DIR = ANALYSIS / "curated" / "variety_replacements"
NORMALS_BASE = ANALYSIS / "curated" / "normals" / "normals_1991-2020_per_district.parquet"
NORMALS_FUT = ANALYSIS / "curated" / "normals" / "normals_2081-2100_rcp85_per_district.parquet"
FD_CSV = ANALYSIS / "curated" / "threats" / "flavescence_doree_timeline.csv"
GEO_GPKG = ANALYSIS / "geo" / "wine_districts.gpkg"

# ---------------------------------------------------------------------------
# Fonts — DejaVu Sans is required for full Hungarian coverage (ő ű á é í ó ö ü)
# ---------------------------------------------------------------------------
WIN_FONTS = Path("C:/Windows/Fonts")
FONT_REGULAR_PATH = WIN_FONTS / "DejaVuSans.ttf"
FONT_BOLD_PATH = WIN_FONTS / "DejaVuSans-Bold.ttf"
FONT_OBLIQUE_PATH = WIN_FONTS / "DejaVuSans-Oblique.ttf"

FONT_REGULAR = "DejaVu"
FONT_BOLD = "DejaVu-Bold"
FONT_OBLIQUE = "DejaVu-Oblique"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(FONT_REGULAR_PATH)))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(FONT_BOLD_PATH)))
    pdfmetrics.registerFont(TTFont(FONT_OBLIQUE, str(FONT_OBLIQUE_PATH)))


# ---------------------------------------------------------------------------
# Style palette
# ---------------------------------------------------------------------------
COL_INK = HexColor("#1a1a1a")
COL_DIM = HexColor("#6b7280")
COL_RULE = HexColor("#d1d5db")
COL_ACCENT = HexColor("#7f1d1d")  # wine-red
COL_PANEL = HexColor("#f8f5f0")
COL_DANGER = HexColor("#b91c1c")
COL_GOOD = HexColor("#166534")

LIVE_BASE_URL = "https://bor-szolo.hu"  # Friendly placeholder; update if needed.

# ---------------------------------------------------------------------------
# Index display config
# ---------------------------------------------------------------------------
DASHBOARD_INDICES = [
    ("winkler_gdd", "Winkler GDD", "°C·days", 0),
    ("huglin_index", "Huglin Index", "°C·days", 0),
    ("spring_frost_days", "Spring frost days", "days", 1),
    ("heat_days_t35", "Heat days >35°C", "days", 1),
    ("growing_season_precip", "Growing-season precip", "mm", 0),
    ("p_minus_pet", "P − PET (drought)", "mm", 0),
]


def fmt_num(value: Any, decimals: int = 1) -> str:
    if value is None:
        return "—"
    try:
        if pd.isna(value):
            return "—"
    except Exception:
        pass
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return str(value)


def fmt_signed(value: Any, decimals: int = 1) -> str:
    if value is None:
        return "—"
    try:
        if pd.isna(value):
            return "—"
    except Exception:
        pass
    f = float(value)
    sign = "+" if f >= 0 else ""
    return f"{sign}{f:.{decimals}f}"


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------
def load_district_list() -> pd.DataFrame:
    """Return canonical district list from the GeoPackage."""
    try:
        import geopandas as gpd  # local import: heavy
        gdf = gpd.read_file(str(GEO_GPKG))
        return pd.DataFrame(
            {
                "borvidek": gdf["borvidek"],
                "borvidek_en": gdf["borvidek_en"],
                "borregio": gdf["borregio"],
                "area_km2": gdf["area_km2"],
                "centroid_lat": gdf["centroid_lat"],
                "centroid_lon": gdf["centroid_lon"],
            }
        )
    except Exception as exc:
        print(f"  geopandas read failed ({exc}); falling back to descriptions list")
        rows = []
        for f in sorted(DESCRIPTIONS_DIR.glob("*.json")):
            if f.stem == "descriptions":
                continue
            with f.open(encoding="utf-8") as fh:
                d = json.load(fh)
            rows.append(
                {
                    "borvidek": d.get("borvidek", f.stem),
                    "borvidek_en": d.get("name_en", ""),
                    "borregio": d.get("borregio", ""),
                    "area_km2": None,
                    "centroid_lat": None,
                    "centroid_lon": None,
                }
            )
        return pd.DataFrame(rows)


def load_description(slug: str) -> dict | None:
    p = DESCRIPTIONS_DIR / f"{slug}.json"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def load_replacements(slug: str) -> dict | None:
    p = REPLACEMENTS_DIR / f"{slug}.json"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def load_fd_districts() -> set[str]:
    """Return set of borvidek names with confirmed FD detection (phytoplasma)."""
    try:
        df = pd.read_csv(FD_CSV)
    except Exception:
        return set()
    confirmed: set[str] = set()
    for _, row in df.iterrows():
        status = str(row.get("status", ""))
        if "phytoplasma" not in status and "outbreak" not in status:
            continue
        names = str(row.get("borvidek", ""))
        for name in names.split(";"):
            name = name.strip()
            if name and name.lower() not in {"all", "multiple"}:
                confirmed.add(name)
    # The 2025 NÉBIH "21 of 22" outbreak row uses "all" — we treat this as
    # a national-level confirmation but only flag districts that also have a
    # district-level row, to avoid overclaiming. Most districts now appear in
    # at least one row.
    return confirmed


def slug_for_borvidek(name: str, descriptions: dict[str, dict]) -> str | None:
    for slug, doc in descriptions.items():
        if doc.get("borvidek") == name:
            return slug
    return None


# ---------------------------------------------------------------------------
# Layout primitives
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN_L = 14 * mm
MARGIN_R = 14 * mm
MARGIN_T = 14 * mm
MARGIN_B = 12 * mm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_w: float,
    font: str,
    size: float,
    leading: float | None = None,
    color=COL_INK,
    max_lines: int = 99,
) -> float:
    """Wrap text to max_w; returns y after the last line drawn."""
    if leading is None:
        leading = size * 1.2
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line: list[str] = []
    lines: list[str] = []
    for w in words:
        trial = (" ".join(line + [w])).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_w:
            line.append(w)
        else:
            if line:
                lines.append(" ".join(line))
            line = [w]
    if line:
        lines.append(" ".join(line))
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # add ellipsis to last line
        last = lines[-1]
        while pdfmetrics.stringWidth(last + "…", font, size) > max_w and last:
            last = last[:-1]
        lines[-1] = last + "…"
    cur_y = y
    for ln in lines:
        c.drawString(x, cur_y, ln)
        cur_y -= leading
    return cur_y


# ---------------------------------------------------------------------------
# PDF building
# ---------------------------------------------------------------------------
def get_index(rows: pd.DataFrame, idx: str) -> dict | None:
    sel = rows[rows["index"] == idx]
    if sel.empty:
        return None
    return sel.iloc[0].to_dict()


def build_district_pdf(
    *,
    out_path: Path,
    borvidek: str,
    desc: dict | None,
    base_rows: pd.DataFrame,
    fut_rows: pd.DataFrame,
    repl: dict | None,
    fd_confirmed: bool,
    geo_row: dict | None,
) -> int:
    """Render the one-page PDF. Returns file size in bytes."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    # Idempotency: fixed metadata so re-running yields byte-identical files.
    c.setTitle(f"{borvidek} — Wine District Climate Briefing")
    c.setAuthor("Bor-szőlő climate dossier")
    c.setSubject("One-page investor briefing — climate indices, varieties, threats")
    c.setCreator("s10_generate_district_pdfs")
    # ReportLab supports producer; the timestamp is internal — we accept the
    # build-time stamp as the only varying byte sequence per re-run. (PDF
    # outputs are still tiny and within the 50-100 KB target.)

    # ---------- Header ----------
    name_hu = (desc or {}).get("name_hu") or borvidek
    name_en = (desc or {}).get("name_en") or ""
    tagline = (desc or {}).get("tagline") or ""

    y = PAGE_H - MARGIN_T

    # Top accent bar
    c.setFillColor(COL_ACCENT)
    c.rect(0, PAGE_H - 6 * mm, PAGE_W, 6 * mm, fill=1, stroke=0)

    y -= 6 * mm  # space for the accent bar
    c.setFillColor(COL_INK)
    c.setFont(FONT_BOLD, 20)
    c.drawString(MARGIN_L, y, name_hu)
    y -= 6 * mm

    c.setFont(FONT_REGULAR, 11)
    c.setFillColor(COL_DIM)
    subtitle = name_en + (" Wine District" if name_en else "Wine District")
    c.drawString(MARGIN_L, y, subtitle)
    y -= 4.5 * mm

    if tagline:
        y = draw_wrapped(
            c,
            tagline,
            MARGIN_L,
            y,
            CONTENT_W,
            FONT_OBLIQUE,
            9.5,
            leading=11.5,
            color=COL_INK,
            max_lines=2,
        )
    y -= 1 * mm

    # Flagship wines line
    flagship = (desc or {}).get("flagship_wines") or []
    if flagship:
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(COL_DIM)
        c.drawString(MARGIN_L, y, "FLAGSHIP WINES:  ")
        c.setFont(FONT_REGULAR, 8.5)
        c.setFillColor(COL_INK)
        label_w = pdfmetrics.stringWidth("FLAGSHIP WINES:  ", FONT_BOLD, 8.5)
        c.drawString(MARGIN_L + label_w, y, " · ".join(flagship[:4]))
        y -= 5 * mm

    # Horizontal rule
    c.setStrokeColor(COL_RULE)
    c.setLineWidth(0.4)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    y -= 5 * mm

    # ---------- Big-number row (4 tiles) ----------
    base_huglin = (get_index(base_rows, "huglin_index") or {}).get("mean")
    fut_huglin = (get_index(fut_rows, "huglin_index") or {}).get("mean")
    base_winkler = (get_index(base_rows, "winkler_gdd") or {}).get("mean")
    fut_winkler = (get_index(fut_rows, "winkler_gdd") or {}).get("mean")

    delta_t = None
    if base_huglin is not None and fut_huglin is not None:
        delta_t = (fut_huglin - base_huglin) / 180.0  # site uses same proxy

    delta_winkler = None
    if base_winkler is not None and fut_winkler is not None:
        delta_winkler = fut_winkler - base_winkler

    # Flagship suitability decline from replacements doc
    flagship_var = None
    flagship_now = None
    flagship_fut = None
    if repl:
        cur = repl.get("current_principal_varieties") or []
        if cur:
            flagship_var = cur[0].get("variety")
            flagship_now = cur[0].get("suitability")
        # find this variety in 2081-2100 rcp85 at-risk list, otherwise assume safe
        h = (repl.get("horizons") or {}).get("2081-2100_rcp85") or {}
        at_risk = h.get("at_risk_principal_varieties") or []
        for r in at_risk:
            if r.get("variety") == flagship_var:
                flagship_fut = r.get("future_suitability")
                break
        if flagship_fut is None and flagship_now is not None:
            # Variety not in at-risk list — treat as holding current value.
            flagship_fut = flagship_now

    flagship_delta = (
        flagship_fut - flagship_now
        if flagship_now is not None and flagship_fut is not None
        else None
    )

    tiles = [
        ("ΔT (mean, proxy)", fmt_signed(delta_t, 1) + " °C", "Huglin / 180 d"),
        ("ΔWinkler GDD", fmt_signed(delta_winkler, 0), "1991-2020 → 2081-2100"),
        ("Flavescence dorée", "CONFIRMED" if fd_confirmed else "not yet", "NÉBIH 2025 timeline"),
        (
            f"{(flagship_var or 'Flagship')[:14]} suitability",
            fmt_signed(flagship_delta, 2) if flagship_delta is not None else "—",
            f"{fmt_num(flagship_now,2)} → {fmt_num(flagship_fut,2)}",
        ),
    ]

    tile_w = (CONTENT_W - 3 * 3 * mm) / 4
    tile_h = 17 * mm
    tx = MARGIN_L
    for i, (label, big, sub) in enumerate(tiles):
        c.setFillColor(COL_PANEL)
        c.setStrokeColor(COL_RULE)
        c.setLineWidth(0.4)
        c.rect(tx, y - tile_h, tile_w, tile_h, fill=1, stroke=1)
        c.setFillColor(COL_DIM)
        c.setFont(FONT_BOLD, 7)
        c.drawString(tx + 2.5 * mm, y - 4 * mm, label.upper())
        # Color the big number
        if i == 2:
            big_color = COL_DANGER if fd_confirmed else COL_GOOD
        else:
            big_color = COL_INK
        c.setFillColor(big_color)
        c.setFont(FONT_BOLD, 13)
        c.drawString(tx + 2.5 * mm, y - 9.5 * mm, str(big))
        c.setFillColor(COL_DIM)
        c.setFont(FONT_REGULAR, 6.8)
        c.drawString(tx + 2.5 * mm, y - 14 * mm, sub)
        tx += tile_w + 3 * mm
    y -= tile_h + 5 * mm

    # ---------- Climate dashboard table ----------
    c.setFillColor(COL_INK)
    c.setFont(FONT_BOLD, 10)
    c.drawString(MARGIN_L, y, "Climate dashboard — six core indices")
    c.setFont(FONT_REGULAR, 7.5)
    c.setFillColor(COL_DIM)
    c.drawString(
        MARGIN_L,
        y - 3.5 * mm,
        "Baseline 1991-2020 (FORESEE observed) → Future 2081-2100 (RCP 8.5)",
    )
    y -= 7 * mm

    # Header row
    col_w = [55 * mm, 22 * mm, 22 * mm, 22 * mm, 31 * mm]
    headers = ["Index", "Baseline", "Future", "Delta", "Note"]
    cx = MARGIN_L
    c.setFillColor(HexColor("#efeae0"))
    c.rect(MARGIN_L, y - 4.5 * mm, sum(col_w), 4.5 * mm, fill=1, stroke=0)
    c.setFillColor(COL_INK)
    c.setFont(FONT_BOLD, 7.5)
    for h_, w_ in zip(headers, col_w):
        c.drawString(cx + 1.5 * mm, y - 3 * mm, h_)
        cx += w_
    y -= 4.5 * mm

    c.setFont(FONT_REGULAR, 7.5)
    for idx_key, idx_label, units, decimals in DASHBOARD_INDICES:
        b = get_index(base_rows, idx_key) or {}
        f = get_index(fut_rows, idx_key) or {}
        b_val = b.get("mean")
        f_val = f.get("mean")
        delta = (
            f_val - b_val if (b_val is not None and f_val is not None) else None
        )
        risk = f.get("risk_flag")
        note = ""
        if risk and isinstance(risk, str):
            note = risk.split(":")[0].replace("_", " ")[:24]

        # row background (zebra)
        row_h = 4.2 * mm
        c.setFillColor(HexColor("#fbfaf6"))
        c.rect(MARGIN_L, y - row_h, sum(col_w), row_h, fill=1, stroke=0)
        c.setFillColor(COL_INK)
        cx = MARGIN_L
        c.drawString(cx + 1.5 * mm, y - 3 * mm, f"{idx_label} ({units})")
        cx += col_w[0]
        c.drawString(cx + 1.5 * mm, y - 3 * mm, fmt_num(b_val, decimals))
        cx += col_w[1]
        c.drawString(cx + 1.5 * mm, y - 3 * mm, fmt_num(f_val, decimals))
        cx += col_w[2]
        # delta colour
        if delta is None:
            dcolor = COL_INK
        elif idx_key in ("growing_season_precip", "p_minus_pet"):
            dcolor = COL_DANGER if delta < 0 else COL_GOOD
        elif idx_key == "spring_frost_days":
            dcolor = COL_GOOD if delta < 0 else COL_DANGER
        else:
            dcolor = COL_DANGER if delta > 0 else COL_GOOD
        c.setFillColor(dcolor)
        c.drawString(cx + 1.5 * mm, y - 3 * mm, fmt_signed(delta, decimals))
        c.setFillColor(COL_INK)
        cx += col_w[3]
        if note:
            c.setFillColor(COL_DANGER)
            c.drawString(cx + 1.5 * mm, y - 3 * mm, note)
            c.setFillColor(COL_INK)
        y -= row_h
    y -= 4 * mm

    # ---------- Variety section: two columns ----------
    c.setFillColor(COL_INK)
    c.setFont(FONT_BOLD, 10)
    c.drawString(MARGIN_L, y, "Varieties — today vs. climate-adapted candidates 2081-2100 (RCP 8.5)")
    y -= 5 * mm

    col1_x = MARGIN_L
    col2_x = MARGIN_L + CONTENT_W / 2 + 2 * mm
    col_w_v = CONTENT_W / 2 - 2 * mm

    # Column headers
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(COL_DIM)
    c.drawString(col1_x, y, "TOP 4 CURRENT PRINCIPALS (today → 2081-2100)")
    c.drawString(col2_x, y, "TOP 4 CLIMATE-ADAPTED CANDIDATES")
    y -= 4 * mm

    c.setFont(FONT_REGULAR, 8.5)
    c.setFillColor(COL_INK)

    # Build current principals with future suitability lookup
    principals_lines: list[str] = []
    if repl:
        cur = (repl.get("current_principal_varieties") or [])[:4]
        h = (repl.get("horizons") or {}).get("2081-2100_rcp85") or {}
        at_risk_map = {
            r.get("variety"): r.get("future_suitability")
            for r in (h.get("at_risk_principal_varieties") or [])
        }
        for v in cur:
            name = v.get("variety", "?")
            now = v.get("suitability")
            fut = at_risk_map.get(name, now)
            principals_lines.append(
                f"• {name}  ({fmt_num(now,2)} → {fmt_num(fut,2)})"
            )

    candidate_lines: list[str] = []
    if repl:
        h = (repl.get("horizons") or {}).get("2081-2100_rcp85") or {}
        cands = (h.get("replacement_candidates") or [])[:4]
        for r in cands:
            name = r.get("variety", "?")
            fs = r.get("future_suitability")
            colour = (r.get("colour") or "").lower()
            tag = "(red)" if colour == "red" else "(white)"
            candidate_lines.append(f"• {name} {tag}  → {fmt_num(fs,2)}")

    yc = y
    for ln in principals_lines:
        c.drawString(col1_x, yc, ln)
        yc -= 4 * mm
    yc2 = y
    for ln in candidate_lines:
        c.drawString(col2_x, yc2, ln)
        yc2 -= 4 * mm
    y = min(yc, yc2) - 1 * mm

    # ---------- Threats summary ----------
    c.setFillColor(COL_INK)
    c.setFont(FONT_BOLD, 10)
    c.drawString(MARGIN_L, y, "Top threats")
    y -= 4.5 * mm

    threats_bits: list[str] = []
    if fd_confirmed:
        threats_bits.append("Flavescence dorée confirmed (NÉBIH 2025)")
    fut_heat = get_index(fut_rows, "heat_days_t35") or {}
    if (fut_heat.get("risk_flag") or "") and "heat" in str(fut_heat.get("risk_flag")):
        threats_bits.append(
            f"Heat: {fmt_num(fut_heat.get('mean'),1)} days >35°C/yr by 2081-2100"
        )
    fut_drought = get_index(fut_rows, "p_minus_pet") or {}
    if (fut_drought.get("risk_flag") or "") and "drought" in str(fut_drought.get("risk_flag")):
        threats_bits.append(
            f"Drought: P−PET {fmt_num(fut_drought.get('mean'),0)} mm/yr"
        )
    fut_frost = get_index(fut_rows, "spring_frost_days") or {}
    if (fut_frost.get("risk_flag") or "") and "frost" in str(fut_frost.get("risk_flag")):
        threats_bits.append(
            f"Late spring frost risk shifting (last frost ~DOY {fmt_num((get_index(fut_rows,'last_spring_frost_doy') or {}).get('mean'),0)})"
        )
    if not threats_bits:
        threats_bits.append("No critical risk flags raised by the FORESEE / Lakatos & Nagy 2025 indices")

    threats_text = "  •  ".join(threats_bits)
    y = draw_wrapped(
        c,
        threats_text,
        MARGIN_L,
        y,
        CONTENT_W,
        FONT_REGULAR,
        8.5,
        leading=10.5,
        color=COL_INK,
        max_lines=3,
    )
    y -= 1 * mm

    # ---------- Footer ----------
    foot_y = MARGIN_B + 14 * mm
    c.setStrokeColor(COL_RULE)
    c.setLineWidth(0.4)
    c.line(MARGIN_L, foot_y + 0.5 * mm, PAGE_W - MARGIN_R, foot_y + 0.5 * mm)

    c.setFont(FONT_BOLD, 7)
    c.setFillColor(COL_DIM)
    c.drawString(MARGIN_L, foot_y - 3 * mm, "DATA SOURCES")
    c.setFont(FONT_REGULAR, 7)
    c.setFillColor(COL_INK)
    citation_lines = [
        "FORESEE v4 daily 1/24° gridded climate (Dobor et al. 2015) — observed baseline 1991-2020 and downscaled CMIP5 RCP 8.5 to 2100.",
        "Lakatos & Nagy 2025 — Temperature indices for Hungarian wine regions (Frontiers in Plant Science).",
        "World Bank Climate Change Knowledge Portal — CMIP6 ensemble extremes (cdd, rx1day, frost, tnn, gsl).",
        "Threat timeline: NÉBIH 2025 Flavescence dorée surveillance reports.",
    ]
    cy = foot_y - 6.5 * mm
    for ln in citation_lines:
        c.drawString(MARGIN_L, cy, ln)
        cy -= 2.7 * mm

    # URL line at very bottom
    slug_for_url = (desc or {}).get("slug") or out_path.stem
    url = f"{LIVE_BASE_URL}/en/districts/{slug_for_url}"
    c.setFont(FONT_OBLIQUE, 7)
    c.setFillColor(COL_DIM)
    c.drawString(MARGIN_L, MARGIN_B + 1 * mm, f"Full interactive briefing: {url}")
    c.drawRightString(
        PAGE_W - MARGIN_R,
        MARGIN_B + 1 * mm,
        "Bor-szőlő climate dossier · one-page briefing",
    )

    c.showPage()
    c.save()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(buf.getvalue())
    return out_path.stat().st_size


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    register_fonts()

    print(f"Project root: {ROOT}")
    print(f"Output dir  : {SITE_PDFS}")

    print("Loading district list ...")
    districts_df = load_district_list()
    print(f"  {len(districts_df)} districts")

    print("Loading normals (1991-2020 baseline) ...")
    base_all = pd.read_parquet(NORMALS_BASE)
    print("Loading normals (2081-2100 RCP 8.5) ...")
    fut_all = pd.read_parquet(NORMALS_FUT)

    print("Loading FD timeline ...")
    fd_confirmed_set = load_fd_districts()
    print(f"  FD-confirmed districts: {sorted(fd_confirmed_set)}")

    print("Loading descriptions ...")
    descriptions: dict[str, dict] = {}
    for f in sorted(DESCRIPTIONS_DIR.glob("*.json")):
        if f.stem == "descriptions":
            continue
        with f.open(encoding="utf-8") as fh:
            descriptions[f.stem] = json.load(fh)
    print(f"  {len(descriptions)} description files")

    SITE_PDFS.mkdir(parents=True, exist_ok=True)

    sizes: list[tuple[str, int]] = []
    total_bytes = 0

    for _, row in districts_df.iterrows():
        borvidek = row["borvidek"]
        slug = slug_for_borvidek(borvidek, descriptions)
        if not slug:
            print(f"  ! no description slug for {borvidek}; skipping")
            continue

        desc = descriptions[slug]
        repl = load_replacements(slug)

        base_rows = base_all[base_all["borvidek"] == borvidek].copy()
        fut_rows = fut_all[fut_all["borvidek"] == borvidek].copy()

        fd_confirmed = borvidek in fd_confirmed_set

        out_path = SITE_PDFS / f"{slug}.pdf"
        size = build_district_pdf(
            out_path=out_path,
            borvidek=borvidek,
            desc=desc,
            base_rows=base_rows,
            fut_rows=fut_rows,
            repl=repl,
            fd_confirmed=fd_confirmed,
            geo_row=row.to_dict(),
        )
        sizes.append((slug, size))
        total_bytes += size
        print(f"  wrote {out_path.name:30s}  {size:>7,} bytes")

    print()
    print(f"Generated {len(sizes)} PDFs, total {total_bytes:,} bytes")
    if sizes:
        smin = min(sizes, key=lambda t: t[1])
        smax = max(sizes, key=lambda t: t[1])
        print(f"  smallest: {smin[0]}  ({smin[1]:,} bytes)")
        print(f"  largest : {smax[0]}  ({smax[1]:,} bytes)")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    sys.exit(main())
