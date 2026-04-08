import { getTranslations } from 'next-intl/server';
import ChartModal from '@/components/ChartModal';
import type { ReplacementDoc, ReplacementCandidate } from '@/lib/data';

// Server Component. The whole section, including the inline default view
// (top 4 candidates @ 2081-2100 RCP8.5) and the modal `expanded` slot
// (full 8-horizon grid), is rendered on the server. ChartModal itself is a
// client component but we only pass it server-rendered ReactNodes.

export type VarietyReplacementsProps = {
  doc: ReplacementDoc | null;
  borvidek: string;
  locale: string;
};

const ALL_HORIZON_KEYS: Array<{ period: string; scenario: 'rcp45' | 'rcp85' }> = [
  { period: '2021-2040', scenario: 'rcp45' },
  { period: '2021-2040', scenario: 'rcp85' },
  { period: '2041-2060', scenario: 'rcp45' },
  { period: '2041-2060', scenario: 'rcp85' },
  { period: '2061-2080', scenario: 'rcp45' },
  { period: '2061-2080', scenario: 'rcp85' },
  { period: '2081-2100', scenario: 'rcp45' },
  { period: '2081-2100', scenario: 'rcp85' },
];

function colourDot(colour: string) {
  const cls =
    colour === 'red'
      ? 'bg-rose-700'
      : colour === 'white'
        ? 'bg-amber-300 ring-1 ring-amber-500'
        : 'bg-neutral-400';
  return (
    <span
      aria-hidden
      className={`inline-block h-3 w-3 shrink-0 rounded-full ${cls}`}
    />
  );
}

function fmtDelta(d: number): string {
  const sign = d > 0 ? '+' : '';
  return `${sign}${d.toFixed(2)}`;
}

function deltaClass(d: number): string {
  if (d > 0.05) return 'text-emerald-700';
  if (d < -0.05) return 'text-rose-700';
  return 'text-neutral-600';
}

export default async function VarietyReplacements({
  doc,
  borvidek,
  locale,
}: VarietyReplacementsProps) {
  const t = await getTranslations({
    locale,
    namespace: 'districts.detail.replacements',
  });

  if (!doc) return null;

  const sortedByRank = (cands: ReplacementCandidate[]) =>
    [...cands].sort(
      (a, b) =>
        b.future_suitability - a.future_suitability || a.rank - b.rank
    );

  // Inline default: top 4 @ 2081-2100 RCP8.5. If that horizon is missing
  // (it can be — see e.g. csongradi), fall back to the latest available
  // RCP8.5 horizon, then RCP4.5.
  const headlineHorizon =
    doc.horizons['2081-2100_rcp85'] ??
    doc.horizons['2061-2080_rcp85'] ??
    doc.horizons['2081-2100_rcp45'] ??
    null;

  const top4 = headlineHorizon
    ? sortedByRank(headlineHorizon.replacement_candidates).slice(0, 4)
    : [];

  const headlineLabel =
    headlineHorizon === doc.horizons['2081-2100_rcp85']
      ? '2081–2100 · RCP8.5'
      : headlineHorizon === doc.horizons['2061-2080_rcp85']
        ? '2061–2080 · RCP8.5'
        : headlineHorizon === doc.horizons['2081-2100_rcp45']
          ? '2081–2100 · RCP4.5'
          : '—';

  // ---- Inline view (server-rendered, non-interactive) ----
  const inline = (
    <div className="rounded-md border border-neutral-200 bg-neutral-50/40 p-4">
      <div className="mb-2 flex items-baseline justify-between gap-2">
        <span className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
          {t('inlineHeader')}
        </span>
        <span className="text-xs tabular-nums text-neutral-500">
          {headlineLabel}
        </span>
      </div>
      {top4.length === 0 ? (
        <p className="text-sm text-neutral-600">{t('noData')}</p>
      ) : (
        <ul className="space-y-2">
          {top4.map((c) => (
            <li
              key={c.variety}
              className="grid grid-cols-[auto_1fr_auto_auto] items-center gap-2 sm:gap-3"
            >
              {colourDot(c.colour)}
              <span className="truncate text-sm font-medium text-neutral-900">
                {c.variety}
              </span>
              <span className="text-xs tabular-nums text-neutral-600">
                {t('suitabilityShort')} {c.future_suitability.toFixed(2)}
              </span>
              <span
                className={`text-xs font-semibold tabular-nums ${deltaClass(c.delta)}`}
              >
                {fmtDelta(c.delta)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  // ---- Expanded view (modal): full 8-horizon grid, grouped by period ----
  const horizonGroups: Array<{
    period: string;
    blocks: Array<{ scenario: 'rcp45' | 'rcp85'; cands: ReplacementCandidate[] }>;
  }> = [];
  const periods = ['2021-2040', '2041-2060', '2061-2080', '2081-2100'];
  for (const period of periods) {
    const blocks: Array<{
      scenario: 'rcp45' | 'rcp85';
      cands: ReplacementCandidate[];
    }> = [];
    for (const scenario of ['rcp45', 'rcp85'] as const) {
      const h = doc.horizons[`${period}_${scenario}`];
      if (!h) continue;
      blocks.push({
        scenario,
        cands: sortedByRank(h.replacement_candidates).slice(0, 4),
      });
    }
    if (blocks.length) horizonGroups.push({ period, blocks });
  }

  const expanded = (
    <div className="space-y-6">
      <p className="text-sm text-neutral-700">{t('caption')}</p>
      <div className="space-y-5">
        {horizonGroups.map((g) => (
          <div key={g.period}>
            <h4 className="mb-2 text-sm font-semibold text-neutral-800">
              {g.period}
            </h4>
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              {g.blocks.map((b) => (
                <div
                  key={b.scenario}
                  className="rounded border border-neutral-200 bg-white p-3"
                >
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-neutral-500">
                    {b.scenario === 'rcp45' ? 'RCP4.5' : 'RCP8.5'}
                  </div>
                  {b.cands.length === 0 ? (
                    <p className="text-xs text-neutral-500">{t('noData')}</p>
                  ) : (
                    <table className="w-full text-xs">
                      <thead className="text-left text-[10px] uppercase tracking-wide text-neutral-500">
                        <tr>
                          <th className="py-1 pr-2">{t('cols.variety')}</th>
                          <th className="py-1 pr-2 text-right">
                            {t('cols.suitability')}
                          </th>
                          <th className="py-1 pr-2 text-right">
                            {t('cols.delta')}
                          </th>
                          <th className="py-1 text-right">{t('cols.note')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {b.cands.map((c) => (
                          <tr
                            key={c.variety}
                            className="border-t border-neutral-100"
                          >
                            <td className="py-1 pr-2">
                              <span className="inline-flex items-center gap-1.5">
                                {colourDot(c.colour)}
                                <span className="font-medium text-neutral-900">
                                  {c.variety}
                                </span>
                              </span>
                            </td>
                            <td className="py-1 pr-2 text-right tabular-nums text-neutral-700">
                              {c.future_suitability.toFixed(2)}
                            </td>
                            <td
                              className={`py-1 pr-2 text-right tabular-nums font-semibold ${deltaClass(c.delta)}`}
                            >
                              {fmtDelta(c.delta)}
                            </td>
                            <td className="py-1 text-right text-[11px] text-neutral-500">
                              {c.status === 'existing principal'
                                ? t('noteExisting')
                                : c.limiting_factor
                                  ? t('noteLimit', { factor: c.limiting_factor })
                                  : ''}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      <p className="rounded border-l-4 border-amber-400 bg-amber-50 p-3 text-xs text-amber-900">
        {t('caveat')}
      </p>
    </div>
  );

  return (
    <section className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
      <h2 className="mb-2 text-lg font-semibold">{t('title')}</h2>
      <p className="mb-3 text-sm text-neutral-700">{t('caption')}</p>
      <ChartModal title={`${borvidek} — ${t('title')}`} expanded={expanded}>
        {inline}
      </ChartModal>
      <details className="mt-3 text-sm">
        <summary className="cursor-pointer text-neutral-700 hover:text-neutral-900">
          {t('expanderLabel')}
        </summary>
        <div className="mt-3">{expanded}</div>
      </details>
      <p className="mt-3 text-xs text-neutral-500">{t('caveat')}</p>
    </section>
  );
}
