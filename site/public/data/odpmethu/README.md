# HungaroMet (odp.met.hu) station observations per wine district

## Source
- Publisher: **HungaroMet Zrt. (Hungarian Meteorological Service)**
- Portal: <https://odp.met.hu/>
- Endpoint used: `climate/observations_hungary/daily/historical/` — one
  `HABP_1D_<station>_<from>_<to>_hist.zip` archive per automatic station,
  covering 2002-01-01 through 2025-12-31 for long-running sites.
- Station metadata: `climate/observations_hungary/meta/station_meta_auto.csv`
- License: **CC-BY-SA**. See
  <https://odp.met.hu/ODP_General_Terms_of_Use.pdf>. When using or
  redistributing, credit *"Forrás: HungaroMet / odp.met.hu, CC-BY-SA"*.

## What we downloaded
The daily **synoptic** CSV endpoint at
`weather/weather_reports/synoptic/hungary/daily/csv/` is a rolling ~10-day
window (only 18 files were listed at the time of fetch), unsuitable for
multi-year climate aggregation. We therefore use the **climate
observations** archive instead, which provides per-station daily records.

To keep bandwidth bounded, we download only the nearest single automatic
station per wine-district centroid (22 districts) that has complete
coverage over 2020-2024 — the most recent 5 full calendar years. That
works out to 21 unique stations (two Lake Balaton districts share
Balatonederics) and roughly 4 MB of zipped CSV.

## Station-to-district matching
For each centroid in `analysis/geo/wine_districts_centroids.csv` we pick
the single closest station (great-circle / Haversine) from the pool of
262 active automatic stations that cover 2020-01-01 through 2024-12-31.

Distance statistics (nearest station only):
- Mean centroid-to-station distance: **9.6 km**
- Max: **16.4 km** (Tolnai → Simontornya)
- Min: **1.6 km** (Neszmélyi → Tata)

Selected stations include Eger (for Egri), Baskó (for Tokaji),
Pécs Árpádtető (for Pécsi), Sopronhorpács (for Soproni), and so on.
See `district_station_assignments.csv` for the full mapping.

## Aggregation
For each (district, year) we compute from the daily records of the
assigned station:

- `tmean_c` — arithmetic mean of the daily mean temperature `t` (°C)
- `precip_mm` — calendar-year sum of daily precipitation `rau` (mm)
- `n_days` — count of days with a valid `t` reading (quality check)

Missing values in the source are marked `-999`; those are dropped before
aggregation. A year is emitted only when at least 200 valid daily
temperature records are present (≥55 % coverage).

## Schema
`odp_station_annual_per_district.parquet` / `.json`

| column         | type    | description                                     |
|----------------|---------|-------------------------------------------------|
| borvidek       | string  | Hungarian wine district name                    |
| year           | int     | Calendar year (2020–2024)                       |
| station_id     | int     | HungaroMet station number                       |
| station_name   | string  | Station name (Hungarian)                        |
| station_lat    | float   | Station latitude (°N)                           |
| station_lon    | float   | Station longitude (°E)                          |
| distance_km    | float   | Haversine distance centroid→station (km)        |
| tmean_c        | float   | Annual mean of daily mean temperature (°C)      |
| precip_mm      | float   | Annual total precipitation (mm)                 |
| n_days         | int     | Valid tmean daily observations in the year      |
| source         | string  | Always `hungaromet_odp`                         |
| source_url     | string  | Full URL to the station zip                     |
| license        | string  | CC-BY-SA reference                              |

## Known caveats
- **Not a hail or severe-storm record.** The HungaroMet daily files do
  not include a hail flag. This dataset gives you observed tmean and
  precipitation totals only; for extreme-storm proxies at district
  level, the best we have is CCKP CMIP6 `rx1day` (annual max 1-day
  precipitation) in `analysis/curated/cckp/`.
- **Single nearest station.** Each district is represented by only the
  one closest station. This is a deliberate bandwidth choice; the
  script is straightforward to extend to k-nearest weighting.
- **Auto-station network only.** The 19th-century long-term series in
  `climate/station_data_series/daily/from_1901/` covers only 10 cities
  (Budapest, Debrecen, Keszthely, Miskolc, Nyíregyháza, Pécs, Sopron,
  Szeged, Szombathely, Debrecen) and is not used here; the automatic
  station network (342 sites) gives much better district coverage for
  the 2002-present period we care about.

## Refresh
```
cd C:\Bor-szőlő\analysis
python src\s08_odpmethu_fetch.py
```

Last refresh: see the logfile at `analysis/logs/s08_odpmethu_fetch.log`.
