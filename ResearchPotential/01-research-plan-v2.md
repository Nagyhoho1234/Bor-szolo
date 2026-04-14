# PhD Research Plan v2: Climate and Terroir of Hungarian Wine Regions

**Author:** Fehér Zsolt Zoltán
**Date:** 2026-04-14
**Version:** 2.1 (revised 2026-04-14 — incorporates station data review, MetAgro findings, and 6-point gap analysis)

This plan frames a three-paper PhD around a single question: *How is climate change reshaping the conditions under which Hungarian wine grapes grow, and what does this mean for the growers?* The national atlas answers this at the country scale. The Tokaj mesoclimate paper answers it at the vineyard scale, in the one region where we have the station density to do so. The follow-up paper adds the soil and canopy layers that complete the terroir picture.

---

## 1. PhD Publication Strategy Overview

### The three papers

**Paper A — National Wine Climate Atlas**
A country-wide assessment of climate susceptibility for all 22 Hungarian wine districts (borvidék), using gridded climate projections (FORESEE-HUN), 9 viticulture indices, and suitability envelopes for 58 grape varieties under RCP4.5 and RCP8.5 through 2100. The Bor-szőlő project is essentially complete: the analysis pipeline, curated dataset, bilingual atlas website, and 22 per-district PDFs exist. This paper writes up the methodology and headline findings for a peer-reviewed journal.

**Paper B — The Tokaj Mesoclimate Paper** (main focus of this plan)
One comprehensive paper combining three acts. A 50-station agrometeorological network in the Tokaj wine region — the densest such network in any Central or Eastern European wine region — captures what no 11 km gridded product can resolve: the actual climate where grapes grow. Act 1 maps the mesoclimatic variability and identifies bioclimatic zones. Act 2 tests whether the historical quality hierarchy among named vineyard parcels (dűlők) reflects measurable climate differences. Act 3 addresses two questions of immediate practical importance: where do conditions favour noble rot (aszú) versus destructive grey rot, and where is spring frost risk greatest after budbreak?

**Paper C — Multi-Layer Tokaj Terroir**
A future paper integrating soil properties (DOSoReMI 25 m maps), remote sensing (Sentinel-2 NDVI, potentially hyperspectral), and LiDAR-derived terrain into the mesoclimatic framework established by Paper B. This extends the climate-only terroir characterisation into a full soil-climate-vegetation terroir model. Requires at least one additional growing season of coordinated observations.

### How they connect

The thesis arc moves from **macro to meso to micro**:

1. Paper A establishes that Hungarian wine districts face divergent climate futures — some districts gain suitability, others lose it, and the trajectory follows an inverted-U pattern where warming initially helps but eventually collapses suitability. Tokaj, as Hungary's most famous and UNESCO-protected wine region, is a natural focus case.

2. Paper B zooms in. The national atlas treats each district as a single point. But within Tokaj, a 50-station network reveals that the district is not climatically uniform — there are distinct mesoclimatic zones, and these zones matter for grape quality, disease pressure, and frost exposure. The national model's limitations become the local model's motivation.

3. Paper C adds the remaining terroir dimensions. Climate alone does not make terroir — soil water-holding capacity, root zone depth, slope drainage, and canopy vigour all interact. The mesoclimatic zones from Paper B become the spatial framework onto which soil and vegetation layers are mapped.

This is a coherent progression: country-level vulnerability (Paper A) motivates vineyard-level investigation (Paper B), which provides the spatial framework for full terroir characterisation (Paper C).

---

## 2. Paper B: The Tokaj Mesoclimate Paper

### Research questions (viticulture-first)

1. **How much climate variation exists within a single wine district?** Gridded products treat Tokaj as climatically homogeneous. Does the 50-station network reveal meaningful differences in growing season heat accumulation, night-time cooling, and water availability across the district's volcanic slopes, river valleys, and plateaux?

2. **Do the historically ranked vineyard parcels occupy measurably different climates?** Tokaj has a centuries-old quality hierarchy among its named dűlők (first formally classified in 1772). Do premier parcels like Szarvas, Szent Tamás, Betsek, and Nyulászó share climate characteristics that distinguish them from average-quality sites — and if so, what are those characteristics?

3. **Where does noble rot thrive, and where does it turn destructive?** Aszú production depends on *Botrytis cinerea* developing as noble rot rather than grey rot. Noble rot requires specific humidity, temperature, and airflow patterns — alternating morning mist and afternoon drying. Can we map where these conditions occur reliably versus where botrytis is more likely to be destructive?

4. **Which vineyards are most exposed to spring frost after budbreak?** Cold air drainage in Tokaj's volcanic valleys creates frost pockets. Which parcels are within the thermal belt (protected), and which sit in cold pools where late frost threatens Furmint after budbreak in April–May?

### Three-act structure

#### Act 1: Climate variability and bioclimatic zones

**What we want to know:** Is Tokaj one climate or several? How different are the warmest and coolest vineyard sites?

**Approach:**
- Compute standard viticulture indices at each of the 50 stations: Huglin Index (heliothermal), Winkler GDD (heat accumulation), Cool Night Index (ripening-period night temperatures), Dryness Index (water balance), and Biologically Effective Degree Days (BEDD). These are the same indices used in Paper A at the national scale, enabling direct comparison.
- Quantify the within-district range. In Bordeaux, de Rességuier et al. (2020) found up to 10 degrees C spatial amplitude in daily minimum temperatures across 90 sensors. Tokaj's volcanic terrain and river-valley topography may produce comparable variation.
- Use principal component analysis to identify which index combinations drive the most spatial variation. In most viticultural networks, the first two components (heat accumulation vs. night-time cooling) explain 70-85% of variance.
- Cluster stations into mesoclimatic zones using k-means on principal component scores, with silhouette analysis to determine the natural number of zones. Hierarchical clustering with Ward linkage provides a complementary view of nested structure.
- Extend point-based station indices to continuous maps using regression-kriging. The deterministic trend relates indices to terrain variables (elevation, slope, aspect, topographic position index) derived from a high-resolution DEM. The stochastic residuals are interpolated via ordinary kriging. Target resolution: 25-50 m, consistent with Bois et al. (2018) in Bordeaux and Gavrilescu et al. (2018) in Burgundy.

**Key outputs:** (a) A table of bioclimatic indices at all 50 stations showing the within-district range. (b) A map of mesoclimatic zones at 25-50 m resolution. (c) Comparison of station-derived index values against the FORESEE-HUN gridded values used in Paper A, quantifying the "added value" of local observations.

#### Act 2: Testing the historical dűlő quality hierarchy

**What we want to know:** Tokaj's dűlő classification has existed for centuries, but it was based on tasting, tradition, and commercial reputation — not measurement. Do premier-ranked parcels share measurable climate traits?

**Approach:**
- Overlay the mesoclimatic zone map from Act 1 onto the official vineyard parcel boundaries (MePAR cadastre).
- Extract the bioclimatic index values (from the interpolated surfaces) for each classified dűlő. Group parcels by their historical classification tier.
- Test statistically whether premier dűlők have significantly different index distributions from average parcels. The hypothesis is that premier sites occupy a "sweet spot" — warm enough for full ripeness but with sufficient night-time cooling for aromatic complexity and acid retention, and with adequate but not excessive water availability.
- Compare the climate profiles of well-known premier sites: Szarvas (Tarcal), Szent Tamás (Mád), Betsek (Mád), Nyulászó (Mád), Király (Mád), Disznókő (Mezőzombor), Előhegy (Tokaj-town). Several of these have stations in our network.
- If the climate signal is strong, identify whether premier sites cluster in a particular range of the Huglin Index, Cool Night Index, or their combination — effectively defining a "quality climate envelope" for Tokaj.

**Key outputs:** (a) Box plots or violin plots of bioclimatic indices by dűlő classification tier. (b) Statistical test results (Kruskal-Wallis or ANOVA) for tier differences. (c) A "quality climate envelope" if the data support it — the climate conditions that historically ranked parcels share.

**Important caveat:** Terroir is not climate alone. Premier dűlő status reflects soil, aspect, drainage, and centuries of human management. We expect the climate signal to be one factor among several, not the sole explanation. This is acknowledged in the paper and motivates Paper C.

#### Act 3: Noble rot geography and frost risk

**Part A — Noble rot vs. grey rot spatial conditions**

**What we want to know:** Aszú is Tokaj's signature product. Its production requires *Botrytis cinerea* to develop as noble rot — a process that depends on morning humidity (fog from the Bodrog and Tisza rivers), followed by afternoon drying and warmth. Where in the district do these conditions occur most reliably?

**Approach:**
- **Requires 10-minute or hourly data** (not daily aggregates). The key mechanism in Tokaj is the **Bodrog–Tisza confluence fog**: morning mist rises from the rivers, envelops south-facing slopes, then burns off by midday as solar heating dries the berries. This diurnal cycle — wet dawn, dry afternoon — is what separates noble rot from grey rot. Daily mean RH cannot capture it.
- Define "noble rot favourability" using sub-daily criteria at each station: (a) RH > 90% at 06:00–09:00 (morning fog window), (b) RH drops below 65% by 14:00–16:00 (afternoon drying), (c) Tmax > 20°C (warmth for berry dehydration), (d) no sustained rainfall > 5 mm/day (rain spreads grey rot). Count favourable days per station during the critical September–November window.
- Define "grey rot risk" as days where RH remains above 80% through 14:00, leaf wetness persists beyond 6 hours, and temperatures remain 15–22°C — conditions favouring destructive *B. cinerea* infection without the drying cycle needed for noble rot.
- Map the spatial distribution of noble rot favourability versus grey rot risk across the district. **The core hypothesis is geographic:** river-proximate sites on south-facing slopes receive morning fog but dry quickly in afternoon sun (favouring noble rot), while enclosed valleys, north-facing sites, or locations far from the rivers remain humid through the day (favouring grey rot). This would explain why the historic aszú-producing dűlők cluster near the Bodrog confluence.
- Correlate noble rot favourability with the mesoclimatic zones from Act 1 and the dűlő quality tiers from Act 2. Do the zones, the history, and the fog-drying patterns all converge on the same parcels?

**Part B — Spring frost exposure**

**What we want to know:** Which vineyard sites are most vulnerable to spring frost damage after Furmint budbreak?

**Approach:**
- Analyse minimum temperature patterns during the frost-risk window (April-May) at all 50 stations. Identify cold air pooling sites (valley floors, concave topography) versus thermal belt sites (mid-slope, convex positions).
- Regress minimum temperatures under radiation frost conditions (clear, calm nights — identified from wind speed and humidity data) against terrain variables: elevation, topographic position index (TPI), cold air flow accumulation paths, and sky view factor.
- Produce a frost probability map at 25-50 m resolution. Overlay this with the phenological vulnerability window: Furmint budbreak (BBCH 07) typically occurs in late April in Tokaj, and the critical damage threshold for emerged shoots is approximately -2 degrees C.
- Estimate return periods for damaging frost events at key vineyard locations using extreme value analysis (GEV distributions).

**Key outputs for Act 3:** (a) A map of noble rot favourability across the district, showing the spatial gradient from river-influenced fog zones to drier interior sites. (b) A frost risk map showing the thermal belt and cold pool locations. (c) Practical recommendations: which parcels are best suited for aszú production, and which require frost protection measures.

### What we already know about the station data

Five stations in Mád have been examined from PDF exports (daily resolution, full 2025). This shapes what the paper can and cannot do:

| Station | ID | Full sensor suite? | Quality issues | Usable for |
|---|---|---|---|---|
| Szilvás | D3006 | Yes (9 variables) | None — complete year | All three acts |
| Szent Tamás | D3005A | Yes (9 variables) | None — complete year | All three acts |
| Kővágó | D3007 | Yes (9 variables) | None — complete year | All three acts |
| Danczka | — | Reduced (4 variables: T, RH, precip, leaf wetness) | No wind, soil T, radiation, soil moisture | Acts 1 & 3A only (indices + noble rot), NOT frost modelling (no wind for calm-night classification) |
| Betsek | — | Rich (10 variables incl. battery) | **Temperature sensor stuck May–Jul 2025** (min=mean=max). Soil moisture reads negative (uncalibrated). No solar radiation. | Act 1 partial (indices only from Jan–Apr + Aug–Dec). Act 2 limited. Betsek is a premier dűlő — this data gap hurts. |

**Critical implications:**
1. **Betsek's growing-season gap** means the most famous dűlő in our network has incomplete 2025 data. The QC pipeline must flag and gap-fill this using neighbouring stations (Szilvás and Szent Tamás are closest). If MetAgro's 10-minute archive has a working backup sensor, that's the first thing to check with credentials.
2. **Danczka's reduced sensor suite** limits it to thermal indices and disease risk — no frost modelling contribution (wind speed needed for radiation frost identification).
3. **Daily resolution is insufficient for Act 3 Part A (noble rot).** Noble rot vs grey rot distinction depends on the diurnal cycle: morning fog (RH > 90% at dawn) followed by afternoon drying (RH < 65% by 14:00). Daily mean RH conflates the two. **We must obtain 10-minute or hourly data from MetAgro** — confirmed available (platform stores 10-min intervals).
4. **Soil moisture at Betsek** reads negative (likely raw sensor millivolt output, not calibrated to volumetric %). This can be calibrated against gravimetric samples or excluded and noted.
5. **All 5 stations lack GPS coordinates and elevation in the PDFs** — must retrieve from MetAgro map interface or field GPS.

### The MetAgro platform (metagro.hu/mad)

The ~50 stations are operated by the **University of Debrecen** (Dr. Attila Dobos, Precision Plant Production R&D Service Center) in partnership with the Mád Wine Academy. Key facts:
- **10-minute data resolution** stored on the server — far richer than the daily PDF exports
- Archive, map, and model sections exist behind a login wall
- **No public registration** — access via Dr. Dobos (06-30-2490794, info@metagro.hu)
- Credentials expected from a colleague; priority once obtained: (1) full station list with coordinates, (2) 10-min data download for all stations, (3) check for multi-year archives pre-2025

### How Paper A's national results frame Paper B

Paper A computes a single set of index values for the Tokaj district (area-weighted polygon mean from FORESEE-HUN at ~11 km). Paper B decomposes that single number into 50 station-level values. The headline framing:

> *"The national atlas assigns Tokaj a Huglin Index of X. Our 50-station network shows the actual range within the district is Y to Z — a spread of W units that spans [N] Huglin classes. The 11 km gridded product misses this variability entirely."*

Specific linkage points:
- **Paper A's Tokaj Huglin/Winkler values** become the "district average" benchmark in Act 1
- **Paper A's Furmint suitability score** for Tokaj (currently computed as a district-level number) can be decomposed: which parcels within Tokaj are above/below the suitability threshold?
- **Paper A's inverted-U trajectory** (suitability peaks ~2040, collapses by 2100) raises the question: does this trajectory affect all parcels equally, or do some micro-climates delay the crossover?
- The FORESEE-HUN gridded values used in Paper A are directly compared against station observations in Act 1, quantifying the "added value" of local monitoring

### Single-year data: framing strategy

With only 2025 data, the paper cannot claim climatological normals. The framing must be explicit:

**What we can say:** "We characterise the *spatial structure* of mesoclimatic variability across 50 stations. The relative differences between sites — which parcels are consistently warmer, cooler, wetter, drier than their neighbours — are robust even from a single season, because the dominant driver (topography) does not change year to year."

**What we cannot say:** "The long-term average Huglin Index at station X is Y." One year is one vintage.

**How to strengthen:** Place 2025 in context using FORESEE-HUN and ERA5-Land long-term normals for the Tokaj grid cell. Report: "The 2025 growing season was Z°C warmer/cooler than the 1991–2020 normal, with W% more/less precipitation. The spatial patterns we observe should be interpreted against this baseline." OMSZ historical records (if obtainable for Tokaj/Tarcal stations) provide additional context.

**If MetAgro has multi-year archives:** This changes everything. Even 3–5 years of data allows computing mean index values with confidence intervals, and testing whether the spatial structure is stable across vintages.

### Why one paper, not three

The three acts are linked by the mesoclimatic framework from Act 1. The zone map is the foundation: Act 2 validates it against historical quality knowledge, and Act 3 demonstrates its practical application. Splitting them into separate papers would mean repeating the network description, station map, and interpolation methodology three times. A single comprehensive paper in a high-impact venue is stronger than three fragmented ones.

The structure also tells a story: *We measured the climate variability (Act 1). The historical vintners already knew about it (Act 2). And it has immediate practical consequences for aszú production and frost management (Act 3).*

---

## 3. Data Requirements for Paper B (Tokaj Mesoclimate)

| Data type | Source | Status | Spatial resolution | Key variables | Needed for |
|---|---|---|---|---|---|
| Station meteorological data (daily) | MetAgro platform (metagro.hu/mad), Univ. Debrecen | **Available** — 2025 full year confirmed for 5 Mád stations; ~50 stations total, login required | Point (~50 locations) | Tmin, Tmean, Tmax, RH, wind speed, precipitation, leaf wetness, soil T, soil moisture (variable per station — see QC section) | All three acts |
| Station meteorological data (10-min) | MetAgro platform archive | **Available behind login** — platform stores 10-min intervals | Point (~50 locations) | Same variables at sub-daily resolution | **Essential for Act 3A** (noble rot diurnal cycle); valuable for Act 3B (frost event timing) |
| Digital elevation model | EU-DEM v1.1 or SRTM | **Freely available**, download needed | 25 m (EU-DEM) or 30 m (SRTM) | Elevation, slope, aspect, TPI, flow accumulation, sky view factor | Act 1 (regression-kriging covariates), Act 3 (frost risk) |
| LiDAR-derived DEM | Hungarian national LiDAR survey or Pásztor et al. (2015) Tokaj dataset | **May be available** — check data access | 1-5 m | High-resolution terrain for cold air drainage modelling | Act 3 (improved frost mapping) |
| Vineyard parcel boundaries | MePAR (Hungarian agricultural parcel registration system) | **Available** via NÉBIH | Cadastral parcels | Parcel geometry, land use classification | Act 2 (dűlő overlay) |
| Historical dűlő classification | Published sources: 1772 classification (Mária Terézia decree), Tokaj-Hegyalja borvidéki rendtartás, Balassa (1991) monograph | **Available but requires careful compilation** — see note below | Named parcels | Classification tier (first class, second class, etc.) | Act 2 (quality hierarchy test) |
| Phenological observations | Field observations at selected vineyard plots | **Partial** — check if BBCH-stage records exist from cooperating estates | Plot-level | Budbreak (BBCH 07), flowering (65), veraison (85), harvest (89) dates | Act 3 (frost vulnerability window); desirable for Act 1 |
| Disease/botrytis field observations | Field surveys or cooperating estate records | **To be collected or obtained** | Plot-level | Noble rot incidence, grey rot incidence, disease severity scores | Act 3 Part A (validation of noble rot model) |
| ERA5-Land reanalysis | Copernicus Climate Data Store (CDS API) | **Freely available**, download needed | ~9 km (0.1 degree) | Hourly T2m, dewpoint, precipitation, wind, radiation | Act 1 (gridded product comparison) |
| FORESEE-HUN gridded dataset | ELTE Department of Meteorology | **Available** — already used in Paper A | ~11 km (0.1 degree) | Daily Tmin, Tmax, precipitation; RCP4.5/8.5 projections | Act 1 (comparison with national-scale values) |
| Weather type classification | OMSZ synoptic records or ERA5 surface pressure fields | **Available** — derivable from ERA5 | Synoptic-scale | Radiation frost nights (clear, calm) vs. advective events | Act 3 Part B (frost type separation) |
| River fog/mist records | OMSZ visibility observations at Tokaj or Tarcal stations | **Check availability** | Point | Fog occurrence, duration | Act 3 Part A (noble rot conditions validation) |
| Historical OMSZ station records | Hungarian Meteorological Service | **Available** — request needed | Point (1-3 stations in Tokaj area) | Long-term Tmin, Tmax, precipitation (for climatological context) | Act 1 (placing 2025 vintage in historical context) |

**Note on dűlő classification data:** The 1772 Mária Terézia decree established the first formal vineyard classification in Tokaj, but the number of tiers, which parcels fall in which tier, and whether the original classification maps to modern parcel boundaries all require scholarly compilation. Balassa Iván's *Tokaj-Hegyalja szőleje és bora* (1991) is the most comprehensive source. The current Tokaj-Hegyalja borvidéki rendtartás provides a modern regulatory framework. **Fallback strategy:** if formal tier data proves incomplete or disputed, Act 2 can still compare the 5 named dűlők where we have stations (Betsek, Szent Tamás, Kővágó, Szilvás, Danczka) against each other — these are all well-known parcels with different reputations. Even without a formal tier system, testing whether historically prized parcels (Betsek, Szent Tamás) have measurably different climates from lesser-known ones is a valid research question.

**Minimum viable dataset for Paper B:** Station data (available) + DEM (freely available) + MePAR parcels (available) + dűlő classification (available but needs compilation). Everything else enhances the paper but is not strictly required.

---

## 4. Data Requirements for Paper A (National Wine Climate Atlas)

| Data type | Source | Status | Spatial resolution | Key variables | Notes |
|---|---|---|---|---|---|
| FORESEE-HUN gridded climate | ELTE | **Complete** — processed in pipeline | ~11 km | Daily Tmin, Tmax, precipitation; 1971-2100, RCP4.5/8.5 | 9 viticulture indices computed |
| Wine district polygons | Official borvidék boundaries | **Complete** — 22 districts in wine_districts.geojson | Administrative boundaries | Geometry | Area-weighted polygon means computed |
| Grape variety envelopes | Literature compilation | **Complete** — 58 varieties in grape_envelopes.csv | N/A | Huglin, Winkler, BEDD, CNI, DI thresholds per variety | 38 Hungarian/CE + 14 Mediterranean + 6 PIWI |
| CCKP CMIP6 ensemble | World Bank Climate Change Knowledge Portal | **Complete** — 14 variables extracted | ~100 km | SSP2-4.5, SSP5-8.5 projections for validation | Independent validation of FORESEE-HUN trends |
| HungaroMet station observations | OMSZ/HungaroMet open data portal | **Complete** — 21 of 22 districts covered | Point | Tmean, precipitation, 2020-2024 | Credibility anchor for gridded data |
| Threats data | Literature and NÉBIH reports | **Complete** — 4 curated CSVs | N/A | Flavescence dorée timeline, trunk diseases, pests, EU pesticide regulations | 67 of 73 rows fully verified |
| Normals and anomalies | Derived from FORESEE-HUN | **Complete** — 10 period-scenario combinations | Per district | 30-year normals, anomalies, risk flags | 6 periods x 2 scenarios (minus observed duplicates) |
| Variety suitability scores | Computed by s04_variety_match.py | **Complete** — per-district JSON files | Per district | Suitability score (0-1) per variety per period per scenario | Soft-Winkler scoring with gap/4.0 |
| Variety replacements | Computed from suitability | **Complete** — per-district JSON files | Per district | Top 4 climate-adapted candidates per horizon | Future-looking adaptation recommendations |
| District descriptions | Curated bilingual prose | **Complete** — 22 districts, EN + HU | Per district | Geography, history, climate narrative, key findings | Atlas content layer |
| Research dossiers | Long-form research documents | **Complete** — ~123K words, fully translated | Per district | Detailed analysis with source citations | 880 unique URLs, 640 fetched |

**Status for Paper A:** All data and analysis are complete. The task is to write the journal manuscript.

**Headline finding and novelty statement:** The first comprehensive, variety-resolved climate susceptibility assessment for all 22 Hungarian wine districts. The central result is the **inverted-U suitability trajectory under RCP8.5**: mean suitability rises from 0.75 (1991–2020) to 0.83 (2021–2040) as warming lifts cool districts into higher quality classes, plateaus through 2060, then collapses to **0.33 by 2081–2100** as even Mediterranean and PIWI varieties cannot compensate. This contradicts the simple narrative that Central European wine regions are "winners" of climate change — they are temporary winners with a crossover point.

**Lead indices:** Huglin Index and Winkler GDD carry the heat-accumulation story (largest increase: Kunság, +581.65°C-d). Cool Night Index and BEDD capture the quality dimension (night-time warming erodes aromatic complexity). Dryness Index and drought days quantify the emerging water stress that is new to historically well-watered Hungarian regions.

**Novelty beyond existing literature:** Lakatos & Nagy (2025) analysed Hungarian viticulture climate change but at the index level only. Paper A adds the variety-suitability matching layer (58 varieties × 22 districts × 6 periods × 2 scenarios) and the replacement recommendation system — showing not just that climate is changing, but which specific varieties should replace which, and when. The counterintuitive finding that **northern Hungary warms faster than southern** also challenges assumptions.

**Framing decision:** For *Agricultural and Forest Meteorology*, lead with the inverted-U trajectory and the variety-suitability methodology. For *OENO One*, lead with the practical variety replacement recommendations. For *Climatic Change*, lead with the adaptation policy implications.

---

## 5. Data Requirements for Paper C (Future Multi-Layer Terroir)

| Data type | Source | Status | Spatial resolution | Key variables | Priority |
|---|---|---|---|---|---|
| Soil property maps | DOSoReMI (Pásztor et al.) | **Available** — 25 m national coverage | 25 m | Sand/silt/clay fractions, organic carbon, pH, available water capacity, depth to bedrock | High — core terroir layer |
| Soil microbiome data | Remenyik et al. (2024) published for 4 Mád dűlők | **Partial** — Betsek, Szent Tamás, Király, Nyulászó characterised | Plot-level | Bacterial and fungal community composition | Medium — contextual |
| Sentinel-2 multispectral | ESA Copernicus Open Access Hub | **Freely available** — needs processing | 10 m (visible/NIR), 20 m (red edge/SWIR) | NDVI, NDWI, Red Edge indices for canopy vigour | High — vegetation response layer |
| Sentinel-2 time series (multi-year) | ESA | **Freely available** — needs cloud-free composite workflow | 10-20 m | Seasonal NDVI profiles for phenology tracking | Medium |
| Hyperspectral imagery | Airborne campaign (cf. Lukácsy et al., 2014) | **Requires new acquisition or data sharing** | 1-5 m | LAI, chlorophyll content, water stress indicators | Low — expensive, nice-to-have |
| LiDAR point cloud | National survey or dedicated flight | **Check availability** of national LiDAR coverage for Tokaj | <1 m | Canopy height model, row orientation, terrain microrelief | Medium — enhances terrain model |
| Yield and quality records | Cooperating estates in Tokaj | **To be negotiated** | Plot/parcel level | Yield (kg/ha), must weight (degrees Brix or KMW), titratable acidity, botrytis incidence | High — the response variable |
| Soil moisture sensor network | Your 50-station network (subset with soil sensors) | **Available** for equipped stations | Point | Volumetric water content at 1-2 depths | High — validates soil water models |
| Water balance model outputs | Computed from station + soil + ET0 | **To be computed** | 25-50 m | Daily soil water deficit, actual ET, drainage | High — connects climate to vine stress |
| Multi-year phenological observations | Coordinated field campaign | **Requires 2-3 additional seasons** | Plot-level | BBCH stages at 10+ plots across mesoclimatic zones | High — links climate to vine response |

**Paper C timeline constraint:** This paper requires at least 2-3 growing seasons of coordinated field observations (phenology, yield, quality) across multiple parcels representing different mesoclimatic zones and soil types. The earliest realistic submission is 2028-2029 if field campaigns begin in 2026.

---

## 6. Timeline and Dependencies

### What can start immediately (2026 spring-summer)

| Task | Depends on | Feeds into |
|---|---|---|
| Write Paper A manuscript | Nothing — data complete | Paper A submission |
| QC pipeline for 50-station 2025 data | Raw station data | Everything in Paper B |
| Compute bioclimatic indices at all stations | QC'd station data | Act 1 |
| Download EU-DEM 25 m for Tokaj extent | Nothing | Act 1 regression-kriging |
| Download ERA5-Land for Tokaj grid cells | CDS API access | Act 1 (gridded comparison) |
| Obtain MePAR parcel boundaries | NÉBIH data request | Act 2 |
| Compile dűlő classification from published sources | Library/archive work | Act 2 |
| Download Sentinel-2 archive for Tokaj (2024-2025) | Nothing | Paper C prep |

### Requires 2026 growing season data collection

| Task | Depends on | Feeds into |
|---|---|---|
| Collect phenological observations (BBCH stages) at 10+ plots | Plot selection, observer training | Act 3 (frost vulnerability window), Paper C |
| Record botrytis incidence — noble rot vs. grey rot | Harvest season (Sept-Nov) | Act 3 Part A validation |
| Operate station network through full 2026 season | Station maintenance | Multi-year analysis, Paper C |

### Analysis workflow for Paper B

```
Phase 1 (Apr-Jun 2026): Data preparation
  - QC and gap-fill 2025 station data
  - Compute terrain covariates from DEM
  - Compute bioclimatic indices at all stations

Phase 2 (Jun-Aug 2026): Act 1 analysis
  - PCA and clustering of stations
  - Regression-kriging for continuous maps
  - Compare against FORESEE-HUN grid values

Phase 3 (Aug-Oct 2026): Act 2 analysis
  - Overlay zones on MePAR parcels
  - Extract index values per dűlő
  - Statistical testing of quality tier differences

Phase 4 (Nov 2026 - Jan 2027): Act 3 analysis
  - Noble rot favourability mapping (using 2025 humidity/temperature data)
  - Frost risk mapping and return period estimation
  - If 2026 botrytis field data available, validate noble rot model

Phase 5 (Jan-Mar 2027): Writing and submission
  - Draft manuscript
  - Internal review, revision
  - Submit to target journal
```

### Paper A timeline

Paper A can be written up and submitted in parallel with Paper B data preparation. Target: manuscript draft by June 2026, submission by August 2026.

### Paper C timeline

Paper C depends on:
- Mesoclimatic zone map from Paper B (available by late 2026)
- At least 2 growing seasons of phenological and yield data (available by end of 2027 at earliest)
- Soil data integration and water balance modelling (can begin mid-2027)
- Realistic submission: late 2028 or early 2029

### Summary Gantt

```
2026  Q2    Q3    Q4    | 2027  Q1    Q2    Q3    Q4    | 2028  Q1    Q2    Q3    Q4
|-----|-----|-----|     |-----|-----|-----|-----|     |-----|-----|-----|-----|
Paper A:
[=====write=====]submit
                  review/revision

Paper B:
[==QC+indices==]
      [===Act 1===]
            [===Act 2===]
                  [===Act 3===]
                        [==write==]submit
                                    review/revision

Paper C:
[====field season 1 (2026)====]
                        [====field season 2 (2027)====]
                                    [===soil+RS integration===]
                                                [===write===]submit
```

---

## 7. Target Journals

### Paper A — National Wine Climate Atlas

| Rank | Journal | IF (approx.) | Rationale |
|---|---|---|---|
| 1 | **Agricultural and Forest Meteorology** | ~6.1 | Top venue for applied climatology in agriculture. The 22-district scope, 58-variety envelope matching, and inverted-U trajectory are well suited. |
| 2 | **OENO One** | ~3.1 | Diamond open access, viticulture-specific Q1. Reaches the wine science community directly. The variety suitability modelling and replacement recommendations fit perfectly. |
| 3 | **Climatic Change** | ~4.8 | If framed around the adaptation challenge — which varieties replace which, and when. The inverted-U finding (warming helps then collapses suitability) is policy-relevant. |
| 4 | **Climate Services** | ~4.5 | If framed as a decision-support tool for the Hungarian wine sector. The atlas website and downloadable dataset strengthen the "service" angle. |
| 5 | **International Journal of Climatology** | ~3.5 | Broader climate audience. Good for the methodological contribution (area-weighted polygon means, multi-index ensemble approach). |

### Paper B — Tokaj Mesoclimate

| Rank | Journal | IF (approx.) | Rationale |
|---|---|---|---|
| 1 | **Agricultural and Forest Meteorology** | ~6.1 | The three-act structure (mesoclimate mapping + terroir validation + practical applications) fits the journal's scope exactly. Dense station network papers from Bordeaux and Burgundy have been published here. |
| 2 | **OENO One** | ~3.1 | Diamond OA, wine-science community. The terroir validation angle (Act 2) and noble rot geography (Act 3) are uniquely viticultural. Bois et al. (2018) Bordeaux zoning was published here. |
| 3 | **Frontiers in Plant Science — Crop Science & Horticulture** | ~4.1 | Open access. De Rességuier et al. (2020) 90-sensor Bordeaux paper was published here. Good for the combined climate-disease-frost scope. |
| 4 | **International Journal of Biometeorology** | ~3.3 | Strong fit for the frost risk and phenological vulnerability aspects. |
| 5 | **Australian Journal of Grape and Wine Research** | ~3.1 | Now published by Wiley. Good for the terroir validation and variety-specific findings. |

### Paper C — Multi-Layer Tokaj Terroir

| Rank | Journal | IF (approx.) | Rationale |
|---|---|---|---|
| 1 | **OENO One** | ~3.1 | The most terroir-focused Q1 journal. Multi-layer terroir characterisation is core to its scope. |
| 2 | **Agricultural and Forest Meteorology** | ~6.1 | If the climate-soil-vegetation interaction modelling is strong enough for a methods contribution. |
| 3 | **European Journal of Agronomy** | ~4.5 | Good for the integrated soil-climate-yield modelling approach. |
| 4 | **Precision Agriculture** | ~5.4 | If the remote sensing and spatial modelling components are prominent. |
| 5 | **Geoderma** | ~5.6 | If the soil property mapping and soil-terroir relationship is the strongest result. |

---

## 8. Key References

### Bioclimatic indices and viticultural climate classification

- **Tonietto, J. and Carbonneau, A. (2004).** A multicriteria climatic classification system for grape-growing regions worldwide. *Agricultural and Forest Meteorology*, 124, 81-97. *The foundational framework combining Huglin Index, Cool Night Index, and Dryness Index. Used in both Paper A (national scale) and Paper B (station-level computation).*

- **Huglin, P. (1978).** Nouveau mode d'évaluation des possibilités héliothermiques d'un milieu viticole. *Comptes Rendus de l'Académie d'Agriculture de France*, 64, 1117-1126. *Defines the heliothermal index used universally in viticultural zoning.*

- **Gladstones, J. (1992).** *Viticulture and Environment.* Winetitles, Adelaide. *Introduced BEDD as a refined heat accumulation metric with biological upper and lower thresholds.*

- **Amerine, M.A. and Winkler, A.J. (1944).** Composition and quality of musts and wines of California grapes. *Hilgardia*, 15, 493-675. *The original GDD-based classification of wine-growing regions into five classes.*

### Terroir science and vine-climate interaction

- **van Leeuwen, C., Friant, P., Choné, X., Tregoat, O., Koundouras, S. and Dubourdieu, D. (2004).** Influence of climate, soil, and cultivar on terroir. *American Journal of Enology and Viticulture*, 55(3), 207-217. *Quantified the relative contribution of climate, soil, and cultivar to wine composition — essential framing for Paper B's Act 2 and Paper C.*

- **van Leeuwen, C. and Seguin, G. (2006).** The concept of terroir in viticulture. *Journal of Wine Research*, 17(1), 1-10. *Defines terroir as an interactive cultivated ecosystem, not just soil type.*

- **van Leeuwen, C., Destrac-Irvine, A., Dubernet, M., Duchêne, E., Gowdy, M., Marguerit, E., Pieri, P., Parker, A., de Rességuier, L. and Ollat, N. (2019).** An update on the impact of climate change in viticulture and potential adaptations. *Agronomy*, 9(9), 514. *Comprehensive review of adaptation strategies including variety switching — directly relevant to Paper A's replacement recommendations.*

- **van Leeuwen, C. et al. (2024).** Climate change impacts and adaptations of wine production. *Nature Reviews Earth and Environment*, 5, 258-275. *The definitive review. Identifies Central Europe as a potential warming beneficiary — Paper A's inverted-U trajectory tests this proposition.*

### Dense station networks in vineyards (direct methodological templates for Paper B)

- **de Rességuier, L., Mary, S., Le Roux, R., Laveau, C., Marchal, A., Ducournau, P. and van Leeuwen, C. (2020).** Temperature variability at local scale in the Bordeaux area. *Frontiers in Plant Science*, 11, 515. *90 sensors, up to 10 degrees C spatial amplitude in daily Tmin. The closest methodological analog to Paper B.*

- **Bois, B., Pauthier, B., Brillante, L., Mathieu, O., Leveque, J., Parker, A., Gaertner, S. and van Leeuwen, C. (2018).** Mapping bioclimatic indices by downscaling modelled monthly air temperature fields at high resolution. *OENO One*, 52(4), 291-306. *50 m resolution zoning via regression kriging with terrain covariates in Bordeaux. The spatial interpolation template for Act 1.*

- **Gavrilescu, C., Quénol, H., Bois, B. and Le Roux, R. (2018).** Fine-scale analysis of climate variability over Burgundy using MODIS LST and spatial interpolation. *E3S Web of Conferences*, 50, 01003. *64 stations, 75 m resolution, regression-kriging across 41,751 ha. Closest in scale to Tokaj's ~11,000 ha.*

- **Le Roux, R., de Rességuier, L., Corpetti, T., Jégou, N., Madelin, M., van Leeuwen, C. and Quénol, H. (2017).** Comparison of two fine-scale spatial models for mapping temperatures at the vineyard scale. *Agricultural and Forest Meteorology*, 247, 159-169. *Compared MLR vs SVR for vineyard temperature mapping — SVR proved superior for non-linear terrain-temperature relationships.*

### LIFE-ADVICLIM project (European-scale template)

- **Quénol, H. et al. (2017).** ADVICLIM: Adaptation of viticulture to climate change. *EGU General Assembly 2017*, EGU2017-18600. *Dense sensor networks across six European pilot sites including Cotnari, Romania — the closest published analog to Tokaj's continental climate and botrytised wine tradition.*

### Noble rot, botrytis, and disease modelling (Act 3 Part A)

- **Broome, J.C., English, J.T., Marois, J.J., Latorre, B.A. and Aviles, J.C. (1995).** Development of an infection model for *Botrytis cinerea* on grapevine based on wetness duration and temperature. *Phytopathology*, 85(1), 97-102. *Empirical model relating leaf wetness duration and temperature to botrytis infection probability.*

- **González-Domínguez, E., Caffi, T., Ciliberti, N. and Rossi, V. (2015).** A mechanistic model of *Botrytis cinerea* on grapevines that includes weather, vine growth stage, and the main infection pathways. *PLoS ONE*, 10(10), e0140444. *Mechanistic model suitable for spatial application across the station network.*

- **Molitor, D., Baus, O., Hoffmann, L. and Beyer, M. (2016).** Meteorological conditions determine the thermal-temporal position of the annual *Botrytis cinerea* infection risk window on *Vitis vinifera* L. cv. Riesling. *OENO One*, 50(4), 231-244. *Demonstrates the narrow meteorological window for noble rot development — relevant to mapping spatial variation in this window.*

- **Rossi, V., Caffi, T. and Salinari, F. (2012).** Helping farmers face the increasing complexity of decision-making for crop protection. *Phytopathologia Mediterranea*, 51(3), 457-479. *Review of decision support systems for disease management — contextualises the practical value of spatial disease risk mapping.*

### Frost risk and cold air drainage (Act 3 Part B)

- **Lundquist, J.D., Pepin, N. and Rochford, C. (2008).** Automated algorithm for mapping regions of cold-air pooling in complex terrain. *Journal of Geophysical Research*, 113, D22107. *Algorithm for identifying cold air pooling from DEM and temperature data — directly applicable to Tokaj's volcanic valleys.*

- **Kimura, K., Yoshida, H. and Toyoshima, Y. (2022).** Mapping spatial patterns of minimum air temperature using a cold flow accumulation algorithm and inversion strength indicators. *Agricultural and Forest Meteorology*, 329, 109260. *The most recent methodological advance for frost risk mapping in complex terrain.*

- **Leolini, L., Moriondo, M., Fila, G., Costafreda-Aumedes, S., Ferrise, R. and Bindi, M. (2018).** Late spring frost impacts on future grapevine distribution in Europe. *Field Crops Research*, 222, 197-208. *Continental-scale frost risk projections — provides context for Tokaj's frost exposure under climate change.*

### Phenology modelling

- **Parker, A., de Cortázar-Atauri, I.G., van Leeuwen, C. and Chuine, I. (2011).** General phenological model to characterise the timing of flowering and veraison of *Vitis vinifera* L. *Australian Journal of Grape and Wine Research*, 17(2), 206-216. *The GFV model. Not yet calibrated for Furmint or Hárslevelű — a clear publication gap.*

- **Parker, A., de Cortázar-Atauri, I.G., Chuine, I., Barbeau, G., Bois, B., Boursiquot, J.-M., Cahurel, J.-Y., Claverie, M., Dufourcq, T., Gény, L., Guimberteau, G., Hofmann, R.W., Jacquet, O., Lacombe, T., Monamy, C., Ojeda, H., Panigai, L., Payan, J.-C., Lovelle, B.R., Rouchaud, E., Schneider, C., Spring, J.-L., Storchi, P., Tomasi, D., Trambouze, W., Trought, M. and van Leeuwen, C. (2013).** Classification of varieties for their timing of flowering and veraison using a modelling approach. *Agricultural and Forest Meteorology*, 180, 249-264. *Extended the GFV model to 95+ cultivars.*

### Tokaj-specific research

- **Pásztor, L., Szabó, J., Bakacsi, Z., Mátéfi, T., Dobos, E. and Szatmári, G. (2015).** Elaboration and applications of spatial soil information systems and digital soil mapping at Research Institute for Soil Science and Agricultural Chemistry of the Hungarian Academy of Sciences. *Presented at EGU 2015*, EGU2015-12660. *The most comprehensive digital terroir map of Tokaj — LiDAR, hyperspectral, and soil at 25 m resolution. Paper C should build on this.*

- **Dobos, E., Seres, A. and Vadnai, P. (2016).** Application of regression kriging for mapping soil properties in the Tokaj wine region. *Proceedings of the Global Symposium on Soil Organic Carbon*. *Regression kriging for soil mapping in Tokaj — same geostatistical method used in Paper B for climate.*

- **Remenyik, J., Biró, B., Czeglédi, L., Paholcsek, M., Tóth, F., Urkon, M., Kovács, B., Balogh, K. and Varga, E. (2024).** Soil microbiome characterization of four historical dűlők (Betsek, Szent Tamás, Király, Nyulászó) in Mád. *PLoS ONE*. *Microbiome data for the same vineyards where we have stations — potential integration in Paper C.*

- **Keve, G., Rácz, C. and Nagy, J. (2024).** Analysis of drought periods in the Tokaj wine region using Markov chains. *Progress in Agricultural Engineering Sciences*. *Drought analysis using OMSZ data 2002-2020 — provides historical water stress context.*

- **Lakatos, L. and Nagy, J. (2025).** Climate change impacts on Hungarian viticulture. *Frontiers in Plant Science*, DOI: 10.3389/fpls.2025.1481431. *The most-cited paper across the Bor-szőlő research corpus. National-scale analysis that Paper A should compare against.*

### Climate change projections and adaptation

- **Hannah, L., Roehrdanz, P.R., Ikegami, M., Shepard, A.V., Shaw, M.R., Tabor, G., Zhi, L., Marquet, P.A. and Hijmans, R.J. (2013).** Climate change, wine, and conservation. *PNAS*, 110(17), 6907-6912. *Projected 25-73% loss of wine-growing area by 2050 — Paper A's national results contextualise Hungary within this global picture.*

- **Morales-Castilla, I., García de Cortázar-Atauri, I., Cook, B.I., Lacombe, T., Parker, A., van Leeuwen, C., Nicholas, K.A. and Wolkovich, E.M. (2020).** Diversity buffers winegrowing regions from climate change losses. *PNAS*, 117(6), 2864-2869. *Cultivar diversity can buffer 56% of projected losses — directly supports Paper A's variety replacement modelling.*

- **Santos, J.A., Fraga, H., Malheiro, A.C., Moutinho-Pereira, J., Dinis, L.-T., Correia, C., Moriondo, M., Leolini, L., Dibari, C., Costafreda-Aumedes, S., Kartschall, T., Menz, C., Molitor, D., Junk, J., Beez, M. and Schultz, H.R. (2020).** A review of the potential climate change impacts and adaptation options for European viticulture. *Applied Sciences*, 10(9), 3092. *European review — Paper A contributes the first comprehensive Hungarian dataset to this literature.*

- **Kern, A., Marjanović, H. and Barcza, Z. (2024).** The FORESEE-HUN dataset: high-resolution gridded climate data for Hungary. *Climate Services*. *Description of the gridded product used in Paper A and compared against in Paper B.*

### Gridded product validation (contextual for Act 1)

- **Vanella, D., Longo-Minnolo, G., Ferretti, L., Ferruzza, G., Ferraro, V. and Pumo, D. (2022).** Comparison of ERA5 and ground-based observations of temperature and precipitation in Italy. *Journal of Hydrology: Regional Studies*. *Temperature RMSE of 2-4 degrees C in mountain terrain — Tokaj's terrain likely in this range.*

### Water balance and drought (contextual for Paper C)

- **Hofmann, M., Lardschneider, E., Stöckl, R., Rach, D. and Schultz, H.R. (2022).** A plot-scale vineyard water balance model for the assessment of water availability and water footprint. *Earth System Dynamics*. *Integrates DEM, soil maps, and station data — template for Paper C's water balance component.*

- **Allen, R.G., Pereira, L.S., Raes, D. and Smith, M. (1998).** Crop evapotranspiration: Guidelines for computing crop water requirements. *FAO Irrigation and Drainage Paper No. 56.* *The ET0 computation standard.*

### Data quality control

- **Estévez, J., Gavilán, P. and Giráldez, J.V. (2011).** Guidelines on validation procedures for meteorological data from automatic weather stations. *Journal of Hydrology*, 402, 144-154. *QC pipeline template for the 50-station network.*

---

## Appendix: What changed from v1 to v2

The original plan (v1, `00-initial analysis.md`) was structured around seven independent research directions and five separate manuscripts, written from a GIS/geostatistics perspective. This v2 plan makes four key changes:

1. **Viticulture-first framing.** Research questions now lead with what matters for the grower and the grape, not with the spatial method. Regression-kriging, PCA, and GEV distributions appear in methodology sections as tools, not as headlines.

2. **Three papers, not five.** The consolidated Paper B (three acts in one comprehensive paper) is stronger than three separate fragmented manuscripts. The national atlas (Paper A) and multi-layer terroir (Paper C) complete the PhD arc.

3. **Coherent thesis structure.** Macro (country) to meso (district) to micro (parcel) — each paper motivates the next.

4. **Realistic timeline.** Paper A can submit in 2026 (data complete). Paper B targets early 2027 (one full growing season analysis). Paper C requires 2-3 field seasons and targets 2028-2029.
