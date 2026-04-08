import Sparkline from './Sparkline';

export type IndexCardProps = {
  label: string;
  units?: string;
  /** Baseline period mean (1991–2020 observed) */
  baseline: number | null;
  /** Future period mean (2071–2100 RCP8.5) */
  future: number | null;
  /** Optional annual series for the sparkline (RCP8.5 is typical) */
  sparkSeries?: number[];
  /** Optional risk flag string (e.g. "heat_risk", "winkler_class_shift:Ib->IV") */
  riskFlag?: string | null;
  /** True if "higher future is worse" (e.g. heat_days). Controls delta colouring. */
  worseWhenHigher?: boolean;
};

function fmt(v: number | null | undefined, digits = 1): string {
  if (v == null || !Number.isFinite(v)) return '—';
  return v.toFixed(digits);
}

export default function IndexCard({
  label,
  units,
  baseline,
  future,
  sparkSeries,
  riskFlag,
  worseWhenHigher = true,
}: IndexCardProps) {
  const delta =
    baseline != null && future != null ? future - baseline : null;
  const deltaBad =
    delta == null
      ? false
      : worseWhenHigher
        ? delta > 0
        : delta < 0;

  return (
    <div className="flex flex-col gap-1 rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
      <div className="text-xs font-medium uppercase tracking-wide text-neutral-500">
        {label}
      </div>
      <div className="mt-0.5 flex items-baseline gap-1">
        <span className="text-2xl font-semibold">{fmt(baseline)}</span>
        {units && (
          <span className="text-xs text-neutral-500">{units}</span>
        )}
      </div>
      <div className="text-xs text-neutral-500">
        →{' '}
        <span className="font-medium text-neutral-800">{fmt(future)}</span>
        {delta != null && (
          <>
            {'  '}
            <span
              className={
                deltaBad
                  ? 'font-medium text-red-600'
                  : 'font-medium text-emerald-600'
              }
            >
              {delta > 0 ? '+' : ''}
              {fmt(delta)}
            </span>
          </>
        )}
      </div>
      {sparkSeries && sparkSeries.length > 2 && (
        <div className="mt-1">
          <Sparkline data={sparkSeries} />
        </div>
      )}
      {riskFlag && (
        <div className="mt-1 text-[10px] uppercase tracking-wide text-amber-700">
          {riskFlag.replace(/_/g, ' ')}
        </div>
      )}
    </div>
  );
}
