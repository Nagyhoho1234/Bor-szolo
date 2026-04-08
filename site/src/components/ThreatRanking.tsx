'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts';

export type ThreatBarRow = {
  borvidek: string;
  baseline: number | null;
  rcp45_2070: number | null;
  rcp85_2070: number | null;
  rcp45_2100: number | null;
  rcp85_2100: number | null;
  cckp_ssp245_2099: number | null;
  cckp_ssp585_2099: number | null;
};

export type ThreatRankingProps = {
  rows: ThreatBarRow[];
  title: string;
  units: string;
  /** True if higher = worse (heat days, drought intensity), false if higher = better (precipitation). */
  worseWhenHigher?: boolean;
  /** Render as a non-interactive snapshot (no toggle chips, no tooltip). */
  staticView?: boolean;
};

const SERIES_OPTIONS: { value: keyof ThreatBarRow; label: string; colour: string }[] = [
  { value: 'baseline', label: 'Now (1991–2020)', colour: '#374151' },
  { value: 'rcp45_2070', label: 'FORESEE 2041–2070 RCP 4.5', colour: '#60a5fa' },
  { value: 'rcp85_2070', label: 'FORESEE 2041–2070 RCP 8.5', colour: '#f87171' },
  { value: 'rcp45_2100', label: 'FORESEE 2071–2100 RCP 4.5', colour: '#1d4ed8' },
  { value: 'rcp85_2100', label: 'FORESEE 2071–2100 RCP 8.5', colour: '#b91c1c' },
  { value: 'cckp_ssp245_2099', label: 'CCKP 2080–2099 SSP2-4.5', colour: '#0ea5e9' },
  { value: 'cckp_ssp585_2099', label: 'CCKP 2080–2099 SSP5-8.5', colour: '#dc2626' },
];

export default function ThreatRanking({
  rows,
  title,
  units,
  worseWhenHigher = true,
  staticView = false,
}: ThreatRankingProps) {
  const [series, setSeries] = useState<(keyof ThreatBarRow)[]>([
    'baseline',
    'rcp85_2100',
    'cckp_ssp585_2099',
  ]);
  const [isNarrow, setIsNarrow] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia('(max-width: 639px)');
    const update = () => setIsNarrow(mq.matches);
    update();
    mq.addEventListener('change', update);
    return () => mq.removeEventListener('change', update);
  }, []);

  const sorted = useMemo(() => {
    const sortKey: keyof ThreatBarRow = series.includes('rcp85_2100')
      ? 'rcp85_2100'
      : series[series.length - 1];
    return [...rows].sort((a, b) => {
      const av = (a[sortKey] as number) ?? -Infinity;
      const bv = (b[sortKey] as number) ?? -Infinity;
      return worseWhenHigher ? bv - av : av - bv;
    });
  }, [rows, series, worseWhenHigher]);

  return (
    <div className={`space-y-3 ${staticView ? 'pointer-events-none' : ''}`}>
      <div className="flex flex-wrap items-center gap-3">
        <h3 className="text-lg font-semibold">{title}</h3>
        <span className="text-xs text-neutral-500">({units})</span>
      </div>
      {staticView ? (
        <div className="flex flex-wrap gap-2 text-xs">
          {SERIES_OPTIONS.filter((o) => series.includes(o.value)).map((o) => (
            <span
              key={o.value}
              className="flex items-center gap-1.5 rounded border border-neutral-300 bg-neutral-50 px-2 py-1"
            >
              <span
                className="inline-block h-2 w-3"
                style={{ backgroundColor: o.colour }}
              />
              {o.label}
            </span>
          ))}
        </div>
      ) : (
        <div className="flex flex-wrap gap-2 text-xs">
          {SERIES_OPTIONS.map((o) => {
            const on = series.includes(o.value);
            return (
              <button
                key={o.value}
                type="button"
                onClick={() =>
                  setSeries(
                    on
                      ? series.filter((s) => s !== o.value)
                      : [...series, o.value],
                  )
                }
                className={`flex items-center gap-1.5 rounded border px-2 py-1 transition ${
                  on
                    ? 'border-neutral-800 bg-neutral-900 text-white'
                    : 'border-neutral-300 bg-white text-neutral-700 hover:border-neutral-500'
                }`}
              >
                <span
                  className="inline-block h-2 w-3"
                  style={{ backgroundColor: o.colour }}
                />
                {o.label}
              </button>
            );
          })}
        </div>
      )}
      <div className="h-[640px] w-full">
        <ResponsiveContainer>
          <BarChart
            data={sorted}
            layout="vertical"
            margin={{ top: 10, right: 12, left: isNarrow ? 4 : 110, bottom: 10 }}
          >
            <CartesianGrid stroke="#e5e5e5" strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" tick={{ fontSize: 10 }} />
            <YAxis
              type="category"
              dataKey="borvidek"
              width={isNarrow ? 86 : 110}
              tick={{ fontSize: isNarrow ? 9 : 11 }}
              interval={0}
            />
            {!staticView && (
              <Tooltip
                formatter={(v) =>
                  typeof v === 'number' ? `${v.toFixed(1)} ${units}` : String(v)
                }
              />
            )}
            {!staticView && <Legend wrapperStyle={{ fontSize: 11 }} />}
            {SERIES_OPTIONS.filter((o) => series.includes(o.value)).map((o) => (
              <Bar
                key={o.value}
                dataKey={o.value}
                name={o.label}
                fill={o.colour}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="text-[11px] text-neutral-500">
        Bars sorted by {worseWhenHigher ? 'highest' : 'lowest'} value of the
        most-recent selected RCP/SSP series. FORESEE = single-model
        CNRM-ALADIN53 high-resolution regional projections; CCKP = World Bank
        CMIP6 0.25° multi-model ensemble mean. Toggle series above to compare.
      </p>
    </div>
  );
}
