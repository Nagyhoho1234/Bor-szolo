import { getTranslations } from 'next-intl/server';

export type HungaroMetRow = {
  year: number;
  tmean_c: number;
  precip_mm: number;
};

export type HungaroMetPanelProps = {
  locale: string;
  stationName: string;
  distanceKm: number;
  rows: HungaroMetRow[];
};

/**
 * "What the nearest weather station actually measured" — a small,
 * deliberately subdued credibility-anchor panel rendered between the
 * extreme-weather outlook and the headline tile row on each district
 * detail page. Renders 5 rows (2020-2024) of station-observed annual
 * mean temperature and total precipitation, plus a 5-year mean. Source:
 * HungaroMet open data portal (https://odp.met.hu/), CC-BY-SA.
 */
export default async function HungaroMetPanel({
  locale,
  stationName,
  distanceKm,
  rows,
}: HungaroMetPanelProps) {
  const t = await getTranslations({ locale, namespace: 'districts.detail.hungaromet' });
  if (!rows || rows.length === 0) return null;

  const meanT =
    rows.reduce((s, r) => s + r.tmean_c, 0) / rows.length;
  const meanP =
    rows.reduce((s, r) => s + r.precip_mm, 0) / rows.length;
  const yearMin = rows[0].year;
  const yearMax = rows[rows.length - 1].year;

  return (
    <section className="rounded-lg border border-neutral-200 bg-neutral-50 p-4 sm:p-5">
      <h2 className="text-base font-semibold text-neutral-800">
        {t('title')}
      </h2>
      <p className="mt-1 text-xs text-neutral-600">
        {t('subtitle', {
          station: stationName,
          distance: distanceKm.toFixed(1),
          yearMin,
          yearMax,
        })}
      </p>

      <div className="mt-3 overflow-x-auto">
        <table className="w-full text-sm tabular-nums">
          <thead>
            <tr className="text-left text-[11px] uppercase tracking-wide text-neutral-500">
              <th className="py-1 pr-3 font-medium">{t('cols.year')}</th>
              <th className="py-1 pr-3 font-medium">{t('cols.tmean')}</th>
              <th className="py-1 font-medium">{t('cols.precip')}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.year} className="border-t border-neutral-200">
                <td className="py-1 pr-3 text-neutral-700">{r.year}</td>
                <td className="py-1 pr-3 text-neutral-900">
                  {r.tmean_c.toFixed(2)} °C
                </td>
                <td className="py-1 text-neutral-900">
                  {r.precip_mm.toFixed(0)} mm
                </td>
              </tr>
            ))}
            <tr className="border-t-2 border-neutral-300">
              <td className="py-1 pr-3 text-xs font-semibold uppercase tracking-wide text-neutral-600">
                {t('meanLabel')}
              </td>
              <td className="py-1 pr-3 font-semibold text-neutral-900">
                {meanT.toFixed(2)} °C
              </td>
              <td className="py-1 font-semibold text-neutral-900">
                {meanP.toFixed(0)} mm
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p className="mt-3 text-xs italic text-neutral-600">{t('caption')}</p>
      <p className="mt-2 text-[11px] text-neutral-500">
        {t('source')}:{' '}
        <a
          href="https://odp.met.hu/"
          target="_blank"
          rel="noreferrer"
          className="text-blue-700 hover:underline"
        >
          HungaroMet ODP
        </a>{' '}
        · {t('license')}
      </p>
    </section>
  );
}
