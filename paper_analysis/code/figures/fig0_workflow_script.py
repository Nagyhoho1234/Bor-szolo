#!/usr/bin/env python3
"""Figure 2: Methodology workflow diagram — branching top-down layout, readable text."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

outdir = os.path.dirname(__file__)

fig, ax = plt.subplots(figsize=(180/25.4, 210/25.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12.5)
ax.set_aspect('equal')
ax.set_axis_off()
fig.patch.set_facecolor('white')


def draw_box(ax, cx, cy, w, h, header, lines, color='#f0f4f8', border='#374151',
             header_size=9, line_size=7.5):
    rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                           boxstyle="round,pad=0.15",
                           facecolor=color, edgecolor=border, linewidth=1.2, zorder=2)
    ax.add_patch(rect)
    y_top = cy + h/2 - 0.35
    ax.text(cx, y_top, header, ha='center', va='top',
            fontsize=header_size, fontweight='bold', color='#1f2937', zorder=3)
    for i, line in enumerate(lines):
        ax.text(cx, y_top - 0.40 - i * 0.34, line, ha='center', va='top',
                fontsize=line_size, color='#4b5563', zorder=3)


def draw_arrow(ax, x0, y0, x1, y1, color='#6b7280'):
    arrow = FancyArrowPatch((x0, y0), (x1, y1),
                             arrowstyle='->', mutation_scale=15,
                             lw=1.8, color=color, zorder=1,
                             connectionstyle='arc3,rad=0')
    ax.add_patch(arrow)


# ── ROW 0: Climate Data (top center) ──
draw_box(ax, 5, 11.2, 5.0, 2.0,
         'CLIMATE DATA',
         ['FORESEE-HUN v1.0 / v1.1',
          'Daily Tmax, Tmin, Precip',
          '0.1° grid · 1971–2100 · RCP4.5 / RCP8.5'],
         color='#dbeafe', border='#2563eb')

ax.text(5, 9.85, '22 districts · area-weighted polygon means',
        ha='center', va='top', fontsize=7, fontstyle='italic', color='#6b7280')

# ── ROW 1: Indices (left) + Variety Envelopes (right) ──
draw_box(ax, 2.5, 7.5, 4.2, 2.2,
         '9 VITICULTURAL INDICES',
         ['Winkler GDD · Huglin Index',
          'Frost days · Hot days >35°C',
          'Precipitation · ET₀ · CNI',
          '6 temporal bins × 2 scenarios'],
         color='#fef3c7', border='#d97706')

draw_box(ax, 7.5, 7.5, 4.2, 2.2,
         '57 VARIETY ENVELOPES',
         ['Huglin range (trapezoidal)',
          'Winkler class (soft penalty)',
          'Frost / heat tolerance',
          '38 HU/CE + 13 Medit. + 6 PIWI'],
         color='#fce7f3', border='#db2777')

# ── ROW 2: Suitability Scoring (center) ──
draw_box(ax, 5, 4.0, 5.5, 2.0,
         'SUITABILITY SCORING',
         ['S = Huglin × Winkler × Frost × Heat',
          '0 (unsuitable) → 1 (optimal)',
          'Per district × variety × period × scenario'],
         color='#d1fae5', border='#059669')

ax.text(5, 2.65, 'Inverted-U trajectory · replacement rankings',
        ha='center', va='top', fontsize=7.5, fontstyle='italic', color='#374151',
        fontweight='bold')

# ── ROW 3: Two validation paths ──
draw_box(ax, 2.5, 1.0, 4.2, 1.6,
         'CCKP CMIP6 CROSS-CHECK',
         ['Independent multi-model ensemble',
          'Temperature + extreme heat'],
         color='#e0e7ff', border='#4f46e5',
         header_size=8.5)

draw_box(ax, 7.5, 1.0, 4.2, 1.6,
         'REAL-WORLD VALIDATION',
         ['22 district research dossiers',
          '5% strict / 20% permissive'],
         color='#e0e7ff', border='#4f46e5',
         header_size=8.5)

# ── ARROWS ──
# Climate Data → Indices (down-left fork)
draw_arrow(ax, 3.5, 10.1, 2.8, 8.7)
# Climate Data → Envelopes (down-right fork)
draw_arrow(ax, 6.5, 10.1, 7.2, 8.7)
# Indices → Suitability (down-right merge)
draw_arrow(ax, 3.3, 6.3, 4.0, 5.1)
# Envelopes → Suitability (down-left merge)
draw_arrow(ax, 6.7, 6.3, 6.0, 5.1)
# Suitability → CCKP (down-left fork)
draw_arrow(ax, 3.8, 2.9, 2.8, 1.9)
# Suitability → Real-world (down-right fork)
draw_arrow(ax, 6.2, 2.9, 7.2, 1.9)

plt.tight_layout(pad=0.3)
fig.savefig(os.path.join(outdir, 'fig0_workflow.pdf'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(outdir, 'fig0_workflow.png'), dpi=300, bbox_inches='tight')
plt.close()

for ext in ('.pdf', '.png'):
    fpath = os.path.join(outdir, f'fig0_workflow{ext}')
    sz = os.path.getsize(fpath)
    print(f'  fig0_workflow{ext}: {sz/1024:.0f} KB')
