"""
s08_odpmethu_fetch.py
Fetch HungaroMet (odp.met.hu) station observations and aggregate per Hungarian
wine district.

Source discovery:
  The daily 'synoptic CSV' endpoint at
    https://odp.met.hu/weather/weather_reports/synoptic/hungary/daily/csv/
  turned out to be a rolling ~10-day archive (one zipped CSV per date, only
  ~18 files total when inspected). It is not suitable for multi-year climate
  aggregation.

  The authoritative multi-decadal endpoint we actually use is:
    https://odp.met.hu/climate/observations_hungary/daily/historical/
  which holds one HABP_1D_<station>_<from>_<to>_hist.zip per automatic station,
  covering 2002-01-01 through 2025-12-31 for the long-lived stations.
  Station metadata:
    https://odp.met.hu/climate/observations_hungary/meta/station_meta_auto.csv

Downloaded subset (to keep bandwidth bounded):
  * Station metadata CSV (~50 kB).
  * For each of the 22 Hungarian wine-district centroids, the 1 nearest
    automatic station with data covering 2020-2024 (so at most 22 distinct
    station files, typically ~500 kB each). This keeps total traffic well
    under 15 MB. We then compute annual mean tmean and annual total precip
    for each year 2020-2024 per district.

Output:
  analysis/curated/odpmethu/odp_station_annual_per_district.parquet + .json
  analysis/curated/odpmethu/README.md

License: HungaroMet ODP is CC-BY-SA, see
  https://odp.met.hu/ODP_General_Terms_of_Use.pdf
"""
import os, sys, io, json, time, datetime, traceback, math, zipfile, re
from pathlib import Path

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
# Force stdout to UTF-8 so Hungarian station names (ő, á, é) don't crash print()
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import requests
import pandas as pd
import numpy as np

ROOT = Path(r"C:\Bor-szőlő\analysis")
CENTROIDS_CSV = ROOT / "geo" / "wine_districts_centroids.csv"
CACHE_DIR = ROOT / "interim" / "odpmethu_cache"
OUT_DIR = ROOT / "curated" / "odpmethu"
LOG_DIR = ROOT / "logs"
for d in (CACHE_DIR, OUT_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "s08_odpmethu_fetch.log"
def log(msg):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

BASE = "https://odp.met.hu"
META_URL = f"{BASE}/climate/observations_hungary/meta/station_meta_auto.csv"
HIST_DIR = f"{BASE}/climate/observations_hungary/daily/historical/"
TARGET_YEARS = list(range(2020, 2025))   # 2020..2024 inclusive (5 years)
SLEEP = 0.25

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2*R*math.asin(math.sqrt(a))

def load_centroids():
    df = pd.read_csv(CENTROIDS_CSV, encoding="utf-8")
    lat_col = "centroid_lat" if "centroid_lat" in df.columns else "lat"
    lon_col = "centroid_lon" if "centroid_lon" in df.columns else "lon"
    df = df.rename(columns={lat_col: "lat", lon_col: "lon"})
    return df[["borvidek", "lat", "lon"]].copy()

def fetch_station_meta():
    cache = CACHE_DIR / "station_meta_auto.csv"
    if cache.exists():
        raw = cache.read_bytes()
    else:
        r = requests.get(META_URL, timeout=60)
        r.raise_for_status()
        raw = r.content
        cache.write_bytes(raw)
        log(f"downloaded station meta {len(raw):,} bytes")
    txt = raw.decode("utf-8", errors="replace")
    rows = []
    lines = txt.splitlines()
    header_idx = 0
    for i, l in enumerate(lines):
        if l.lstrip().startswith("StationNumber"):
            header_idx = i; break
    for l in lines[header_idx+1:]:
        if not l.strip() or ";" not in l:
            continue
        parts = [p.strip() for p in l.split(";")]
        if len(parts) < 8:
            continue
        try:
            sid = int(parts[0])
            start = int(parts[1])
            end = int(parts[2])
            lat = float(parts[3])
            lon = float(parts[4])
            elev = float(parts[5])
            name = parts[6].strip()
            region = parts[7].strip()
        except Exception:
            continue
        rows.append({
            "station_id": sid, "start": start, "end": end,
            "lat": lat, "lon": lon, "elev": elev,
            "name": name, "region": region,
        })
    df = pd.DataFrame(rows)
    # keep rows covering target years: start <= 20200101 and end >= 20241231
    keep = (df["start"] <= 20200101) & (df["end"] >= 20241231)
    df = df[keep].copy()
    # dedupe by station_id (keep widest span)
    df = df.sort_values("end", ascending=False).drop_duplicates("station_id")
    log(f"station meta: {len(df)} active stations covering 2020-2024")
    return df.reset_index(drop=True)

def list_historical_files():
    cache = CACHE_DIR / "historical_listing.html"
    if cache.exists():
        html = cache.read_text(encoding="utf-8", errors="replace")
    else:
        r = requests.get(HIST_DIR, timeout=60)
        r.raise_for_status()
        html = r.text
        cache.write_text(html, encoding="utf-8")
    files = re.findall(r'href="(HABP_1D_\d+_\d+_\d+_hist\.zip)"', html)
    # map station_id -> best (widest/most recent end) file
    bucket = {}
    for f in files:
        m = re.match(r'HABP_1D_(\d+)_(\d+)_(\d+)_hist\.zip', f)
        if not m: continue
        sid = int(m.group(1)); start = int(m.group(2)); end = int(m.group(3))
        prev = bucket.get(sid)
        if prev is None or end > prev[2]:
            bucket[sid] = (f, start, end)
    return bucket

def download_station_file(filename):
    cache = CACHE_DIR / filename
    if cache.exists() and cache.stat().st_size > 0:
        return cache
    url = HIST_DIR + filename
    time.sleep(SLEEP)
    r = requests.get(url, timeout=120)
    if r.status_code != 200:
        log(f"  HTTP {r.status_code} for {filename}")
        return None
    cache.write_bytes(r.content)
    log(f"  downloaded {filename} ({len(r.content):,} B)")
    return cache

def parse_station_csv(zip_path):
    """Return DataFrame with columns: date, tmean, tmin, tmax, precip."""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            name = zf.namelist()[0]
            with zf.open(name) as f:
                raw = f.read().decode("utf-8", errors="replace")
    except Exception as e:
        log(f"  zip fail {zip_path.name}: {e}")
        return None
    # skip meta lines starting with '#'
    lines = [l for l in raw.splitlines() if l and not l.startswith("#") and not l.startswith("##")]
    if not lines:
        return None
    # find header
    header_idx = None
    for i, l in enumerate(lines):
        if "Time" in l and "StationNumber" in l:
            header_idx = i; break
    if header_idx is None:
        return None
    header = [h.strip() for h in lines[header_idx].split(";")]
    data_lines = lines[header_idx+1:]
    rows = []
    for l in data_lines:
        parts = [p.strip() for p in l.split(";")]
        if len(parts) < len(header):
            continue
        d = dict(zip(header, parts))
        try:
            dt = d.get("Time", "")
            if not dt or len(dt) != 8:
                continue
            t = d.get("t", "").strip()
            tn = d.get("tn", "").strip()
            tx = d.get("tx", "").strip()
            rau = d.get("rau", "").strip()
            def flt(x):
                if x in ("", "-999", "-999.0"): return np.nan
                try: return float(x)
                except: return np.nan
            rows.append({
                "date": dt, "tmean": flt(t), "tmin": flt(tn),
                "tmax": flt(tx), "precip": flt(rau),
            })
        except Exception:
            continue
    if not rows:
        return None
    df = pd.DataFrame(rows)
    df["year"] = df["date"].str[:4].astype(int)
    return df

def main():
    LOG_FILE.write_text("", encoding="utf-8")
    log("=== s08_odpmethu_fetch start ===")
    cents = load_centroids()
    log(f"loaded {len(cents)} wine-district centroids")

    meta = fetch_station_meta()
    if meta.empty:
        log("no active stations found — abort")
        return

    hist_files = list_historical_files()
    log(f"historical archive has {len(hist_files)} distinct stations")

    # For each district, pick the nearest station that also has a historical file
    meta_with_file = meta[meta["station_id"].isin(hist_files.keys())].copy()
    log(f"{len(meta_with_file)} stations have both meta + historical zip")

    assignments = []
    for _, c in cents.iterrows():
        best = None
        for _, s in meta_with_file.iterrows():
            d = haversine_km(c.lat, c.lon, s.lat, s.lon)
            if best is None or d < best["distance_km"]:
                best = {
                    "borvidek": c.borvidek,
                    "station_id": int(s.station_id),
                    "station_name": s["name"],
                    "station_lat": float(s.lat),
                    "station_lon": float(s.lon),
                    "distance_km": d,
                }
        assignments.append(best)
    adf = pd.DataFrame(assignments)
    log(f"district -> station mapping (distance km):")
    for _, r in adf.iterrows():
        log(f"  {r.borvidek:<22} -> {r.station_id} {r.station_name:<40} {r.distance_km:5.1f} km")
    log(f"mean distance: {adf['distance_km'].mean():.1f} km  |  max: {adf['distance_km'].max():.1f} km")

    # Download the unique station files
    unique_sids = sorted(adf["station_id"].unique())
    log(f"downloading {len(unique_sids)} unique station files...")
    station_dfs = {}
    for sid in unique_sids:
        fname = hist_files[sid][0]
        zp = download_station_file(fname)
        if zp is None:
            continue
        df = parse_station_csv(zp)
        if df is None:
            log(f"  parse fail {sid}")
            continue
        station_dfs[sid] = df

    log(f"parsed {len(station_dfs)} stations successfully")

    # Aggregate: for each (district, station, year) in TARGET_YEARS, compute
    # annual mean tmean and annual total precip.
    out_rows = []
    for _, a in adf.iterrows():
        sid = a["station_id"]
        sdf = station_dfs.get(sid)
        if sdf is None:
            continue
        for y in TARGET_YEARS:
            ydf = sdf[sdf["year"] == y]
            if len(ydf) < 200:   # require at least ~55% coverage
                continue
            tmean = float(ydf["tmean"].mean(skipna=True)) if ydf["tmean"].notna().any() else np.nan
            precip = float(ydf["precip"].sum(skipna=True)) if ydf["precip"].notna().any() else np.nan
            n_days = int(ydf["tmean"].notna().sum())
            out_rows.append({
                "borvidek": a["borvidek"],
                "year": y,
                "station_id": sid,
                "station_name": a["station_name"],
                "station_lat": a["station_lat"],
                "station_lon": a["station_lon"],
                "distance_km": round(float(a["distance_km"]), 2),
                "tmean_c": round(tmean, 2) if not np.isnan(tmean) else None,
                "precip_mm": round(precip, 1) if not np.isnan(precip) else None,
                "n_days": n_days,
                "source": "hungaromet_odp",
                "source_url": f"{HIST_DIR}{hist_files[sid][0]}",
                "license": "CC-BY-SA (see https://odp.met.hu/ODP_General_Terms_of_Use.pdf)",
            })

    out_df = pd.DataFrame(out_rows)
    log(f"produced {len(out_df)} (district,year) rows")
    parquet = OUT_DIR / "odp_station_annual_per_district.parquet"
    out_df.to_parquet(parquet, index=False)
    json_out = OUT_DIR / "odp_station_annual_per_district.json"
    out_df.to_json(json_out, orient="records", force_ascii=False, indent=2)
    log(f"wrote {parquet.name} ({parquet.stat().st_size:,} B)")
    log(f"wrote {json_out.name}  ({json_out.stat().st_size:,} B)")

    # Station directory export too
    adf_out = adf.copy()
    adf_out["distance_km"] = adf_out["distance_km"].round(2)
    adf_out.to_csv(OUT_DIR / "district_station_assignments.csv", index=False, encoding="utf-8")

    log("=== done ===")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
