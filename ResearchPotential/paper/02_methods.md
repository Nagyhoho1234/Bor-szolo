## 2. Materials and Methods

### 2.1 Study area and wine-district delineation

Hungary's legally defined wine-growing territory comprises 22 wine districts (*borvidék*), spanning a latitude range of approximately 46.0–48.6°N and a climate gradient from the cool, Atlantic-influenced northwest (Sopron) to the hot, continental southeast (Csongrád). The 22 districts were delineated from OpenStreetMap administrative-level-8 polygons (3,174 settlement units, EPSG:3785 Web Mercator projection). Of these, 618 settlements carrying an official wine-district designation were manually attributed with a *Borvidek* field, then dissolved into 22 multi-polygon districts covering a combined area of 25,254 km².

Climate variables were extracted using area-weighted polygon means rather than centroid point sampling. A precomputed weight matrix **W** of dimensions 22 × *n*_grid was constructed, where each element *w*_ij records the fractional overlap between wine district *i* and FORESEE-HUN grid cell *j*. For each daily climate field, the district-level value was computed as the dot product of the weight vector and the gridded field. This approach avoids the representativeness bias inherent in single-point extraction, particularly for districts with irregular shapes or strong internal elevation gradients (e.g., the Bükk foothills in Egri or the Balaton littoral districts).

Lakatos and Nagy (2025) independently analysed the same 22 wine districts using the FORESEE-HUN dataset, but extracted climate values at district centroids. Our area-weighted extraction yields qualitatively similar index trajectories but slightly different baseline magnitudes, particularly for spatially heterogeneous districts.

### 2.2 Climate data

Three climate datasets were used, serving complementary roles as primary projection, independent ensemble validation, and observational credibility anchor.

**FORESEE-HUN** (Kern et al., 2024) is a daily gridded climate dataset for Hungary at 0.1° × 0.1° spatial resolution. The observed component (version 1.1, 1971–2022) provides seven variables: daily maximum temperature (Tmax), daily minimum temperature (Tmin), precipitation (pr), daily mean dew-point temperature (Tdmean), vapour pressure deficit (VPD), global radiation, and day length. The projected component (version 1.0, 2022–2100) was generated from the CNRM-ALADIN53 regional climate model, one of 14 EURO-CORDEX RCMs available in the full FORESEE-HUN archive. Projections are bias-corrected against the HUCLIM national reference climatology and are available under Representative Concentration Pathways RCP4.5 and RCP8.5. The projected fields provide three variables: daily maximum temperature (tasmax), daily minimum temperature (tasmin), and precipitation (pr). Time series were stitched by using the observed record through 31 December 2021, then the RCP projections from 1 January 2022, with no offset correction required because the projected fields are already bias-corrected against the observed baseline. We note that newer FORESEE-HUN releases (versions 1.2 and 1.3) extend the observed period to approximately 2024, but the projected fields are derived from the same EURO-CORDEX experiments and are numerically identical.

A key limitation is our use of a single RCM member (CNRM-ALADIN53) rather than the full 14-member EURO-CORDEX ensemble available in FORESEE-HUN. This choice was made for computational tractability and was partly mitigated by the independent multi-model cross-check described below.

**World Bank Climate Change Knowledge Portal (CCKP) CMIP6 data** (World Bank, 2024; available at worldbank.github.io/climateknowledgeportal) provided a multi-model ensemble validation layer at 0.25° resolution. We extracted ensemble mean, 10th-percentile, and 90th-percentile values for 14 variables: mean temperature (tas), maximum temperature (tasmax), minimum temperature (tasmin), precipitation (pr), hot days above 35°C (hd35), maximum of daily maximum temperature (txx), minimum of daily minimum temperature (tnn), frost days (fd), growing season length (gsl), maximum 1-day precipitation (rx1day), maximum 5-day precipitation (rx5day), consecutive dry days (cdd), consecutive wet days (cwd), and heavy precipitation days above 20 mm (r20mm). Data were available for three time slices — 1995–2014 (historical), 2040–2059 (mid-century), and 2080–2099 (end-century) — under Shared Socioeconomic Pathways SSP2-4.5 and SSP5-8.5. The CCKP data served exclusively as an independent validation layer to assess whether the single-RCM FORESEE-HUN trajectories fall within the multi-model ensemble range; they were not used as primary projections.

**HungaroMet station observations** (Hungarian Meteorological Service, open data portal odp.met.hu; CC-BY-SA licence) provided actual measured annual mean temperature and total precipitation from 21 stations nearest to district centroids (mean station-to-centroid distance: 9.6 km), covering the period 2020–2024. These served as a credibility anchor, confirming that the FORESEE-HUN observed baseline is consistent with recent ground-truth measurements.

All analyses were conducted over six temporal bins: 1971–2000 (historical baseline), 1991–2020 (reference baseline for anomaly computation), and four 20-year future periods — 2021–2040, 2041–2060, 2061–2080, and 2081–2100 — under both RCP4.5 and RCP8.5.

### 2.3 Viticultural climate indices

Nine viticultural climate indices were computed from the FORESEE-HUN daily fields for each district and each year. All indices were subsequently averaged over the temporal bins defined above to produce period normals.

**1. Winkler growing degree-days (GDD).** The Winkler index (Winkler et al., 1974) accumulates thermal units above a 10°C base temperature over the growing season (1 April – 31 October): GDD = sum of max(0, Tmean - 10) for each day in the window, where Tmean = (Tmax + Tmin) / 2. Districts were classified into Winkler regions Ia (<1,389 °C-days), Ib (1,389–1,667), II (1,667–1,944), III (1,944–2,222), IV (2,222–2,500), and V (>2,500 °C-days).

**2. Huglin heliothermal index (HI).** The Huglin index (Huglin, 1978; Tonietto and Carbonneau, 2004) integrates both mean and maximum temperatures over 1 April – 30 September with a latitude-dependent day-length correction: HI = sum of [max(0, ((Tmean - 10) + (Tmax - 10)) / 2) × K(phi)] for each day, where K(phi) is a latitude correction factor interpolated linearly between published anchor values (K = 1.02 at 40°N, 1.03 at 44°N, 1.04 at 46°N, 1.05 at 48°N, 1.06 at 50°N). For the Hungarian wine districts (approximately 46–48.5°N), K ranges from 1.04 to 1.05.

**3. Late spring frost days.** The count of days with Tmin < 0°C during the post-dormancy window of 1 March – 31 May, capturing the risk of frost damage to emerged buds and young shoots.

**4. Last spring frost day-of-year.** The latest calendar day (expressed as day-of-year) on which Tmin < 0°C occurred within the 1 January – 15 June window, indicating the frost-free date relevant to phenological safety.

**5. Hot days (>35°C).** The count of summer days (1 June – 31 August) with Tmax exceeding 35°C, a threshold associated with photosynthetic shutdown, berry sunburn, and accelerated sugar accumulation in grapevines.

**6. Extreme heat days (>38°C).** As above but with a 38°C threshold, representing conditions under which even heat-adapted cultivars may experience irreversible physiological damage.

**7. Growing-season precipitation.** Total precipitation accumulated over 1 April – 31 October (mm), matching the Winkler integration window.

**8. Hargreaves reference evapotranspiration (ET0) and precipitation–evapotranspiration balance (P − PET).** Reference ET0 was estimated using the Hargreaves–Samani equation (Hargreaves and Samani, 1985): ET0 = 0.0023 × (Tmean + 17.8) × (Tmax - Tmin)^0.5 × Ra, where Ra is extraterrestrial radiation computed as a function of latitude and day-of-year following FAO Irrigation and Drainage Paper 56 (Allen et al., 1998), expressed in mm day⁻¹ water equivalent (MJ m⁻² day⁻¹ divided by 2.45). ET0 was accumulated over the growing season (1 April – 31 October), and the drought balance was computed as P − PET. The Hargreaves method was chosen over the more physically complete Penman–Monteith equation because the FORESEE-HUN projected fields provide only temperature and precipitation; the humidity, radiation, and wind-speed inputs required by Penman–Monteith are available in the observed record but not in the RCM projections.

**9. Cool Night Index (CI).** The mean September minimum temperature (Tonietto and Carbonneau, 2004), an indicator of nocturnal thermal amplitude during the ripening period that influences aromatic compound preservation, particularly in white and aromatic grape varieties.

### 2.4 Variety-suitability scoring

A climate-envelope suitability score was computed for each combination of grape variety, wine district, time period, and emissions scenario. The variety pool comprised 58 cultivars: 38 Hungarian and Central European varieties traditionally grown in the 22 districts (including Furmint, Hárslevelű, Olaszrizling, Kékfrankos, Kadarka, Cabernet Franc, and others); 14 Mediterranean additions representing warm-climate candidates that may become viable under future warming (Tempranillo, Touriga Nacional, Garnacha, Mourvèdre, Carignan, Aglianico, Nero d'Avola, Sangiovese, Vermentino, Assyrtiko, Fiano, Verdejo, and Albariño); and 6 disease-resistant interspecific hybrid (PIWI) varieties from the Freiburg and Geilweilerhof breeding programmes (Solaris, Bronner, Johanniter, Muscaris, Souvignier Gris, and Cabernet Cortis).

For each variety, a climate envelope was defined by four parameters: a Huglin index range (minimum, optimal-low, optimal-high, maximum), a Winkler class range (minimum class, maximum class), a frost tolerance threshold (days), and a heat tolerance threshold (days). Envelope parameters were calibrated from published viticulture references: Tonietto and Carbonneau (2004) for the Huglin and Winkler classification of internationally studied varieties; the Hungarian Wine Marketing Agency variety profiles for Hungarian-specific cultivars; OIV (International Organisation of Vine and Wine) descriptor sheets for widely grown international varieties; and breeding programme documentation from the Freiburg and Geilweilerhof institutes for PIWI cultivars. Confidence levels (high, medium, low) were assigned to each envelope based on the availability and consistency of published data.

The composite suitability score S for variety *v* in district *d* at period *t* under scenario *s* was computed as the product of four sub-scores, each bounded in [0, 1]:

S(v, d, t, s) = H_score × W_score × F_penalty × T_penalty

where:

*Huglin trapezoidal score (H_score):* A trapezoidal membership function over the Huglin index. H_score = 0 when the district's mean Huglin value falls below huglin_min or above huglin_max; H_score ramps linearly from 0 to 1 between huglin_min and huglin_opt_low and from 1 to 0 between huglin_opt_high and huglin_max; H_score = 1.0 within the optimal plateau [huglin_opt_low, huglin_opt_high].

*Winkler soft penalty (W_score):* W_score = 1.0 when the district's Winkler class falls within [winkler_class_min, winkler_class_max]. Outside this range, W_score decays linearly as W_score = max(0, 1 - gap / 4), where gap is the number of Winkler classes by which the district deviates from the nearest boundary of the acceptable range. A variety thus reaches zero suitability only at four classes off, reflecting the empirical observation that cultivars can grow beyond their classical optimal Winkler class with quality changes rather than outright failure.

*Frost penalty (F_penalty):* F_penalty = 1 - min(1, max(0, (frost_days - tolerance) / tolerance)), where frost_days is the district's mean late-spring-frost-day count and tolerance is the variety's frost_tolerance_days parameter. A variety experiencing frost days equal to its tolerance threshold receives a penalty of 0.5; double the tolerance yields a penalty of 1.0 (F_penalty = 0).

*Heat penalty (T_penalty):* Computed identically to the frost penalty but using hot days (>35°C) and the variety's heat_tolerance_days parameter.

The composite score S therefore lies in [0, 1], where 1.0 represents a variety within its optimal Huglin and Winkler range with no frost or heat stress, and 0.0 indicates complete climate unsuitability on at least one axis. For each district and future period, varieties were ranked by suitability to identify adaptation candidates — specifically, varieties not currently among the district's principal cultivars but scoring above a suitability floor (0.55) under future conditions.

We acknowledge that this scoring approach is a simplified envelope match, not a process-based crop model. It captures the first-order climate signal — the thermal and stress requirements of each variety — but cannot represent phenological shifts, soil effects, rootstock interactions, disease pressure, microclimate variation below the 0.1° grid resolution, or vineyard management practices. It is designed as a horizon-scanning tool, not a planting prescription.

### 2.5 Validation against real-world adaptation

To assess the ecological plausibility of the model's recommendations, we cross-referenced them against documented adaptation practices already underway in Hungarian wine districts. For each of the 22 districts, a research dossier was compiled from peer-reviewed literature, government reports (NÉBIH, HungaroMet), trade press, producer communications, and Protected Designation of Origin (PDO) regulatory documents. Each dossier contains a dedicated section (§12, "Adaptation already underway") documenting which grape varieties growers are currently planting, trialling, or publicly discussing as climate-adaptation responses.

Validation proceeded as follows. For each district, the model's top four replacement candidates — defined as varieties not currently among the district's principal cultivars, ranked by suitability score at 2081–2100 under RCP8.5 — were compared against the set of varieties mentioned in the corresponding §12 section. Two convergence metrics were computed across the 22 districts:

*Strict overlap:* the fraction of district × variety pairs in which a model top-four pick appeared by exact name in the district's §12 qualitative record. Across the 20 districts for which the model produced at least one recommendation above the 0.55 suitability floor (Csongrád and Szekszárd fell below this threshold for all varieties), four exact name matches were identified (three in Hajós-Baja — Mourvèdre, Garnacha, and Assyrtiko — and one in Villány — Grenache/Garnacha), yielding a strict convergence rate of 4/80 = 5%.

*Permissive overlap:* including cases where the §12 text endorsed the model's recommendation as a generic class (e.g., "Mediterranean varieties in experimental plantings") without naming the specific cultivar, the convergence rate rose to approximately 16/80 = 20%.

The low strict-overlap rate is interpretable rather than damning. The model explores a 58-variety possibility space extending to 2100 under an extreme emissions pathway, whereas growers' documented trials reflect near-term decisions constrained by PDO regulations, rootstock availability, market positioning, and cultural identity. Many of the qualitative-only varieties (Furmint, Kadarka, Kékfrankos, Grüner Veltliner) are being actively *defended* by growers through clonal selection, canopy management, and site migration — adaptation strategies invisible to a climate-envelope model. Conversely, several model-only picks (particularly Nero d'Avola, Touriga Nacional, and Aglianico) represent forward-looking projections that Hungarian growers have not yet considered at scale. The validation is discussed further in Section 4.2.
