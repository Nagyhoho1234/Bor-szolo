"""
s06b_cckp_extras.py
Fetch ADDITIONAL World Bank CCKP CMIP6 variables per Hungarian wine district.

Extends the original s06_cckp_fetch.py with extreme-weather metrics:
  cdd, cwd, rx5day, rx1day, tnn, fd, gsl (+ tx90p/tn90p if available).

Same schema and S3 / xarray-via-BytesIO pattern as s06_cckp_fetch.py to
bypass the 'ő' non-ASCII path issue on Windows.

IMPORTANT: CMIP6 does NOT directly simulate hail. The closest proxy we can
get from this collection is rx1day (annual maximum 1-day precipitation),
which tracks convective storm intensity. Labels must be honest about this.
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

LOG_FILE = LOG_DIR / "s06b_cckp_extras.log"
FAIL_LOG = LOG_DIR / "cckp_extras_failures.log"

def log(msg):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def fail_log(msg):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}"
    with open(FAIL_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# -----------------------------------------------------------------------------
# Extra variables (var_code, units, description)
# -----------------------------------------------------------------------------
VARIABLES = [
    ("cdd",    "days",    "Annual max consecutive dry days (drought intensity)"),
    ("cwd",    "days",    "Annual max consecutive wet days"),
    ("rx5day", "mm",      "Annual max 5-day precipitation total (flood proxy)"),
    ("rx1day", "mm",      "Annual max 1-day precipitation (convective storm / hail proxy; CMIP6 does NOT model hail directly)"),
    ("tnn",    "degC",    "Annual minimum of daily minimum temperature (frost severity)"),
    ("fd",     "days",    "Frost days (tmin < 0 C)"),
    ("gsl",    "days",    "Growing season length"),
    ("tx90p",  "percent", "Percent of days tmax > 90th percentile (warm days)"),
    ("tn90p",  "percent", "Percent of days tmin > 90th percentile (warm nights)"),
]

COMBOS = [
    ("1995-2014", "historical"),
    ("2040-2059", "ssp245"),
    ("2040-2059", "ssp585"),
    ("2080-2099", "ssp245"),
    ("2080-2099", "ssp585"),
]

STATS = [("mean", "median"), ("p10", "p10"), ("p90", "p90")]

API_BASE = "https://cckpapi.worldbank.org/cckp/v1"
S3_BUCKET = "wbg-cckp"
S3_PREFIX = "data/cmip6-x0.25"
SLEEP = 0.15

stats_counter = {
    "http_requests": 0, "http_cached": 0, "s3_downloads": 0, "s3_cached": 0,
    "bytes_downloaded": 0, "district_succ": 0, "country_fallback": 0,
    "failed": 0, "var_skipped": 0,
}

def load_centroids():
    df = pd.read_csv(CENTROIDS_CSV, encoding="utf-8")
    lat_col = "centroid_lat" if "centroid_lat" in df.columns else "lat"
    lon_col = "centroid_lon" if "centroid_lon" in df.columns else "lon"
    df = df.rename(columns={lat_col: "lat", lon_col: "lon"})
    if "borregio" not in df.columns:
        df["borregio"] = ""
    return df[["borvidek", "borregio", "lat", "lon"]].copy()

# --- API ---
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
        try:
            return json.loads(cp.read_text(encoding="utf-8"))
        except Exception:
            pass
    time.sleep(SLEEP)
    try:
        r = requests.get(url, timeout=60)
    except Exception as e:
        log(f"  API error: {type(e).__name__}: {e}")
        return None
    stats_counter["http_requests"] += 1
    stats_counter["bytes_downloaded"] += len(r.content)
    if r.status_code != 200:
        return None
    try:
        j = r.json()
    except Exception:
        return None
    cp.write_text(json.dumps(j), encoding="utf-8")
    return j

def parse_api_value(j):
    if not j: return None
    data = j.get("data")
    if not data or not isinstance(data, dict): return None
    hun = data.get("HUN")
    if not hun or not isinstance(hun, dict): return None
    vals = list(hun.values())
    if not vals: return None
    try:
        return float(vals[0])
    except Exception:
        return None

# --- S3 ---
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED, retries={"max_attempts": 3}))

def s3_key(var, scenario, pct_token, period):
    return (
        f"{S3_PREFIX}/{var}/ensemble-all-{scenario}/"
        f"climatology-{var}-annual-mean_cmip6-x0.25_ensemble-all-{scenario}_"
        f"climatology_{pct_token}_{period}.nc"
    )

def variable_available(var):
    """Check whether the variable has an 'ensemble-all-historical' folder at all."""
    prefix = f"{S3_PREFIX}/{var}/ensemble-all-historical/"
    r = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix, MaxKeys=1)
    return "Contents" in r and len(r["Contents"]) > 0

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
        log(f"  S3 miss [{key}]: {type(e).__name__}")
        return None

def sample_nc_at_points(nc_path, var, lats, lons):
    try:
        raw = Path(nc_path).read_bytes()
        if raw[:3] == b"CDF":
            bio = io.BytesIO(raw)
            ds = xr.open_dataset(bio, engine="scipy", decode_times=False)
        else:
            bio = io.BytesIO(raw)
            ds = xr.open_dataset(bio, engine="h5netcdf", decode_times=False)
        with ds:
            cand = None
            for name in (var, f"climatology-{var}-annual-mean", "climatology", "annual"):
                if name in ds.data_vars:
                    cand = name; break
            if cand is None:
                for v in ds.data_vars:
                    cand = v; break
            if cand is None:
                return None
            da = ds[cand].squeeze(drop=True)
            lat_name = lon_name = None
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

def convert_value(var, val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    # All extras are already in their declared units from CCKP; just cast.
    return float(val)

def convert_array(var, arr):
    if arr is None: return None
    return [convert_value(var, v) for v in arr]

def main():
    LOG_FILE.write_text("", encoding="utf-8")
    FAIL_LOG.write_text("", encoding="utf-8")
    log("=== s06b_cckp_extras start ===")
    cents = load_centroids()
    log(f"Loaded {len(cents)} centroids")
    lats = cents["lat"].tolist()
    lons = cents["lon"].tolist()
    bnames = cents["borvidek"].tolist()

    fetch_date = datetime.date.today().isoformat()
    summary_rows = []

    # Availability pre-check
    available_vars = []
    for var, units, desc in VARIABLES:
        if variable_available(var):
            available_vars.append((var, units, desc))
            log(f"  available: {var}")
        else:
            log(f"  SKIP (not on bucket): {var}")
            fail_log(f"variable_not_available: {var}")
            stats_counter["var_skipped"] += 1

    for var, units, desc in available_vars:
        for period, scenario in COMBOS:
            rows = []
            for stat_name, pct_token in STATS:
                # country-level API
                url = api_url(var, period, scenario, pct_token)
                j = fetch_api(url)
                country_val_raw = parse_api_value(j)
                country_val = convert_value(var, country_val_raw)

                # district-level S3
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
                        log(f"  FAIL {var} {scenario} {period} {stat_name}")
                        fail_log(f"no_data: {var} {scenario} {period} {stat_name}")
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
                    "description": desc,
                })

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

                # json mirror
                json_out = out.with_suffix(".json")
                df_full.to_json(json_out, orient="records", force_ascii=False, indent=2)

                log(f"wrote {out.name}: {len(df_full)} rows (added {len(df_new)})")

    # Summary CSV — APPEND to existing
    summary_csv = OUT_DIR / "cckp_summary.csv"
    sdf_new = pd.DataFrame(summary_rows)
    if summary_csv.exists():
        try:
            sdf_old = pd.read_csv(summary_csv)
            # drop any overlapping rows first
            keep = ~sdf_old["variable"].isin(sdf_new["variable"].unique())
            sdf_old = sdf_old[keep]
            sdf_full = pd.concat([sdf_old, sdf_new], ignore_index=True)
        except Exception:
            sdf_full = sdf_new
    else:
        sdf_full = sdf_new
    sdf_full.to_csv(summary_csv, index=False, encoding="utf-8")
    log(f"wrote {summary_csv.name}: {len(sdf_full)} rows")

    log("=== Verification ===")
    for k, v in stats_counter.items():
        log(f"  {k}: {v}")

    # rx1day sanity
    log("Sanity rx1day historical mean (mm):")
    try:
        p = OUT_DIR / "cckp_cmip6_rx1day_historical_per_district.parquet"
        if p.exists():
            d = pd.read_parquet(p)
            d = d[(d.period=="1995-2014")&(d.stat=="mean")]
            for _, r in d.iterrows():
                log(f"  {r.borvidek:<22} {r.value:6.2f}")
    except Exception as e:
        log(f"  sanity fail: {e}")

    log("Output extras files:")
    total_bytes = 0
    for p in sorted(OUT_DIR.glob("cckp_cmip6_*")):
        sz = p.stat().st_size
        total_bytes += sz
        log(f"  {p.name}: {sz:,} bytes")
    log(f"TOTAL cckp dir: {total_bytes:,} bytes ({total_bytes/1e6:.2f} MB)")
    log("=== done ===")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
