# bor-szolo curated bundle (v1.0.0)

This bundle is the analysis-ready output of the Hungarian wine district
climate pipeline. It provides per-district viticulture indices, 30-year
climate normals, variety-suitability scores, a multi-model validation
layer from the World Bank CCKP, and a curated (draft) threats dossier,
all keyed to Hungary's 22 official wine districts (borvidek) grouped into
6 wine regions (borregio): Balaton, Duna, Eger, Pannon, Sopron, and
Tokaj.

## Folder layout

- `wine_districts.geojson` - 22 districts dissolved from the
  manually-labelled admin8 settlements layer (EPSG:4326, simplified).
- `indices/` - Annual viticulture indices per district for each RCP
  scenario (FORESEE v1.1, CNRM-ALADIN53).
- `normals/` - 30-year normals with trends, anomalies vs 1991-2020, and
  risk flags for each (period, scenario) combo.
- `variety_match/` - Per-(district, variety, period, scenario)
  suitability scores with limiting factors, plus a long-format union
  and a headline winners/losers CSV.
- `cckp/` - World Bank CCKP CMIP6 multi-model ensemble per-district
  stats for 7 variables across 3 scenarios. Used as an independent
  validation layer, not as the primary projection.
- `threats/` - Curated dossier on Flavescence doree, grapevine trunk
  diseases, pest/disease regulatory status, and EU pesticide actives.
  **DRAFT - needs web verification before publication.**

## Data sources and roles

| Source | Role |
|---|---|
| FORESEE v1.1 (Dobor et al.) | Primary daily-resolution projection (CNRM-ALADIN53 under RCP4.5 and RCP8.5). Drives `indices/`, `normals/`, `variety_match/`. |
| World Bank CCKP CMIP6 0.25 deg | Independent multi-model validation layer (`cckp/`). |
| Frontiers in Plant Science 2025 (10.3389/fpls.2025.1481431) | Benchmark reference for Hungarian wine region temperature indices. |
| Curated threats dossier | Flavescence doree, trunk diseases, EU regulation (DRAFT). |

## Viticulture indices (9)

| Index | One-line definition |
|---|---|
| `winkler_gdd` | Growing-season degree days base 10 C, Apr-Oct (Amerine & Winkler regions). |
| `huglin_index` | Heliothermal index with daylength correction, Apr-Sep. |
| `gst` | Mean growing-season temperature, Apr-Oct (Jones wine-style bands). |
| `bedd` | Biologically Effective Degree Days base 10 C, capped at 19 C. |
| `cool_night_index` | Mean minimum temperature in September (colour & aroma proxy). |
| `frost_days` | Count of days with Tmin < -2 C between bud-break and Oct. |
| `heat_days` | Count of days with Tmax >= 35 C during the growing season. |
| `growing_season_precip` | Cumulative precipitation Apr-Oct. |
| `dry_days_js` | Count of July-August days with P < 1 mm (drought proxy). |

## Periods and scenarios

- **Periods:** 1971-2000 (historical), 1991-2020 (observed baseline),
  2041-2070 (mid-century), 2071-2100 (end-century).
- **Scenarios:** `observed` (for the two historical periods), `rcp45`,
  `rcp85` (for the two future periods).

## Citation

If you use this bundle, please cite ALL of:

1. FORESEE v1.1 (Dobor et al.) for the underlying daily climate data.
2. World Bank Climate Change Knowledge Portal CMIP6 0.25 deg for the
   validation layer.
3. Frontiers in Plant Science 2025,
   <https://doi.org/10.3389/fpls.2025.1481431>, for the Hungarian wine
   region temperature-index benchmark that the indices in this bundle
   are calibrated against.

## License

Derived data only. Raw underlying FORESEE and CCKP fields are **not**
redistributed in this bundle; only per-district aggregates, normals,
and derived indices are published here. Users needing the raw fields
must fetch them directly from the original providers under their
respective licenses.

## Known limitations

- **Single-model RCP projection.** The primary future projection uses
  only the CNRM-ALADIN53 run of FORESEE v1.1; the CCKP layer is the
  multi-model ensemble cross-check.
- **Hargreaves PET.** Future-period evapotranspiration uses Hargreaves
  (Tmin/Tmax/Ra) rather than Penman-Monteith, because radiation and
  wind fields were unavailable at daily resolution for the projections.
- **Bootstrapped variety envelopes.** The 38-variety climate envelopes
  are seeded from training-knowledge literature and need expert review;
  `confidence` ratings reflect the bootstrap provenance.
- **Draft threats CSVs.** Everything under `threats/` is a
  domain-knowledge stub; subagent web tools were denied during initial
  curation, so sources are **unverified**. Do not publish without
  live-source verification.
- **RCP8.5 2071-2100 suitability collapse.** Under end-century RCP8.5,
  suitability scores for many districts collapse toward zero. This
  should be read as "currently-grown varieties become unsuited" rather
  than "no wine production possible" - drought- and heat-tolerant
  southern varieties outside the current 38-variety list are not
  evaluated here.

## Headline numbers

- Total files: 44
- Total size: 1.127 MB
- Normals rows (district x index x period x scenario): 1320
- Suitability rows (district x variety x period x scenario): 5016
- CCKP rows (district x variable x period x scenario x stat): 2310
- **Biggest Winkler-class shift (RCP8.5, 2071-2100):** Villányi moves from class Ib to IV (3 steps, +682 GDD).
