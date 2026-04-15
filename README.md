# Hungarian Wine Climate Atlas

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19466301.svg)](https://doi.org/10.5281/zenodo.19466301)
[![Districts](https://img.shields.io/badge/wine%20districts-22-burgundy)](analysis/curated/wine_districts.geojson)
[![Varieties](https://img.shields.io/badge/grape%20varieties-58-darkgreen)](analysis/config/grape_envelopes.csv)
[![Languages](https://img.shields.io/badge/languages-HU%20%7C%20EN-yellow)](site/src/messages)
[![Climate scenarios](https://img.shields.io/badge/scenarios-RCP4.5%20%7C%20RCP8.5%20%7C%20SSP2--4.5%20%7C%20SSP5--8.5-blue)](analysis/curated/normals)
[![Static pages](https://img.shields.io/badge/static%20pages-1091-brightgreen)](DEPLOYMENT.md)

> A district-level climate-change susceptibility atlas for the **22 Hungarian
> wine districts** (borvidék) — combining FORESEE regional climate
> projections, the World Bank CCKP CMIP6 ensemble, HungaroMet station
> observations, and a curated knowledge base of 58 grape varieties.

## What Is This?

The **Hungarian Wine Climate Atlas** is a bilingual (Hungarian + English)
information site that visualises how climate change is reshaping each of
Hungary's 22 wine districts — from the warming autumns of Tokaj to the
existential heat squeeze in Csongrád. It is built for **two audiences on the
same pages**:

- **Wine investors** who want defensible numbers — climate trajectories,
  variety suitability scores, threat exposure, source citations, and
  downloadable curated data.
- **The wine-curious public** who want a clear story per region — what's
  grown there, how the climate is changing, and what threatens the wines
  they love.

The site joins three peer-reviewed climate datasets to a curated grape
variety knowledge base and surfaces the result as a publishable
**Next.js + MapLibre + deck.gl static site** with 1,091 prerendered pages
across both locales.

## Features

- **22 wine-district profiles** with extreme-weather outlook, climate
  dashboard, variety suitability bars, climate-adapted replacement
  candidates, threat panel, full research dossier, and one-page PDF download.
- **Variety × district climate-suitability scoring** for 58 grape varieties
  across 4 future periods × 2 RCP/SSP scenarios — 462 (district × variety)
  combinations × 8 horizons × honest validation against real-world plantings.
- **Side-by-side district comparison** at `/compare/[a]/[b]` for any of the
  462 directed pairs.
- **Threat-ranking views** for heat, drought, frost, and the active 2025
  Flavescence dorée outbreak (NÉBIH detected in 21 of 22 wine districts).
- **HungaroMet station observations** as a credibility anchor on each
  district page (2020–2024 actual measurements vs FORESEE projections).
- **Visitor-friendly methods explainers** with analogies and a collapsed
  formulas drawer for the technically curious.
- **Two long-form synthesis briefs** (scientific synthesis, decision-support
  brief) translated to Hungarian.
- **22 downloadable A4 PDFs** generated at build time, one per district.
- **44-file curated data bundle** with manifest.json + SHA-256 checksums.
- Bilingual interface — Hungarian and English sit at `/hu/...` and `/en/...`
  respectively, with native Hungarian translations of all UI strings,
  description prose (130+ short paragraphs), the methods drawer, and the
  full long-form research dossiers (~123,000 words) and synthesis briefs
  (~17,000 words).

## Quick Start

```bash
git clone https://github.com/Nagyhoho1234/Bor-szolo
cd Bor-szolo

# Build the site
cd site
npm install
npm run build         # produces site/out/

# Or run the dev server
npm run dev           # http://localhost:3000
```

That's enough to get a working local site — `analysis/curated/` is committed,
so you don't need to re-run the Python pipeline.

To re-run the pipeline from scratch (for example after dropping in new
climate data):

```bash
cd analysis
python src/s00_build_districts.py
python src/s01_extract_daily_districts.py    # needs FORESEE NetCDFs
python src/s02_compute_indices.py
python src/s03_normals_and_anomalies.py
python src/s04_variety_match.py
python src/s04b_split_suitability_by_district.py
python src/s05_threats_curate.py
python src/s06_cckp_fetch.py                  # downloads from World Bank S3
python src/s06b_cckp_extras.py
python src/s07_publish_curated.py
python src/s08_odpmethu_fetch.py              # downloads from odp.met.hu
python src/s10_generate_district_pdfs.py
cd ../site && node scripts/sync_curated.mjs   # mirror to site/public/data
```

## Pages Overview

| Section | Routes | What's there |
|---|---|---|
| **Landing** | `/` `/en` `/hu` | Hero, 4 headline tiles, lazy-loaded national choropleth, 22-district picker grid |
| **Districts index** | `/{locale}/districts` | Sortable card grid with tagline + flagship wines + climate threat per district |
| **District detail** | `/{locale}/districts/{slug}` | Hero + extreme outlook + HungaroMet station panel + 2×3 IndexCard climate dashboard (click to expand) + variety suitability bars + climate-adapted replacements + threat cards + full research dossier with numbered references + PDF download |
| **Compare** | `/{locale}/compare` | 22-district sortable ranking table + picker form for side-by-side |
| **Compare pair** | `/{locale}/compare/{a}/{b}` | Side-by-side climate + variety comparison for any 2 districts |
| **Varieties** | `/{locale}/varieties` `/{locale}/varieties/{slug}` | Index of 38 grape varieties + per-variety district map |
| **Threats overview** | `/{locale}/threats` | Cards linking to the 4 threat sub-pages |
| **Threat sub-pages** | `/{locale}/threats/{flavescence-doree,heat,drought,frost}` | Per-threat narrative + horizontal-bar district ranking with toggleable FORESEE + CCKP series |
| **Methods** | `/{locale}/methods` (+ `/data-sources`, `/indices`, `/uncertainty`) | Visitor-friendly explainers — why → what → how, with analogies and collapsed formulas |
| **Synthesis** | `/{locale}/synthesis` (+ `/scientific`, `/policy-brief`) | Two long-form briefs (~7K + ~10K words each) |
| **About / Downloads** | `/{locale}/about` `/{locale}/downloads` | Site overview + bulk data download manifest |

## Data Coverage

| Dataset | Variables | Period | Resolution | License |
|---|---|---|---|---|
| **FORESEE v1.1** ([Dobor et al. 2015](https://doi.org/10.1002/gdj3.22)) | Daily T<sub>max</sub>, T<sub>min</sub>, precipitation, VPD, radiation | 1971–2100 | ~10 km, regional climate model (CNRM-ALADIN53), RCP4.5 + RCP8.5, bias-corrected | Open access |
| **World Bank CCKP CMIP6 0.25°** | tas, tasmax, tasmin, pr, hd35, txx, r20mm, cdd, cwd, rx1day, rx5day, fd, gsl, tnn (14 variables) | 1995–2099 | 0.25°, multi-model ensemble, SSP2-4.5 + SSP5-8.5 | CC BY 4.0 |
| **HungaroMet odp.met.hu** | Daily station observations (T<sub>mean</sub>, precip) | 2020–2024 | 21 stations near district centroids | CC BY-SA |
| **OpenStreetMap admin level 8** | 3,174 Hungarian settlement polygons | current | EOV (EPSG:23700) → reprojected | ODbL |
| **Variety knowledge base** | 58 varieties × Huglin/Winkler bands + frost/heat tolerance | curated | Tonietto & Carbonneau 2004, OIV, HWMA | MIT (this repo) |
| **Lakatos & Nagy 2025** ([Frontiers in Plant Science](https://doi.org/10.3389/fpls.2025.1481431)) | Hungarian wine-region temperature indices benchmark | 1971–2100 | 22 borvidék | CC BY 4.0 |

The 22 wine districts cover **25,254 km²** and **618 of Hungary's 3,174
settlements**, dissolved from the manually-labelled OSM admin8 layer.

## Architecture

```
Bor-szolo/
├── analysis/                       # Python pipeline + curated outputs
│   ├── config/                     # variety envelopes, district metadata
│   ├── src/                        # s00 → s10 pipeline scripts
│   ├── geo/                        # 22-district shapefile / GeoPackage
│   └── curated/                    # publishable bundle
│       ├── wine_districts.geojson  # 22 polygons + properties
│       ├── descriptions/           # 22 district descriptions, EN + HU
│       ├── indices/                # annual viticulture indices per district
│       ├── normals/                # 30-year climate normals × 6 periods
│       ├── variety_match/          # district × variety suitability
│       │   └── by_district/        # split per-district JSONs (perf)
│       ├── variety_replacements/   # top climate-adapted candidates
│       ├── cckp/                   # CCKP CMIP6 ensemble extracts
│       ├── odpmethu/               # HungaroMet station observations
│       ├── threats/                # FD timeline, trunk diseases, EU pesticides
│       ├── manifest.json           # full bundle metadata + checksums
│       └── SHA256SUMS.txt
├── paper_analysis/                 # Manuscript reproducibility bundle
│   ├── code/                       # s00–s15 pipeline + figure scripts
│   ├── config/                     # 81-variety envelopes
│   ├── figures/                    # PNG + PDF main and appendix figures
│   ├── tables/                     # manuscript tables as CSV
│   └── data/                       # indices, suitability, 14-member ensemble (CSV)
├── research/
│   ├── districts/                  # 22 EN + 22 HU long-form dossiers
│   ├── synthesis/                  # 2 EN + 2 HU long-form briefs
│   └── sources/                    # source catalog (raw/ md/ excluded)
├── site/                           # Next.js 16 site
│   ├── src/
│   │   ├── app/[locale]/...        # bilingual routes (en + hu)
│   │   ├── components/             # charts, modal, picker, panels
│   │   ├── lib/                    # data loaders, district meta
│   │   └── messages/{en,hu}.json   # i18n strings
│   ├── public/
│   │   ├── data/                   # mirror of analysis/curated/
│   │   └── pdfs/                   # 22 per-district A4 PDFs
│   └── scripts/sync_curated.mjs
├── LICENSE                         # MIT
├── README.md                       # this file
├── CITATION.cff                    # GitHub citation widget
├── .zenodo.json                    # Zenodo archival metadata
├── DEPLOYMENT.md                   # deployment instructions
├── CLAUDE.md                       # development guide for Claude Code
└── .gitignore
```

## Research Paper Analysis Bundle

The folder [`paper_analysis/`](paper_analysis/) contains the complete
analysis workflow, numerical results, and figures underlying the
manuscript *"Variety-level climate suitability for the 22 Hungarian wine
districts under a 14-member EURO-CORDEX ensemble (1971–2100)"*
(Fehér, submitted to *Frontiers in Plant Science*, Crop and Product
Physiology). It is kept separate from the site pipeline so that
reviewers and replicators can find the paper artefacts without
traversing the web-application code.

```
paper_analysis/
├── code/          s00–s15 pipeline scripts + figure scripts
├── config/        grape_envelopes.csv (81 cultivars: 38 Central European + 13 Mediterranean + 6 PIWI + 24 Hungarian endemics & crosses)
├── figures/       all main-text and appendix figures (PNG + PDF)
├── tables/        manuscript tables as CSV
└── data/
    ├── indices/          annual Winkler GDD, Huglin, BEDD, AGST, PET per district (RCP4.5, RCP8.5)
    ├── suitability/      district × variety × horizon × scenario (CSV), including the cos²-centred V1 variant
    └── ensemble/         14-member EURO-CORDEX aggregate + per-member outputs (CSV)
```

The paper pool of 81 varieties is a superset of the 57-variety site
envelope; the extra 24 low-confidence rows are flagged in
`config/grape_envelopes.csv`.

## Tech Stack

| Layer | Technology |
|---|---|
| **Pipeline** | Python 3.12 · pandas · geopandas · xarray · regionmask · pyarrow · scipy · pymannkendall · reportlab |
| **Site framework** | Next.js 16 (Turbopack) · TypeScript 5 · Tailwind CSS 4 + typography plugin |
| **i18n** | next-intl with locale-routed `[locale]` segments |
| **Mapping** | MapLibre GL JS + deck.gl 9 + @luma.gl/webgl adapter (lazy-loaded) |
| **Charts** | Recharts (line + bar + sparkline) · TanStack Table (sortable ranking) |
| **Markdown** | react-markdown + remark-gfm + rehype-raw + custom processor |
| **Data formats** | Apache Parquet (analysis), JSON + GeoJSON (site), CSV (manifests) |
| **Static export** | Next.js `output: 'export'` — no server, no database |

## Climate Indices

The pipeline computes nine viticulture indices from FORESEE daily fields,
plus ten extreme-weather indices from the CCKP ensemble:

| FORESEE-derived | CCKP-derived (ETCCDI) |
|---|---|
| Winkler GDD (base 10°C, Apr–Oct) | hd35 — heat days >35°C |
| Huglin Index (Apr–Sep, latitude-corrected) | txx — annual max tasmax |
| Late spring frost days (Mar–May) | tnn — annual min tasmin |
| Last spring frost DOY | fd — frost days (tmin <0°C) |
| Hot days >35°C (Jun–Aug) | gsl — growing season length |
| Extreme heat days >38°C | rx1day — max 1-day precipitation |
| Growing-season precipitation | rx5day — max 5-day precipitation |
| Hargreaves PET drought balance | cdd — consecutive dry days |
| Cool Night Index (mean September tmin) | cwd — consecutive wet days |
|  | r20mm — heavy precipitation days |

See `site/src/app/[locale]/methods/indices/page.tsx` and the corresponding
visitor-facing explainer page for the formulas, interpretation, and
literature references.

## Deployment

The site is a static Next.js export. Cloudflare Pages, Vercel, Netlify and
GitHub Pages all work out of the box. See [`DEPLOYMENT.md`](DEPLOYMENT.md)
for the build configuration for each provider.

Before going live, change `https://example.com` to your real production
domain in three places:

1. `site/src/app/layout.tsx` — `metadataBase`
2. `site/src/app/sitemap.ts` — `SITE_URL`
3. `site/src/app/robots.ts` — sitemap reference

## Citation

If you use this atlas, the curated dataset, or any of its outputs, please
cite it as:

```bibtex
@misc{feher2026hungarianwineclimateatlas,
  author    = {Fehér, Zsolt Zoltán},
  title     = {Hungarian Wine Climate Atlas — district-level climate
               susceptibility, variety suitability and threats for the
               22 Hungarian wine districts (1971–2100)},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.19466301},
  url       = {https://doi.org/10.5281/zenodo.19466301},
  note      = {22 wine districts, 58 grape varieties, RCP4.5/8.5 +
               SSP2-4.5/5-8.5, bilingual Hungarian + English}
}
```

A machine-readable version is in [`CITATION.cff`](CITATION.cff). The Zenodo
record archives v1.0.0 and is citable via
[**doi:10.5281/zenodo.19466301**](https://doi.org/10.5281/zenodo.19466301).

When citing, please **also** acknowledge the upstream sources:

- Dobor, L. et al. (2015). *Bridging the gap between climate models and
  impact studies: the FORESEE database.* Geoscience Data Journal,
  doi:[10.1002/gdj3.22](https://doi.org/10.1002/gdj3.22).
- Lakatos, L. & Nagy, R. (2025). *Assessment of historical and future
  changes in temperature indices for winegrape suitability in Hungarian
  wine regions (1971–2100).* Frontiers in Plant Science,
  doi:[10.3389/fpls.2025.1481431](https://doi.org/10.3389/fpls.2025.1481431).
- Tonietto, J. & Carbonneau, A. (2004). *A multicriteria climatic
  classification system for grape-growing regions worldwide.* Agricultural
  and Forest Meteorology,
  doi:[10.1016/j.agrformet.2003.06.001](https://doi.org/10.1016/j.agrformet.2003.06.001).
- World Bank Group. *Climate Change Knowledge Portal — CMIP6 0.25° dataset.*
  <https://climateknowledgeportal.worldbank.org/>.
- HungaroMet (OMSZ). *Open Data Portal.* <https://odp.met.hu/>, CC BY-SA.

## License

This repository is released under the [MIT License](LICENSE).

The curated derived data in `analysis/curated/` is also released under MIT.
The upstream input datasets retain their own licenses (see Data Coverage
table above) and are **not redistributed** in this repository.

## Author

**Fehér Zsolt Zoltán** — University of Debrecen.

Other open-source projects:
- [DatasetCadaster](https://github.com/Nagyhoho1234/DatasetCadaster) — a
  comprehensive catalog of geospatial and environmental datasets.
