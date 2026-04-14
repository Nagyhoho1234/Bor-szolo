# Bor-szőlő — Hungarian Wine Climate Atlas

**Published:** [github.com/Nagyhoho1234/Bor-szolo](https://github.com/Nagyhoho1234/Bor-szolo)
**DOI:** [10.5281/zenodo.19466301](https://doi.org/10.5281/zenodo.19466301)
**Version:** v1.0.0 (released 2026-04-08)
**Author:** Fehér Zsolt Zoltán · MIT License

## What this project is

A bilingual (HU/EN) static website that visualises climate-change susceptibility for the **22 Hungarian wine districts** (borvidék). It joins three peer-reviewed climate datasets to a curated knowledge base of **58 grape varieties** and surfaces the result as a publishable, citation-ready atlas with **1,091 prerendered pages**.

**Three layers:**
1. **Python pipeline** (`analysis/src/s00 → s10`) — area-weighted polygon means from FORESEE NetCDF, 9 viticulture indices, 30-year normals, variety suitability matcher, CCKP CMIP6 ensemble validation, HungaroMet station fetch, threats curation, per-district PDF generation, manifest + checksums.
2. **Curated bundle** (`analysis/curated/`) — the publishable dataset: 22 district polygons, annual indices, normals, variety suitability, variety replacements, CCKP extracts, HungaroMet observations, threats CSVs, descriptions (bilingual), manifest.json, SHA256SUMS.txt. Synced into `site/public/data/` by `site/scripts/sync_curated.mjs`.
3. **Site** (`site/`) — Next.js 16 + MapLibre + deck.gl + Recharts + TanStack Table + next-intl. Static export (`output: 'export'`), no server.

**Research corpus** (`research/`) — 22 long-form district dossiers (~123K words) + 2 synthesis briefs (~17K words), all fully translated to Hungarian. 880 unique source URLs scanned (640 successfully fetched, indexed in `research/sources/`; raw HTML excluded from git).

## Key facts about the user

- Hungarian scientist, not a programmer — focus on outcomes and results, not code quality or implementation details. Don't show or explain code unless asked.
- Uses fast/parallel workflows: 32-thread AMD 9950X, 96 GB RAM
- Wants **parallel background agents** over sequential execution wherever independent work allows (up to 10+ in parallel, explicitly authorised)
- WebSearch / WebFetch work in subagents on this project (verified across 22 parallel research agents in April 2026)

## Hungarian EOV coordinates (do not trust headers, check value ranges)
- Northing: 0 – 400,000
- Easting: 400,000 – 1,000,000

## Climate-pipeline period bins

20-year future bins for both RCP scenarios. **Do not reintroduce 2041–2070 or 2071–2100 anywhere.**

| Bin | RCP4.5 | RCP8.5 | User-facing label |
|---|---|---|---|
| 1971–2000 | observed | observed | historical baseline |
| 1991–2020 | observed | observed | reference baseline |
| 2021–2040 | ✓ | ✓ | near term |
| 2041–2060 | ✓ | ✓ | ≈ +20 y |
| 2061–2080 | ✓ | ✓ | ≈ +40 y |
| 2081–2100 | ✓ | ✓ | ≈ +60–80 y |

## Variety envelope state (`analysis/config/grape_envelopes.csv`)

**58 varieties total** as of v1.0.0:
- 38 Hungarian + Central European originals
- 14 Mediterranean additions (2026-04-07): Tempranillo, Touriga Nacional, Garnacha, Mourvèdre, Carignan, Aglianico, Nero d'Avola, Sangiovese, Vermentino, Assyrtiko, Fiano, Verdejo, Albariño
- 6 PIWI additions (Wave 11A, 2026-04-07): Solaris, Bronner, Johanniter, Muscaris, Souvignier Gris, Cabernet Cortis

**Calibration issues status** (from Wave 11A):
1. ~~Mourvèdre too generous (21/22)~~ → **FIXED**: tightened to Huglin 2700+, now 10/22 districts >0.5
2. ~~Nero d'Avola too generous (14/22)~~ → **FIXED**: tightened to Huglin 2800+, now 4/22
3. ~~Furmint ejected from Tokaji~~ → **FIXED**: huglin_max raised, Tokaji Furmint 0.73→0.64 at 2081-2100 RCP8.5 (was 0.32)
4. ~~Csongrád/Szekszárd zero picks~~ → **FIXED**: both now 8 varieties >0.5
5. **~24 varieties named in §12 sections still have no envelope row** — mostly Hungarian endemics and additional PIWIs. Not blocking but worth filling eventually.

**Soft-Winkler scoring:** `s04_variety_match.py` uses `gap/4.0` so a variety reaches zero suitability only at 4 Winkler classes off.

## Anchor reference paper

**Lakatos & Nagy 2025**, Frontiers in Plant Science, DOI **10.3389/fpls.2025.1481431**. The single most-cited paper across the corpus. **Citation drift was fixed** in Wave 11C (~118 corrections across 22 research markdowns). The paper has **no supplementary materials** (verified definitively in Wave 14F via the Frontiers Nuxt SSR payload `hasSupplementalData = false`). Per-district numerical data exists only as figure raster plots — not machine-extractable. See `research/synthesis/lakatos_nagy_si_hunt.md` for the full search report.

## Headline numbers

| Finding | District | Value |
|---|---|---|
| Largest GDD increase | Kunság | +581.65 °C-d (1971–2100) |
| Largest BEDD increase | Bükk | +258.49 °C-d (started coolest) |
| Highest AGST warming | Csongrád | >+2.5 °C, RCP8.5 |
| Slowest-warming | Sopron | GDD +66.16 °C-d |
| Smallest end-century warming | Pannonhalma | +2.3 °C, RCP8.5 |
| Counterintuitive gradient | — | Northern HU warms faster than southern |
| CCKP Tokaji warming | Tokaji | 11.05 → 16.24 °C (+5.19 °C, SSP5-8.5 2080-2099) |
| Existential variety risks | — | Móri Ezerjó (>14k → 1.6k ha), Pécsi Cirfandli (13.9 ha), Nagy-Somló Juhfark (~80–150 ha globally) |
| Flavescence dorée | 21/22 districts | NÉBIH confirmed, 3.8 BHUF emergency aid, vector established 2006, disease detected 2013, catastrophe 2025 |
| Replacement validation | — | Model vs real-world plantings: 5% strict / 20% permissive convergence |

## Inverted-U trajectory under RCP8.5

| Period | Mean suitability | Interpretation |
|---|---|---|
| 1991–2020 | 0.75 | reference |
| 2021–2040 | 0.83 | warming helps — cool districts lift into class III |
| 2041–2060 | 0.83 | plateau |
| 2061–2080 | 0.59 | crossover — Mediterranean ceiling exceeded |
| 2081–2100 | **0.33** | collapse — even with Mediterranean + PIWI varieties added |

## Site architecture (1,091 static pages)

**Routes × 2 locales (EN + HU):**
- Landing, districts index, 22 district detail pages (with PDF download + variety replacements + HungaroMet station panel + research dossier)
- 462 directed comparison pairs (`/compare/[a]/[b]`), ranking table + picker
- 38 variety detail pages, variety index
- 4 threat sub-pages (Flavescence dorée, heat, drought, frost) + overview
- 4 methods pages (About this atlas, About the data, What the numbers mean, How sure are we?)
- 3 synthesis pages (hub, scientific, policy-brief)
- About, Downloads

**Key components:**
- `DistrictMap` — MapLibre + deck.gl choropleth with **official Hungarian wine-region colour scheme** (regional families: purples for Észak-Dunántúl, greens for Balaton, pinks/reds for Pannon, yellows/cream for Duna, oranges for Észak-Magyarországi, brown for Tokaj). Lazy-loaded via `DistrictMapClient` wrapper. Locale-aware click navigation.
- `IndexCard` + `ChartModal` — static-by-default 2×3 dashboard, click-to-expand interactive trajectory
- `VarietySuitabilityBars` — two sub-charts (principals + climate-hedge candidates), 4 future periods, both RCPs side-by-side
- `VarietyReplacements` — top 4 climate-adapted replacement candidates per district per horizon
- `HungaroMetPanel` — actual station observations credibility anchor (21/22 districts)
- `ThreatRanking` — horizontal-bar ranking with toggleable FORESEE + CCKP series
- `DownloadPdfButton` — links to `/pdfs/<slug>.pdf` (22 per-district A4 PDFs generated by `s10`)

## Curated data bundle state

44+ files in `analysis/curated/`. Everything here is the publishable output; `analysis/interim/` is NOT published. Sync to site via `node site/scripts/sync_curated.mjs`.

**Key outputs:**
- `wine_districts.geojson` — 22 polygons, simplified for web (<500 KB)
- `indices/indices_{rcp45,rcp85}_annual.parquet` — 9 viticulture indices per district per year
- `normals/normals_<period>_<scenario>_per_district.parquet` × 10 — 30-year normals + anomalies + risk flags
- `variety_match/by_district/<slug>.json` — per-district suitability (split from monolith in Wave 12, ~284 KB each)
- `variety_match/suitability_long.parquet` — full cross-district (for comparison pages only)
- `variety_replacements/<slug>.json` — top climate-adapted candidates per horizon
- `cckp/` — 14 CCKP CMIP6 variables (original 7 + 7 ETCCDI extras from Wave 8)
- `odpmethu/` — 21 HungaroMet stations, 2020-2024, mean distance 9.6 km from centroids
- `threats/` — 4 CSVs (FD timeline, trunk diseases, pest/regulatory, EU pesticides); all verified except 2 partial rows (sulphur + kaolin approval dates)
- `descriptions/` — 22 district descriptions with `*_hu` parallel fields for all prose

## Bilingual coverage

| Content | EN | HU |
|---|---|---|
| UI strings (267+ keys) | ✅ | ✅ |
| Description JSON prose (22 districts × ~10 fields) | ✅ | ✅ |
| 22 research dossiers (~123K words) | ✅ | ✅ |
| 2 synthesis briefs (~17K words) | ✅ | ✅ |
| Methods pages (4) | ✅ | ✅ |
| Methods formula drawer | ✅ | ✅ |
| Research dossier source titles | EN only | EN (source titles not translatable) |

**Loader pattern:** `loadResearch(slug, locale)` prefers `<slug>.hu.md` when locale is `hu`, falls back to `<slug>.md`. Same for synthesis briefs. Description JSONs use `localizeDescription(desc, locale)` helper in `site/src/lib/data.ts` to pick `*_hu` fields.

## Threats data state

| CSV | Rows | Verified | Partial | Unverified |
|---|---|---|---|---|
| flavescence_doree_timeline | 10 | 10 | 0 | 0 |
| trunk_diseases | 9 | 7 | 2 | 0 |
| pest_disease_regulatory | 26 | 24 | 2 | 0 |
| eu_pesticides_actives | 28 | 26 | 2 (sulphur, kaolin) | 0 |

FD first HU detection: August 2013, Zala county. Vector (*Scaphoideus titanus*) established 2006 — seven years before disease arrived.

## User-facing content tone & citation discipline

Hard-won rules from multiple correction cycles. Apply any time you or a subagent writes visitor-visible content.

**Tone**
- Visitor-friendly explainer journalism. Plain English. Why → what → how. "you / we" voice. Analogies welcome.
- **Methods pages** are visitor explainers, NOT journal methods. Forbidden: pipeline-script names, DOI inline citations, Hargreaves-vs-Penman jargon, "what we did NOT model" lists, code/file references. Formulas live only in a collapsed `<details>` drawer.
- **Don't render `hail_caveat` field on district pages** — too academic for visitor-facing site.

**Sources & citations**
- **No JSON / parquet / manifest links in user-facing source boxes.** Those belong on `/downloads` only.
- **Use `https://doi.org/<DOI>` for academic citations**, never publisher-direct URLs. Mark `(paywalled)` where applicable.
- **No "Please cite..." lines** — the citation block IS the cite.
- **Real source titles only.** WebFetch every URL before committing. Run `site/scripts/fix_sources.py` for the canonical URL → title map.
- **Frontiers 2025 = Lakatos & Nagy 2025** — never Kovács, never Zhao.
- **Research dossier markdown** processed via `processResearchMarkdown` (`site/src/lib/research-markdown.ts`) which strips `[OBSERVED]`/`[PROJECTED]`/etc tags and converts `> Sources (§N):` blockquotes to numbered references.

**Charts UX — static-by-default, click-to-interact**
Every inline chart uses `staticView={true}`. Wrap in `<ChartModal>`, pass the interactive copy as `expanded`. One chart style on district pages: the IndexCard 2×3 dashboard. Do not add a second top-level chart grid — that regression was fixed once already.

**District map colours**
Uses the official Hungarian wine-region colour scheme from `Borvidekterkep.png` (regional colour families, not a hash-based qualitative palette). Defined as a named lookup in `DISTRICT_COLORS` in `DistrictMap.tsx`. The `/regions/` pages and `BORREGIO_LIST` navigation layer were deleted from the site — do not reintroduce.

## Infrastructure gaps still open

1. ~~Lakatos & Nagy 2025 supplementary tables~~ → **RESOLVED: no supplementary materials exist.** Per-district numerical data is in figure rasters only. Alternatives: email authors, recompute on same FORESEE input + 1986-2005 window, or WebPlotDigitizer.
2. **EURO-CORDEX 12 km does not resolve Lake Balaton** — the lake mesoclimate that defines four borvidék is missing from public projections.
3. **No multi-decadal phenology series** for any district except Tokaj.
4. **No district-level pest/disease monitoring** for *Scaphoideus titanus*, *Drosophila suzukii*, *Halyomorpha halys*, esca, Flavescence dorée.
5. **Móri-szél has no published multi-decadal climatology.**
6. **~24 varieties named in §12 sections still have no envelope row** — mostly Hungarian endemics and additional PIWIs beyond the 6 added in Wave 11A.
7. **Pannonhalmi HungaroMet station (Pér airport)** has all-null tmean/precip — should find a better station.

## Workflow conventions

- **Plan first, then run unattended.** Only stop on errors.
- **Parallelise everything independent.** Up to 10+ parallel background agents.
- **Curated → site sync:** `cd site && node scripts/sync_curated.mjs` after any `analysis/curated/` change.
- **PDF refresh:** `python analysis/src/s10_generate_district_pdfs.py` after normals or variety_match changes.
- **Save points:** git commit before major batch operations.
- **Codex cross-review:** `codex exec --model gpt-5.4 "prompt"` for second opinions.
- **Don't show/explain code unless asked.**
- **Rate-limit handling:** expect `You've hit your limit` bounces with 10+ parallel agents. Stagger or relaunch survivors after the reset window.

## Subprojects

- `site/CLAUDE.md` → imports `site/AGENTS.md` which has the full Next.js stack gotchas (luma.gl webgl adapter, tailwind typography plugin, Sapling hydration, static export limits, chart UX contract, variety chart data contract, build verification patterns, mobile responsive approach, and the full user-facing content tone rules).

## Known repository quirks

- **Path contains `ő`:** `C:\Bor-szőlő\` → use forward slashes, quote in shell. netCDF4's C library crashes on this path; use `scipy` or `h5netcdf` engine + bytes-in-memory bypass for .nc files under this path.
- **ArcGIS Pro Python cp1252 crash:** `s03` and `s04` crash on the last `print()` because cp1252 can't encode `ő`. Data files write successfully before the crash. Use `PYTHONIOENCODING=utf-8` to silence.
- **Two shapefile lineages:** `wine_districts.shp` (22 borvidék) and `admin8_with_district.shp` (3,174 admin units with `borvidek` column). Use the correct one.
- **Orphan `main` branch:** the git history was squashed to a single v1.0.0 commit for a clean GitHub push. The original development history was on `master` (now deleted). The `.git` folder is 8.7 MB.
