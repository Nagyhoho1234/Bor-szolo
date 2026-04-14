# Turning 50 weather stations into viticultural science: a research roadmap for Tokaj

**A dense agrometeorological network across the Tokaj wine region fills a critical gap identified by Hungary's own digital terroir mapping efforts — existing terrain, soil, and remote sensing data for Tokaj are excellent, but fine-scale in-situ climate observations have been missing.** Your ~50-station network in this UNESCO World Heritage landscape positions you to replicate methodologies proven in Bordeaux (90 sensors; de Rességuier et al., 2020) and Burgundy (64 stations; Gavrilescu et al., 2018), adapted for a continental climate with volcanic terroir. The combination of your geostatistical expertise (SGSIM, kriging), GIS/remote sensing background, and Python skills aligns almost perfectly with the dominant analytical workflows in viticultural climatology. This briefing maps out **seven concrete research directions**, five publishable manuscript concepts, and the methods and references needed to begin executing analyses immediately.

---

## 1. A menu of research directions your data can support

Each direction below is feasible with your current dataset of daily air temperature (min/mean/max), relative humidity, wind speed, soil temperature, precipitation, leaf wetness, soil moisture, and battery voltage across ~50 stations in complex volcanic terrain.

### Direction 1: Mesoclimatic terroir zoning through multivariate clustering

The scientific question asks whether the ~90 named vineyard parcels (dűlők) of Tokaj can be objectively grouped into distinct mesoclimatic zones using station-derived bioclimatic indices. **Variables needed** include daily Tmin, Tmean, Tmax, and precipitation for computing the Huglin Index, Winkler GDD, Cool Night Index, and Dryness Index at each station. Methods involve PCA for dimensionality reduction followed by k-means or hierarchical clustering (Ward linkage) on principal component scores, with silhouette analysis for optimal cluster selection. Spatial interpolation via regression-kriging with DEM covariates extends point-based indices to continuous 25–50 m resolution maps. The foundational framework is Tonietto and Carbonneau's (2004) Multicriteria Climatic Classification in *Agricultural and Forest Meteorology*. Bois et al. (2018) demonstrated this exact workflow for Bordeaux in *OENO One*, achieving 50 m resolution temperature-based zoning using regression kriging with terrain covariates. Target venues include *OENO One* (Q1, diamond open access), *Agricultural and Forest Meteorology* (Q1, IF ~6.1), and *Theoretical and Applied Climatology* (Q2).

### Direction 2: Spatially explicit disease risk modeling across the vineyard landscape

This direction asks how downy mildew (*Plasmopara viticola*), powdery mildew (*Erysiphe necator*), and *Botrytis cinerea* risk vary spatially across Tokaj's complex terrain. The dataset's **leaf wetness duration, temperature, relative humidity, and precipitation** are precisely the inputs required by established disease models. For downy mildew, the Rossi-Caffi mechanistic model (Rossi et al., 2008, *Ecological Modelling*; Brischetto et al., 2021, *Frontiers in Plant Science*) and the EPI generic infection model (Magarey et al., 2005, *Phytopathology*) both require temperature and leaf wetness duration. Powdery mildew risk uses the Gubler-Thomas index requiring only hourly temperature (Thomas et al., 1994; revised by Peduto et al., 2014, *Plant Disease*). Botrytis prediction combines leaf wetness duration with temperature following Broome et al. (1995, *Phytopathology*) or the González-Domínguez mechanistic model (2015, *PLoS ONE*). Running these models across all 50 stations and interpolating the outputs produces vineyard-scale disease risk maps — a novel contribution for any Central European wine region. Target venues: *European Journal of Plant Pathology*, *Plant Disease*, *Crop Protection*, or *OENO One*.

### Direction 3: Spring frost risk mapping and cold air pooling characterization

Tokaj's volcanic hills create significant topographic complexity where cold air drainage during clear, calm spring nights produces frost pockets that threaten buds after budbreak. **Variables needed** are daily and sub-daily Tmin and the DEM-derived topographic variables (TPI, flow accumulation, sky view factor, relative elevation). Methods include empirical regression of Tmin against terrain indices following Lundquist et al. (2008, *Journal of Geophysical Research*) and Kimura et al. (2022, *Agricultural and Forest Meteorology*), who combined a cold flow accumulation algorithm with inversion strength indicators. With 50 stations spanning different elevations, slopes, and valley positions, you can quantify the **thermal belt** effect and map frost probability at high resolution. Return period estimation via Gumbel/GEV extreme value distributions, overlaid with phenology-based vulnerability windows, produces actionable frost risk assessments. Target venues: *Agricultural and Forest Meteorology* (Q1), *International Journal of Biometeorology* (Q2), *Theoretical and Applied Climatology* (Q2).

### Direction 4: Grapevine phenology modeling calibrated across a mesoclimatic gradient

This direction calibrates and validates temperature-based phenology models for Tokaj's key cultivars (Furmint, Hárslevelű, Sárga Muskotály) using thermal time accumulation across the station network. **Variables needed** are daily Tmin and Tmax (to derive Tmean); **additional data required** are multi-year phenological observations (BBCH stages 07, 65, 85, 89) at representative plots. The GFV model (Parker et al., 2011, *Australian Journal of Grape and Wine Research*; 2013, *Agricultural and Forest Meteorology*) is the standard framework — a forcing-only model with base temperature 0°C, start date DOY 60, and cultivar-specific thermal thresholds F*. It has been parameterized for 95+ cultivars but **not yet for Furmint or Hárslevelű**, representing a clear publication opportunity. The 50-station gradient allows testing whether a single F* value works across all mesoclimatic zones or whether spatial calibration is needed. Target venues: *Agricultural and Forest Meteorology* (Q1), *OENO One* (Q1), *American Journal of Enology and Viticulture* (Q1).

### Direction 5: Vineyard water balance and drought stress spatial dynamics

Using temperature, humidity, wind speed, and precipitation, you can compute reference evapotranspiration (ET0) via the FAO Penman-Monteith equation (Allen et al., 1998, FAO-56) at stations with full data, or the Hargreaves-Samani method at temperature-only stations. Combined with soil moisture sensor data and soil property maps (available from Pásztor et al.'s 25 m DOSoReMI mapping), this enables a spatially distributed daily water balance model. **Soil moisture data** from your stations provide direct validation. The Dryness Index (Tonietto and Carbonneau, 2004) quantifies seasonal water availability, while SPEI and SPI indices characterize drought severity. Hofmann et al. (2022, *Earth System Dynamics*) provide the best methodological template, having built a plot-scale vineyard water balance model for the Rheingau integrating DEM, soil maps, and station data. Target venues: *Agricultural Water Management* (Q1), *Agricultural and Forest Meteorology* (Q1), *European Journal of Agronomy* (Q1).

### Direction 6: Validating gridded products against dense observations in complex terrain

Your 50-station network represents an unusually dense ground-truth dataset for evaluating how well ERA5-Land (~9 km), AgERA5, and the Hungarian FORESEE-HUN (0.1° grid, ~11 km) gridded datasets capture mesoclimatic variability in volcanic, dissected terrain. **All measured variables** can be compared, but temperature, precipitation, and humidity are most informative. Vanella et al. (2022, *Journal of Hydrology: Regional Studies*) compared ERA5 against 66 Italian agrometeorological stations and found temperature RMSE of 0.98–1.76°C in plains but **2.11–4.84°C in mountains** — Tokaj's terrain likely falls in this problematic range. Demonstrating the added value of your local network over coarse gridded products, and developing station-trained bias correction functions (quantile mapping, random forest regression), is a high-impact methodological contribution. Target venues: *International Journal of Climatology* (Q1), *Journal of Applied Meteorology and Climatology* (Q1), *Climate Services* (Q1).

### Direction 7: Climate change trend detection and shifting bioclimatic suitability

If your dataset spans multiple years (or can be extended with OMSZ historical records), Mann-Kendall trend tests and Sen's slope estimators applied to bioclimatic indices reveal how Tokaj's viticultural climate is shifting. This is especially relevant given that van Leeuwen et al. (2024, *Nature Reviews Earth and Environment*) identified Central European wine regions as potential beneficiaries of warming, with expanding suitability for red varieties. The FORESEE-HUN dataset provides RCP4.5/8.5 projections that can be bias-corrected against your stations for future scenario analysis. Even with a single year of data, you can compute the 2025 bioclimatic indices for all 50 stations and compare against 30-year normals from FORESEE-HUN or HuClim to characterize the current vintage's climatic anomaly. Target venues: *Climatic Change* (Q1), *Climate Research* (Q3), *International Journal of Biometeorology* (Q2).

---

## 2. The analytical toolkit for a 50-station volcanic landscape

### Spatial interpolation: regression-kriging is the optimal choice

With approximately 50 stations, your network provides sufficient data for stable variogram estimation and robust regression-kriging. The recommended workflow separates the deterministic trend from stochastic spatial residuals. First, fit a multiple linear regression of the target variable (e.g., daily Tmin) against DEM-derived predictors — **elevation is universally the strongest predictor**, typically explaining 50–80% of temperature variance through the environmental lapse rate of approximately –6.5°C/km. Additional covariates include slope, aspect (decomposed into northness and eastness components), TPI at multiple scales (100 m, 500 m, 1000 m), terrain wetness index, and modeled potential solar radiation from SAGA GIS or GRASS r.sun. Second, fit a variogram to the regression residuals and apply ordinary kriging to interpolate them. The sum of the regression surface and kriged residuals produces the final map.

Bois et al. (2018) achieved **50 m resolution** temperature maps across Bordeaux using this exact method. Le Roux et al. (2017, *Agricultural and Forest Meteorology*) compared multiple linear regression with support vector regression (SVR) for the non-linear relationship between temperature and topography, finding SVR superior — worth testing with your Python scikit-learn workflow. For precipitation, which has weaker topographic determinism, cokriging with elevation or simple OK may perform better than regression-kriging.

The topographic variables most relevant to Tokaj's terrain include TPI for identifying cold air pooling sites, sky view factor for radiative frost susceptibility, and flow accumulation computed from a hydrologically corrected DEM for modeling cold air drainage pathways. Hungarian high-resolution DEMs are available from the EU-DEM at 25 m or the SRTM at 30 m, and Pásztor et al. (2015) used airborne LiDAR for Tokaj at even finer resolution.

### Clustering vineyard parcels into mesoclimatic zones

The standard pipeline involves computing bioclimatic indices (Huglin, Winkler, CI, DI) at each station, applying PCA to extract orthogonal components explaining >90% of variance (following Tonietto and Carbonneau, 2004), and then clustering stations on the PC scores. K-means with silhouette-based selection of k is most common, but hierarchical clustering with Ward linkage produces informative dendrograms showing nested structure. For time-series-based clustering, Dynamic Time Warping (DTW) distance captures seasonal pattern similarity independent of absolute values — particularly useful for identifying stations with similar temperature curves but different elevations.

### Remote sensing integration amplifies station data

Sentinel-2 NDVI at **10 m resolution** maps vine vigor across the entire landscape, providing a vegetation response variable that can be correlated with station-derived climate indices. MODIS LST at 1 km offers daily thermal information that can be statistically downscaled using your station data and DEM covariates — Hengl et al. (2011) achieved R² = 0.84 using local space-time regressions. The STARFM algorithm fuses Sentinel-2 spatial detail with MODIS temporal frequency for continuous monitoring. For Tokaj specifically, Lukácsy et al. (2014) already acquired airborne hyperspectral imagery (NDVI, LAI, Red Edge) that could be integrated with your station data.

---

## 3. What has already been done in Tokaj — and the gap your network fills

### Existing Tokaj research establishes the foundation

Pásztor et al. (2015) produced the most comprehensive digital terroir map of Tokaj, integrating LiDAR, hyperspectral imagery, and digital soil maps at 25 m resolution. Dobos et al. (2016) applied regression kriging for soil property mapping. Remenyik et al. (2024, *PLoS ONE*) characterized soil microbiomes across four historic dűlők including **Betsek, Szent Tamás, Király, and Nyúlászó** in Mád — notably, the same Betsek vineyard in your station dataset. Keve et al. (2024, *Progress in Agricultural Engineering Sciences*) analyzed drought periods using Markov chains on OMSZ data from 2002–2020. The 10th International Terroir Congress was held in Tokaj in 2014, and the University of Tokaj-Hegyalja (Lorántffy Institute) has ongoing viticulture research.

**The critical gap is in-situ mesoclimatic data.** All existing Tokaj climate characterization relies on interpolated legacy records or coarse gridded products (FORESEE-HUN at ~11 km, HuClim at ~11 km). Your 50-station network is the first dense observational dataset capturing the actual mesoclimatic variability across Tokaj's volcanic slopes, river-influenced lowlands, and varied aspects. This directly parallels the transformative impact that dense sensor deployments had in Bordeaux and Burgundy.

### European templates directly transferable to Tokaj

The LIFE-ADVICLIM project (2014–2020, coordinated by Hervé Quénol at CNRS Rennes) deployed dense temperature sensor networks across six European pilot sites including Bordeaux, Loire, Sussex, Rheingau, and — most relevantly — **Cotnari, Romania**, which shares Tokaj's continental climate and botrytized wine tradition. Cotnari is the closest published analog to your research context. The ADVICLIM methodology (dense sensors → spatial climate modeling at 25 m → DEM integration → climate projection downscaling) is directly transferable. Gavrilescu et al.'s (2018) Burgundy study, using 64 stations across 41,751 ha with regression-kriging at 75 m resolution, is the closest in scale to Tokaj's ~11,000 ha vineyard area.

---

## 4. Five publishable manuscripts from your dataset

### Manuscript 1: "Mesoclimatic zoning of the Tokaj wine region using a dense agrometeorological network and geostatistical interpolation"

The core hypothesis is that Tokaj's volcanic terrain creates statistically distinct mesoclimatic zones that correspond to historically recognized quality tiers among dűlők. This paper computes Huglin, Winkler, Cool Night, and Dryness indices at all 50 stations, applies regression-kriging with DEM covariates to produce continuous 25–50 m maps, and uses PCA + k-means clustering to delineate mesoclimatic zones. Additional data needed: high-resolution DEM (available from EU-DEM or Hungarian LiDAR), vineyard parcel boundaries (MePAR system). Compare the resulting zones against the historical classification of premier cru dűlők. **Target: *OENO One* (Q1, diamond OA) or *Agricultural and Forest Meteorology* (Q1).** This is the highest-priority first paper because it establishes the foundational spatial framework that all subsequent analyses can reference.

### Manuscript 2: "Spatially distributed disease risk assessment for *Plasmopara viticola* and *Botrytis cinerea* across complex volcanic terrain in Tokaj"

The research question asks whether disease pressure varies systematically across topographic positions, and whether a 50-station network can identify high-risk zones missed by single-station forecasts. Run the Rossi-Caffi downy mildew model (or simplified EPI model) and Botrytis risk calculations at each station using temperature, leaf wetness, and humidity. Interpolate risk scores to produce continuous maps. Additional data needed: phenological observations for model timing, and ideally field disease severity scores for validation from at least one growing season. **The Botrytis angle is uniquely important for Tokaj** because *Botrytis cinerea* as noble rot (aszú) is the region's defining product — spatial mapping of conditions favoring noble rot vs. destructive grey rot is economically significant and scientifically novel. **Target: *European Journal of Plant Pathology* (Q1) or *Crop Protection* (Q1).**

### Manuscript 3: "Cold air pooling and spring frost risk mapping in the Tokaj volcanic hills: a DEM-integrated station network approach"

This paper quantifies the thermal belt effect and cold air drainage patterns using multi-station minimum temperature analysis. Regress nightly Tmin against TPI, flow accumulation, sky view factor, and relative elevation under radiation frost conditions (clear, calm nights). Identify frost-prone and frost-free zones at high resolution. Additional data needed: sub-daily temperature data (if available), classified weather types for separating radiation vs. advective frost events, and phenological vulnerability windows for Furmint. Apply extreme value analysis (GEV distributions) for return period estimation of damaging frost events. **Target: *Agricultural and Forest Meteorology* (Q1) or *International Journal of Biometeorology* (Q2).** This has strong practical appeal and policy relevance for the UNESCO heritage site.

### Manuscript 4: "Added value of a dense agrometeorological network over ERA5-Land and FORESEE-HUN in a complex-terrain wine region"

Compare station observations against ERA5-Land (9 km) and FORESEE-HUN (11 km) for all available variables. Quantify systematic biases, particularly how unresolved sub-grid topography causes these products to miss cold air pooling, thermal belt effects, and slope-aspect radiation differences. Develop bias correction functions using quantile mapping and machine learning (XGBoost). Demonstrate that station-derived bioclimatic indices and disease risk assessments diverge significantly from gridded-product-derived ones in complex terrain. **This paper has broad methodological appeal beyond viticulture.** Additional data: ERA5-Land hourly downloads via CDS API, FORESEE-HUN gridded fields from ELTE. **Target: *International Journal of Climatology* (Q1) or *Journal of Applied Meteorology and Climatology* (Q1).**

### Manuscript 5: "First calibration of the GFV phenology model for Furmint and Hárslevelű across a mesoclimatic gradient in Tokaj"

This paper requires multi-year phenological observation data (BBCH stages) collected at representative vineyard plots near your stations. Calibrate the GFV model's F* parameter for Furmint and Hárslevelű — these cultivars have never been parameterized, so this fills a genuine gap in the international phenology database. Test spatial transferability of the calibrated model across the 50-station gradient. If only one year of phenological data exists, frame the paper as a pilot calibration with spatial validation. Additional data needed: **minimum 3 years (ideally 6+) of phenological observations at 5–10 plots** using standardized BBCH protocol. **Target: *Australian Journal of Grape and Wine Research* (Q1) or *OENO One* (Q1).**

---

## 5. Essential references organized by theme

### Bioclimatic indices and viticultural classification

Tonietto and Carbonneau (2004) established the Multicriteria Climatic Classification combining Huglin Index, Cool Night Index, and Dryness Index across 97 regions worldwide (*Agricultural and Forest Meteorology*, 124, 81–97). Huglin (1978) defined the heliothermal index in *Comptes Rendus de l'Académie d'Agriculture de France*. Gladstones (1992) introduced Biologically Effective Degree Days in *Viticulture and Environment* (Winetitles). Amerine and Winkler (1944) created the original GDD classification in *Hilgardia*.

### Terroir and vine-climate interactions

Van Leeuwen et al. (2004) quantified the relative influence of climate, soil, and cultivar on terroir in *American Journal of Enology and Viticulture*, 55(3), 207–217. Van Leeuwen and Seguin (2006) defined terroir as an interactive cultivated ecosystem in *Journal of Wine Research*. Van Leeuwen et al. (2024) published the definitive review on climate change impacts and adaptations for wine production in *Nature Reviews Earth and Environment*, 5, 258–275.

### Dense station networks and spatial climate modeling in vineyards

De Rességuier et al. (2020) deployed 90 sensors across Bordeaux's Saint-Émilion/Pomerol, revealing **up to 10°C spatial amplitude** in daily minimum temperatures (*Frontiers in Plant Science*, 11, 515). Le Roux et al. (2017) compared MLR and SVR for vineyard temperature mapping (*Agricultural and Forest Meteorology*, 247, 159–169). Bois et al. (2018) achieved 50 m temperature zoning via regression kriging (*OENO One*, 52(4), 291–306). Gavrilescu et al. (2018) zoned Burgundy using 64 stations and regression-kriging at 75 m (*E3S Web of Conferences*, 50, 01003).

### Phenology modeling

Parker et al. (2011, 2013) developed and extended the GFV model for 95+ cultivars (*Australian Journal of Grape and Wine Research*, 17(2), 206–216; *Agricultural and Forest Meteorology*, 180, 249–264). García de Cortázar-Atauri et al. (2009) compared budburst models in *International Journal of Biometeorology*, 53, 317–326. The BBCH scale for grapevine was codified by Lorenz et al. (1995) in *Australian Journal of Grape and Wine Research*, 1, 100–103.

### Disease risk models

Rossi et al. (2008) built the mechanistic downy mildew model in *Ecological Modelling*, 212, 480–491, extended by Brischetto et al. (2021) in *Frontiers in Plant Science*. Magarey et al. (2005) created the generic EPI infection model in *Phytopathology*, 95(1), 92–100. The Gubler-Thomas powdery mildew index was established by Thomas et al. (1994) and revised by Peduto et al. (2014, *Plant Disease*, 98, 1000–1006). González-Domínguez et al. (2015) published the mechanistic Botrytis model in *PLoS ONE*, 10(10), e0140444. Rossi et al. (2014) described the integrated vite.net® DSS in *Computers and Electronics in Agriculture*, 100, 88–99.

### Climate change and viticulture

Hannah et al. (2013) projected 25–73% loss of wine-growing area by 2050 in *PNAS*, 110(17), 6907–6912. Santos et al. (2020) reviewed European viticulture impacts in *Applied Sciences*, 10(9), 3092. Morales-Castilla et al. (2020) showed cultivar diversity could buffer 56% of losses in *PNAS*, 117(6), 2864–2869.

### Tokaj-specific

Pásztor et al. (2015) mapped Tokaj's digital terroir at 25 m using LiDAR and soil data (EGU2015-12660). Remenyik et al. (2024) characterized soil microbiomes in Mád dűlők including Betsek in *PLoS ONE*. Keve et al. (2024) modeled Tokaj drought periods in *Progress in Agricultural Engineering Sciences*. Kern et al. (2024) described the FORESEE-HUN dataset in *Climate Services*.

### Geostatistical methods

Hudson and Wackernagel (1994) demonstrated kriging with external drift for temperature in *International Journal of Climatology*, 14, 77–91. Hengl (2007) formalized regression-kriging equivalences in *Geoderma*. Kimura et al. (2022) combined cold flow accumulation with inversion strength for fine-scale Tmin mapping in *Agricultural and Forest Meteorology*, 329, 109260.

---

## 6. Data quality control and gap-filling for your network

### A three-tier QC pipeline is standard for agrometeorological networks

Your sample data showing gaps and missing values is typical for automated weather stations. Following Estévez et al. (2011, *Journal of Hydrology*, 402, 144–154) and WMO guidelines, implement three sequential checks. **Range tests** flag values outside physically plausible or climatologically expected bounds — for Tokaj, reasonable daily Tmax bounds might be –25°C to +42°C, with tighter monthly climatological ranges. **Step tests** flag implausible jumps between consecutive readings (e.g., >15°C change in daily Tmean). **Persistence tests** flag runs of identical values indicating sensor failure. Battery voltage below a manufacturer-specified threshold (often ~11.5 V for 12V systems) should flag all concurrent observations as suspect, since low voltage causes systematic measurement errors across all sensors.

Leaf wetness sensors deserve special attention because they require local calibration against visual observations, and paint-type vs. impedance-type sensors respond differently (Magarey et al., 2005). Soil moisture sensors can drift over time due to soil settling or root intrusion. A spatial buddy check — comparing each station against the expected value from its neighbors via spatial interpolation — catches errors that temporal checks miss, and is particularly powerful with 50 stations.

### Gap-filling leverages your network density

Short gaps (1–3 days) are best filled with temporal linear interpolation for slowly varying quantities (temperature, soil moisture) or set to zero for event-based variables (precipitation on non-rain days). Longer gaps use regression against the nearest correlated stations — Tardivo and Berti (2012, *Journal of Applied Meteorology and Climatology*) achieved errors near 0°C using dynamically selected predictor stations. ERA5-Land provides an independent gap-filling source: Cerlini et al. (2020, *Meteorological Applications*) developed a WMO-compliant two-step validation-reconstruction procedure for 73 stations in Umbria, Italy. Machine learning approaches (MICE with ERA5 predictors, or LSTM networks) handle complex multivariate gaps. The recommended priority order is: (1) regression with nearby stations, (2) ERA5-Land-assisted imputation with bias correction, (3) temporal interpolation for short gaps only.

---

## Conclusion: where to start and what matters most

Your 50-station network in Tokaj is, based on the published literature, **the densest agrometeorological observation system currently operating in any Central or Eastern European wine region**. This represents genuine scientific infrastructure that can generate a portfolio of publications.

The highest-priority first paper is the mesoclimatic zoning study (Manuscript 1) because it establishes the spatial framework that all other analyses reference. It requires no additional data beyond your stations and a freely available DEM, plays directly to your geostatistical strengths, and has clear methodological precedents in Bordeaux and Burgundy. The disease risk mapping (Manuscript 2), particularly the Botrytis spatial analysis, offers the most distinctive angle — no other study has mapped noble rot conditions at vineyard-parcel resolution using a dense station network. The ERA5 validation paper (Manuscript 4) has the broadest audience beyond viticulture.

Three practical steps to execute immediately: compute the six standard bioclimatic indices at all 50 stations for 2025, run the QC pipeline on your full dataset, and extract ERA5-Land time series at each station location for comparison. These three tasks, achievable in days with Python, generate the raw material for at least three of the five manuscripts described above. The Tokaj terroir research community — centered at the University of Debrecen, the Lorántffy Institute, and HUN-REN's soil science group — provides natural collaborators who can supply the phenological observations, soil maps, and local expertise needed for the more data-intensive directions.