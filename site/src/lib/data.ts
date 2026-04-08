// Data loaders for the curated bundle.
//
// DESIGN DECISION: All parquet files are converted to JSON at sync time by
// `scripts/sync_curated.mjs` (using pyarrow). The browser therefore only
// needs `fetch + JSON.parse`, which is much more robust under Next.js
// `output: 'export'` than wiring up parquet-wasm + its WASM blob. The
// original .parquet files are still published under /data/ for the
// downloads page.
//
// All loaders are in-memory-cached by URL so the same file is fetched once
// per session.

import type { FeatureCollection, Feature, Geometry } from 'geojson';

export type Scenario = 'observed' | 'rcp45' | 'rcp85';
export type Period =
  | '1971-2000'
  | '1991-2020'
  | '2021-2040'
  | '2041-2060'
  | '2061-2080'
  | '2081-2100';

export type IndicesAnnualRow = {
  year: number;
  borvidek: string;
  borregio: string;
  winkler_gdd: number;
  huglin_index: number;
  spring_frost_days: number;
  last_spring_frost_doy: number;
  heat_days_t35: number;
  extreme_heat_days_t38: number;
  growing_season_precip: number;
  hargreaves_pet: number;
  p_minus_pet: number;
  cool_night_index: number;
};

export type NormalsRow = {
  borvidek: string;
  borregio: string;
  period: string;
  scenario: string;
  index: string;
  mean: number;
  std: number;
  p10: number;
  p50: number;
  p90: number;
  trend_per_decade: number | null;
  mk_pvalue: number | null;
  anomaly_vs_1991_2020: number | null;
  anomaly_pct: number | null;
  risk_flag: string | null;
};

export type SuitabilityRow = {
  borvidek: string;
  borregio: string;
  variety: string;
  variety_en: string;
  period: string;
  scenario: string;
  huglin_mean: number;
  winkler_mean: number;
  frost_days_mean: number;
  heat_days_mean: number;
  huglin_score: number;
  winkler_ok: boolean;
  frost_score: number;
  heat_score: number;
  suitability: number;
  limiting_factor: string | null;
  colour: 'red' | 'white' | string;
  confidence: string;
  in_principal_varieties: boolean;
  delta_vs_1991_2020: number;
};

export type HeadlineRow = {
  borvidek: string;
  biggest_winner_variety: string;
  winner_delta: number;
  biggest_loser_variety: string;
  loser_delta: number;
  current_suitability_loser: number;
  future_suitability_loser: number;
};

export type CckpRow = {
  borvidek: string;
  variable: string;
  scenario: string;
  period: string;
  stat: string;
  value: number;
  units: string;
  granularity: string;
  source: string;
  source_url: string;
  fetch_date: string;
};

export type DistrictExtremesOutlook = {
  summary: string;
  summary_hu?: string;
  hail_caveat: string;
  hail_caveat_hu?: string;
  metrics: Record<string, number>;
  source: string;
  source_url: string;
};

export type DistrictDescription = {
  borvidek: string;
  name_hu: string;
  name_en: string;
  slug?: string;
  tagline: string;
  tagline_hu?: string;
  elevator_pitch: string;
  elevator_pitch_hu?: string;
  flagship_wines: string[];
  flagship_wines_hu?: string[];
  principal_grapes_summary: string;
  principal_grapes_summary_hu?: string;
  terroir_summary: string;
  terroir_summary_hu?: string;
  climate_today: string;
  climate_today_hu?: string;
  climate_threat_headline: string;
  climate_threat_headline_hu?: string;
  climate_winner_loser: string;
  climate_winner_loser_hu?: string;
  key_facts: { label: string; value: string }[];
  key_facts_hu?: { label_hu: string; value_hu: string }[];
  top_sources: { title: string; url: string }[];
  climate_extremes_outlook?: DistrictExtremesOutlook;
};

/**
 * Returns a "view object" with all description fields collapsed to whichever
 * locale's value is present. Falls back to English when the HU field is empty
 * or missing. Use this whenever rendering description fields in JSX so that
 * /hu/* pages display the Hungarian translations.
 */
export function localizeDescription(
  d: DistrictDescription | null | undefined,
  locale: string,
): DistrictDescription | null {
  if (!d) return null;
  const isHu = locale === 'hu';
  if (!isHu) return d;
  const pick = <T,>(hu: T | undefined, en: T): T =>
    hu !== undefined && hu !== null && (typeof hu !== 'string' || hu.length > 0)
      ? hu
      : en;
  return {
    ...d,
    tagline: pick(d.tagline_hu, d.tagline),
    elevator_pitch: pick(d.elevator_pitch_hu, d.elevator_pitch),
    flagship_wines: pick(d.flagship_wines_hu, d.flagship_wines),
    principal_grapes_summary: pick(
      d.principal_grapes_summary_hu,
      d.principal_grapes_summary,
    ),
    terroir_summary: pick(d.terroir_summary_hu, d.terroir_summary),
    climate_today: pick(d.climate_today_hu, d.climate_today),
    climate_threat_headline: pick(
      d.climate_threat_headline_hu,
      d.climate_threat_headline,
    ),
    climate_winner_loser: pick(
      d.climate_winner_loser_hu,
      d.climate_winner_loser,
    ),
    key_facts: d.key_facts_hu?.length
      ? d.key_facts_hu.map((kf) => ({ label: kf.label_hu, value: kf.value_hu }))
      : d.key_facts,
    climate_extremes_outlook: d.climate_extremes_outlook
      ? {
          ...d.climate_extremes_outlook,
          summary: pick(
            d.climate_extremes_outlook.summary_hu,
            d.climate_extremes_outlook.summary,
          ),
          hail_caveat: pick(
            d.climate_extremes_outlook.hail_caveat_hu,
            d.climate_extremes_outlook.hail_caveat,
          ),
        }
      : undefined,
  };
}

export type Manifest = {
  bundle_name: string;
  version: string;
  generated_at: string;
  license: string;
  citation_required: string[];
  files: Array<{
    path: string;
    type: string;
    size_bytes: number;
    rows?: number;
    columns?: string[];
    description?: string;
  }>;
  totals?: Record<string, unknown>;
  headline?: Record<string, unknown>;
  draft_flags?: string[];
};

// ---- Base URL helper ----
// On the server (Node, at build time), we read directly from the filesystem
// under site/public/data/ because there is no HTTP origin during SSG for a
// statically-exported Next.js app.
// In the browser we hit /data/ via fetch.
const DATA_BASE = '/data';
const isServer = typeof window === 'undefined';

// ---- Per-URL in-memory cache ----
const cache = new Map<string, Promise<unknown>>();

async function readServerFile(urlPath: string): Promise<string> {
  // Only imported on the server side — never bundled into client code.
  const fs = await import('node:fs/promises');
  const path = await import('node:path');
  const rel = urlPath.replace(/^\/+/, '');
  const abs = path.join(process.cwd(), 'public', rel);
  return fs.readFile(abs, 'utf-8');
}

async function fetchJson<T>(url: string): Promise<T> {
  let pending = cache.get(url) as Promise<T> | undefined;
  if (pending) return pending;
  pending = (async () => {
    if (isServer) {
      const text = await readServerFile(url);
      return JSON.parse(text) as T;
    }
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`fetch ${url} failed: ${res.status}`);
    }
    return (await res.json()) as T;
  })();
  cache.set(url, pending);
  return pending;
}

async function fetchText(url: string): Promise<string> {
  if (isServer) return readServerFile(url);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url} failed: ${res.status}`);
  return res.text();
}

// ---- CSV (tiny) parser for headline_winners_losers.csv ----
function parseCsv(text: string): Record<string, string>[] {
  const lines = text.replace(/\r\n/g, '\n').split('\n').filter((l) => l.length);
  if (lines.length === 0) return [];
  const header = lines[0].split(',');
  const rows: Record<string, string>[] = [];
  for (let i = 1; i < lines.length; i++) {
    // Simple parser — handles quoted fields with commas
    const row: Record<string, string> = {};
    const cells: string[] = [];
    let cur = '';
    let inQuotes = false;
    for (let j = 0; j < lines[i].length; j++) {
      const c = lines[i][j];
      if (c === '"' && lines[i][j + 1] === '"') {
        cur += '"';
        j++;
      } else if (c === '"') {
        inQuotes = !inQuotes;
      } else if (c === ',' && !inQuotes) {
        cells.push(cur);
        cur = '';
      } else {
        cur += c;
      }
    }
    cells.push(cur);
    header.forEach((h, k) => (row[h] = cells[k] ?? ''));
    rows.push(row);
  }
  return rows;
}

// ---- Loaders ----

export async function loadDistricts(): Promise<
  FeatureCollection<Geometry, { borvidek: string; borregio: string; n_settlements: number; area_km2: number }>
> {
  return fetchJson(`${DATA_BASE}/wine_districts.geojson`);
}

export async function loadIndicesAnnual(
  scenario: 'rcp45' | 'rcp85'
): Promise<IndicesAnnualRow[]> {
  return fetchJson(`${DATA_BASE}/indices/indices_${scenario}_annual.json`);
}

export async function loadNormals(
  period: Period,
  scenario: Scenario | 'observed'
): Promise<NormalsRow[]> {
  // The curated file-naming convention is:
  //   1971-2000 + observed    -> normals_1971-2000_per_district
  //   1991-2020 + observed    -> normals_1991-2020_per_district
  //   2021-2040 + rcp45/rcp85 -> normals_2021-2040_rcpXX_per_district
  //   2041-2060 + rcp45/rcp85 -> normals_2041-2060_rcpXX_per_district
  //   2061-2080 + rcp45/rcp85 -> normals_2061-2080_rcpXX_per_district
  //   2081-2100 + rcp45/rcp85 -> normals_2081-2100_rcpXX_per_district
  const isObserved = period === '1971-2000' || period === '1991-2020';
  const tag = isObserved ? period : `${period}_${scenario}`;
  return fetchJson(`${DATA_BASE}/normals/normals_${tag}_per_district.json`);
}

export async function loadSuitabilityLong(): Promise<SuitabilityRow[]> {
  // Full ~6 MB monolith. Only callers that genuinely need every district in
  // one go (e.g. cross-district comparison pages) should use this. For a
  // single district detail page, use loadSuitabilityByDistrict(slug) instead
  // — it fetches ~290 KB of already-filtered rows.
  return fetchJson(`${DATA_BASE}/variety_match/suitability_long.json`);
}

export async function loadSuitabilityByDistrict(
  slug: string
): Promise<SuitabilityRow[]> {
  return fetchJson(`${DATA_BASE}/variety_match/by_district/${slug}.json`);
}

export async function loadHeadlineWinnersLosers(): Promise<HeadlineRow[]> {
  const url = `${DATA_BASE}/variety_match/headline_winners_losers.csv`;
  let pending = cache.get(url) as Promise<HeadlineRow[]> | undefined;
  if (pending) return pending;
  pending = (async () => {
    const text = await fetchText(url);
    const raw = parseCsv(text);
    return raw.map((r) => ({
      borvidek: r.borvidek,
      biggest_winner_variety: r.biggest_winner_variety,
      winner_delta: parseFloat(r.winner_delta),
      biggest_loser_variety: r.biggest_loser_variety,
      loser_delta: parseFloat(r.loser_delta),
      current_suitability_loser: parseFloat(r.current_suitability_loser),
      future_suitability_loser: parseFloat(r.future_suitability_loser),
    }));
  })();
  cache.set(url, pending);
  return pending;
}

export async function loadCckp(
  variable: 'hd35' | 'pr' | 'tas' | 'tasmax' | 'tasmin' | 'tnn' | 'txx' | string,
  scenario: 'historical' | 'ssp245' | 'ssp585'
): Promise<CckpRow[]> {
  return fetchJson(
    `${DATA_BASE}/cckp/cckp_cmip6_${variable}_${scenario}_per_district.json`
  );
}

export async function loadManifest(): Promise<Manifest> {
  return fetchJson(`${DATA_BASE}/manifest.json`);
}

// ---- Variety replacement recommendations ----
// One JSON per district at /data/variety_replacements/<slug>.json. Contains
// the model's top replacement candidates per (period × scenario) horizon —
// up to 8 horizons (4 future bins × 2 RCPs). Some districts may be missing
// individual horizons if every candidate failed the suitability gate; the
// loader simply returns whatever is present.
export type ReplacementCandidate = {
  rank: number;
  variety: string;
  variety_en: string;
  colour: 'red' | 'white' | string;
  future_suitability: number;
  delta: number;
  confidence: string;
  limiting_factor: string | null;
  status: string; // "new" or "existing principal"
  huglin_mean?: number;
  winkler_mean?: number;
};

export type ReplacementHorizon = {
  period: string;
  scenario: string;
  at_risk_principal_varieties: Array<{
    variety: string;
    variety_en: string;
    colour: 'red' | 'white' | string;
    future_suitability: number;
    delta: number;
    limiting_factor: string | null;
  }>;
  replacement_candidates: ReplacementCandidate[];
};

export type ReplacementDoc = {
  borvidek: string;
  borregio: string;
  slug: string;
  current_principal_varieties: Array<{
    variety: string;
    variety_en: string;
    colour: 'red' | 'white' | string;
    suitability: number;
  }>;
  horizons: Record<string, ReplacementHorizon>;
};

export async function loadReplacements(
  slug: string
): Promise<ReplacementDoc | null> {
  try {
    return await fetchJson<ReplacementDoc>(
      `${DATA_BASE}/variety_replacements/${slug}.json`
    );
  } catch {
    return null;
  }
}

// ---- HungaroMet ODP station observations (2020-2024) ----
// One row per (district, year). The "annual mean temperature" and
// "annual total precipitation" measured at the weather station nearest to
// each district centroid. Used as a credibility-anchor sanity check on the
// FORESEE projections elsewhere on the district page.
export type OdpStationRow = {
  borvidek: string;
  year: number;
  station_id: number;
  station_name: string;
  station_lat: number;
  station_lon: number;
  distance_km: number;
  tmean_c: number;
  precip_mm: number;
  n_days: number;
  source: string;
  source_url: string;
  license: string;
};

export type OdpAssignmentRow = {
  borvidek: string;
  station_id: number;
  station_name: string;
  station_lat: number;
  station_lon: number;
  distance_km: number;
};

export async function loadOdpMetAssignments(): Promise<OdpAssignmentRow[]> {
  const url = `${DATA_BASE}/odpmethu/district_station_assignments.csv`;
  let pending = cache.get(url) as Promise<OdpAssignmentRow[]> | undefined;
  if (pending) return pending;
  pending = (async () => {
    const text = await fetchText(url);
    const raw = parseCsv(text);
    return raw.map((r) => ({
      borvidek: r.borvidek,
      station_id: parseInt(r.station_id, 10),
      station_name: r.station_name,
      station_lat: parseFloat(r.station_lat),
      station_lon: parseFloat(r.station_lon),
      distance_km: parseFloat(r.distance_km),
    }));
  })();
  cache.set(url, pending);
  return pending;
}

export async function loadOdpMetStation(slug: string): Promise<OdpStationRow[]> {
  // The bundled JSON contains all districts in one file (~46 KB). We load
  // it once (cached by URL) and filter to the requested district. The
  // `slug` arg is the URL slug (e.g. "tokaji"); we resolve it against the
  // borvidek name via the assignments file the caller already loaded, but
  // for callers that just want filtering by slug we also accept a direct
  // borvidek-name match by lowercasing and stripping diacritics.
  try {
    const all = await fetchJson<OdpStationRow[]>(
      `${DATA_BASE}/odpmethu/odp_station_annual_per_district.json`,
    );
    const norm = (s: string) =>
      s
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '');
    const target = norm(slug);
    const rows = all.filter((r) => norm(r.borvidek) === target);
    rows.sort((a, b) => a.year - b.year);
    return rows;
  } catch {
    return [];
  }
}

// District descriptions: aggregated as one file (slug -> DistrictDescription)
// or per-slug files under /data/descriptions/<slug>.json
export async function loadDescriptions(): Promise<Record<string, DistrictDescription>> {
  return fetchJson(`${DATA_BASE}/descriptions.json`);
}

export async function loadDescription(
  slug: string
): Promise<DistrictDescription | null> {
  try {
    return await fetchJson(`${DATA_BASE}/descriptions/${slug}.json`);
  } catch {
    return null;
  }
}

// ---- Convenience selectors ----

export function selectForDistrict<T extends { borvidek: string }>(
  rows: T[],
  borvidek: string
): T[] {
  return rows.filter((r) => r.borvidek === borvidek);
}

export function selectIndex<T extends { index: string }>(
  rows: T[],
  index: string
): T | undefined {
  return rows.find((r) => r.index === index);
}
