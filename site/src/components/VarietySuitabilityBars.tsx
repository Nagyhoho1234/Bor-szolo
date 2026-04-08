'use client';

import { useMemo, useState } from 'react';

export type VarietySuitabilityRecord = {
  variety: string;
  period: string;
  scenario: string;
  suitability: number;
  colour: 'red' | 'white' | string;
  in_principal_varieties?: boolean;
};

export type VarietyRow = {
  variety: string;
  baseline: number; // 0..1, 1991-2020 observed
  rcp45: number; // 0..1, future under RCP4.5
  rcp85: number; // 0..1, future under RCP8.5
  colour: 'red' | 'white' | string;
};

export type VarietySuitabilityBarsProps = {
  /** All suitability rows for this district (all periods × scenarios). */
  rows: VarietySuitabilityRecord[];
  /** When true, render a fixed snapshot (default 2081-2100) without
   *  the period selector. */
  staticView?: boolean;
};

const PERIOD_OPTIONS: { value: string; label: string }[] = [
  { value: '2021-2040', label: '2021–2040 (near term)' },
  { value: '2041-2060', label: '2041–2060 (≈ +20y)' },
  { value: '2061-2080', label: '2061–2080 (≈ +40y)' },
  { value: '2081-2100', label: '2081–2100 (≈ +60–80y)' },
];

const DEFAULT_PERIOD = '2081-2100';
const TOP_N_NEW = 5;
const EXPANDED_MIN_SUITABILITY = 0.5;

function BarRow({
  d,
  labelW,
}: {
  d: VarietyRow;
  labelW: number;
}) {
  const dot =
    d.colour === 'red'
      ? 'bg-rose-700'
      : d.colour === 'white'
        ? 'bg-amber-200'
        : 'bg-neutral-400';
  return (
    <div className="flex items-center gap-2">
      <div
        className="flex w-[90px] shrink-0 items-center gap-1 text-xs text-neutral-700 sm:w-[var(--label-w)]"
        style={{ ['--label-w' as string]: `${labelW}px` }}
      >
        <span className={`h-2 w-2 shrink-0 rounded-full ${dot}`} />
        <span className="truncate">{d.variety}</span>
      </div>
      <div className="relative h-6 flex-1 overflow-hidden rounded bg-neutral-100">
        <div
          className="absolute left-0 top-0 h-2 bg-slate-500"
          style={{
            width: `${Math.max(0, Math.min(1, d.baseline)) * 100}%`,
          }}
          title={`baseline ${d.baseline.toFixed(2)}`}
        />
        <div
          className="absolute left-0 top-2 h-2 bg-amber-500"
          style={{
            width: `${Math.max(0, Math.min(1, d.rcp45)) * 100}%`,
          }}
          title={`RCP4.5 ${d.rcp45.toFixed(2)}`}
        />
        <div
          className="absolute left-0 top-4 h-2 bg-rose-700"
          style={{
            width: `${Math.max(0, Math.min(1, d.rcp85)) * 100}%`,
          }}
          title={`RCP8.5 ${d.rcp85.toFixed(2)}`}
        />
      </div>
      <div className="hidden w-32 shrink-0 text-right text-[11px] tabular-nums text-neutral-600 sm:block">
        {d.baseline.toFixed(2)} → {d.rcp45.toFixed(2)} /{' '}
        {d.rcp85.toFixed(2)}
      </div>
    </div>
  );
}

export default function VarietySuitabilityBars({
  rows,
  staticView = false,
}: VarietySuitabilityBarsProps) {
  const [period, setPeriod] = useState(DEFAULT_PERIOD);

  // Build a baseline-keyed map once per render
  const baselineMap = useMemo(() => {
    const m = new Map<string, VarietySuitabilityRecord>();
    for (const r of rows) {
      if (r.period === '1991-2020' && r.scenario === 'observed') {
        m.set(r.variety, r);
      }
    }
    return m;
  }, [rows]);

  // Main chart: principal varieties of the district (or, if no flags
  // are present in the data, fall back to the legacy "all varieties"
  // view sorted by max).
  const principalData: VarietyRow[] = useMemo(() => {
    const rcp45 = rows.filter(
      (r) => r.period === period && r.scenario === 'rcp45',
    );
    const rcp85 = rows.filter(
      (r) => r.period === period && r.scenario === 'rcp85',
    );
    const out: VarietyRow[] = [];
    for (const [variety, b] of baselineMap.entries()) {
      // Only include principal varieties in the main chart
      if (b.in_principal_varieties === false) continue;
      const f45 = rcp45.find((x) => x.variety === variety);
      const f85 = rcp85.find((x) => x.variety === variety);
      if (!f45 && !f85) continue;
      out.push({
        variety,
        baseline: b.suitability,
        rcp45: f45 ? f45.suitability : 0,
        rcp85: f85 ? f85.suitability : 0,
        colour: b.colour,
      });
    }
    return out.sort((a, b) => b.baseline - a.baseline);
  }, [rows, period, baselineMap]);

  // Second chart: climate-adapted candidates that are NOT already principal
  // in this district. In the collapsed (staticView) view we cap at TOP_N_NEW
  // candidates to keep the card tight. In the expanded (interactive) view we
  // show every non-principal variety whose max(RCP4.5, RCP8.5) suitability
  // exceeds EXPANDED_MIN_SUITABILITY at the selected period.
  // Ranked by RCP8.5, then RCP4.5, then baseline (so varieties that already
  // work today win the saturation ties at end-century).
  const candidateData: VarietyRow[] = useMemo(() => {
    const rcp45 = rows.filter(
      (r) => r.period === period && r.scenario === 'rcp45',
    );
    const rcp85 = rows.filter(
      (r) => r.period === period && r.scenario === 'rcp85',
    );
    const out: VarietyRow[] = [];
    for (const [variety, b] of baselineMap.entries()) {
      // Only include NON-principal varieties (climate-hedge candidates)
      if (b.in_principal_varieties !== false) continue;
      const f45 = rcp45.find((x) => x.variety === variety);
      const f85 = rcp85.find((x) => x.variety === variety);
      if (!f45 && !f85) continue;
      out.push({
        variety,
        baseline: b.suitability,
        rcp45: f45 ? f45.suitability : 0,
        rcp85: f85 ? f85.suitability : 0,
        colour: b.colour,
      });
    }
    const ranked = out.sort((a, b) => {
      if (b.rcp85 !== a.rcp85) return b.rcp85 - a.rcp85;
      if (b.rcp45 !== a.rcp45) return b.rcp45 - a.rcp45;
      return b.baseline - a.baseline;
    });
    if (staticView) {
      return ranked.slice(0, TOP_N_NEW);
    }
    return ranked.filter(
      (d) => Math.max(d.rcp45, d.rcp85) > EXPANDED_MIN_SUITABILITY,
    );
  }, [rows, period, baselineMap, staticView]);

  if (!rows || rows.length === 0) {
    return (
      <div className="text-xs text-neutral-500">
        No principal varieties listed for this district.
      </div>
    );
  }

  const allBars = [...principalData, ...candidateData];
  const maxLabelLen = Math.max(...allBars.map((d) => d.variety.length), 1);
  const labelW = Math.min(180, Math.max(100, maxLabelLen * 7));

  const currentLabel =
    PERIOD_OPTIONS.find((o) => o.value === period)?.label ?? '';

  return (
    <div className={`w-full ${staticView ? 'pointer-events-none' : ''}`}>
      {/* Period selector + legend (shared by both sub-charts) */}
      <div className="mb-3 flex flex-wrap items-center gap-3">
        {staticView ? (
          <span className="text-xs text-neutral-600">
            Future: <strong>{currentLabel}</strong>
          </span>
        ) : (
          <label className="text-xs text-neutral-600">
            Future period:&nbsp;
            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="rounded border border-neutral-300 bg-white px-2 py-0.5 text-xs"
            >
              {PERIOD_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          </label>
        )}
        <span className="flex items-center gap-1 text-[11px] text-neutral-600">
          <span className="inline-block h-2 w-4 bg-slate-500" /> Baseline
          1991–2020
        </span>
        <span className="flex items-center gap-1 text-[11px] text-neutral-600">
          <span className="inline-block h-2 w-4 bg-amber-500" /> RCP 4.5
          (moderate)
        </span>
        <span className="flex items-center gap-1 text-[11px] text-neutral-600">
          <span className="inline-block h-2 w-4 bg-rose-700" /> RCP 8.5 (high)
        </span>
      </div>

      {/* Main chart: current principal varieties */}
      <div className="mb-2 text-[11px] font-semibold uppercase tracking-wide text-neutral-700">
        Current principal varieties of the district
      </div>
      <div className="flex flex-col gap-2">
        {principalData.length === 0 ? (
          <div className="text-xs text-neutral-500">
            No principal varieties matched in the suitability dataset for this
            district.
          </div>
        ) : (
          principalData.map((d) => (
            <BarRow key={`p-${d.variety}`} d={d} labelW={labelW} />
          ))
        )}
      </div>

      {/* Second chart: climate-adapted candidates not currently grown */}
      <div className="mt-6 mb-2 text-[11px] font-semibold uppercase tracking-wide text-neutral-700">
        {staticView
          ? `Top ${TOP_N_NEW} climate-adapted candidates`
          : `All climate-adapted candidates (suitability > ${EXPANDED_MIN_SUITABILITY})`}{' '}
        (not currently grown here) · ranked by RCP 8.5 at{' '}
        {currentLabel || period}
        {!staticView && candidateData.length > 0 && (
          <span className="ml-1 font-normal normal-case text-neutral-500">
            ({candidateData.length} varieties)
          </span>
        )}
      </div>
      <div className="flex flex-col gap-2">
        {candidateData.length === 0 ? (
          <div className="text-xs text-neutral-500">
            No non-principal varieties meet the suitability floor for this
            period.
          </div>
        ) : (
          candidateData.map((d) => (
            <BarRow key={`c-${d.variety}`} d={d} labelW={labelW} />
          ))
        )}
      </div>

      <p className="mt-3 text-[11px] text-neutral-500">
        Suitability scores combine Huglin Index, Winkler class, frost and heat
        tolerance per variety. Three bars per variety: gray = baseline
        (1991–2020 observed), amber = RCP 4.5, rose = RCP 8.5. The lower
        chart filters to varieties NOT currently in the district&apos;s
        principal list and re-ranks them every time the period changes,
        showing the top {TOP_N_NEW} climate-hedge candidates under RCP 8.5.
        A score near 0 typically means the projected Huglin Index exceeds
        the variety&apos;s upper envelope — read as &quot;variety becomes
        unsuited&quot; rather than &quot;no wine possible&quot;.
      </p>
    </div>
  );
}
