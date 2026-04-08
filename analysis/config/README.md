# Hungarian wine variety knowledge base — `analysis/config/`

Bootstrap files for the variety × district climate-suitability analysis.
Drafted 2026-04-07. **All numeric values need expert review before being used in
production.** Where the source web pages were unavailable at draft time, content
was reconstructed from Claude's training-data knowledge of Hungarian viticulture
(Wikipedia borvidék pages, Hungarian Wine Marketing Agency variety profiles,
Tonietto & Carbonneau 2004, Jones 2006). This is flagged in the `confidence` and
`notes` columns and should be treated as a starting point, not ground truth.

## Files

### `districts.yml`
The 22 official Hungarian wine districts (borvidék) grouped under their 6
parent regions (borrégió). Each district lists 3–8 principal grape varieties,
1–3 flagship wine-style tags, a one-sentence identity note, and source URLs.
Hungarian diacritics are preserved in `name_hu` and variety names; `name_en` is
an ASCII-friendly display alias.

### `grape_envelopes.csv`
Climate envelope per variety. 38 rows covering the full union of varieties
referenced in `districts.yml` plus the most common international varieties.
Columns:

| column                 | meaning                                                              |
|------------------------|----------------------------------------------------------------------|
| `variety`              | Hungarian primary spelling                                           |
| `variety_en`           | English / international alias                                        |
| `huglin_min`           | lower viable Huglin Index (°C·day, rounded to 50)                    |
| `huglin_opt_low`       | lower bound of optimum Huglin band                                   |
| `huglin_opt_high`      | upper bound of optimum Huglin band                                   |
| `huglin_max`           | upper viable Huglin Index                                            |
| `winkler_class_min`    | lowest tolerated Winkler region (1–5)                                |
| `winkler_class_max`    | highest tolerated Winkler region                                     |
| `frost_tolerance_days` | typical late-spring frost days a healthy crop tolerates              |
| `heat_tolerance_days`  | typical Jun–Aug days with Tmax > 35 °C tolerated                     |
| `min_gs_precip_mm`     | minimum unirrigated growing-season (Apr–Oct) precipitation           |
| `colour`               | red / white                                                          |
| `confidence`           | high / medium / low — honest source-quality assessment               |
| `source`               | semicolon-separated short citations / URLs                           |
| `notes`                | one-line free text, especially where data is sketchy                 |

Huglin numbers are rounded to 50 °C·day; frost and heat-day counts to whole days.

### `indices.yml`
Reference definitions of the climate indices the downstream pipeline will
compute (Winkler, Huglin, spring frost, last-frost DOY, hot days >35 °C,
extreme-heat days >38 °C, growing-season precipitation, dryness index, Cool
Night Index). For each index: English and Hungarian display names, formula,
season window, units, interpretation guide, and source reference.

## Review priority — please look at these first

1. **Low-confidence indigenous varieties** in `grape_envelopes.csv`. The
   following rows are essentially educated guesses cloned from related varieties:
   - **Kabar** (modern Tokaj crossing — no published envelope)
   - **Kövérszőlő** (recently revived; no modern data)
   - **Kéknyelű** (Badacsony specialty; very thin literature)
   - **Juhfark** (Somló specialty; volcanic-soil-specific data only)
   - **Ezerjó** (Móri specialty)
   - **Cirfandli** (Pécsi; relies on Austrian Zierfandler analogues)
   - **Generosa**, **Arany sárfehér**, **Budai zöld** (sparse data)

   If you have access to NÉBIH variety bulletins, the Magyar Szőlő- és
   Borgazdasági Tanszék publications, or your own field measurements, please
   correct these in priority order.

2. **District principal-variety lists**. The lists for the small Duna-region
   districts (**Csongrádi**, **Hajós-Bajai**) and **Bükki** are the least
   confident — these are short, regional and the public sources are thin in
   English. The Tokaji, Egri, Villányi, Soproni, Szekszárdi and Tokaj/Balaton
   district lists should be reasonably accurate.

3. **Huglin upper bands for cool-climate varieties** (Riesling, Pinot noir,
   Tramini, Müller-Thurgau, Grüner Veltliner). Whether you treat the upper band
   as a hard wall or as a soft "quality-collapse" threshold is a methodological
   choice — please confirm before the suitability scoring step.

4. **Winkler region bounds** for late-ripening reds (Cabernet Sauvignon, Syrah,
   Kadarka). The upper bound of "5" is theoretical for Hungary; real
   constraints come from heat-day and dryness indices, not Winkler.

5. **Climate index thresholds in `indices.yml`** — the Winkler region cut-offs
   are the original 1974 imperial-derived numbers; please confirm you want
   those rather than the more recent metric revisions (e.g. Hall & Jones 2010).

## What is NOT in here yet

- District polygons / geometry (lives in `analysis/geo/`)
- Per-district climate observations or projections (lives in `analysis/interim/`)
- The actual suitability scoring rules (will live in `analysis/src/`)
- Soil and elevation modifiers
- Vintage-by-vintage historical yields

## Provenance note

When this draft was generated, both `WebFetch` and `WebSearch` were unavailable
in the agent environment, so the planned online cross-checks against
`hungarianwines.eu`, the Hungarian Wine Society slide deck and Wikipedia were
**not performed**. The `sources` fields list the URLs that *should* be checked
against on review. Please treat the `medium` and `low` confidence rows
accordingly.
