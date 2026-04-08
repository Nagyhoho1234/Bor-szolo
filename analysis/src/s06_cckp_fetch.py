"""
s06_cckp_fetch.py
Fetch World Bank CCKP CMIP6 ensemble climatologies per Hungarian wine district.

Strategy:
  1) Country-level (HUN) values via CCKP REST API for all (var, scenario, period, stat).
  2) District-level values via gridded NetCDFs from the AWS open-data bucket
     (s3://wbg-cckp/data/cmip6-x0.25/), using pre-computed `ensemble-all-<scenario>`
     files (median/p10/p90) sampled at the 22 district centroids by nearest-neighbor.
  3) If S3 sampling fails for any combination, fall back to the country-level value
     duplicated for all 22 districts and tag granularity='country'.

Outputs:
  analysis/curated/cckp/cckp_cmip6_<var>_<scenario>_per_district.parquet
  analysis/curated/cckp/cckp_summary.csv
Cache:
  analysis/interim/cckp_cache/  (raw JSON for API + .nc files for S3)
"""
import os, sys, io, json, time, hashlib, datetime, traceback
from pathlib import Path

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

import requests
import pandas as pd
import numpy as np
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import xarray as xr

ROOT = Path(r"C:\Bor-szőlő\analysis")
CENTROIDS_CSV = ROOT / "geo" / "wine_districts_centroids.csv"
CACHE_DIR = ROOT / "interim" / "cckp_cache"
NC_CACHE = CACHE_DIR / "nc"
API_CACHE = CACHE_DIR / "api"
OUT_DIR = ROOT / "curated" / "cckp"
LOG_DIR = ROOT / "logs"
for d in (CACHE_DIR, NC_CACHE, API_CACHE, OUT_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "s06_cckp_fetch.log"
def log(msg):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# -----------------------------------------------------------------------------
# Configuration: variables, periods, scenarios, stats
# -----------------------------------------------------------------------------
# (var_code on CCKP, units, description)
VARIABLES = [
    ("tas",    "degC",         "Annual mean of daily mean temperature"),
    ("tasmax", "degC",         "Annual mean of daily max temperature"),
    ("tasmin", "degC",         "Annual mean of daily min temperature"),
    ("pr",     "mm/year",      "Annual total precipitation"),
    ("hd35",   "days",         "Days with tmax > 35 C (heat days)"),
    ("txx",    "degC",         "Annual maximum of daily max temperature"),
    ("r20mm",  "days",         "Days with precip >= 20 mm"),
]

# (period, scenario)  -- historical only paired with 'historical'
COMBOS = [
    ("1995-2014", "historical"),
    ("2040-2059", "ssp245"),
    ("2040-2059", "ssp585"),
    ("2080-2099", "ssp245"),
    ("2080-2099", "ssp585"),
]

# CCKP API uses median/p10/p90 as the percentile token; we expose them as
# stat names mean/p10/p90 (median ~ ensemble central tendency).
STATS = [("mean", "median"), ("p10", "p10"), ("p90", "p90")]

API_BASE = "https://cckpapi.worldbank.org/cckp/v1"
S3_BUCKET = "wbg-cckp"
S3_PREFIX = "data/cmip6-x0.25"
SLEEP = 0.2

# -----------------------------------------------------------------------------
# Counters
# -----------------------------------------------------------------------------
stats_counter = {
    "http_requests": 0,
    "http_cached": 0,
    "s3_downloads": 0,
    "s3_cached": 0,
    "bytes_downloaded": 0,
    "district_succ": 0,
    "country_fallback": 0,
    "failed": 0,
}

# -----------------------------------------------------------------------------
# Centroids
# -----------------------------------------------------------------------------
def load_centroids():
    df = pd.read_csv(CENTROIDS_CSV, encoding="utf-8")
    # tolerate either column naming
    lat_col = "centroid_lat" if "centroid_lat" in df.columns else "lat"
    lon_col = "centroid_lon" if "centroid_lon" in df.columns else "lon"
    df = df.rename(columns={lat_col: "lat", lon_col: "lon"})
    return df[["borvidek", "borregio", "lat", "lon"]].copy()

# -----------------------------------------------------------------------------
# CCKP API (country-level HUN)
# -----------------------------------------------------------------------------
def api_url(var, period, scenario, pct_token):
    return (
        f"{API_BASE}/cmip6-x0.25_climatology_{var}_climatology_annual_"
        f"{period}_{pct_token}_{scenario}_ensemble_all_mean/HUN?_format=json"
    )

def cache_path_for_url(url):
    h = hashlib.md5(url.encode("utf-8")).hexdigest()[:16]
    return API_CACHE / f"{h}.json"

def fetch_api(url):
    cp = cache_path_for_url(url)
    if cp.exists():
        stats_counter["http_cached"] += 1
        return json.loads(cp.read_text(encoding="utf-8"))
    time.sleep(SLEEP)
    r = requests.get(url, timeout=60)
    stats_counter["http_requests"] += 1
    stats_counter["bytes_downloaded"] += len(r.content)
    if r.status_code != 200:
        log(f"  API HTTP {r.status_code}: {url}")
        return None
    try:
        j = r.json()
    except Exception:
        log(f"  API non-JSON: {url}")
        return None
    cp.write_text(json.dumps(j), encoding="utf-8")
    return j

def parse_api_value(j):
    """Return float value from CCKP API response, or None."""
    if not j: return None
    data = j.get("data")
    if not data or not isinstance(data, dict): return None
    hun = data.get("HUN")
    if not hun or not isinstance(hun, dict): return None
    # take the single value (key like '1995-07' or '2080-07')
    vals = list(hun.values())
    if not vals: return None
    try:
        return float(vals[0])
    except Exception:
        return None

# -----------------------------------------------------------------------------
# S3 NetCDF (district-level via centroid sampling)
# -----------------------------------------------------------------------------
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED, retries={"max_attempts": 3}))

def s3_key(var, scenario, pct_token, period):
    return (
        f"{S3_PREFIX}/{var}/ensemble-all-{scenario}/"
        f"climatology-{var}-annual-mean_cmip6-x0.25_ensemble-all-{scenario}_"
        f"climatology_{pct_token}_{period}.nc"
    )

def fetch_nc(var, scenario, pct_token, period):
    key = s3_key(var, scenario, pct_token, period)
    local = NC_CACHE / key.replace("/", "__")
    if local.exists() and local.stat().st_size > 0:
        stats_counter["s3_cached"] += 1
        return local
    try:
        time.sleep(SLEEP)
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        body = resp["Body"].read()
        local.write_bytes(body)
        stats_counter["s3_downloads"] += 1
        stats_counter["bytes_downloaded"] += len(body)
        return local
    except Exception as e:
        log(f"  S3 miss [{key}]: {type(e).__name__}: {e}")
        return None

def sample_nc_at_points(nc_path, var, lats, lons):
    """Open NetCDF and return list of values at the given lat/lon points (nearest).

    Reads file bytes into memory and opens via h5netcdf to avoid Windows
    non-ASCII path issues with the netCDF4 C library (the 'ő' in the project
    root breaks netCDF4 file opening).
    """
    try:
        raw = Path(nc_path).read_bytes()
        # Try engines in order: scipy handles NetCDF3 classic (CDF\x01 / CDF\x02),
        # h5netcdf handles NetCDF4/HDF5 (\x89HDF). Both accept file-like buffers
        # and therefore bypass the Windows non-ASCII path issue in the C netCDF lib.
        if raw[:3] == b"CDF":
            bio = io.BytesIO(raw)
            ds = xr.open_dataset(bio, engine="scipy", decode_times=False)
        else:
            bio = io.BytesIO(raw)
            ds = xr.open_dataset(bio, engine="h5netcdf", decode_times=False)
        with ds:
            # Variable name in the file: try common patterns
            cand = None
            for name in (var, "climatology-" + var + "-annual-mean", "climatology", "annual"):
                if name in ds.data_vars:
                    cand = name; break
            if cand is None:
                # take the first non-coord var
                for v in ds.data_vars:
                    cand = v; break
            if cand is None:
                return None
            da = ds[cand]
            # squeeze any singleton dims (time, bnds, etc.)
            da = da.squeeze(drop=True)
            # detect coord names
            lat_name = None; lon_name = None
            for n in da.coords:
                ln = n.lower()
                if ln in ("lat","latitude","y"): lat_name = n
                if ln in ("lon","longitude","x"): lon_name = n
            if lat_name is None or lon_name is None:
                return None
            out = []
            for la, lo in zip(lats, lons):
                v = da.sel({lat_name: la, lon_name: lo}, method="nearest").values
                v = float(np.asarray(v).item())
                out.append(v)
            return out
    except Exception as e:
        log(f"  sample fail {nc_path.name}: {type(e).__name__}: {e}")
        return None

# -----------------------------------------------------------------------------
# Unit conversion helpers
# -----------------------------------------------------------------------------
def convert_value(var, val):
    """Apply unit harmonization to match the units string we declare."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    if var in ("tas","tasmax","tasmin","txx"):
        # CCKP serves these in degC already (we saw 11.45 for HUN historical)
        return float(val)
    if var == "pr":
        # CCKP serves pr as mm/day annual climatology -> convert to mm/year
        # If the value is already > 200, assume it's mm/year already
        v = float(val)
        if v < 50:  # mm/day range
            v = v * 365.25
        return v
    # hd35, r20mm: counts/days
    return float(val)

def convert_array(var, arr):
    if arr is None: return None
    return [convert_value(var, v) for v in arr]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    LOG_FILE.write_text("", encoding="utf-8")
    log("=== s06_cckp_fetch start ===")
    cents = load_centroids()
    log(f"Loaded {len(cents)} centroids from {CENTROIDS_CSV.name}")
    lats = cents["lat"].tolist()
    lons = cents["lon"].tolist()
    bnames = cents["borvidek"].tolist()

    fetch_date = datetime.date.today().isoformat()
    summary_rows = []
    sanity_tas_2080_585 = None

    for var, units, desc in VARIABLES:
        for period, scenario in COMBOS:
            rows = []
            for stat_name, pct_token in STATS:
                # 1) API country-level
                url = api_url(var, period, scenario, pct_token)
                j = fetch_api(url)
                country_val_raw = parse_api_value(j)
                country_val = convert_value(var, country_val_raw)

                # 2) S3 district-level
                granularity = "country"
                values = None
                nc = fetch_nc(var, scenario, pct_token, period)
                if nc is not None:
                    sampled = sample_nc_at_points(nc, var, lats, lons)
                    if sampled is not None and not all(np.isnan(s) for s in sampled):
                        values = convert_array(var, sampled)
                        granularity = "district"
                        stats_counter["district_succ"] += 1

                if values is None:
                    if country_val is not None:
                        values = [country_val] * len(bnames)
                        granularity = "country"
                        stats_counter["country_fallback"] += 1
                    else:
                        log(f"  FAIL {var} {scenario} {period} {stat_name} (no API, no S3)")
                        stats_counter["failed"] += 1
                        continue

                src_url = url if granularity == "country" else (
                    f"s3://{S3_BUCKET}/{s3_key(var, scenario, pct_token, period)}"
                )
                for bn, v in zip(bnames, values):
                    rows.append({
                        "borvidek": bn,
                        "variable": var,
                        "scenario": scenario,
                        "period": period,
                        "stat": stat_name,
                        "value": np.float32(v) if v is not None else np.float32("nan"),
                        "units": units,
                        "granularity": granularity,
                        "source": "worldbank_cckp_cmip6",
                        "source_url": src_url,
                        "fetch_date": fetch_date,
                    })

                summary_rows.append({
                    "variable": var,
                    "scenario": scenario,
                    "period": period,
                    "stat": stat_name,
                    "granularity": granularity,
                    "n_districts": len(values) if values else 0,
                    "country_value_raw": country_val_raw,
                    "country_value_conv": country_val,
                })

                # sanity check capture
                if (var=="tas" and scenario=="ssp585" and period=="2080-2099"
                        and stat_name=="mean" and granularity=="district"):
                    sanity_tas_2080_585 = list(zip(bnames, values))

            # Write per-(var, scenario) parquet, but include all periods covered
            if rows:
                out = OUT_DIR / f"cckp_cmip6_{var}_{scenario}_per_district.parquet"
                df_new = pd.DataFrame(rows)
                if out.exists():
                    df_old = pd.read_parquet(out)
                    keep = ~(
                        (df_old["variable"]==var) &
                        (df_old["scenario"]==scenario) &
                        (df_old["period"]==period)
                    )
                    df_old = df_old[keep]
                    df_full = pd.concat([df_old, df_new], ignore_index=True)
                else:
                    df_full = df_new
                df_full.to_parquet(out, index=False)
                log(f"wrote {out.name}: {len(df_full)} rows (added {len(df_new)})")

    # Summary CSV
    sdf = pd.DataFrame(summary_rows)
    sdf.to_csv(OUT_DIR / "cckp_summary.csv", index=False, encoding="utf-8")

    # Verification print-out
    log("=== Verification ===")
    log(f"HTTP requests made:    {stats_counter['http_requests']}")
    log(f"HTTP cache hits:       {stats_counter['http_cached']}")
    log(f"S3 downloads:          {stats_counter['s3_downloads']}")
    log(f"S3 cache hits:         {stats_counter['s3_cached']}")
    log(f"Bytes downloaded:      {stats_counter['bytes_downloaded']:,}  ({stats_counter['bytes_downloaded']/1e6:.1f} MB)")
    log(f"District-granularity successes: {stats_counter['district_succ']}")
    log(f"Country-level fallbacks:        {stats_counter['country_fallback']}")
    log(f"Total failures:                 {stats_counter['failed']}")

    if sanity_tas_2080_585:
        log("Sanity: tas annual mean, 2080-2099 ssp585 (degC) per borvidek:")
        for bn, v in sanity_tas_2080_585:
            log(f"  {bn:<22} {v:6.2f}")
        vals = [v for _,v in sanity_tas_2080_585]
        log(f"  range: {min(vals):.2f} - {max(vals):.2f} (mean {np.mean(vals):.2f})")
    else:
        log("Sanity capture for tas 2080-2099 ssp585 mean unavailable.")

    # File sizes
    log("Output files:")
    for p in sorted(OUT_DIR.glob("*")):
        log(f"  {p.name}: {p.stat().st_size:,} bytes")

    log("=== done ===")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
