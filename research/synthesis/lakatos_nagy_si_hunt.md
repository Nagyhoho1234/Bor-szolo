# Lakatos & Nagy 2025 Supplementary-Material Hunt

**Paper:** Lakatos L. & Nagy R. (2025). *Assessment of historical and future changes in temperature indices for winegrape suitability in Hungarian wine regions (1971-2100).* Frontiers in Plant Science 16, 1481431. https://doi.org/10.3389/fpls.2025.1481431
**Hunt date:** 2026-04-07
**Hunt status:** **Negative result.** No supplementary materials exist for this paper.

## TL;DR

The paper publishes per-district numerical results **only as figure plots**, never as a table — neither in the article body nor in supplementary files. There are no `Data Sheet`, `Table S`, `.docx`, `.xlsx`, `.csv` or `.pdf` supplementary attachments on either the publisher (Frontiers) or PMC mirror. The Data Availability Statement points only to the FORESEE meteorological input dataset (`https://nimbus.elte.hu/FORESEE/`), not to derived per-district values.

The "highest-leverage single fix" framing in the project CLAUDE.md is therefore unachievable from this paper alone — the per-district AGST/GDD/HI/BEDD numbers we want **do not exist as published structured data**. They would have to be (a) digitised manually from the figures, (b) requested directly from the corresponding author, or (c) recomputed by ourselves from the FORESEE input the authors used.

## URLs tried

| URL | Result |
|---|---|
| `https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1481431/full` | 200 OK. Nuxt-3 SSR payload includes the entire article structure. Field `hasSupplementalData` resolves to `false`. `appendixContent` and `otherBackSections` are empty arrays. |
| `https://doi.org/10.3389/fpls.2025.1481431` | 301 to the URL above. |
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC11842426/` | 200 OK. Full article text mirrored. The "Associated Data" section contains only the Data Availability Statement (FORESEE link) — no `<supplementary-material>` block. |

## What is in the paper

5 in-body tables, none of which are per-district:

1. **Table 1** — Definitions and class limits of AGST, GDD, HI, BEDD.
2. **Table 2** — Mapping of GDD-Winkler regions (I-V) to climate classes.
3. **Table 3** — Frequency-of-occurrence (% of region-years) for each climate class across all 22 regions, for 1986-2005 / 2016-2035 / 2081-2100. **Aggregate, not per-district.**
4. **Table 4** — Probability of falling within optimal temperature interval, **per grape variety** (21 varieties), per RCP and decade. Not per-region.
5. **Table 5** — Decadal suitability values S(T), **per grape variety**. Not per-region.

12 figures, several of which appear to show per-district lines/bars but are published only as raster images (`fpls-16-1481431-g00X.jpg` on PMC).

## What I extracted

**Zero per-district numerical rows.** `research/synthesis/lakatos_nagy_supplementary_tables.csv` was not created — there is nothing to put in it.

The article-body numbers I did capture (Table 3 frequency distributions) are aggregate over all 22 regions and over 20 climate-model members; they are not directly comparable to per-district pipeline normals.

## Cross-check status

`analysis/reports/tables/frontiers2025_crosscheck.csv` was rewritten to contain:

- All **66 rows** (22 districts × 3 indices: GDD-Winkler, Huglin, CNI) of our pipeline's 1971-2000 baseline values from `analysis/curated/normals/normals_1971-2000_per_district.parquet`.
- `paper_value` blank for every row, `status = no_paper_data`.
- Header comments documenting *why* every row is blank (so a future agent doesn't waste another hunt iteration).

**Soft (qualitative) cross-check from paper Table 3 prose:**

- Paper claims that for **1986-2005** the modal AGST class across the 22 wine regions was "warm" (17-19 °C) and the modal GDD-Winkler class was Region II (1389-1667).
- Our 1971-2000 GDD-Winkler values range **1223-1547 °C-day** (median ~1320), placing most districts in Region I (cool) and a few warmer ones in Region II (intermediate).
- This is **slightly cooler** than the paper's modal class — fully consistent with our baseline being a 1971-2000 window vs. their 1986-2005 window (15 years earlier centroid; Hungarian growing-season temperature trend ~+0.4 °C per decade since 1980, so ~0.4-0.6 °C cooler is the expected offset).
- **Qualitative agreement, no numeric divergence flagged.** No bias-correction discrepancy is detectable from the information available.

`pct_diff` could not be computed for any row.

## Recommendations

1. **Drop the "Frontiers 2025 per-district cross-check" target from the project roadmap** — it cannot be done from published material. Replace it with one of:
   - **Author contact**: email László Lakatos (Eszterházy Károly Catholic University, Eger) and politely request the per-district numerical tables underlying figures 2-9. Hungarian academics are usually willing.
   - **Independent recomputation**: download the same FORESEE inputs the paper used, compute Winkler/Huglin on the same baseline (1986-2005), and compare to ours computed on the same window. This is a real cross-check of *our pipeline*, not of the paper, but it has the same scientific value.
   - **Figure digitisation**: WebPlotDigitizer over the paper's per-district bar charts. Tedious; ~5-10% extraction error per bar. Only worth doing if author contact fails.
2. **Stop framing this paper as a "peer-reviewed cross-check" source.** It is a peer-reviewed *modelling study with the same input as ours but using a single grid-cell sampling per region instead of district aggregation*. The most we can ever say is "qualitative agreement with class membership", which is what we already say.
3. The 19-of-22 district research files flagged as "missing Frontiers numbers" are missing them because **the numbers do not exist in the paper**, not because of an extraction failure. The flag should be cleared with a note pointing to this hunt report.

## Files touched

- `research/synthesis/lakatos_nagy_si_hunt.md` (this file, NEW)
- `analysis/reports/tables/frontiers2025_crosscheck.csv` (REWRITTEN — was 3-row placeholder, now 66 rows + metadata header)
- `research/synthesis/lakatos_nagy_supplementary_tables.csv` (NOT CREATED — nothing to put in it)
