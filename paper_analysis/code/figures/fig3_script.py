#!/usr/bin/env python3
"""Figure 3: Variety-by-district suitability heatmaps.

Generates:
  - 10 appendix heatmaps (all 57 varieties, all period-scenario combos) WITH cell annotations
  - 1 main-text heatmap (ALL 57 varieties, 2061-2080 RCP8.5) WITH cell annotations
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

# ── Data ──────────────────────────────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated')
df = pd.read_parquet(os.path.join(BASE, 'variety_match', 'suitability_long.parquet'))
OUTDIR = os.path.dirname(__file__)

# English display names for districts
DISTRICT_DISPLAY = {
    'Soproni': 'Sopron', 'Pannonhalmi': 'Pannonhalma', 'Neszmélyi': 'Neszmély',
    'Móri': 'Mór', 'Etyek-Budai': 'Etyek-Buda',
    'Nagy-Somlói': 'Nagy-Somló', 'Zalai': 'Zala', 'Balatonfelvidéki': 'Balatonfelvidék',
    'Badacsonyi': 'Badacsony', 'Balatonfüred-Csopaki': 'Balatonfüred-Csopak',
    'Balatonboglári': 'Balatonboglár',
    'Tolnai': 'Tolna', 'Szekszárdi': 'Szekszárd', 'Pécsi': 'Pécs', 'Villányi': 'Villány',
    'Hajós-Bajai': 'Hajós-Baja', 'Csongrádi': 'Csongrád', 'Kunsági': 'Kunság',
    'Mátrai': 'Mátra', 'Egri': 'Eger', 'Bükki': 'Bükk',
    'Tokaji': 'Tokaj',
}

# ── District ordering by borrégió (NW coolest → SE warmest) ──────────────
DISTRICT_ORDER = [
    # North Transdanubia
    'Soproni', 'Pannonhalmi', 'Neszmélyi', 'Móri', 'Etyek-Budai',
    # Balaton
    'Nagy-Somlói', 'Zalai', 'Balatonfelvidéki', 'Badacsonyi',
    'Balatonfüred-Csopaki', 'Balatonboglári',
    # Pannon
    'Tolnai', 'Szekszárdi', 'Pécsi', 'Villányi',
    # Duna
    'Hajós-Bajai', 'Csongrádi', 'Kunsági',
    # Northern Hungary
    'Mátrai', 'Egri', 'Bükki',
    # Tokaj
    'Tokaji',
]

# Group boundary positions (cumulative count of districts per group)
GROUP_BOUNDARIES = [5, 11, 15, 18, 21]  # after each group except the last

# 10 appendix combos (fixed: was missing 2041-2060 and had duplicate 2061-2080)
APPENDIX_COMBOS = [
    ('1971-2000', 'observed'),
    ('1991-2020', 'observed'),
    ('2021-2040', 'rcp45'),
    ('2021-2040', 'rcp85'),
    ('2041-2060', 'rcp45'),
    ('2041-2060', 'rcp85'),
    ('2061-2080', 'rcp45'),
    ('2061-2080', 'rcp85'),
    ('2081-2100', 'rcp45'),
    ('2081-2100', 'rcp85'),
]

# Nice scenario labels
SCENARIO_LABELS = {'observed': 'observed', 'rcp45': 'RCP4.5', 'rcp85': 'RCP8.5'}

# Spotlight districts for main-text figure
SPOTLIGHTS = ['Tokaji', 'Villányi', 'Csongrádi', 'Soproni']

# Principal varieties lookup (for bold cell borders in main figure)
_principal_lookup = df[df['in_principal_varieties'] == True][['variety', 'borvidek']].drop_duplicates()
PRINCIPAL_PAIRS = set(zip(_principal_lookup['variety'], _principal_lookup['borvidek']))
# Varieties that are principal in at least ONE district (for bold y-labels)
PRINCIPAL_VARIETIES = set(_principal_lookup['variety'].unique())


def make_pivot(sub, district_order, sort_varieties=True, top_n=None):
    """Pivot subset to variety × district matrix."""
    pivot = sub.pivot_table(index='variety', columns='borvidek',
                            values='suitability', aggfunc='mean')
    # Reorder columns to match district ordering
    cols = [d for d in district_order if d in pivot.columns]
    pivot = pivot[cols]
    # Sort varieties by mean suitability (highest at top)
    variety_means = pivot.mean(axis=1).sort_values(ascending=False)
    if top_n is not None:
        variety_means = variety_means.head(top_n)
    pivot = pivot.loc[variety_means.index[::-1]]  # ascending for imshow (top=highest)
    return pivot


def draw_heatmap(pivot, title, figsize, outpath_base,
                 row_fontsize=7, col_fontsize=8,
                 show_values=False, value_fontsize=4, bold_cols=None,
                 bold_principal_cells=False,
                 group_boundaries=None):
    """Draw and save a suitability heatmap."""
    fig, ax = plt.subplots(figsize=figsize)

    # Stretched custom colormap: more range in 0.6-1.0 to reduce saturation
    colors_list = [
        (0.0, '#a50026'),   # dark red
        (0.15, '#d73027'),  # red
        (0.3, '#fdae61'),   # orange
        (0.45, '#fee08b'),  # yellow
        (0.55, '#d9ef8b'),  # yellow-green
        (0.65, '#a6d96a'),  # light green
        (0.75, '#66bd63'),  # green
        (0.85, '#1a9850'),  # dark green
        (0.95, '#006837'),  # very dark green
        (1.0, '#004529'),   # darkest green
    ]
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'stretched_RdYlGn', [(v, c) for v, c in colors_list], N=256)
    norm = mcolors.Normalize(vmin=0, vmax=1.0)

    im = ax.imshow(pivot.values, cmap=cmap, norm=norm, aspect='auto')

    # Y-axis (variety labels): bold = currently grown somewhere, italic = replacement only
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(list(pivot.index), fontsize=row_fontsize)
    for i, label in enumerate(ax.get_yticklabels()):
        variety_name = pivot.index[i]
        if variety_name in PRINCIPAL_VARIETIES:
            label.set_fontweight('bold')
        else:
            label.set_fontstyle('italic')
            label.set_color('#555555')

    # X-axis (district labels — use English display names)
    ax.set_xticks(range(len(pivot.columns)))
    display_cols = [DISTRICT_DISPLAY.get(c, c) for c in pivot.columns]
    ax.set_xticklabels(display_cols, fontsize=col_fontsize,
                       rotation=45, ha='right')

    # Bold spotlight columns
    if bold_cols:
        tick_labels = ax.get_xticklabels()
        for sp in bold_cols:
            if sp in pivot.columns:
                idx = list(pivot.columns).index(sp)
                tick_labels[idx].set_fontweight('bold')
                tick_labels[idx].set_color('#b91c1c')

    # Group separator lines
    if group_boundaries:
        for gb in group_boundaries:
            ax.axvline(x=gb - 0.5, color='#374151', linewidth=1.0,
                       linestyle='-', zorder=5)

    # Bold cell borders for principal varieties
    n_annotated = 0
    if bold_principal_cells:
        from matplotlib.patches import Rectangle
        for i, variety in enumerate(pivot.index):
            for j, district in enumerate(pivot.columns):
                # Strip any "\n(period)" suffix for lookup
                district_base = district.split('\n')[0] if '\n' in district else district
                if (variety, district_base) in PRINCIPAL_PAIRS:
                    rect = Rectangle((j - 0.5, i - 0.5), 1, 1,
                                     linewidth=1.2, edgecolor='black',
                                     facecolor='none', zorder=6)
                    ax.add_patch(rect)

    # Cell value annotations
    if show_values:
        for i in range(pivot.shape[0]):
            for j in range(pivot.shape[1]):
                val = pivot.values[i, j]
                if not np.isnan(val):
                    tc = 'white' if (val < 0.15 or val > 0.9) else 'black'
                    ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                            fontsize=value_fontsize, color=tc)
                    n_annotated += 1

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('Suitability', fontsize=9)
    cbar.ax.tick_params(labelsize=7)

    ax.set_title(title, fontsize=10, pad=8)

    plt.tight_layout()
    for ext in ('.pdf', '.png'):
        fig.savefig(outpath_base + ext, dpi=300, bbox_inches='tight')
    plt.close()
    # Report file sizes
    for ext in ('.pdf', '.png'):
        fpath = outpath_base + ext
        sz = os.path.getsize(fpath)
        print(f'  {os.path.basename(fpath)}: {sz/1024:.0f} KB')
    if n_annotated > 0:
        print(f'  Annotated cells: {n_annotated}')
    return n_annotated


# ── Generate 10 appendix heatmaps (WITH cell annotations) ──────────────
print('=== APPENDIX HEATMAPS ===')
missing_report = []
total_annotated_appendix = 0
for period, scenario in APPENDIX_COMBOS:
    sub = df[(df['period'] == period) & (df['scenario'] == scenario)]
    if sub.empty:
        print(f'  WARNING: no data for {period} {scenario}')
        continue

    pivot = make_pivot(sub, DISTRICT_ORDER)

    # Check for missing cells
    n_missing = int(pivot.isna().sum().sum())
    if n_missing > 0:
        missing_report.append(f'{period} {scenario}: {n_missing} missing cells')

    scn_label = SCENARIO_LABELS[scenario]
    scn_file = scenario.replace('.', '')
    title = f'Variety suitability \u2014 {period} {scn_label}'
    fname = f'fig3_appendix_{period}_{scn_file}'
    outpath = os.path.join(OUTDIR, fname)

    # A4 portrait: ~210mm wide, ~300mm tall
    figsize = (210/25.4, 300/25.4)

    print(f'{period} {scn_label}:')
    n = draw_heatmap(pivot, title, figsize, outpath,
                     row_fontsize=7, col_fontsize=8,
                     show_values=True, value_fontsize=4,
                     bold_principal_cells=True,
                     group_boundaries=GROUP_BOUNDARIES)
    total_annotated_appendix += n

# ── Generate main-text heatmap (4 spotlights × 2 periods, grouped with gaps) ─
print('\n=== MAIN-TEXT HEATMAP (4 spotlights × 2 periods) ===')
SPOTLIGHT_ORDER = ['Soproni', 'Tokaji', 'Villányi', 'Csongrádi']
MAIN_PERIODS = ['2061-2080', '2081-2100']
PERIOD_SHORT = {'2061-2080': "'61–'80", '2081-2100': "'81–'00"}

# Build pivots per period
pivots_by_period = {}
for period in MAIN_PERIODS:
    sub = df[(df['period'] == period) & (df['scenario'] == 'rcp85')]
    pivots_by_period[period] = make_pivot(sub, SPOTLIGHT_ORDER)

# Filter: keep only varieties that are (a) currently grown in at least one spotlight,
# OR (b) have suitability > 0 in at least one spotlight at 2081-2100
# This removes varieties that are neither planted nor future-viable here.
piv_future = pivots_by_period['2081-2100']
keep_varieties = set()
for variety in piv_future.index:
    # Currently grown in any of the 4 spotlights?
    is_principal = any((variety, d) in PRINCIPAL_PAIRS for d in SPOTLIGHT_ORDER)
    # Has meaningful suitability (>0.10) in at least one spotlight at 2081-2100?
    future_viable = (piv_future.loc[variety] > 0.10).any()
    if is_principal or future_viable:
        keep_varieties.add(variety)

# Apply filter to both period pivots
for period in MAIN_PERIODS:
    piv = pivots_by_period[period]
    pivots_by_period[period] = piv.loc[piv.index.isin(keep_varieties)]

# Sort varieties by mean across both periods (highest at top)
all_vals = pd.concat([pivots_by_period[p] for p in MAIN_PERIODS], axis=1)
variety_order = all_vals.mean(axis=1).sort_values(ascending=True).index  # ascending for imshow (top=highest)
print(f'  Kept {len(variety_order)} varieties (removed {57 - len(variety_order)} with no current planting and no future viability)')

# Custom figure with pcolormesh and gaps between district pairs
GAP = 0.4  # gap width between districts (in column units)
n_districts = len(SPOTLIGHT_ORDER)
n_periods = len(MAIN_PERIODS)
n_varieties = len(variety_order)

# Column positions: each district gets 2 columns (one per period) + gap after
col_positions = []  # (x_center, district, period) for each cell column
district_group_centers = []  # (x_center, district_name) for top header
x = 0
for di, district in enumerate(SPOTLIGHT_ORDER):
    group_start = x
    for pi, period in enumerate(MAIN_PERIODS):
        col_positions.append((x, district, period))
        x += 1
    district_group_centers.append((group_start + 0.5, DISTRICT_DISPLAY.get(district, district)))
    if di < n_districts - 1:
        x += GAP  # gap between districts

total_width = x

fig, ax = plt.subplots(figsize=(180/25.4, 270/25.4))

# Colormap (same as draw_heatmap)
colors_list = [
    (0.0, '#a50026'), (0.15, '#d73027'), (0.3, '#fdae61'),
    (0.45, '#fee08b'), (0.55, '#d9ef8b'), (0.65, '#a6d96a'),
    (0.75, '#66bd63'), (0.85, '#1a9850'), (0.95, '#006837'),
    (1.0, '#004529'),
]
cmap = mcolors.LinearSegmentedColormap.from_list(
    'stretched_RdYlGn', [(v, c) for v, c in colors_list], N=256)
norm = mcolors.Normalize(vmin=0, vmax=1.0)

# Draw cells as rectangles with gaps
from matplotlib.patches import Rectangle
n_annotated = 0
for ci, (cx, district, period) in enumerate(col_positions):
    piv = pivots_by_period[period]
    for vi, variety in enumerate(variety_order):
        val = piv.loc[variety, district] if variety in piv.index and district in piv.columns else np.nan
        y = vi
        if not np.isnan(val):
            color = cmap(norm(val))
            rect = Rectangle((cx - 0.5, y - 0.5), 1, 1,
                              facecolor=color, edgecolor='#e5e7eb', linewidth=0.2, zorder=2)
            ax.add_patch(rect)
            # Cell annotation
            tc = 'white' if (val < 0.15 or val > 0.9) else 'black'
            ax.text(cx, y, f'{val:.2f}', ha='center', va='center',
                    fontsize=4.5, color=tc, zorder=3)
            n_annotated += 1
            # Bold border for principal pairs
            if (variety, district) in PRINCIPAL_PAIRS:
                border = Rectangle((cx - 0.5, y - 0.5), 1, 1,
                                   linewidth=1.2, edgecolor='black',
                                   facecolor='none', zorder=6)
                ax.add_patch(border)

# Set axis limits
ax.set_xlim(-0.6, total_width - 0.4)
ax.set_ylim(-0.6, n_varieties - 0.4)

# Y-axis: variety labels
ax.set_yticks(range(n_varieties))
ax.set_yticklabels(list(variety_order), fontsize=6)
for i, label in enumerate(ax.get_yticklabels()):
    vname = variety_order[i]
    if vname in PRINCIPAL_VARIETIES:
        label.set_fontweight('bold')
    else:
        label.set_fontstyle('italic')
        label.set_color('#555555')

# X-axis bottom: short period labels under each column
x_ticks = [cx for cx, _, _ in col_positions]
x_labels = [PERIOD_SHORT[p] for _, _, p in col_positions]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=6, rotation=0, ha='center')

# X-axis top: district names centered over each pair
ax2 = ax.secondary_xaxis('top')
ax2.set_xticks([xc for xc, _ in district_group_centers])
ax2.set_xticklabels([d for _, d in district_group_centers],
                     fontsize=8, fontweight='bold')
ax2.tick_params(length=0)

# Vertical separator lines between district groups (in the gap)
for di in range(n_districts - 1):
    # Position of the gap: after 2 columns of district di, before next district
    gap_x = col_positions[di * n_periods + n_periods - 1][0] + 0.5 + GAP / 2
    ax.axvline(gap_x, color='#9ca3af', linewidth=0.5, linestyle='-', alpha=0.4, zorder=1)

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.02)
cbar.set_label('Suitability', fontsize=9)
cbar.ax.tick_params(labelsize=7)

# No title or legend text on main-text figures — goes to figure caption instead
ax.invert_yaxis()

plt.tight_layout()
outpath_main = os.path.join(OUTDIR, 'fig3_heatmap_suitability')
for ext in ('.pdf', '.png'):
    fig.savefig(outpath_main + ext, dpi=300, bbox_inches='tight')
plt.close()
for ext in ('.pdf', '.png'):
    fpath = outpath_main + ext
    sz = os.path.getsize(fpath)
    print(f'  {os.path.basename(fpath)}: {sz/1024:.0f} KB')
print(f'  Annotated cells: {n_annotated}')
n_main = n_annotated

# ── Summary report ────────────────────────────────────────────────────────
print('\n=== SUMMARY ===')
print(f'Matrices generated: 10 appendix + 1 main-text = 11 total')
print(f'Files created: {10*2 + 2} (PDF + PNG for each)')
print(f'Total annotated cells (appendix): {total_annotated_appendix}')
print(f'Total annotated cells (main): {n_main}')

if missing_report:
    print('\nMissing data:')
    for m in missing_report:
        print(f'  {m}')
else:
    print('No missing data in any matrix.')

# Top 5 varieties at 2061-2080 RCP8.5
sub_top = df[(df['period'] == '2061-2080') & (df['scenario'] == 'rcp85')]
top5 = sub_top.groupby('variety')['suitability'].mean().sort_values(ascending=False).head(5)
print('\nTop 5 varieties at 2061-2080 RCP8.5 (mean suitability):')
for v, s in top5.items():
    print(f'  {v}: {s:.3f}')
