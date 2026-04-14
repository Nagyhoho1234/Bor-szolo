# Temperature-Based Zoning of the Bordeaux Wine Region

- **Authors:** Benjamin Bois, Daniel Joly, Hervé Quénol, Philippe Pieri, Jean-Pierre Gaudillere, Dominique Guyon, Etienne Saur, Cornelis van Leeuwen
- **Year:** 2018
- **Journal:** OENO One, 52(4), 291-306
- **DOI:** 10.20870/oeno-one.2018.52.4.1580
- **Access:** Diamond open access at [OENO One](https://oeno-one.eu/article/view/1580) and [HAL](https://hal.science/hal-02056427v1)
- **Status:** FULL TEXT AVAILABLE (open access)

## Abstract

This study reports interpolation of daily minimum and maximum temperature data from 2001 to 2005 in the Bordeaux region using regression kriging with terrain, satellite and land-cover derived covariates. It analyzes interpolation procedure errors in agroclimatic indices through cross validation and compares field observations of grapevine phenology to temperature-based predicted phenology applied to interpolated data.

## Key Findings

- Achieved **50 m resolution** temperature maps across Bordeaux using regression kriging
- Elevation is the strongest predictor of temperature variability, explaining 50-80% of variance
- Additional covariates include slope, aspect, TPI, terrain wetness index, and modeled solar radiation
- Cross-validation demonstrated robust performance for agroclimatic index mapping
- Phenological predictions from interpolated temperature data matched field observations

## Methodology

- Regression kriging: deterministic trend (MLR against DEM-derived predictors) + stochastic residuals (ordinary kriging)
- DEM-derived covariates: elevation, slope, aspect (northness/eastness), TPI at multiple scales, TWI, potential solar radiation
- Cross-validation for error assessment
- Application to standard viticultural indices (Huglin, Winkler, etc.)

## Relevance to Tokaj Research

This is the exact workflow recommended for Manuscript 1 (mesoclimatic zoning). With 50 stations in Tokaj, regression-kriging with DEM covariates at 25-50 m resolution is directly feasible. The paper provides the methodological template for separating deterministic trend from stochastic spatial residuals.
