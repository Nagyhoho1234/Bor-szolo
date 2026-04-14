#!/usr/bin/env python3
"""Figure 1: The inverted-U suitability trajectory."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Style ---
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

# --- Data ---
DATA = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'analysis', 'curated',
                     'variety_match', 'suitability_long.parquet')
df = pd.read_parquet(DATA)

periods = ['1971-2000', '1991-2020', '2021-2040', '2041-2060', '2061-2080', '2081-2100']
x = np.arange(len(periods))

# Compute national mean suitability per period x scenario
agg = df.groupby(['period', 'scenario'])['suitability'].agg(['mean', 'std']).reset_index()
# Also compute p10 and p90 across districts
dist_agg = df.groupby(['period', 'scenario', 'borvidek'])['suitability'].mean().reset_index()
ribbon = dist_agg.groupby(['period', 'scenario'])['suitability'].agg(
    p10=lambda s: s.quantile(0.10),
    p90=lambda s: s.quantile(0.90)
).reset_index()

# Build observed + scenario lines
# Observed periods are shared; then scenarios diverge
obs = agg[agg['scenario'] == 'observed'].set_index('period')
r45 = agg[agg['scenario'] == 'rcp45'].set_index('period')
r85 = agg[agg['scenario'] == 'rcp85'].set_index('period')

obs_rib = ribbon[ribbon['scenario'] == 'observed'].set_index('period')
r45_rib = ribbon[ribbon['scenario'] == 'rcp45'].set_index('period')
r85_rib = ribbon[ribbon['scenario'] == 'rcp85'].set_index('period')

def build_line(obs_df, scen_df, periods):
    vals = []
    for p in periods:
        if p in obs_df.index:
            vals.append(obs_df.loc[p, 'mean'])
        elif p in scen_df.index:
            vals.append(scen_df.loc[p, 'mean'])
        else:
            vals.append(np.nan)
    return np.array(vals)

def build_ribbon(obs_df, scen_df, periods, stat):
    vals = []
    for p in periods:
        if p in obs_df.index:
            vals.append(obs_df.loc[p, stat])
        elif p in scen_df.index:
            vals.append(scen_df.loc[p, stat])
        else:
            vals.append(np.nan)
    return np.array(vals)

y45 = build_line(obs, r45, periods)
y85 = build_line(obs, r85, periods)

p10_45 = build_ribbon(obs_rib, r45_rib, periods, 'p10')
p90_45 = build_ribbon(obs_rib, r45_rib, periods, 'p90')
p10_85 = build_ribbon(obs_rib, r85_rib, periods, 'p10')
p90_85 = build_ribbon(obs_rib, r85_rib, periods, 'p90')

# --- Plot ---
fig, ax = plt.subplots(figsize=(180/25.4, 90/25.4))  # 180mm wide

ax.fill_between(x, p10_85, p90_85, color=RED, alpha=0.10, label='RCP8.5 p10–p90')
ax.fill_between(x, p10_45, p90_45, color=BLUE, alpha=0.10, label='RCP4.5 p10–p90')

ax.plot(x, y45, color=BLUE, linewidth=1.5, marker='o', markersize=5, label='RCP4.5', zorder=5)
ax.plot(x, y85, color=RED, linewidth=1.5, marker='s', markersize=5, label='RCP8.5', zorder=5)

# Crossover annotation
cross_idx = periods.index('2041-2060')
ax.axvline(cross_idx, color=GREY, linestyle='--', linewidth=1.0, alpha=0.6)
ax.text(cross_idx + 0.08, 0.92, 'crossover', fontsize=8, color=GREY, rotation=90, va='top')

ax.set_xticks(x)
ax.set_xticklabels(periods, rotation=30, ha='right')
ax.set_ylabel('Mean variety suitability')
ax.set_ylim(0, 1.0)
ax.set_xlim(-0.3, len(periods) - 0.7)
ax.legend(fontsize=8, loc='lower left', framealpha=0.9)

plt.tight_layout()
outdir = os.path.dirname(__file__)
fig.savefig(os.path.join(outdir, 'fig1_inverted_u.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig1_inverted_u.png'), dpi=300, bbox_inches='tight')
plt.close()
print('Figure 1 saved.')
