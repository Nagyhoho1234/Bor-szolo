#!/usr/bin/env python3
"""Figure 2 Appendix: 22-district Winkler GDD trends, one combined A4 page,
grouped by borrégió, max 3 panels per row."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
})

BLUE = '#2563eb'
RED  = '#dc2626'
GREY = '#374151'

BASE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated')
df45 = pd.read_parquet(os.path.join(BASE, 'indices', 'indices_rcp45_annual.parquet'))
df85 = pd.read_parquet(os.path.join(BASE, 'indices', 'indices_rcp85_annual.parquet'))

WINKLER_BOUNDS = [1389, 1667, 1944, 2222]
WINKLER_LABELS = {1389: 'I/II', 1667: 'II/III', 1944: 'III/IV', 2222: 'IV/V'}
Y_MIN, Y_MAX = 1100, 2500

def get_winkler_class(gdd):
    if gdd < 1389: return 'I'
    elif gdd < 1667: return 'II'
    elif gdd < 1944: return 'III'
    elif gdd < 2222: return 'IV'
    else: return 'V'

# English display names for districts (data column → display)
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

GROUPS = [
    ('North Transdanubia', ['Soproni', 'Pannonhalmi', 'Neszmélyi', 'Móri', 'Etyek-Budai']),
    ('Balaton', ['Nagy-Somlói', 'Zalai', 'Balatonfelvidéki', 'Badacsonyi', 'Balatonfüred-Csopaki', 'Balatonboglári']),
    ('Pannon', ['Tolnai', 'Szekszárdi', 'Pécsi', 'Villányi']),
    ('Duna', ['Hajós-Bajai', 'Csongrádi', 'Kunsági']),
    ('Tokaj', ['Tokaji']),
    ('Northern Hungary', ['Mátrai', 'Egri', 'Bükki']),
]

MAX_COLS = 3

def rolling(series, years, window=11):
    s = pd.Series(series.values, index=years.values)
    return s.rolling(window, center=True, min_periods=6).mean()

outdir = os.path.dirname(__file__)
missing = []

# Build row plan: split groups into rows of max MAX_COLS
# Each row_entry = (group_title_or_None, [districts])
# group_title only on the first row of that group
rows = []
for group_title, districts in GROUPS:
    for i in range(0, len(districts), MAX_COLS):
        chunk = districts[i:i + MAX_COLS]
        title = group_title if i == 0 else None
        rows.append((title, chunk))

n_rows = len(rows)  # 9 rows

# Find the LAST row that has all 3 columns — x-axis dates only shown there
last_full_row = max(i for i, (_, dists) in enumerate(rows) if len(dists) == MAX_COLS)

# A4 portrait dimensions
fig = plt.figure(figsize=(210/25.4, 297/25.4))
gs = gridspec.GridSpec(n_rows, MAX_COLS, figure=fig,
                       hspace=0.35, wspace=0.20,
                       left=0.08, right=0.95, top=0.94, bottom=0.03)

fig.suptitle('Winkler GDD trajectories — 22 Hungarian wine districts\n'
             'Grey = observed · Blue = RCP4.5 · Red = RCP8.5 · 11-yr rolling mean',
             fontsize=9, fontweight='bold')

for row_idx, (group_title, districts) in enumerate(rows):
    n_dist = len(districts)

    for col_idx in range(MAX_COLS):
        ax = fig.add_subplot(gs[row_idx, col_idx])

        if col_idx >= n_dist:
            ax.set_visible(False)
            continue

        district = districts[col_idx]

        d45 = df45[df45['borvidek'] == district].sort_values('year')
        d85 = df85[df85['borvidek'] == district].sort_values('year')

        if len(d45) == 0 or len(d85) == 0:
            missing.append(district)
            ax.text(0.5, 0.5, f'{district}\nNo data', transform=ax.transAxes,
                    ha='center', va='center', fontsize=6, color='red')
            continue

        obs = d45[d45['year'] <= 2021]
        proj45 = d45[d45['year'] >= 2022]
        proj85 = d85[d85['year'] >= 2022]

        obs_roll = rolling(obs['winkler_gdd'], obs['year'])
        p45_roll = rolling(proj45['winkler_gdd'], proj45['year'])
        p85_roll = rolling(proj85['winkler_gdd'], proj85['year'])

        baseline_mask = (d85['year'] >= 1991) & (d85['year'] <= 2020)
        future_mask = (d85['year'] >= 2081) & (d85['year'] <= 2100)
        baseline_gdd = d85[baseline_mask]['winkler_gdd'].mean()
        future_gdd = d85[future_mask]['winkler_gdd'].mean()
        transition = f'{get_winkler_class(baseline_gdd)} \u2192 {get_winkler_class(future_gdd)}'

        ax.plot(obs_roll.index, obs_roll.values, color=GREY, linewidth=0.8)
        ax.plot(p45_roll.index, p45_roll.values, color=BLUE, linewidth=0.8)
        ax.plot(p85_roll.index, p85_roll.values, color=RED, linewidth=0.8)

        for wb in WINKLER_BOUNDS:
            if wb <= Y_MAX:
                ax.axhline(wb, color='#4b5563', linestyle='--', linewidth=0.5, alpha=0.7)
                # Winkler class label on EVERY panel (right edge)
                ax.text(2103, wb, WINKLER_LABELS[wb], fontsize=4,
                        va='center', ha='left', color='#374151', fontweight='bold',
                        clip_on=False)

        ax.axvline(2022, color='#9ca3af', linestyle=':', linewidth=0.35, alpha=0.5)

        ax.set_ylim(Y_MIN, Y_MAX)
        ax.set_yticks([1250, 1500, 1750, 2000, 2250, 2500])
        ax.set_xlim(1971, 2100)
        display = DISTRICT_DISPLAY.get(district, district)
        ax.set_title(f'{display}  ({transition})', fontsize=5.5, fontweight='bold', pad=2)
        ax.tick_params(labelsize=4.5)

        # Only show x-axis labels on the last full row (3 columns)
        if row_idx != last_full_row:
            ax.set_xticklabels([])

        if col_idx > 0:
            ax.set_yticklabels([])

    # Group label on the left for the first row of each group
    if group_title is not None:
        row_top = gs[row_idx, 0].get_position(fig).y1
        # Find last row of this group
        last_row = row_idx
        for r2 in range(row_idx + 1, n_rows):
            if rows[r2][0] is not None:
                break
            last_row = r2
        row_bot = gs[last_row, 0].get_position(fig).y0
        row_center = (row_top + row_bot) / 2
        fig.text(0.01, row_center, group_title, fontsize=6, fontweight='bold',
                 rotation=90, va='center', ha='left', color='#374151')

fig.savefig(os.path.join(outdir, 'fig2_appendix_combined.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig2_appendix_combined.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

for ext in ('.pdf', '.png'):
    fpath = os.path.join(outdir, f'fig2_appendix_combined{ext}')
    sz = os.path.getsize(fpath)
    print(f'  fig2_appendix_combined{ext}: {sz/1024:.0f} KB')

if missing:
    print(f'WARNING: Missing data for: {missing}')
else:
    print(f'All 22 districts on one A4 page ({n_rows} rows × {MAX_COLS} cols max).')
print('Appendix generation complete.')
