# Literature Matrix: Cross-Reference Against Paper B Acts and Papers A / C

**Generated:** 2026-04-14
**Purpose:** Map each indexed paper against the three acts of Paper B, Papers A and C, and extract reusable methodological parameters.

---

## Table 1: Paper-by-Paper Relevance Matrix

Legend for relevance entries:
- **Template** = primary methodological model to follow
- **Comparison** = provides comparison dataset or benchmark values
- **Index def** = defines an index or threshold used in the analysis
- **Context** = provides framing, background, or literature context
- **Validation** = provides validation data or approach
- **Input** = provides direct input data or parameters
- **(blank)** = no direct relevance to that column

| # | Paper | Act 1 (Mesoclimate zoning) | Act 2 (Dulu terroir validation) | Act 3A (Noble rot mapping) | Act 3B (Frost risk) | Paper A (National atlas) | Paper C (Soil+RS terroir) | Access | Key methodological contribution |
|---|-------|------|------|------|------|------|------|--------|------|
| 1 | Tonietto & Carbonneau 2004 | **Index def:** HI, CI, DI class boundaries; PCA+clustering on 97 regions | Context: terroir classification framework | | | **Index def:** same HI/CI/DI indices used at district scale | Context: MCC framework | FULL | Defines HI classes (<=1500 to >3000), CI classes (<=12 to >18 C), DI classes (<=200 to >-50 mm), PCA on standardised indices |
| 2 | Huglin 1978 | **Index def:** HI formula with latitude coefficient d=1.02-1.06 | | | | **Index def:** same | | HISTORIC | HI = Sum[(Tmean-10)+(Tmax-10)]/2 * d, Apr-Sep; d varies by latitude |
| 3 | Gladstones 1992 | **Index def:** BEDD = min(Tmean-10, 9) capped at 19 C | | | | **Index def:** same BEDD | | STUB | BEDD cap at 19 C reflects biological plateau in vine development above that temperature |
| 4 | Amerine & Winkler 1944 | **Index def:** Winkler GDD classes (Region I <1390 to Region V >2220 C-days) | | | | **Index def:** same 5-region classification | | HISTORIC | GDD = Sum(Tmean-10) for Tmean>10, Apr-Oct; 5 regions with class boundaries at 1390/1670/1950/2220 |
| 5 | De Resseguier et al. 2020 | **Template:** 90 sensors, up to **10 C spatial amplitude** in daily Tmin; Winkler varied **320 degree-days** within single seasons | Comparison: phenological maps linked to thermal zones | | Context: anticyclonic conditions amplify spatial variation | Context: shows what gridded products miss | | FULL | 90 iButtons in canopy, 7 vintages (2012-2018), 19,233 ha; spatial amplitude benchmark: 10 C Tmin, 320 GDD Winkler |
| 6 | Bois et al. 2018 | **Template:** regression-kriging at **50 m resolution**; elevation explains **50-80%** of T variance; covariates: slope, aspect, TPI, TWI, solar radiation | Context: phenology predictions from interpolated T match field obs | | | Comparison: viticultural index mapping | | FULL | 50 m resolution via RK; DEM covariates: elevation, slope, aspect (northness/eastness), TPI multi-scale, TWI, potential solar radiation |
| 7 | Gavrilescu et al. 2018 | **Template:** 64 stations, **75 m resolution**, regression-kriging; GFV phenology model for Chardonnay/Pinot noir; **7-15 day variation** in phenological dates | Comparison: subregional differentiation in Burgundy | | Comparison: Chablis frost risk identification | | | FULL | 64 stations, 41,751 ha, 75 m RK; 6 phenological categories; heat stress days (>=35 C), frost risk days (<=-1 C); closest scale analog to Tokaj |
| 8 | Le Roux et al. 2017 | **Template:** SVR outperforms MLR for non-linear terrain-temperature; same DEM covariates | | | | | | ABSTRACT | SVR vs MLR comparison; SVR superior for non-linear terrain-T relationships; scikit-learn implementation |
| 9 | Van Leeuwen et al. 2024 | Context: Central Europe as warming beneficiary | Context: terroir under climate change | Context: disease pressure changes | | **Context:** anchor for inverted-U framing; identifies Central European regions | Context: adaptation strategies | ABSTRACT | Definitive review; Central European wine regions identified as potential beneficiaries of warming |
| 10 | Van Leeuwen et al. 2004 | | **Template:** quantified relative influence of climate, soil, cultivar on terroir; soil water supply is primary soil driver | | | | **Template:** climate-soil-cultivar interaction framework | ABSTRACT | Simultaneous study of climate, soil, cultivar; soil water supply = primary soil-related terroir driver |
| 11 | Van Leeuwen & Seguin 2006 | | **Context:** formal definition of terroir as interactive cultivated ecosystem | | | | Context: conceptual basis | ABSTRACT | Terroir = interactive cultivated ecosystem (climate + soil + vine + management) |
| 12 | Parker et al. 2011 | | | | | | | ABSTRACT | GFV model: base T=0 C, start DOY 60, cultivar-specific F*; calibrated on 81 varieties, 2278 flowering obs; Furmint/Harslevelyu NOT parameterised |
| 13 | Parker et al. 2013 | | | | | | | ABSTRACT | F* values for 95 (flowering) and 104 (veraison) varieties; classification framework for phenological timing |
| 14 | Garcia de Cortazar-Atauri et al. 2009 | | | | Context: budburst prediction for frost vulnerability window | | | ABSTRACT | BRIN model outperforms forcing-only for budburst; base T is key parameter; hourly resolution improves predictions |
| 15 | Lorenz et al. 1995 | | | | Context: BBCH 07 = budburst damage threshold | | | ABSTRACT | BBCH scale for grapevine: 07=budburst, 65=full bloom, 85=veraison, 89=harvest ripe |
| 16 | Rossi et al. 2008 | | | Context: downy mildew primary infection model (complements Botrytis) | | | | ABSTRACT | Mechanistic hourly model; inputs: T, leaf wetness, RH, precip; multiple oospore cohorts; sporangia production/survival/dispersal |
| 17 | Brischetto et al. 2021 | | | Context: downy mildew secondary infection extension | | | | FULL | Extends Rossi 2008; predicted 39/40 sporangia peaks; 87% accuracy on non-infection periods |
| 18 | Gonzalez-Dominguez et al. 2015 | | | **Template:** mechanistic Botrytis model; SEV1 (flowering), SEV2+SEV3 (veraison-harvest); **81% accuracy** classifying 17/21 epidemics; thresholds: mild <24%, intermediate 25-74%, severe >=75% incidence | | | | FULL | Two infection periods: flowering (SEV1) and veraison-harvest (SEV2 conidial + SEV3 mycelial); inputs: T, wetness duration, host susceptibility; 71.4% cross-validation accuracy |
| 19 | Magarey et al. 2005 | | | Context: generic EPI infection model, R=**0.83** across 53 validation studies, RMSE=**4.9 hours** | | | | ABSTRACT | Generic infection model; inputs: T + surface wetness duration; Wmin = hours for 20% incidence at given T; applicable to multiple pathogens |
| 20 | Thomas et al. 1994 | | | Context: powdery mildew risk index (temperature-only, 21-30 C range) | | | | STUB | Gubler-Thomas index: consecutive hours in 21-30 C = risk; high-T lethal threshold (later revised upward) |
| 21 | Peduto et al. 2014 | | | Context: revised high-T threshold for powdery mildew; E. necator survives higher T than assumed | | | | ABSTRACT | Upward revision of Gubler-Thomas high-T threshold; T x exposure duration = multiplicative interaction |
| 22 | Broome et al. 1995 | | | **Comparison:** empirical Botrytis model; inputs: wetness duration + temperature; response surface for infection probability | | | | ABSTRACT | Empirical wetness-temperature response surface for B. cinerea infection on flowers/berries; simpler alternative to Gonzalez-Dominguez 2015 |
| 23 | Rossi et al. 2014 | | | Context: vite.net DSS integrating disease models into farmer decision support | | | | ABSTRACT | Operational DSS integrating downy mildew, powdery mildew, Botrytis models; template for practical application |
| 24 | Hannah et al. 2013 | | | | | **Context:** 25-73% loss of wine area by 2050 (RCP8.5); 19-62% (RCP4.5) | | FULL | Global suitability projections; Mediterranean most affected; new regions at higher latitudes |
| 25 | Santos et al. 2020 | | | | | **Context:** European viticulture adaptation review | | FULL | Comprehensive European review: phenology, yield, composition, pests, water stress, adaptation strategies |
| 26 | Morales-Castilla et al. 2020 | | | | | **Template:** cultivar diversity buffers **56% of losses at 2 C**; 11 varieties, Smoothed-Utah + Wang-Engel models | | FULL | Without adaptation: 51% area lost at 2 C; with cultivar turnover: 24% lost; later-ripening varieties (Grenache, Monastrell) essential |
| 27 | Kimura et al. 2022 | | | | **Template:** cold flow accumulation + inversion strength; **6.7 C** Tmin difference across only **73 m** elevation; improved valley residuals from **1.9 C to 0.03 C** | | | ABSTRACT | Modified flow accumulation algorithm + vertical potential T gradient (inversion strength); 10x7 km study area, 15 stations |
| 28 | Lundquist et al. 2008 | | | | **Template:** automated cold-air pooling mapping from DEM; TPI + flow accumulation as key predictors | | | ABSTRACT | DEM-based algorithm for cold-air pool susceptibility; tested in Rocky Mts, Pyrenees, Yosemite; clear calm nights = strongest pooling |
| 29 | Hofmann et al. 2022 | | | | | | **Template:** plot-scale water balance; ~24,858 vineyard plots; drought threshold: soil water <**15% AWC** | FULL | Stochastic weather generator + 10 RCMs; historical ~6% drought affected, projected 10-30% (RCP8.5 2041-2070); steep slopes + low AWC = highest risk |
| 30 | Allen et al. 1998 (FAO 56) | Context: ET0 for Dryness Index | | | | Context: ET0 computation | **Input:** Penman-Monteith ET0 + Hargreaves-Samani for T-only stations; Kc for grapevine | FULL | FAO Penman-Monteith equation (radiation, T, humidity, wind); Hargreaves-Samani simplified (T-only); crop coefficient Kc |
| 31 | Pasztor et al. 2015 | Comparison: existing 25 m Tokaj terroir map; **identified mesoclimate gap** that stations fill | **Comparison:** LiDAR + soil map baseline for dulu characterisation; point density **4/m2**, RMSE=**15 cm** | | | | **Template:** 25 m resolution, LiDAR+hyperspectral+soil; precocity, water capacity, vigor potential | ABSTRACT | 11,000+ ha, 27 villages; LEICA ALS70HP on Cessna; soil = dominant terroir factor; drainage, WHC, depth, pH most relevant |
| 32 | Remenyik et al. 2024 | | **Comparison:** microbiome fingerprints for 4 dulu (Betsek, Szent Tamas, Kiraly, Nyulaszo); Bradyrhizobium high at Szent Tamas | | | | **Input:** soil microbiome data for same parcels as stations; 60 samples, seasonal variation | FULL | Shotgun metabarcoding; 3 fungal phyla = 97% of fungi; bacterial diversity correlates with Mn, Mg; seasonal shifts in bacteria |
| 33 | Keve et al. 2024 | | | | | | Context: drought context for Tokaj | ABSTRACT | Markov chain drought model; OMSZ 2002-2020; P2 limiting probability = **20.8%** (any day in veg season in drought); short-term forecast only |
| 34 | Dobos et al. 2016 | | Context: soil property maps for overlay | | | | **Input:** regression-kriging soil maps for Tokaj; drainage, WHC, depth, pH | STUB | Classification trees for soil maps; same RK method as climate interpolation |
| 35 | Lukacsy et al. 2014 | | Comparison: hyperspectral canopy mapping of entire Tokaj region | | | | **Input:** NDVI, LAI, Red Edge Position from airborne campaign, Sept 2014; SWIR 1000-2450 nm | FULL | Entire Tokaj wine region (~11,000 ha); canopy continuity, row structure, variety determination; LiDAR + SWIR hyperspectral |
| 36 | Kern et al. 2024 | **Comparison:** FORESEE-HUN at 0.1 deg (~11 km); 1951-2100; **+1.5-1.7 C** (RCP4.5) by 2071-2100; 14 EURO-CORDEX RCMs | | | | **Input:** primary gridded dataset for Paper A; ensemble of 28 bias-corrected projections | | FULL | Daily Tmin/Tmax/precip/radiation/VPD; historical source = HUCLIM; growing season onset advances **9.1 d** (RCP4.5) to **19.8 d** (RCP8.5) |
| 37 | Vanella et al. 2022 | **Comparison:** ERA5 validation benchmarks; T RMSE **1.46-1.76 C** (plains), **2.11-4.84 C** (mountains) | | | | Comparison: gridded product error ranges | | FULL | 66 Italian stations, 2008-2020; performance ranking: Tair > RH > Rs > u10; systematic biases in complex terrain |
| 38 | Hengl et al. 2007 | **Template:** proves RK = UK = KED mathematically; practical guidelines for implementation | | | | | | ABSTRACT | RK, UK, KED yield identical predictions with same inputs; RK advantage = extensibility to broader regression methods (e.g., SVR) |
| 39 | Hudson & Wackernagel 1994 | **Template:** KED for temperature mapping; elevation as external drift | | | | | | FULL | KED in Scotland; January mean T; elevation as primary drift variable; foundational for climate-DEM kriging |
| 40 | Hengl et al. 2011 | Context: MODIS LST downscaling, R2=**0.84** | | | | | Context: satellite thermal downscaling | STUB | Local space-time regression; MODIS LST 1 km + station + DEM covariates = daily high-resolution thermal maps |
| 41 | Estevez et al. 2011 | **Input:** QC pipeline template (range, step, persistence, spatial buddy tests) | | | | | | ABSTRACT | Range tests (physically plausible bounds), step tests (>15 C jump flag), persistence tests (identical runs), battery voltage checks |
| 42 | Tardivo & Berti 2012 | **Input:** gap-filling via dynamic predictor station selection; errors near **0 C** | | | | | | ABSTRACT | Regression-based gap filling; dynamic selection of predictor stations + coupling period; outperforms static selection |
| 43 | Cerlini et al. 2020 | **Input:** WMO-compliant QC + gap-filling; 80% valid data threshold; linear interp for 1-hr gaps, EOF for >=2 hr | | | | | | ABSTRACT | Two-step validation-reconstruction; 7/74 stations failed (<80% valid); ERA5 as independent gap-filling source |

---

## Table 2: Methodological Building Blocks

For each key method needed across Papers A, B, and C, which papers provide the template and what specific reusable parameters/thresholds do they report?

### 2.1 Regression-Kriging for Spatial Interpolation

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Bois et al. 2018 | Primary template: RK workflow for vineyard temperature zoning | Resolution: **50 m**; elevation explains **50-80%** of T variance; covariates: elevation, slope, aspect (northness cos(a), eastness sin(a)), TPI at multiple scales (100/500/1000 m), TWI, potential solar radiation; cross-validation for error assessment |
| Hengl et al. 2007 | Theoretical foundation: proves RK = UK = KED equivalence | RK preferred operationally because the regression component can be swapped (MLR, SVR, random forest) without changing the kriging step |
| Hudson & Wackernagel 1994 | Original KED for temperature mapping | Elevation as external drift variable; applied to monthly mean T in Scotland |
| Gavrilescu et al. 2018 | Scale analog template | **75 m** resolution; 64 stations over 41,751 ha; directly demonstrates feasibility at Tokaj's density (~50 stations, ~11,000 ha) |
| Le Roux et al. 2017 | Alternative regression: SVR | SVR outperforms MLR for non-linear terrain-T; same DEM covariates; scikit-learn compatible; worth testing for Tokaj's volcanic terrain |
| Dobos et al. 2016 | Same RK method applied to Tokaj soil properties | Demonstrates RK works for Tokaj terrain specifically (not just climate applications) |

**Recommended Tokaj workflow:** MLR or SVR trend against elevation + slope + northness + eastness + TPI(100,500,1000) + TWI + solar radiation, then OK of residuals. Target resolution 25-50 m. Cross-validate with leave-one-out.

### 2.2 PCA Clustering for Bioclimatic Zoning

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Tonietto & Carbonneau 2004 | Foundational framework: PCA on HI, CI, DI for 97 regions | HI classes: Very cool <=1500, Cool 1500-1800, Temperate 1800-2100, Warm temperate 2100-2400, Warm 2400-3000, Very warm >3000; CI classes: Very cool nights <=12 C, Cool 12-14, Temperate 14-18, Warm >18 C; DI classes: Very dry <=-200 mm, Mod. dry -200 to -100, Sub-humid -100 to -50, Humid >-50 |
| Gavrilescu et al. 2018 | Applied PCA+clustering at vineyard scale in Burgundy | 6 phenological categories for pixel classification; heat stress threshold: **>=35 C**; frost risk threshold: **<=-1 C** |
| De Resseguier et al. 2020 | Documented within-region variance benchmarks | Within-season Winkler range: **320 degree-days**; Tmin spatial amplitude: up to **10 C** on a single day |

**Recommended Tokaj workflow:** Compute HI, Winkler, BEDD, CI, DI at all 50 stations. Standardise. PCA: expect first 2 components (heat vs. night cooling) to explain 70-85% variance. K-means with silhouette analysis for optimal k. Alternative: hierarchical clustering (Ward linkage) for dendrogram of nested structure.

### 2.3 Botrytis Modelling (Noble Rot vs. Grey Rot)

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Gonzalez-Dominguez et al. 2015 | **Primary template:** mechanistic model with two infection periods | Period 1 (flowering): conidial infection -> SEV1; Period 2 (veraison-harvest): conidial (SEV2) + mycelial berry-to-berry (SEV3); sporulation rates f(T, moisture, mycelial colonisation); epidemic classes: Mild **<24% incidence**, Intermediate **25-74%**, Severe **>=75%**; 81% classification accuracy (17/21 epidemics); cross-validation 71.4% |
| Broome et al. 1995 | Empirical alternative | Empirical response surface: B. cinerea infection severity = f(wetness duration, temperature); simpler to implement across 50 stations; suitable as a first-pass before full mechanistic model |
| Magarey et al. 2005 | Generic infection model applicable to Botrytis | EPI model: T response function scaled to Wmin; R=**0.83**, RMSE=**4.9 hours** across 53 studies; inputs: T + surface wetness duration; applicable when pathogen-specific parameters unavailable |
| Research plan v2 (Act 3A criteria) | Tokaj-specific noble rot vs. grey rot thresholds | **Noble rot favourability:** RH>90% at 06-09h (morning fog), RH<65% by 14-16h (afternoon drying), Tmax>20 C, no sustained rain >5 mm/day; **Grey rot risk:** RH>80% through 14:00, leaf wetness >6 hours, T 15-22 C; critical window: September-November; **requires 10-minute or hourly data** |

**Recommended Tokaj workflow:** (1) Define noble rot favourability index from sub-daily RH/T criteria (plan v2 thresholds above). (2) Apply Gonzalez-Dominguez 2015 mechanistic model at each station for Botrytis severity prediction. (3) Cross-reference: stations with high noble rot favourability AND low grey rot risk = optimal aszu parcels.

### 2.4 Frost Mapping and Cold Air Pooling

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Kimura et al. 2022 | **Primary template:** cold flow accumulation + inversion strength | Tmin range across only **73 m elevation**: **6.7 C**; modified flow accumulation algorithm improved valley zone residuals from **1.9 C to 0.03 C**; integration of vertical potential T gradient for atmospheric stability; 10x7 km study area with 15 stations |
| Lundquist et al. 2008 | Automated cold-air pool mapping algorithm | DEM-derived variables: TPI and flow accumulation are key predictors; tested across Rocky Mts, Pyrenees, Yosemite; clear calm nights produce strongest pooling; algorithm automates identification of susceptible regions |
| Gavrilescu et al. 2018 | Frost risk identification at vineyard scale | Frost risk threshold: **<=-1 C**; frost risk days mapped at 75 m resolution; Chablis identified as elevated frost risk zone |
| Research plan v2 (Act 3B) | Tokaj-specific frost parameters | Furmint budbreak (BBCH 07): late April; critical damage threshold for emerged shoots: approx. **-2 C**; radiation frost identification: clear sky + calm wind (from wind speed + RH data); GEV/Gumbel extreme value distributions for return period estimation |

**Recommended Tokaj workflow:** (1) Identify radiation frost nights (clear + calm from wind speed + cloud proxy). (2) Regress Tmin on those nights against elevation, TPI, flow accumulation, sky view factor, relative elevation. (3) Apply Kimura 2022 cold flow accumulation algorithm with inversion strength. (4) Produce 25-50 m frost probability map. (5) Overlay with Furmint budbreak window (late April) and -2 C damage threshold. (6) GEV return period estimation for each dulu.

### 2.5 GFV Phenology Model Calibration

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Parker et al. 2011 | GFV model definition | Type: forcing-only thermal time; base temperature: **0 C**; start date: **DOY 60** (March 1); cultivar-specific parameter: **F*** (thermal threshold); input: daily Tmin + Tmax -> Tmean; calibrated on 81 varieties, 2278 flowering + 2088 veraison observations, 1960-2007, 123 locations; **Furmint and Harslevelyu NOT parameterised** |
| Parker et al. 2013 | Extended variety database | F* values for **95 (flowering)** and **104 (veraison)** varieties; classification framework for comparing newly calibrated Hungarian varieties against international database |
| Garcia de Cortazar-Atauri et al. 2009 | Alternative budburst model | BRIN model: adds dormancy calculation + hourly T; base T is the critical parameter; improvement over forcing-only for budburst (but not necessarily for flowering/veraison) |
| Lorenz et al. 1995 | Observation protocol | BBCH scale: 07=budburst, 65=full bloom, 85=veraison, 89=harvest ripe; standardised recording protocol |

**What is needed for Tokaj:** Minimum 3 years (ideally 6+) of BBCH-stage observations at 5-10 plots with co-located station data. Calibrate F* for Furmint and Harslevelyu by minimising RMSE between predicted and observed flowering/veraison dates. Test spatial transferability of a single F* across the 50-station mesoclimatic gradient.

### 2.6 ERA5 / Gridded Product Validation

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Vanella et al. 2022 | **Primary benchmark:** ERA5 vs. 66 Italian stations | T RMSE: **1.46 C** (Bsk), **1.70 C** (Cfa), **1.76 C** (Csa) in plains; **2.11-4.84 C in mountains**; performance ranking: Tair > RH > Rs > u10; systematic biases in complex terrain where sub-grid topography unresolved |
| Kern et al. 2024 | FORESEE-HUN dataset description | 0.1 deg (~11 km) grid; daily Tmin/Tmax/precip/radiation/VPD; historical from HUCLIM; 28 bias-corrected projections (14 EURO-CORDEX RCMs x 2 RCPs); warming: **+1.5-1.7 C** (RCP4.5), more under RCP8.5 by 2071-2100 |
| Cerlini et al. 2020 | ERA5 as gap-filling source | ERA5 provides independent validation/gap-filling; 80% valid data threshold for station usability |

**Expected Tokaj finding:** RMSE in the 2-4 C range for temperature in volcanic terrain (based on Vanella 2022 mountain results). Gridded products will miss: cold air pooling (underestimate Tmin in valleys), thermal belt (underestimate Tmax on mid-slopes), slope-aspect radiation differences. Bias correction: quantile mapping or XGBoost with terrain covariates.

### 2.7 Data Quality Control and Gap Filling

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Estevez et al. 2011 | QC pipeline design | Three sequential tests: (1) **Range tests** -- flag outside physical/climatological bounds (Tokaj: daily Tmax bounds approx. -25 to +42 C); (2) **Step tests** -- flag jumps >**15 C** in consecutive daily Tmean; (3) **Persistence tests** -- flag identical value runs indicating sensor failure; battery voltage checks (often **<11.5 V** for 12V systems flags all concurrent observations) |
| Tardivo & Berti 2012 | Gap-filling method | Dynamic predictor station selection + dynamic coupling period; errors near **0 C** for temperature; outperforms static predictor selection; applicable to dense networks |
| Cerlini et al. 2020 | WMO-compliant workflow | Two-step: validation then reconstruction; linear interpolation for **1-hour gaps**; EOF algorithm for gaps **>=2 hours**; stations with **<80% valid data** excluded; 7/74 failed validation |
| Magarey et al. 2005 | Leaf wetness sensor calibration | Paint-type vs. impedance-type sensors respond differently; local calibration against visual observations required |

**Recommended Tokaj QC pipeline:** (1) Range tests with Tokaj-specific bounds. (2) Step tests: >15 C daily Tmean jump = flag. (3) Persistence tests: identical T runs > threshold duration. (4) Battery voltage < 11.5 V flags all concurrent sensors. (5) Spatial buddy check against nearest stations. (6) Gap filling: regression with nearest correlated stations (Tardivo method) for gaps >3 days; linear interpolation for 1-3 day gaps; ERA5-Land with bias correction as independent source. Known issue: Betsek T sensor stuck May-Jul 2025 (min=mean=max).

### 2.8 Vineyard Water Balance (Paper C)

| Source | Specific contribution | Reusable parameters/thresholds |
|--------|----------------------|-------------------------------|
| Hofmann et al. 2022 | **Primary template:** plot-scale water balance | ~24,858 individual vineyard plots; drought threshold: soil water content below **15% available water capacity**; DEM for slope/aspect effects on ET; stochastic weather generator + 10 RCMs; historical ~6% Rheingau vineyards drought-affected; projected 10-30% (RCP8.5 2041-2070); T warming **2.5-5.6 C** by 2100 |
| Allen et al. 1998 (FAO 56) | ET0 computation standard | Penman-Monteith (requires radiation, T, humidity, wind); Hargreaves-Samani (T-only): ET0 = 0.0023 * Ra * (Tmean+17.8) * (Tmax-Tmin)^0.5; Kc for grapevine: initial 0.3, mid-season 0.7, late 0.45 (approximate, variety-dependent) |
| Tonietto & Carbonneau 2004 | Dryness Index definition | DI = climatic water balance, Penman-type PET, Apr-Sep; classes: Very dry <=-200 mm, Mod. dry -200 to -100, Sub-humid -100 to -50, Humid >-50 mm |
| Keve et al. 2024 | Tokaj drought baseline | Markov chain analysis, OMSZ 2002-2020; **20.8%** limiting probability of drought on any vegetation-season day; vegetation season: March 1 - October 31 |

---

## Table 3: Access Status Summary

| Category | Count | Papers |
|----------|-------|--------|
| **FULL TEXT** | 17 | Tonietto 2004, De Resseguier 2020, Bois 2018, Gavrilescu 2018, Gonzalez-Dominguez 2015, Brischetto 2021, Hannah 2013, Santos 2020, Morales-Castilla 2020, Hofmann 2022, Remenyik 2024, Kern 2024, Vanella 2022, Allen 1998 (FAO), Lukacsy 2014, Hudson 1994, Huglin 1978 |
| **ABSTRACT only** | 21 | Le Roux 2017, Van Leeuwen 2024, Van Leeuwen 2004, Van Leeuwen 2006, Parker 2011, Parker 2013, Garcia de Cortazar-Atauri 2009, Lorenz 1995, Rossi 2008, Magarey 2005, Peduto 2014, Broome 1995, Rossi 2014, Kimura 2022, Lundquist 2008, Hengl 2007, Estevez 2011, Tardivo 2012, Cerlini 2020, Keve 2024, Pasztor 2015 |
| **STUB / not located** | 5 | Gladstones 1992, Amerine & Winkler 1944, Thomas 1994, Dobos 2016, Hengl 2011 |

### Priority full-text acquisitions (paywalled papers critical to methodology)

1. **Kimura et al. 2022** -- primary frost mapping template (Act 3B); need flow accumulation algorithm details and inversion strength formulation
2. **Parker et al. 2011** -- GFV model full parameter tables needed for Furmint calibration reference
3. **Rossi et al. 2008** -- mechanistic downy mildew model hourly parameterisation (complements Botrytis for Act 3A)
4. **Le Roux et al. 2017** -- SVR implementation details and comparison statistics vs MLR
5. **Broome et al. 1995** -- empirical Botrytis response surface (wetness x temperature) for simpler noble rot mapping
6. **Estevez et al. 2011** -- full QC pipeline details with specific threshold values for agrometeorological networks
