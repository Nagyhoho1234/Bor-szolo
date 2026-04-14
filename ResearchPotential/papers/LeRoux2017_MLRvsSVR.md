# Comparison of Two Fine Scale Spatial Models for Mapping Temperatures Inside Winegrowing Areas

- **Authors:** Renan Le Roux, Laure de Resseguier, Thomas Corpetti, Nicolas Jegou, Malika Madelin, Cornelis van Leeuwen, Herve Quenol
- **Year:** 2017
- **Journal:** Agricultural and Forest Meteorology, 247, 159-169
- **DOI:** 10.1016/j.agrformet.2017.07.020
- **Access:** [HAL](https://hal.science/hal-01575344v1) (open access repository); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0168192317302368) (paywalled)
- **Status:** PAYWALLED (HAL access blocked by security; ScienceDirect paywalled)

## Abstract

The study compared two fully automated methods for estimating daily temperature and temperature sums at very fine scale: Multiple Linear Regression (MLR) and Support Vector Regression (SVR). Both methods were applied in the Bordeaux wine region (Saint-Emilion and Pomerol sub-appellations) using data from 2012-2014.

## Key Findings

- **SVR presented better results in each case** thanks to the non-linear component
- Equivalent computing time for both methods
- Non-linear relationships between temperature and topography are better captured by SVR
- Both methods use terrain-derived covariates (elevation, slope, aspect, TPI, etc.)

## Methodology

- MLR: Standard multiple linear regression with DEM-derived predictors
- SVR: Support vector regression (scikit-learn compatible) with same predictors
- Cross-validation comparison
- Application to standard viticultural indices

## Relevance to Tokaj Research

Worth testing SVR as an alternative to MLR in the regression-kriging framework. Tokaj's volcanic terrain with steep slopes and diverse aspects may exhibit non-linear temperature-topography relationships that SVR captures better. Python scikit-learn implementation is straightforward.
