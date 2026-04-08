'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
  ReferenceLine,
} from 'recharts';
import type { IndicesAnnualRow } from '@/lib/data';

export type ClimateTrendChartProps = {
  borvidek: string;
  index: keyof IndicesAnnualRow;
  label?: string;
  units?: string;
  /** When true, render as a non-interactive snapshot (no tooltip, no legend interaction).
   *  Inline charts on long pages should be static; the modal-expanded version is interactive. */
  staticView?: boolean;
};

type Row = {
  year: number;
  historical?: number;
  rcp45?: number;
  rcp85?: number;
};

const HIST_END = 2021;

async function fetchScenario(
  scenario: 'rcp45' | 'rcp85',
  borvidek: string,
  index: keyof IndicesAnnualRow
): Promise<{ year: number; value: number }[]> {
  const url = `/data/indices/indices_${scenario}_annual.json`;
  const res = await fetch(url);
  const all = (await res.json()) as IndicesAnnualRow[];
  return all
    .filter((r) => r.borvidek === borvidek)
    .map((r) => ({ year: r.year, value: r[index] as unknown as number }))
    .sort((a, b) => a.year - b.year);
}

function rollingMean(
  series: { year: number; value: number }[],
  window: number
): { year: number; value: number }[] {
  const out: { year: number; value: number }[] = [];
  for (let i = 0; i < series.length; i++) {
    const lo = Math.max(0, i - Math.floor(window / 2));
    const hi = Math.min(series.length, i + Math.ceil(window / 2));
    let s = 0;
    let n = 0;
    for (let j = lo; j < hi; j++) {
      if (Number.isFinite(series[j].value)) {
        s += series[j].value;
        n++;
      }
    }
    out.push({ year: series[i].year, value: n > 0 ? s / n : NaN });
  }
  return out;
}

export default function ClimateTrendChart({
  borvidek,
  index,
  label,
  units,
  staticView = false,
}: ClimateTrendChartProps) {
  const [rcp45, setRcp45] = useState<{ year: number; value: number }[]>([]);
  const [rcp85, setRcp85] = useState<{ year: number; value: number }[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    Promise.all([
      fetchScenario('rcp45', borvidek, index),
      fetchScenario('rcp85', borvidek, index),
    ])
      .then(([a, b]) => {
        if (!alive) return;
        setRcp45(a);
        setRcp85(b);
      })
      .catch((e) => setErr(String(e)));
    return () => {
      alive = false;
    };
  }, [borvidek, index]);

  const data: Row[] = useMemo(() => {
    const sm45 = rollingMean(rcp45, 11);
    const sm85 = rollingMean(rcp85, 11);
    const byYear = new Map<number, Row>();
    // Historical period (1971-2021) is identical in both files (observed
    // stitched in). Put it in its own series in grey.
    for (const r of sm45) {
      const existing = byYear.get(r.year) ?? { year: r.year };
      if (r.year <= HIST_END) {
        existing.historical = r.value;
      } else {
        existing.rcp45 = r.value;
      }
      byYear.set(r.year, existing);
    }
    for (const r of sm85) {
      const existing = byYear.get(r.year) ?? { year: r.year };
      if (r.year > HIST_END) existing.rcp85 = r.value;
      byYear.set(r.year, existing);
    }
    return Array.from(byYear.values()).sort((a, b) => a.year - b.year);
  }, [rcp45, rcp85]);

  if (err) return <div className="text-xs text-red-600">{err}</div>;
  if (data.length === 0)
    return <div className="text-xs text-neutral-500">Loading…</div>;

  return (
    <div
      className={`h-64 w-full ${staticView ? 'pointer-events-none select-none' : ''}`}
    >
      <ResponsiveContainer>
        <ComposedChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
          <XAxis dataKey="year" tick={{ fontSize: 10 }} />
          <YAxis
            tick={{ fontSize: 10 }}
            label={
              units
                ? {
                    value: units,
                    angle: -90,
                    position: 'insideLeft',
                    offset: 10,
                    style: { fontSize: 10 },
                  }
                : undefined
            }
          />
          {!staticView && (
            <Tooltip
              formatter={(v) =>
                typeof v === 'number' ? v.toFixed(1) : String(v)
              }
            />
          )}
          {!staticView && <Legend wrapperStyle={{ fontSize: 11 }} />}
          <ReferenceLine x={HIST_END} stroke="#999" strokeDasharray="3 3" />
          <Line
            type="monotone"
            dataKey="historical"
            name="Observed 1971–2021"
            stroke="#374151"
            strokeWidth={2}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="rcp45"
            name="RCP 4.5"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="rcp85"
            name="RCP 8.5"
            stroke="#dc2626"
            strokeWidth={2}
            dot={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
      {label && (
        <div className="mt-1 text-center text-xs text-neutral-500">{label}</div>
      )}
    </div>
  );
}
