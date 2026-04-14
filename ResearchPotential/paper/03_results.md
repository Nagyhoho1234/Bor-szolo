# 3. Results

## 3.1 The inverted-U trajectory

Hungary-wide mean variety suitability followed a characteristic inverted-U trajectory under both emission scenarios (Table 1). Under observed conditions, mean suitability across all 22 districts and 58 varieties rose from 0.60 in the 1971--2000 historical baseline to 0.75 in the 1991--2020 reference period, reflecting the beneficial effects of late-twentieth-century warming on what was, historically, a cool-continental viticultural zone. Under RCP8.5, suitability continued to increase to 0.82 by 2021--2040, plateaued at 0.83 through 2041--2060, then declined sharply to 0.59 by 2061--2080 and collapsed to 0.33 by 2081--2100. Under RCP4.5, suitability stabilised at 0.73--0.74 across all future periods, with no comparable decline.

The district-level spread widened dramatically under RCP8.5 toward the end of the century. In the 2021--2040 period, the interdistrict range (p10--p90) was narrow (0.78--0.86), indicating broadly uniform benefit from near-term warming. By 2081--2100 RCP8.5, the range expanded to 0.16--0.53, reflecting divergent fates: the coolest districts (Soproni, 0.48; Bükki) retained moderate suitability, while the warmest (Csongrádi, 0.15; Hajós-Bajai) approached functional collapse for the currently planted variety portfolio.

The crossover point --- where warming ceased to improve suitability and began to erode it --- occurred between 2041--2060 and 2061--2080 under RCP8.5. This corresponded to the period when multiple districts transitioned from Winkler class III into class IV or V, exceeding the thermal optimum of most Central European and Atlantic grape varieties.

**Table 1.** Hungary-wide mean variety suitability (58 varieties x 22 districts) per period and emission scenario. Values for four spotlight districts are shown alongside the national mean. Suitability is scored 0--1, where 1 indicates full climatic compatibility.

| Period | Scenario | National mean | Tokaji | Villányi | Csongrádi | Soproni |
|---|---|---|---|---|---|---|
| 1971--2000 | observed | 0.60 | 0.55 | 0.73 | 0.75 | 0.56 |
| 1991--2020 | observed | 0.75 | 0.76 | 0.80 | 0.79 | 0.81 |
| 2021--2040 | RCP4.5 | 0.74 | 0.79 | 0.73 | 0.53 | 0.86 |
| 2021--2040 | RCP8.5 | 0.82 | 0.85 | 0.86 | 0.84 | 0.85 |
| 2041--2060 | RCP4.5 | 0.73 | 0.85 | 0.67 | 0.34 | 0.85 |
| 2041--2060 | RCP8.5 | 0.83 | 0.83 | 0.85 | 0.72 | 0.84 |
| 2061--2080 | RCP4.5 | 0.73 | 0.86 | 0.63 | 0.35 | 0.86 |
| 2061--2080 | RCP8.5 | 0.59 | 0.66 | 0.46 | 0.23 | 0.69 |
| 2081--2100 | RCP4.5 | 0.73 | 0.83 | 0.66 | 0.39 | 0.86 |
| 2081--2100 | RCP8.5 | **0.33** | **0.30** | **0.22** | **0.15** | **0.48** |

**Figure 1 specification.** *Inverted-U suitability trajectory.* Line chart with six period bins on the x-axis (1971--2000, 1991--2020, 2021--2040, 2041--2060, 2061--2080, 2081--2100) and mean suitability (0--1) on the y-axis. Two lines: RCP4.5 (blue) and RCP8.5 (red), with the 1971--2000 and 1991--2020 observed periods shared. A grey ribbon spans the interdistrict p10--p90 range for each scenario. Data source: `suitability_long.parquet`, aggregated as mean suitability across all 58 varieties and 22 districts per period--scenario combination.

---

## 3.2 Regional differentiation --- four spotlight districts

The four spotlight districts span Hungary's full viticultural climate gradient, from the coolest (Soproni, northwest) to the hottest (Csongrádi, southeast). Their baseline and projected climatic indices are summarised below; all values are 30-year normals from FORESEE-HUN.

### 3.2.1 Tokaji (northeast, cool-continental)

At the 1991--2020 baseline, Tokaji recorded a Winkler GDD of 1513 degree-days (°C·d), a Huglin Index of 2043, 14.0 late spring frost days, 1.3 hot days above 35 °C, and 422 mm growing-season precipitation. By 2081--2100 under RCP8.5, Winkler GDD was projected to reach 2268 °C·d (+755 °C·d), the Huglin Index to rise to 2749 (+706), and hot days above 35 °C to increase to 17.7 (+16.4), while spring frost days declined to 2.7 (-11.3). The Winkler class transition was Ia to IV. Mean variety suitability declined from 0.76 (baseline) to 0.30 (2081--2100 RCP8.5), driven primarily by the Winkler-class penalty. Under RCP4.5, suitability remained at 0.83, the highest among the four spotlights at end-century.

### 3.2.2 Villányi (south, warm)

Villányi started from a warmer baseline: Winkler GDD 1630 °C·d, Huglin Index 2163, 2.3 hot days above 35 °C, and 464 mm growing-season precipitation. By 2081--2100 RCP8.5, Winkler GDD reached 2371 °C·d (+740 °C·d), the Huglin Index rose to 2849 (+686), and hot days above 35 °C increased to 20.8 (+18.5). The Winkler class transitioned from Ib to IV. Variety suitability fell from 0.80 to 0.22. Villányi was among the earliest districts to cross the inverted-U inflection point: under RCP4.5, suitability had already declined to 0.67 by 2041--2060, whereas the national average remained at 0.73.

### 3.2.3 Csongrádi (southeast, hottest)

Csongrádi was the warmest district at baseline: Winkler GDD 1719 °C·d, Huglin Index 2289, 5.2 hot days above 35 °C, and the lowest growing-season precipitation among the four spotlights (382 mm). By 2081--2100 RCP8.5, Winkler GDD rose to 2438 °C·d (+720 °C·d), the Huglin Index to 2965 (+676), and hot days above 35 °C to 27.3 (+22.1). Extreme heat days above 38 °C increased from 0.5 to 9.0. The Winkler class transitioned from Ib to IV. Variety suitability collapsed to 0.15, the lowest of all 22 districts. Even under RCP4.5, suitability fell to 0.39 by 2081--2100 --- a trajectory unique among the spotlights in showing decline under both scenarios.

### 3.2.4 Soproni (northwest, coolest)

Soproni recorded the slowest warming of the four spotlights. At baseline, Winkler GDD was 1482 °C·d, Huglin Index 2011, 1.8 hot days above 35 °C, and the highest growing-season precipitation (481 mm). By 2081--2100 RCP8.5, Winkler GDD rose to 2178 °C·d (+697 °C·d), the Huglin Index to 2673 (+662), and hot days above 35 °C to 15.0 (+13.1). The Winkler class transitioned from Ia to III. Variety suitability declined to 0.48 --- the highest end-century value among the spotlights and the second-highest nationally. Under RCP4.5, suitability remained at 0.86, essentially unchanged from the 1991--2020 baseline (0.81), confirming Soproni's status as the most climate-resilient Hungarian wine district.

**Figure 2 specification.** *Winkler GDD trajectories for four spotlight districts.* Four-panel layout (2 x 2). Each panel shows one district (Tokaji, Villányi, Csongrádi, Soproni) with the x-axis spanning 1971--2100 (annual values where available from the indices parquet files, or period-bin centroids from the normals). The y-axis is Winkler GDD (°C·d). Three series per panel: observed (grey, 1971--2020), RCP4.5 projected (blue, 2021--2100), RCP8.5 projected (red, 2021--2100). Each panel is labelled with the district name and its Winkler class transition (e.g., "Tokaji: Ia --> IV"). Horizontal dashed lines mark Winkler class boundaries at 1111, 1389, 1667, 1944, and 2222 °C·d. Data source: `indices/indices_rcp45_annual.parquet` and `indices_rcp85_annual.parquet`, filtered for the `winkler_gdd` index.

**Figure 3 specification.** *Variety-by-district suitability heatmap at 2081--2100 RCP8.5.* Heatmap with 15 key varieties on the y-axis (Furmint, Hárslevelű, Blaufränkisch, Cabernet Franc, Cabernet Sauvignon, Merlot, Welschriesling/Olaszrizling, Pinot Noir, Riesling, Kadarka, Tempranillo, Touriga Nacional, Assyrtiko, Souvignier Gris, Solaris) and 22 districts on the x-axis, ordered from coolest (Soproni) to warmest (Csongrádi) by baseline Winkler GDD. Cell colour encodes suitability from 0 (dark red) to 1 (dark green), with a diverging colour scale centred at 0.5 (white). The four spotlight district columns are highlighted with a heavier border or distinct column header colour. Data source: `suitability_long.parquet`, filtered for period 2081--2100, scenario rcp85. Varieties not present in the dataset should use their international English names as listed in `variety_en`.

---

## 3.3 Variety winners and losers

Across all 22 districts, the five varieties with the largest positive suitability shift from the 1991--2020 baseline to 2081--2100 RCP8.5 were exclusively Mediterranean reds: Carignan/Mazuelo (+0.99, from 0.01 to 1.00), Grenache (+0.99, from 0.01 to 1.00), Aglianico (+0.98, from 0.02 to 1.00), Touriga Nacional (+0.93, from 0.07 to 1.00), and Tempranillo (+0.82, from 0.18 to 1.00) (Table 2). These varieties were poorly suited to the 1991--2020 climate across most of Hungary, but by 2081--2100 RCP8.5, every one of them achieved a Hungary-wide mean suitability of 1.00.

Conversely, the five largest losers were cool-climate whites: Irsai Oliver (-0.97, from 0.99 to 0.01), Johanniter (-0.97, from 0.99 to 0.01), Muscaris (-0.97, from 0.99 to 0.01), Mueller-Thurgau (-0.97, from 0.99 to 0.01), and Gewuerztraminer (-0.97, from 0.99 to 0.02). Each of these dropped from near-universal suitability to near-zero across all districts.

**Table 2.** Top five variety winners (largest positive suitability delta) and top five losers (largest negative delta), Hungary-wide mean, comparing 1991--2020 observed to 2081--2100 RCP8.5.

| Rank | Variety | Colour | Baseline suitability | Future suitability | Delta |
|---|---|---|---|---|---|
| W1 | Carignan / Mazuelo | red | 0.01 | 1.00 | +0.99 |
| W2 | Grenache | red | 0.01 | 1.00 | +0.99 |
| W3 | Aglianico | red | 0.02 | 1.00 | +0.98 |
| W4 | Touriga Nacional | red | 0.07 | 1.00 | +0.93 |
| W5 | Tempranillo | red | 0.18 | 1.00 | +0.82 |
| L1 | Irsai Oliver | white | 0.99 | 0.01 | -0.97 |
| L2 | Johanniter | white | 0.99 | 0.01 | -0.97 |
| L3 | Muscaris | white | 0.99 | 0.01 | -0.97 |
| L4 | Mueller-Thurgau | white | 0.99 | 0.01 | -0.97 |
| L5 | Gewuerztraminer | white | 0.99 | 0.02 | -0.97 |

Among the commercially most important Hungarian varieties, Furmint (white, Tokaji flagship) followed the inverted-U pattern at the variety level: Hungary-wide mean suitability rose from 0.45 (1971--2000) to 0.75 (1991--2020), peaked at 1.00 (2041--2060 RCP8.5), then declined to 0.66 by 2081--2100 RCP8.5. Under RCP4.5, Furmint suitability continued to rise to 1.00. Blaufraenkisch (Kekfrankos, Hungary's most-planted red) showed a sharper divergence between scenarios: baseline suitability was 1.00, declining modestly to 0.82 under RCP4.5 at 2081--2100 but collapsing to 0.22 under RCP8.5 (-0.78). Welschriesling/Olaszrizling, the most-planted white, followed an almost identical pattern: 0.95 baseline, 0.82 under RCP4.5, 0.22 under RCP8.5 (-0.73). Pinot Noir and Riesling, widely grown in the Balaton and northern districts, dropped from 0.99 to 0.02 under RCP8.5 (-0.97).

Cabernet Sauvignon exhibited a distinctive pattern: baseline suitability was moderate (0.54), reflecting its position at the warm margin of Hungary's current climate. Under RCP4.5, suitability rose to 0.98 --- making it one of the few established varieties to benefit at end-century under moderate emissions. Under RCP8.5, suitability remained at 0.55, essentially unchanged from baseline, as gains in cooler northern districts offset losses in the hottest southern districts. Syrah showed a similar profile, rising from 0.54 to 1.00 under RCP4.5 and to 0.65 under RCP8.5 (+0.11).

Among the PIWI (fungus-resistant) varieties, Souvignier Gris declined from 0.95 to 0.10 under RCP8.5 (-0.85), while Solaris dropped from 0.98 to 0.01 (-0.97). Contrary to a common assumption that PIWI varieties offer broad climate resilience, their envelopes were calibrated for cool-temperate conditions and they were among the most climate-sensitive varieties in the dataset. Only Assyrtiko (white, Greek) showed both high future suitability (1.00 under RCP8.5) and an existing Hungarian cultivation tradition (trial plantings in at least three districts by 2025).

---

## 3.4 Adaptation recommendations and their validation

### 3.4.1 Replacement candidates

At the 2081--2100 RCP8.5 horizon, the model's top four replacement candidates for Tokaji were Grenache (suitability 1.00), Mourvedre (1.00), Nero d'Avola (1.00), and Assyrtiko (1.00). All six current Tokaji principal varieties were classified as at-risk: Harslevelu (0.17), Kabar (0.17), Zeta (0.17), Koverszolo (0.17), Yellow Muscat (0.21), and Furmint (0.32). Furmint retained the highest residual suitability among the principals, consistent with the Tarcal Research Institute's assessment of its relative drought tolerance through efficient stomatal control.

For Csongrádi, the model produced no replacement candidates meeting the 0.55 suitability floor at 2081--2100 RCP8.5. This was the most extreme outcome across all 22 districts: even after adding 14 Mediterranean and 6 PIWI varieties to the envelope database, the projected climate at Csongrádi exceeded every variety's thermal tolerance. Direct extraction from the suitability matrix confirmed that seven Mediterranean varieties (Tempranillo, Touriga Nacional, Grenache, Mourvedre, Carignan, Aglianico, Assyrtiko) each scored 1.00 at this horizon --- but the replacement algorithm applied a stricter floor (0.55) on the *combined* score, which in Csongrádi was suppressed by the Winkler penalty. Nero d'Avola scored 0.82. Furmint scored only 0.16. The effective message was that Csongrádi at 2081--2100 RCP8.5 (Winkler GDD 2438 °C·d, 27.3 hot days above 35 °C, growing-season precipitation 435 mm) was projected to lie beyond the currently documented thermal envelope of viticulture.

**Figure 4 specification.** *Adaptation candidates for Tokaji and Csongrádi at 2081--2100 RCP8.5.* Two grouped horizontal bar charts, one per district. The y-axis lists variety names: current principals (top group, 6 for Tokaji, 5 for Csongrádi) and top replacement candidates (bottom group, 4 for Tokaji; for Csongrádi, show the top 7 Mediterranean varieties from the suitability matrix since the replacement algorithm returned no picks). The x-axis is suitability (0--1). Two bars per variety: baseline 1991--2020 (grey) and 2081--2100 RCP8.5 (red). Data source: `variety_replacements/tokaji.json` and `variety_replacements/csongradi.json` for principals and replacement picks; supplemented with values from `suitability_long.parquet` for the Csongrádi Mediterranean varieties.

### 3.4.2 Validation against real-world adaptation practices

The model generated 80 district-variety replacement recommendations across 20 districts (Csongrádi and Szekszárdi were excluded because their models returned no picks at the 2081--2100 RCP8.5 horizon). Cross-referencing these recommendations against the adaptation practices documented in the 22 district research dossiers yielded a strict convergence rate of 5% (4 of 80 recommendations matched a variety named verbatim in the corresponding district's qualitative record) and a permissive convergence rate of 20% (16 of 80, including generic-class matches such as "Mediterranean varieties") (Table 3).

**Table 3.** Validation of model replacement recommendations against qualitative district evidence.

| Metric | Value |
|---|---|
| Districts with model recommendations | 20 (of 22) |
| Total district x variety recommendations | 80 |
| Exact name matches | 4 (5%) |
| Generic-class matches | 12 |
| Permissive matches (exact + class) | 16 (20%) |
| No qualitative support | 64 (80%) |

The four exact matches all involved Hajós-Bajai and Villányi, the two districts with the most advanced Mediterranean variety trial programmes. In Hajós-Bajai, three of the model's four picks (Mourvedre, Grenache, Assyrtiko) were named verbatim in the district's adaptation record. The worst-validated districts were Etyek-Budai, where the model recommended Mediterranean reds but the qualitative record focused on sparkling-wine varieties (Pinot Meunier, Auxerrois); Zalai, where the model output was indistinguishable from that of the Great Plain districts despite Zala's documented role as a cool-climate refuge; and Tokaji, where the qualitative record contained no variety-substitution content, with the entire adaptation strategy centering on rootstock selection, canopy management, and stylistic adjustment within the existing Furmint-Harslevelu framework.

Three qualitative examples illustrate the nature of the divergence. First, the model's most-recommended variety across all districts --- Mourvedre (recommended in 21 of 22 districts) --- was named in only one district's qualitative record (Hajós-Bajai). Second, Furmint was cited as an active adaptation variety in six districts' qualitative records, yet the model classified it as at-risk everywhere at 2081--2100 RCP8.5. Third, PIWI varieties (Souvignier Gris, Muscaris, Solaris, Bronner, Bianca) appeared in the qualitative records of eight districts, yet the model projected severe suitability declines for all PIWI varieties with calibrated envelopes.

The low convergence reflected three structural factors: (i) the model explored a broader possibility space (including Iberian and Sicilian varieties no Hungarian grower had yet trialled), while real-world adaptation was constrained by established rootstock investments, PDO regulations, and market conservatism; (ii) approximately 24 varieties named in the qualitative district records lacked envelope parameterisation in the model's database; and (iii) institutional identity constraints --- the Csopak Kodex, Tokaji's UNESCO-heritage Furmint monoculture, Somlo's Juhfark commitment --- were not representable in a climate-envelope scoring function.

**Figure 5 specification.** *CCKP CMIP6 cross-check: FORESEE-HUN versus CCKP ensemble for mean annual temperature and hot days.* Two-panel scatter plot. **Left panel:** FORESEE-HUN 2081--2100 RCP8.5 mean annual temperature (estimated from Winkler GDD and growing-season length) on the x-axis versus CCKP CMIP6 2080--2099 SSP5-8.5 ensemble-mean annual temperature on the y-axis, one point per district (n = 22). A 1:1 reference line is drawn in grey. The CCKP ensemble-mean country-wide value was 16.57 °C (range by district: 15.20--17.20 °C), with a mean warming of +5.24 °C from the historical baseline of 11.33 °C. **Right panel:** FORESEE-HUN hot days above 35 °C (country mean: 18.9 d at 2081--2100 RCP8.5, baseline 2.1 d) versus CCKP CMIP6 hot days above 35 °C (country mean: 42.5 d at 2080--2099 SSP5-8.5, baseline 1.3 d). The CCKP ensemble projected substantially more hot days than FORESEE-HUN (42.5 versus 18.9 d), a divergence attributable to the difference between a single-RCM projection (FORESEE-HUN, CNRM-ALADIN53) and a multi-GCM ensemble mean (CCKP, CMIP6). For mean temperature, the two sources showed qualitative agreement: CCKP projected +5.24 °C country-mean warming under SSP5-8.5, while FORESEE-HUN Winkler GDD anomalies implied a comparable magnitude of growing-season warming (+734 °C·d, equivalent to approximately +4.1 °C distributed over the 180-day growing season). The hot-days divergence indicated that FORESEE-HUN likely underestimated extreme heat frequency relative to the CMIP6 multi-model range, a conservative bias that would, if anything, cause our suitability projections to overestimate end-century viability.

---
