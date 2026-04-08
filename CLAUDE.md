# Bor-szőlő — Hungarian wine-district climate susceptibility project

## What this project is

A bilingual (HU/EN) website that visualises climate-change susceptibility for the **22 Hungarian wine districts** (borvidék), built on:
- **Frontend:** Next.js + MapLibre + deck.gl in `site/`
- **Spatial data:** `wine_districts.shp` (22 borvidék) and `admin8_with_district.shp` (district-attributed admin units) in the project root, EOV-projected
- **Climate analysis pipeline:** Python in `analysis/src/` (`s01_extract_daily_districts.py` → `s07_publish_curated.py`), with computed outputs in `analysis/curated/` (indices, normals, variety_match, variety_match_combined, variety_replacements, cckp). The curated bundle is published into `site/public/data/` by **`site/scripts/sync_curated.mjs`** — run that whenever you regenerate any curated file.
- **Pre-computed figures:** `analysis/reports/figures/` (`suitability_heatmap_2071-2100_rcp85.png`, `winkler_trends_all_districts.png`)
- **Research corpus:** 22 deep-research markdown files + scientific synthesis + decision-support brief + variety-replacement analysis + validation report in `research/` (see `research/RESEARCH_LOG.md` for the original task log)

## Key facts about the user

- Hungarian scientist, not a programmer — focus on outcomes and results, not code quality
- Uses fast/parallel workflows: 32-thread AMD 9950X, 96 GB RAM
- Wants **parallel background agents** over sequential execution wherever independent work allows
- Builds the website in parallel with research work — don't block on website progress

## Hungarian EOV coordinates (do not trust headers, check value ranges)
- Northing: 0 – 400,000
- Easting: 400,000 – 1,000,000

## Climate-pipeline period bins (current, as of 2026-04-07 evening)

The pipeline now uses **20-year future bins for both RCP scenarios** (changed from the original 30-year bins). All scripts and site components have been migrated. **Do not reintroduce 2041–2070 or 2071–2100 anywhere.**

| Bin | RCP4.5 | RCP8.5 | User-facing label |
|---|---|---|---|
| 1971–2000 | observed | observed | historical baseline |
| 1991–2020 | observed | observed | reference baseline |
| 2021–2040 | ✓ | ✓ | near term |
| 2041–2060 | ✓ | ✓ | ≈ +20 y |
| 2061–2080 | ✓ | ✓ | ≈ +40 y |
| 2081–2100 | ✓ | ✓ | ≈ +60–80 y |

## Variety envelope state (`analysis/config/grape_envelopes.csv`)

**52 varieties total** (38 Hungarian + Central European original + 14 Mediterranean added 2026-04-07):
- **Reds added:** Tempranillo, Touriga Nacional, Garnacha (Grenache), Mourvèdre, Carignan, Aglianico, Nero d'Avola, Sangiovese
- **Whites added:** Vermentino, Assyrtiko, Fiano, Verdejo, Albariño

**Known calibration issues** flagged by the validation audit (`research/synthesis/replacement_validation.md`):
1. **Mourvèdre and Nero d'Avola envelopes too generous** — Mourvèdre is recommended in 21/22 districts but appears in 1/22 §12 sections; Nero d'Avola in 14/22 vs 0/22. Tighten upper Huglin/Winkler bounds.
2. **Furmint water-stress parameterisation likely wrong** — Tarcal Research Institute literature says Furmint is drought-tolerant due to efficient stomatal control, but the model ejects it from Tokaji at 2081–2100 RCP8.5. Widen Furmint's upper Huglin envelope.
3. **Csongrád & Szekszárd produce zero replacement picks** at 2081–2100 RCP8.5 because the Winkler envelope collapses for every variety. Their §12 sections explicitly name Touriga Nacional / Tempranillo / Grenache as actual trial plantings, so this is calibration, not real unfarmability.
4. **~30 varieties named in §12 sections have no envelope row at all** — most consequentially the PIWI group (Souvignier Gris, Muscaris, Solaris, Bronner) and Hungarian endemics (Cirfandli, Juhfark, Kéknyelű — though some are present, just under-represented).

**Soft-Winkler scoring:** `s04_variety_match.py` softened from `gap/3.0` to `gap/4.0` so a variety reaches zero suitability only at 4 Winkler classes off (was 3). Reflects that varieties *can* grow beyond their classical class with quality changes.

## Research corpus state (as of 2026-04-07)

`research/districts/*.md` contains 22 district synthesis files (~123,000 words, ~1,200 source citations, 880 unique URLs after dedup). Each follows a 15-section template with `[OBSERVED]` vs `[PROJECTED]` tags and `[HU-AGGREGATE]` / `[GAP]` fall-back markers. **Tokaji is the pilot template** — match its structure when generating new content.

`research/synthesis/` contains:
- `scientific_synthesis.md` — manuscript-grade review (~7,080 words)
- `decision_support_brief.md` — grower/policy-facing (~9,700 words)
- `variety_replacements.{md,csv,py}` — per-district top-4 replacement candidates across 8 horizon combinations (4 future bins × 2 RCPs); 696 recommendations
- `export_combined_suitability.py` — generates `analysis/curated/variety_match_combined/{slug}.json` for the chart's two-sub-chart UI (baseline + RCP4.5 + RCP8.5 nested per future period)
- `export_replacements_to_site.py` — generates `analysis/curated/variety_replacements/{slug}.json` for per-district replacement deep-dives
- `replacement_validation.md` — 4,311-word audit cross-referencing the model's recommendations against the qualitative §12 evidence in the 22 district MDs. **Headline: only 5% strict / 20% permissive convergence.** Read this before publishing the chart as authoritative.

`research/sources/` — 880 unique URLs scanned, **640 successfully downloaded and converted to local Markdown** (73% success), 239 failed, 1 auth-gated. Indexed in `research/sources/index.json` and `research/sources/INDEX.md`. Re-runnable via `python research/sources/fetch_sources.py` (idempotent).

## Anchor reference paper

The single most-cited paper across the corpus is the **Frontiers in Plant Science 2025** Hungarian wine regions thermal-indices study, DOI **10.3389/fpls.2025.1481431**. **Citation drift warning:** the paper is referenced as both *"Lakatos & Nagy 2025"* and *"Kovács et al. 2025"* across different district files — same DOI, ambiguous author ordering. Standardise before publication.

## Headline numbers worth memorising

| Finding | District | Value |
|---|---|---|
| Largest GDD increase | Kunság | +581.65 °C-d (1971–2100) |
| Largest BEDD increase | Bükk | +258.49 °C-d (because it started coolest) |
| Highest AGST warming | Csongrád | >+2.5 °C, RCP8.5 |
| Slowest-warming | Sopron | GDD +66.16 °C-d |
| Smallest end-century warming | Pannonhalma | +2.3 °C, RCP8.5 |
| Counterintuitive gradient | — | Northern HU warms faster than southern (inverts traditional ordering) |
| Climate "winners" (provisional) | Sopron, Zala, Pannonhalma, Móri | Klímapolitikai Intézet 2023/2024 |
| Existential variety risks | Móri Ezerjó (>14k → 1.6k ha), Pécsi Cirfandli (13.9 ha), Nagy-Somló Juhfark (~80–150 ha *globally*) | — |

## Inverted-U Hungary-wide trajectory under RCP8.5

| Period | Mean suitability | Interpretation |
|---|---|---|
| 1991–2020 | 0.74 | reference |
| 2021–2040 | 0.85 | warming *helps* — cool districts lift into class III |
| 2041–2060 | 0.85 | plateau |
| 2061–2080 | 0.63 | crossover — Mediterranean ceiling exceeded |
| 2081–2100 | **0.33** | collapse — even with Mediterranean varieties added |

Hungarian viticulture as a whole *gains* from moderate warming through ~2050, then deteriorates rapidly. This is the headline trajectory worth featuring prominently on the website timeline.

## Variety chart UI contract (`site/src/components/VarietySuitabilityBars.tsx`)

The chart now reads `suitability_long.json` (passed in as `rows`) and renders **two sub-charts under one shared period dropdown**:

1. **Upper:** the district's current principal varieties only (`in_principal_varieties === true`), sorted by baseline suitability descending. Three bars per variety: gray = baseline 1991–2020, amber = RCP 4.5, rose = RCP 8.5.
2. **Lower:** climate-adapted candidates that are NOT currently grown in the district (`in_principal_varieties === false`), ranked by RCP 8.5 → RCP 4.5 → baseline. **Top 5 in collapsed (`staticView`) mode; all candidates with `max(rcp45, rcp85) > 0.5` in expanded modal mode.**

The parent district page (`site/src/app/[locale]/districts/[borvidek]/page.tsx`) must pass **all** suitability rows for the district (not pre-filtered to principals) and preserve the `in_principal_varieties` field in the row mapping. Pre-filtering breaks the lower chart silently.

Default period is `2081-2100`. The dropdown lists 4 future periods only — there is no scenario selector because both RCPs are always shown side-by-side.

## Hard infrastructure gaps blocking deeper work

1. **FORESEE 4.0 / Lakatos & Nagy 2025 supplementary tables** — district-level AGST/GDD/HI/BEDD numbers are not in the open-access body; flagged as missing in 19 of 22 district files. This is the highest-leverage single fix for the whole project.
2. **EURO-CORDEX 12 km does not resolve Lake Balaton** — the lake mesoclimate that defines four borvidék is missing from public projections.
3. **No multi-decadal phenology series** for any district except Tokaj.
4. **No district-level pest/disease monitoring** for *Scaphoideus titanus*, *Drosophila suzukii*, *Halyomorpha halys*, esca, Flavescence dorée.
5. **Móri-szél has no published multi-decadal climatology** despite anchoring the Móri district's resilience narrative.
6. **Variety envelope calibration** — see "Known calibration issues" above.

## User-facing content tone & citation discipline

Hard-won rules from multiple correction cycles. Apply these any time you (or a subagent) write content that the visitor will see on the site.

**Tone**
- Visitor-friendly explainer journalism, like a museum interpretive panel or a *Wine Folly* feature article. Plain English. Why → what → how. Use "you / we" voice. Use analogies (a Huglin Index is "a sun-clock for the vine"; a Winkler GDD is "an oven that only counts warmth above 10 °C").
- **Methods pages** (`site/src/app/[locale]/methods/*`) are visitor explainers, NOT a journal methods section. **Forbidden in body text:** pipeline-script names (s00–s09), DOI-style inline citations, Hargreaves-vs-Penman trade-off discussion, ETCCDI verbatim definitions, "what we did NOT model" lists, file/code/manifest references. Formulas live only in a collapsed `<details>` "Want the formulas?" drawer at the bottom of `methods/indices`. Page H1s can be friendly ("About the data" / "What the numbers mean" / "How sure are we?") while URLs stay stable.
- Aim for ~250–500 words per Methods page body, with one optional collapsed depth drawer for the technically curious.
- **Don't render the `hail_caveat` field on district pages.** The field stays in `descriptions/*.json` for the Methods/Uncertainty page reference, but the long disclaimer reads like a methods footnote on a public site.

**Sources, citations, and external links**
- **No JSON / parquet / manifest.json links in user-facing source boxes.** Internal data files belong on `/downloads` only.
- **Use `https://doi.org/<DOI>` for academic citations**, never publisher-direct URLs. Springer / Wiley / Elsevier paywall and reorganise URLs; the DOI redirector is the only stable scholarly link. Mark `(paywalled)` after the link if the reader can't get full text.
- **No "Please cite..." lines** — the citation block IS the cite.
- **Real source titles only.** WebFetch every URL before committing the title text. The bootstrap pass produced ~110 fake titles (mostly "Kovács et al." attributions for the Frontiers paper) that took a full audit to fix. Run `site/scripts/fix_sources.py` if you want the canonical URL → title map.
- **Anchor paper attribution:** the Frontiers in Plant Science 2025 Hungarian wine regions paper (DOI **10.3389/fpls.2025.1481431**) is **Lakatos & Nagy 2025** — never Kovács et al., never Zhao et al.
- **Research dossier markdown** at the bottom of each district page must be processed via `processResearchMarkdown` (`site/src/lib/research-markdown.ts`) before rendering. The processor strips the `> Reading guide` blockquote, all `[OBSERVED]`/`[PROJECTED]`/`[HU-AGGREGATE]`/`[N-HU ANALOGUE]` etc. inline meta-tags, and converts inline `> Sources (§N): [title](url)` blockquotes into superscript numeric markers `[1] [2]` linking to a single References section appended at the bottom of the dossier.

**Charts UX contract — static-by-default, click-to-interact**
The user does not want interactive controls (tooltips, hover, toggle chips, period selectors) visible inline on a page. Every inline chart must use `staticView={true}` or its equivalent (no Tooltip, no Legend, `pointer-events-none`). Wrap each chart in `<ChartModal>` (`site/src/components/ChartModal.tsx`) and pass the **interactive copy** as the `expanded` prop. There must be **only one** style of climate line chart on the district detail page: the bottom **IndexCard 2×3 dashboard**, each card wrapped in `<ChartModal>` whose `expanded` slot is the interactive `ClimateTrendChart`. Do not add a second top-level "climate trajectory" grid above it — this is a regression we already fixed once.

**District map**
Uses a 22-colour qualitative palette hashed by district name. The borrégió layer was deleted from the site entirely (`/regions/` pages, `BORREGIO_COLORS`, `BORREGIO_LIST`). Do not reintroduce it; the borrégió grouping has been deprecated in Hungarian wine law since ~2020 and was an organisational layer the user explicitly rejected.

## Workflow conventions to follow

- **For multi-step tasks:** present a plan first, wait for approval, then run the entire workflow unattended without pausing between steps. Only stop on errors.
- **Parallelise everything independent.** Launch background agents in single-message batches (up to 10+ in parallel — the user has explicitly authorised this).
- **Subagent web access:** WebSearch and WebFetch *do* work in subagents on this project (the earlier memory note saying otherwise was stale — corrected during the 22-district research run on 2026-04-07).
- **Rate-limit handling:** when running 10+ parallel agents, expect occasional `You've hit your limit · resets <time>` bounces. Stagger or relaunch survivors after the reset window. Save points (git commits) before each parallel wave make recovery painless.
- **Curated → site sync:** after any change to `analysis/curated/`, run `node site/scripts/sync_curated.mjs` from the `site/` directory to publish to `site/public/data/`. The sync script wipes the destination first, so anything you write directly into `site/public/data/` outside the sync flow gets deleted on the next run.
- **Save points:** create git commits before any major batch operation per the global rules in `~/.claude/CLAUDE.md`.
- **Codex cross-review:** for second opinions on manuscripts or analysis, run `codex exec --model gpt-5.4 "prompt"` via Bash.
- **Don't show or explain code unless asked** — the user is a scientist, not a programmer.

## Subprojects with their own CLAUDE.md

- `site/CLAUDE.md` → Next.js subproject. **WARNING in `site/AGENTS.md`:** the Next.js version in use has breaking changes from training-data conventions. Read `site/node_modules/next/dist/docs/` before writing site code.

## Known repository quirks

- Project root path contains the non-ASCII character `ő`: `C:\Bor-szőlő\` → use forward slashes and quote in shell commands. Some bash output mojibakes the directory name; this is cosmetic only.
- `s03_normals_and_anomalies.py` and `s04_variety_match.py` both crash on the **last** stdout `print()` statement when run through ArcGIS Pro's bundled Python on Windows because cp1252 cannot encode `ő`. The data files all write successfully before the crash — it is harmless, but use `python -X utf8 ...` or set `PYTHONIOENCODING=utf-8` to silence it.
- Many top-level files are work-in-progress geospatial intermediates (`_affine_params.npy`, `_legrow_*.png`, `wine_map_georef*.tif`, etc.) — do not touch unless asked.
- Two parallel shapefile lineages: `wine_districts.shp` (22 borvidék polygons) and `admin8_with_district.shp` (3,174 admin units with `borvidek`/`borregio` columns). Use the correct one for the task.
