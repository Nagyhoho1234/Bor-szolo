# Hungarian Wine Districts Climate Research — Task Log

**Project:** Wine-district climate susceptibility (Bor-szőlő)
**Started:** 2026-04-07
**Source paper anchor:** Lakatos & Nagy 2025 / Kovács et al. 2025, *Frontiers in Plant Science*, DOI 10.3389/fpls.2025.1481431 — *Assessment of historical and future changes in temperature indices for winegrape suitability in Hungarian wine regions (1971–2100)*. **Note:** the paper is cited under both author orderings across the district files (same DOI).

---

## Workflow

1. **Develop the research prompt** (15 sections) via directed AskUserQuestion clarification.
2. **Extract the 22 borvidék** from `wine_districts.shp` / `admin8_with_district.shp`.
3. **Pilot:** Tokaji synthesis from main thread to validate template quality.
4. **Wave 1:** 10 parallel background research agents (1 district each, full WebSearch/WebFetch access).
5. **Wave 2+3:** 11 parallel agents (rate-limit hit at first attempt, relaunched after reset, all completed).
6. **Synthesis layer:** 3 parallel agents → scientific synthesis, decision-support brief, source-downloader Python pipeline.
7. **(Pending)** Run `fetch_sources.py` to localise all 880 unique source URLs.

---

## Per-district output table

| # | District | Region | KB | Words (est) | Notes |
|---|---|---|---|---|---|
| 1 | tokaji | Tokaj | 33 | ~9,000 | Pilot template; aszú reliability is the existential risk |
| 2 | egri | Felső-Magyarországi | 40 | ~4,937 | 65 sources; Bíró et al. terroir PDF unparseable via WebFetch |
| 3 | villanyi | Pannon | 34 | ~4,445 | 45 sources; 2014 Villányi Franc PDO reform = early climate response |
| 4 | szekszardi | Pannon | 42 | ~5,112 | Pieczka et al. 2021 dedicated Szekszárd vulnerability paper, exposure +1.61/+2.03 vs national +1.39/+1.57 |
| 5 | badacsonyi | Balaton | 49 | ~5,621 | 55 sources; Klímapolitikai Intézet excludes Badacsony from "winners" — contested |
| 6 | balaton-felvideki | Balaton | 55 | ~5,760 | 85 sources; Lake Balaton +2.2 °C surface T over 150 yr, 2022 record water-balance extreme |
| 7 | balatonboglari | Balaton | 62 | (largest in Wave 1) | Completed before Wave 2+3 rate-limit |
| 8 | balatonfured-csopaki | Balaton | 63 | ~6,740 | 85 sources; Csopak Kódex as climate-defence instrument; Furmint as Kódex hedge variety |
| 9 | nagy-somloi | Balaton | 44 | ~5,654 | Most identity-vulnerable + most data-poor; Juhfark ~80–150 ha *globally* |
| 10 | zalai | Balaton | 42 | ~5,465 | Klímapolitikai Intézet flags Sopron+Zala as "winners"; +2.3 °C 1991–2020 vs 1961–90 |
| 11 | soproni | Felső-Pannon | 39 | ~4,802 | 55 sources; SLOWEST-warming Hungarian district (GDD +66.16 °C-d); +1.97 °C annual; Lake Fertő 2022 record low |
| 12 | pannonhalmi | Felső-Pannon | 43 | ~4,750 | 75 sources; smallest end-century warming (+2.3 °C RCP8.5); Liptai Zsolt named Hungarian Winemaker of Year 2024 |
| 13 | etyek-budai | Felső-Pannon | 33 | ~4,184 | 55 sources; Hungary's COOLEST district (9.5–10.5 °C); Chardonnay TA −1.5 to −2.5 g/L 1980–2020; Törley 13–14M bottles/yr, 65–70% of HU sparkling |
| 14 | mori | Felső-Pannon | 45 | ~6,030 | 35 sources; cool-climate "winner" *but* highest projected water deficit; Ezerjó >14k ha (1970) → 1,655 ha |
| 15 | neszmelyi | Felső-Pannon | 59 | ~6,740 | 80 sources; only ONE peer-reviewed district paper (Bertalan-Balázs 2022); Hilltop Neszmély = ~30% of district |
| 16 | bukki | Felső-Magyarországi | 50 | ~5,890 | 50 sources; LARGEST BEDD increase (+258.49 °C-d); "moving into Eger's 1990s climate space" |
| 17 | matrai | Felső-Magyarországi | 44 | ~4,970 | 45 sources; altitude headroom ~150–500 m; Olaszrizling harvest advanced 4–6 weeks |
| 18 | csongradi | Duna | 52 | ~6,120 | 55 sources; HIGHEST AGST warming (>+2.5 °C RCP8.5); existential viability question |
| 19 | hajos-bajai | Duna | 47 | ~5,890 | 50 sources; Lakatos & Nagy 2025 explicit name-check (HadGEM2-CCLM most pessimistic); Homokhátság −2 to −5 m groundwater |
| 20 | kunsagi | Duna | 68 | ~7,480 | 85 sources; LARGEST GDD increase (+581.65 °C-d); Hungary's largest district by area; Bianca ~90% concentration |
| 21 | pecsi | Pannon | 39 | ~4,885 | 55 sources; Cirfandli vintages 2/10 → 6/10, *but* −40% ha in 5 yr to 13.9 ha |
| 22 | tolnai | Pannon | 50 | ~6,190 | 60 sources; 1998 carve-out from Szekszárd was Paks-defensive; Antinori-controlled Tűzkő as Mediterranean tech import |

**Totals:** 22 districts • ~123,000 words • ~1,200 raw source citations (880 unique URLs after dedup) • 1.1 MB of synthesis MDs.

---

## Hungary-wide narrative the corpus enables

### Warming gradient (Lakatos & Nagy 2025 anchor)
- **Csongrád > Tokaj/Eger > Mátra/Bükk > national mean > Pannonhalma/Sopron/Zala**
- Counterintuitive: **northern districts warm faster than southern** — flips the traditional thermal ordering of Hungary
- Largest absolute changes by index:
  - **GDD:** Kunság +581.65 °C-d
  - **BEDD:** Bükk +258.49 °C-d *(because it started coolest)*
  - **AGST:** Csongrád >+2.5 °C
  - **Huglin:** Eger +566.15 °C-d
- Slowest-warming: **Sopron** GDD +66.16 °C-d (≈1/8 of Kunság)

### Climate "winners" (provisional verdict — Klímapolitikai Intézet 2023/2024)
- Sopron, Zala, Pannonhalma, Móri (near-term expansion)
- ⚠️ Móri caveat: **highest projected water deficit** of any Hungarian district

### Existential identity risks (variety-specific)
| Variety | District | Status |
|---|---|---|
| Tokaji aszú (botrytised wine) | Tokaji | Noble-rot reliability declining |
| Ezerjó | Móri | >14,000 ha (1970) → 1,655 ha Hungary-wide |
| Cirfandli | Pécsi | −40% in 5 years → 13.9 ha (2024) |
| Juhfark | Nagy-Somlói | ~80–150 ha *of global ~100–170 ha* |
| Kéknyelű | Badacsonyi | Endemic, near-extinction, heat-sensitive |

### Adaptation infrastructure already deployed
- **Csopak Kódex** (Balatonfüred-Csopaki, 2013) — terroir code with explicit yield/alcohol/TA limits
- **Villányi Franc** (Villányi, 2014) — PDO reform against alcohol creep
- **Bianca plantings** (Kunsági, ~90% national concentration)
- **Tokaj rootstock benchmarking** (Tarcal Research Institute): 140 Ruggeri / 1103 Paulsen / 110 Richter vs Teleki 5C
- **Late-pruning trials** (Eger, Pernesz et al.) — delays budburst 3–10 days, re-couples to frost-free window
- **Antinori Tűzkő** (Tolnai) — implicit Mediterranean technology transfer

### Cross-cutting infrastructure gaps every agent flagged
1. **Lakatos & Nagy 2025 supplementary tables** are not in the open-access body — district-level AGST/GDD/HI/BEDD numbers locked in FORESEE supplementary data. **Highest-leverage single fix.** Flagged in 19 of 22 files.
2. **No multi-decadal phenology series** for any district except Tokaj.
3. **EURO-CORDEX 12 km does not resolve Lake Balaton** — the lake-mesoclimate signal that defines 4 borvidék is missing from public projections.
4. **No district-level pest/disease monitoring** anywhere (S. titanus, D. suzukii, H. halys, esca, FD).
5. **Móri-szél has no published multi-decadal climatology** — district's entire resilience narrative rests on it.
6. **Soil erosion rates on steep loess/basalt slopes** under intensifying convective rain — methodology exists, no trend data.

### Top 5 contested findings
1. **Bene 2023 polyphenol non-trend** in Tokaj botrytised wines, against the global warming-drives-phenolics expectation
2. **"Climate winners" verdict** for cool districts — provisional, dependent on future water budget evolution
3. **Tokaji dry-wine pivot** — climate-driven vs market-driven causation conflated in the literature
4. **Per-district Lakatos & Nagy 2025 rankings** for non-extremes are provisional pending FORESEE table extraction
5. **Móri-szél resilience narrative** — uncharacterised wind; *"global stilling would be silent first-order degradation"*

---

## Output files inventory

```
research/
├── districts/                          22 files, 1.1 MB
│   ├── badacsonyi.md
│   ├── balaton-felvideki.md
│   ├── balatonboglari.md
│   ├── balatonfured-csopaki.md
│   ├── bukki.md
│   ├── csongradi.md
│   ├── egri.md
│   ├── etyek-budai.md
│   ├── hajos-bajai.md
│   ├── kunsagi.md
│   ├── matrai.md
│   ├── mori.md
│   ├── nagy-somloi.md
│   ├── neszmelyi.md
│   ├── pannonhalmi.md
│   ├── pecsi.md
│   ├── soproni.md
│   ├── szekszardi.md
│   ├── tokaji.md          ← pilot template
│   ├── tolnai.md
│   ├── villanyi.md
│   └── zalai.md
├── synthesis/
│   ├── scientific_synthesis.md         ~7,080 words, 80 cross-refs, 13 sections
│   └── decision_support_brief.md       ~9,700 words, 22-district risk table, policy actions, glossary
├── sources/
│   ├── fetch_sources.py                570 lines; 880 unique URLs; 8 parallel workers; idempotent
│   └── README.md                       126 lines
└── RESEARCH_LOG.md                     this file
```

## File-format conventions used by every district MD
- Section structure: 1. Profile · 2. Terroir · 3. Baseline climate · 4. Observed trends · 5. Phenology/yield · 6. Chemistry · 7. Sensory/style · 8. Biotic stressors · 9. Abiotic extremes · 10. Indirect effects · 11. Future projections · 12. Adaptation · 13. Economic & market · 14. Knowledge gaps · 15. Sources
- Every claim tagged: `[OBSERVED]` vs `[PROJECTED]`
- Fall-back markers: `[HU-AGGREGATE]` (Hungary-wide proxy), `[ALFÖLD-AGGREGATE]` (regional proxy), `[GAP]` (no data)
- Sources cited inline as Markdown links plus a consolidated §15 list

---

## Top 5 policy actions (from the decision-support brief)

1. **Ease vineyard irrigation legal restrictions** — unanimous call across Tokaji, Egri, Kunsági, Csongrádi, Hajós-Bajai, Villányi, Szekszárdi, Móri, Balaton files. Regulated deficit irrigation with SPEI/PDSI triggers; explicit exclusion of Lake Balaton withdrawals and Homokhátság shallow groundwater.
2. **Modify PDO borders, variety lists, chemistry/yield caps** — using Csopak Kódex (2013) and Villányi Franc (2014) as templates. Admit Pinot Meunier to Etyeki Pezsgő PDO; Mediterranean varieties to Villány/Szekszárd/Tolna/Pécs/Csongrád.
3. **Fund FORESEE 4.0 / Lakatos & Nagy 2025 supplementary table extraction at per-PDO resolution** — cheapest, fastest single policy win.
4. **Establish district-level phenology + pest-monitoring networks** — ~22 OMSZ reference stations + PEP725-compatible phenology + S. titanus/H. halys/D. suzukii/FD/esca surveillance.
5. **Coupled lake-vineyard mesoclimate downscaling** for the four Balaton PDOs and Lake Fertő.

## Top 5 grower actions by season (decision-support brief)

1. **Spring** — late winter pruning to delay budburst 3–10 days (Pernesz et al. Eger).
2. **Early summer** — retain canopy cover on afternoon side, raise fruiting wire 100–110 cm (Werner & Kozma Badacsony protocol).
3. **Summer** — switch from calendar to lab-marker harvest decisions; night harvesting; multi-pass picking.
4. **Harvest** — rapid chilling, whole-bunch pressing for whites, cooler ferment, partial whole-cluster reds, tartaric acidification within PDO bounds in hot vintages.
5. **Winter (dormant)** — cover crops, mulching, dry-stone terrace restoration; replant on **140 Ruggeri / 1103 Paulsen / 110 Richter** drought-tolerant rootstocks.

---

## Open follow-ups

- [ ] Run `python research/sources/fetch_sources.py` (~1 hour, 880 URLs)
- [ ] Standardise the **Lakatos & Nagy 2025** vs **Kovács et al. 2025** citation across all 22 district files (same DOI 10.3389/fpls.2025.1481431)
- [ ] Inject `analysis/curated/` computed Winkler/Huglin/normals into each district's §3 Baseline + §4 Observed sections, replacing agent-pulled proxy values
- [ ] Generate per-district website JSON (one-line verdicts, key numbers, threat tags) for `site/public/data/`
- [ ] Add Hungarian-language translations to each district MD's identity-risk and adaptation sections for the bilingual site
