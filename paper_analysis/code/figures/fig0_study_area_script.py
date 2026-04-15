"""
Figure 0 — Study area map of the 22 Hungarian wine districts.
Coloured by borrégió (wine region group), with spotlight districts highlighted.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import matplotlib
matplotlib.use('Agg')

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects
from pathlib import Path

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
GEOJSON = Path(r"C:\Bor-szőlő\analysis\curated\wine_districts.geojson")
ADMIN8_SHP = Path(r"C:\Bor-szőlő\admin8.shp")
OUT_PDF = SCRIPT_DIR / "fig0_study_area.pdf"
OUT_PNG = SCRIPT_DIR / "fig0_study_area.png"

# ------------------------------------------------------------------
# Palette: borrégió → colour
# ------------------------------------------------------------------
REGION_COLORS = {
    "Felső-Pannon": "#7B4EA0",
    "Balaton":       "#2E8B57",
    "Pannon":        "#A51E37",
    "Duna":          "#E8A030",
    "Felső-Magyarországi": "#DC5A32",
    "Tokaj":         "#784628",
}

REGION_ENGLISH = {
    "Felső-Pannon":        "North Transdanubia",
    "Balaton":              "Balaton",
    "Pannon":               "Pannon",
    "Duna":                 "Duna",
    "Felső-Magyarországi":  "Northern Hungary",
    "Tokaj":                "Tokaj",
}

# ------------------------------------------------------------------
# Hungarian → English district display names
# ------------------------------------------------------------------
DISTRICT_ENGLISH = {
    "Soproni":              "Sopron",
    "Pannonhalmi":          "Pannonhalma",
    "Neszmélyi":            "Neszmély",
    "Móri":                 "Mór",
    "Etyek-Budai":          "Etyek-Buda",
    "Nagy-Somlói":          "Nagy-Somló",
    "Zalai":                "Zala",
    "Balatonfelvidéki":     "Balatonfelvidék",
    "Badacsonyi":           "Badacsony",
    "Balatonfüred-Csopaki": "Balatonfüred-Csopak",
    "Balatonboglári":       "Balatonboglár",
    "Tolnai":               "Tolna",
    "Szekszárdi":           "Szekszárd",
    "Pécsi":                "Pécs",
    "Villányi":             "Villány",
    "Hajós-Bajai":          "Hajós-Baja",
    "Csongrádi":            "Csongrád",
    "Kunsági":              "Kunság",
    "Mátrai":               "Mátra",
    "Egri":                 "Eger",
    "Bükki":                "Bükk",
    "Tokaji":               "Tokaj",
}

SPOTLIGHT = {"Sopron", "Tokaj", "Villány", "Csongrád"}

# ------------------------------------------------------------------
# Load and prepare data
# ------------------------------------------------------------------
gdf = gpd.read_file(GEOJSON)
gdf["en_name"] = gdf["borvidek"].map(DISTRICT_ENGLISH)
gdf["color"]   = gdf["borregio"].map(REGION_COLORS)

# Country outline from admin8 settlements (dissolved)
admin8 = gpd.read_file(ADMIN8_SHP)
# Reproject admin8 to match wine districts CRS if needed
if admin8.crs != gdf.crs:
    admin8 = admin8.to_crs(gdf.crs)
hungary = admin8.dissolve()

# ------------------------------------------------------------------
# Figure: 180 mm × 130 mm at 300 dpi
# ------------------------------------------------------------------
mm_to_inch = 1 / 25.4
fig, ax = plt.subplots(
    1, 1,
    figsize=(210 * mm_to_inch, 150 * mm_to_inch),
    dpi=300,
)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Country outline from admin8 — light grey fill + thin border
hungary.plot(ax=ax, facecolor="#f0f0f0", edgecolor="#AAAAAA", linewidth=0.6, zorder=0)

# District fills
for _, row in gdf.iterrows():
    is_spot = row["en_name"] in SPOTLIGHT
    gdf[gdf.index == row.name].plot(
        ax=ax,
        color=row["color"],
        edgecolor="black" if is_spot else "#444444",
        linewidth=2.0 if is_spot else 0.5,
        alpha=0.85,
    )

# Labels — place at centroid with manual offsets for crowded areas
LABEL_OFFSETS = {
    # Balaton cluster: spread labels to avoid overlap
    "Balatonfelvidék":     (0.15, 0.18),
    "Balatonfüred-Csopak": (0.55, 0.05),
    "Badacsony":           (-0.10, 0.12),
    "Zala":                (-0.45, -0.12),
    "Balatonboglár":       (0.1, -0.15),
    "Nagy-Somló":          (-0.15, 0.12),
    # Pannon: Pécs small polygon
    "Pécs":                (-0.15, -0.08),
}

for _, row in gdf.iterrows():
    centroid = row.geometry.representative_point()
    name = row["en_name"]
    dx, dy = LABEL_OFFSETS.get(name, (0, 0))
    ax.text(
        centroid.x + dx, centroid.y + dy,
        name,
        fontsize=8,
        ha="center", va="center",
        fontweight="bold" if name in SPOTLIGHT else "normal",
        color="white",
        path_effects=[
            matplotlib.patheffects.Stroke(linewidth=2.0, foreground="black"),
            matplotlib.patheffects.Normal(),
        ],
    )

# Legend — region colours with English names
legend_order = [
    "Felső-Pannon", "Balaton", "Pannon", "Duna",
    "Felső-Magyarországi", "Tokaj",
]
handles = [
    mpatches.Patch(
        facecolor=REGION_COLORS[r], edgecolor="#444444", linewidth=0.5,
        label=REGION_ENGLISH[r],
    )
    for r in legend_order
]
ax.legend(
    handles=handles,
    loc="lower left",
    fontsize=9,
    frameon=True,
    framealpha=0.9,
    edgecolor="#CCCCCC",
    title="Wine regions",
    title_fontsize=10,
)

# ------------------------------------------------------------------
# Scale bar (bottom-right)
# ------------------------------------------------------------------
# Get axis extent in data coordinates
x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()

# Scale bar: 100 km. CRS is EPSG:4326, so 1 degree longitude ≈ 111 km * cos(lat)
# At ~47°N, cos(47°) ≈ 0.682, so 1° ≈ 75.7 km. 100 km ≈ 1.32°
import numpy as np
lat_mid = (y0 + y1) / 2
km_per_deg_lon = 111.32 * np.cos(np.radians(lat_mid))
bar_len_deg = 100.0 / km_per_deg_lon  # 100 km in degrees longitude

bar_x = x1 - bar_len_deg - 0.3  # offset from right edge
bar_y = y0 + 0.15

ax.plot([bar_x, bar_x + bar_len_deg], [bar_y, bar_y],
        color='black', linewidth=1.5, solid_capstyle='butt', zorder=10)
# End ticks
for bx in [bar_x, bar_x + bar_len_deg]:
    ax.plot([bx, bx], [bar_y - 0.04, bar_y + 0.04],
            color='black', linewidth=1.0, zorder=10)
ax.text(bar_x + bar_len_deg / 2, bar_y - 0.12, '100 km',
        ha='center', va='top', fontsize=5.5, color='black', zorder=10)

# ------------------------------------------------------------------
# North arrow (top-right, in axes fraction so it always shows)
# ------------------------------------------------------------------
ax.annotate('N',
            xy=(0.95, 0.95), xycoords='axes fraction',
            xytext=(0.95, 0.80), textcoords='axes fraction',
            ha='center', va='bottom', fontsize=9, fontweight='bold',
            arrowprops=dict(arrowstyle='->', lw=2.0, color='black'),
            zorder=10)

# ------------------------------------------------------------------
# Inset: Europe locator map (top-left, small)
# ------------------------------------------------------------------
# Build simplified European country outlines from the admin8 Hungary outline
# + a simple rectangle approach for the locator
# Instead: use naturalearth shapefile downloaded locally or draw simplified borders

# Try to load naturalearth from a URL-based GeoJSON
import urllib.request, json as _json
_ne_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
try:
    # Use a lightweight approach: just the Hungary dissolved outline on a simple European box
    # Draw a small inset with European country borders from naturalearth
    _ne_path = Path(r"C:\Bor-szőlő\analysis\curated") / "ne_europe.geojson"
    if not _ne_path.exists():
        # Download 110m cultural vectors (small file)
        _url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
        import zipfile, tempfile
        _tmp = tempfile.mktemp(suffix='.zip')
        urllib.request.urlretrieve(_url, _tmp)
        world = gpd.read_file(f"zip://{_tmp}")
    else:
        world = gpd.read_file(_ne_path)

    europe = world[
        (world.geometry.centroid.x > -15) & (world.geometry.centroid.x < 40) &
        (world.geometry.centroid.y > 34) & (world.geometry.centroid.y < 72) &
        (world['NAME'] != 'Russia')
    ].copy()

    # Small inset in top-left white area
    inset_ax = fig.add_axes([-0.05, 0.68, 0.22, 0.35])
    inset_ax.set_facecolor('white')

    europe.plot(ax=inset_ax, facecolor='#e8e8e8', edgecolor='#bbbbbb', linewidth=0.2)

    hungary_eu = europe[europe['NAME'] == 'Hungary']
    if len(hungary_eu) > 0:
        hungary_eu.plot(ax=inset_ax, facecolor='#dc2626', edgecolor='black', linewidth=0.5)

    inset_ax.set_xlim(-12, 35)
    inset_ax.set_ylim(35, 72)
    inset_ax.set_axis_off()

    for spine in inset_ax.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('#999999')
        spine.set_linewidth(0.5)

except Exception as e:
    print(f"WARNING: Could not create Europe inset: {e}")

ax.set_axis_off()
fig.tight_layout(pad=0.3)

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------
fig.savefig(OUT_PDF, dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)

print(f"Saved: {OUT_PDF}")
print(f"Saved: {OUT_PNG}")
