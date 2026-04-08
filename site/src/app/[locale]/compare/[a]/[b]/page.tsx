import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import {
  BORVIDEK_LIST,
  getBorvidekBySlug,
  INDEX_META,
  type BorvidekMeta,
} from '@/lib/district-meta';
import {
  loadDescription,
  loadNormals,
  loadSuitabilityByDistrict,
  type NormalsRow,
  type SuitabilityRow,
  type DistrictDescription,
} from '@/lib/data';

// All directed pairs (22 × 21 = 462) so the picker form on /compare can
// generate a URL for any combination the user picks. We exclude self-pairs
// (a === b) — comparing a district with itself isn't useful.
export function generateStaticParams() {
  const locales = ['en', 'hu'];
  const slugs = BORVIDEK_LIST.map((d) => d.slug);
  const pairs: { locale: string; a: string; b: string }[] = [];
  for (const locale of locales) {
    for (const a of slugs) {
      for (const b of slugs) {
        if (a !== b) pairs.push({ locale, a, b });
      }
    }
  }
  return pairs;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; a: string; b: string }>;
}): Promise<Metadata> {
  const { locale, a, b } = await params;
  const ma = getBorvidekBySlug(a);
  const mb = getBorvidekBySlug(b);
  if (!ma || !mb) return {};
  const isHu = locale === 'hu';
  const title = isHu
    ? `${ma.borvidek} vs ${mb.borvidek} — borvidék-összehasonlítás`
    : `Compare ${ma.nameEn} vs ${mb.nameEn}`;
  const description = isHu
    ? `${ma.borvidek} és ${mb.borvidek} oldal-oldal mellett: hőmérsékleti összegek, csapadék, fagy- és hőhullámkockázat 1991–2100.`
    : `${ma.nameEn} and ${mb.nameEn} side-by-side: heat sums, rainfall, frost and heat-stress days from 1991 to 2100.`;
  return {
    title,
    description: description.slice(0, 158),
    openGraph: {
      title,
      description: description.slice(0, 158),
      type: 'website',
      locale: isHu ? 'hu_HU' : 'en_US',
      images: ['/opengraph-image'],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description: description.slice(0, 158),
    },
  };
}

// Indices to display in the comparison table, in order.
const COMPARE_INDICES: Array<keyof typeof INDEX_META> = [
  'winkler_gdd',
  'huglin_index',
  'cool_night_index',
  'spring_frost_days',
  'heat_days_t35',
  'extreme_heat_days_t38',
  'growing_season_precip',
  'hargreaves_pet',
  'p_minus_pet',
];

function pickIndex(rows: NormalsRow[], borvidek: string, index: string) {
  return rows.find((r) => r.borvidek === borvidek && r.index === index);
}

function fmt(n: number | null | undefined, digits = 0): string {
  if (n == null || Number.isNaN(n)) return '—';
  return n.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function fmtDelta(n: number | null | undefined, digits = 0): string {
  if (n == null || Number.isNaN(n)) return '—';
  const sign = n > 0 ? '+' : '';
  return `${sign}${n.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })}`;
}

function pickSuit(
  rows: SuitabilityRow[],
  variety: string,
  period: string,
  scenario: string,
): SuitabilityRow | undefined {
  return rows.find(
    (r) => r.variety === variety && r.period === period && r.scenario === scenario,
  );
}

function suitClass(v: number | undefined | null): string {
  if (v == null) return 'text-neutral-400';
  if (v >= 0.75) return 'text-emerald-700 font-semibold';
  if (v >= 0.5) return 'text-emerald-600';
  if (v >= 0.25) return 'text-amber-600';
  return 'text-rose-600';
}

function StatBlock({
  label,
  value,
  unit,
}: {
  label: string;
  value: string;
  unit?: string;
}) {
  return (
    <div className="rounded-lg border border-neutral-200 bg-white p-3">
      <div className="text-[11px] uppercase tracking-wide text-neutral-500">
        {label}
      </div>
      <div className="mt-1 text-xl font-semibold text-neutral-900">
        {value}
        {unit && (
          <span className="ml-1 text-xs font-normal text-neutral-500">
            {unit}
          </span>
        )}
      </div>
    </div>
  );
}

function DistrictColumn({
  meta,
  description,
  baseWinkler,
  futWinkler,
  futHeatDays,
  t,
}: {
  meta: BorvidekMeta;
  description: DistrictDescription | null;
  baseWinkler: number | null;
  futWinkler: number | null;
  futHeatDays: number | null;
  t: (k: string) => string;
}) {
  const winklerDelta =
    baseWinkler != null && futWinkler != null ? futWinkler - baseWinkler : null;
  return (
    <div className="space-y-4">
      <div>
        <div className="text-xs uppercase tracking-wide text-neutral-500">
          {meta.borregio}
        </div>
        <h2 className="text-2xl font-bold">
          <Link
            href={`/districts/${meta.slug}`}
            className="hover:text-amber-700 hover:underline"
          >
            {meta.borvidek}
          </Link>
        </h2>
        <div className="mt-1 text-sm text-neutral-600">
          {meta.flagshipStyles.join(' · ')}
        </div>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <StatBlock
          label={t('stat.winklerNow')}
          value={fmt(baseWinkler)}
          unit="°C·d"
        />
        <StatBlock
          label={t('stat.winklerFuture')}
          value={fmt(futWinkler)}
          unit="°C·d"
        />
        <StatBlock
          label={t('stat.winklerDelta')}
          value={fmtDelta(winklerDelta)}
          unit="°C·d"
        />
        <StatBlock
          label={t('stat.heatDaysFuture')}
          value={fmt(futHeatDays)}
          unit={t('unit.days')}
        />
      </div>
      {description?.tagline && (
        <p className="text-sm italic text-neutral-700">{description.tagline}</p>
      )}
    </div>
  );
}

export default async function CompareTwoDistrictsPage({
  params,
}: {
  params: Promise<{ locale: string; a: string; b: string }>;
}) {
  const { locale, a, b } = await params;
  setRequestLocale(locale);
  const metaA = getBorvidekBySlug(a);
  const metaB = getBorvidekBySlug(b);
  if (!metaA || !metaB) notFound();

  const t = await getTranslations({ locale, namespace: 'comparePair' });

  const [baseNormals, futNormals, descA, descB, suitA, suitB] = await Promise.all([
    loadNormals('1991-2020', 'observed'),
    loadNormals('2081-2100', 'rcp85'),
    loadDescription(a),
    loadDescription(b),
    loadSuitabilityByDistrict(a),
    loadSuitabilityByDistrict(b),
  ]);

  const baseWinklerA = pickIndex(baseNormals, metaA.borvidek, 'winkler_gdd')?.mean ?? null;
  const futWinklerA = pickIndex(futNormals, metaA.borvidek, 'winkler_gdd')?.mean ?? null;
  const futHeatA = pickIndex(futNormals, metaA.borvidek, 'heat_days_t35')?.mean ?? null;
  const baseWinklerB = pickIndex(baseNormals, metaB.borvidek, 'winkler_gdd')?.mean ?? null;
  const futWinklerB = pickIndex(futNormals, metaB.borvidek, 'winkler_gdd')?.mean ?? null;
  const futHeatB = pickIndex(futNormals, metaB.borvidek, 'heat_days_t35')?.mean ?? null;

  // Index comparison rows: for each index in COMPARE_INDICES, show baseline (A, B)
  // and 2081-2100 RCP8.5 (A, B) plus the absolute A−B difference at the future bin.
  const indexRows = COMPARE_INDICES.map((key) => {
    const meta = INDEX_META[key];
    const baseA = pickIndex(baseNormals, metaA.borvidek, key)?.mean ?? null;
    const baseB = pickIndex(baseNormals, metaB.borvidek, key)?.mean ?? null;
    const futA = pickIndex(futNormals, metaA.borvidek, key)?.mean ?? null;
    const futB = pickIndex(futNormals, metaB.borvidek, key)?.mean ?? null;
    const diff = futA != null && futB != null ? futA - futB : null;
    // Choose decimals: precip / pet / drought get 0, indices that are days get 0,
    // cool night index gets 1.
    const digits = key === 'cool_night_index' ? 1 : 0;
    return { key, label: meta.label, units: meta.units, baseA, baseB, futA, futB, diff, digits };
  });

  // Variety comparison: union of both districts' principal varieties.
  const principalUnion = Array.from(
    new Set<string>([...metaA.principalVarieties, ...metaB.principalVarieties]),
  );

  const varietyRows = principalUnion
    .map((variety) => {
      const baseRowA = pickSuit(suitA, variety, '1991-2020', 'observed');
      const baseRowB = pickSuit(suitB, variety, '1991-2020', 'observed');
      const futRowA = pickSuit(suitA, variety, '2081-2100', 'rcp85');
      const futRowB = pickSuit(suitB, variety, '2081-2100', 'rcp85');
      return {
        variety,
        inA: metaA.principalVarieties.includes(variety),
        inB: metaB.principalVarieties.includes(variety),
        baseA: baseRowA?.suitability ?? null,
        baseB: baseRowB?.suitability ?? null,
        futA: futRowA?.suitability ?? null,
        futB: futRowB?.suitability ?? null,
      };
    })
    .sort((x, y) => {
      const xMax = Math.max(x.futA ?? 0, x.futB ?? 0);
      const yMax = Math.max(y.futA ?? 0, y.futB ?? 0);
      return yMax - xMax;
    });

  return (
    <section className="space-y-8">
      <div>
        <div className="text-sm">
          <Link href="/compare" className="text-amber-700 hover:underline">
            ← {t('backToCompare')}
          </Link>
        </div>
        <h1 className="mt-2 text-3xl font-bold sm:text-4xl">
          {t('title', { a: metaA.borvidek, b: metaB.borvidek } as never)}
        </h1>
        <p className="mt-2 text-neutral-600">{t('subtitle')}</p>
      </div>

      {/* Side-by-side district headers */}
      <div className="grid gap-6 md:grid-cols-2">
        <DistrictColumn
          meta={metaA}
          description={descA}
          baseWinkler={baseWinklerA}
          futWinkler={futWinklerA}
          futHeatDays={futHeatA}
          t={t}
        />
        <DistrictColumn
          meta={metaB}
          description={descB}
          baseWinkler={baseWinklerB}
          futWinkler={futWinklerB}
          futHeatDays={futHeatB}
          t={t}
        />
      </div>

      {/* Climate index comparison table */}
      <div>
        <h2 className="text-xl font-semibold">{t('indices.heading')}</h2>
        <p className="mt-1 text-sm text-neutral-600">{t('indices.subtitle')}</p>
        <div className="mt-3 overflow-x-auto">
          <table className="w-full min-w-[640px] border-collapse text-sm">
            <thead>
              <tr className="border-b border-neutral-300 text-left">
                <th className="px-2 py-2 font-semibold">{t('indices.index')}</th>
                <th className="px-2 py-2 text-right font-semibold" colSpan={2}>
                  {t('indices.baseline')}
                </th>
                <th className="px-2 py-2 text-right font-semibold" colSpan={2}>
                  {t('indices.future')}
                </th>
                <th className="px-2 py-2 text-right font-semibold">
                  {t('indices.diff')}
                </th>
              </tr>
              <tr className="border-b border-neutral-200 text-xs text-neutral-500">
                <th></th>
                <th className="px-2 py-1 text-right font-normal">{metaA.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">{metaB.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">{metaA.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">{metaB.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">A − B</th>
              </tr>
            </thead>
            <tbody>
              {indexRows.map((r) => (
                <tr key={r.key} className="border-b border-neutral-100">
                  <td className="px-2 py-2">
                    <div className="font-medium">{r.label}</div>
                    <div className="text-xs text-neutral-500">{r.units}</div>
                  </td>
                  <td className="px-2 py-2 text-right tabular-nums">
                    {fmt(r.baseA, r.digits)}
                  </td>
                  <td className="px-2 py-2 text-right tabular-nums">
                    {fmt(r.baseB, r.digits)}
                  </td>
                  <td className="px-2 py-2 text-right font-semibold tabular-nums">
                    {fmt(r.futA, r.digits)}
                  </td>
                  <td className="px-2 py-2 text-right font-semibold tabular-nums">
                    {fmt(r.futB, r.digits)}
                  </td>
                  <td
                    className={`px-2 py-2 text-right tabular-nums ${
                      r.diff != null && Math.abs(r.diff) > 0
                        ? 'bg-amber-50 font-semibold'
                        : ''
                    }`}
                  >
                    {fmtDelta(r.diff, r.digits)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Variety suitability comparison */}
      <div>
        <h2 className="text-xl font-semibold">{t('varieties.heading')}</h2>
        <p className="mt-1 text-sm text-neutral-600">{t('varieties.subtitle')}</p>
        <div className="mt-3 overflow-x-auto">
          <table className="w-full min-w-[640px] border-collapse text-sm">
            <thead>
              <tr className="border-b border-neutral-300 text-left">
                <th className="px-2 py-2 font-semibold">{t('varieties.variety')}</th>
                <th className="px-2 py-2 text-right font-semibold" colSpan={2}>
                  {t('varieties.baseline')}
                </th>
                <th className="px-2 py-2 text-right font-semibold" colSpan={2}>
                  {t('varieties.future')}
                </th>
              </tr>
              <tr className="border-b border-neutral-200 text-xs text-neutral-500">
                <th></th>
                <th className="px-2 py-1 text-right font-normal">{metaA.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">{metaB.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">{metaA.borvidek}</th>
                <th className="px-2 py-1 text-right font-normal">{metaB.borvidek}</th>
              </tr>
            </thead>
            <tbody>
              {varietyRows.map((r) => (
                <tr key={r.variety} className="border-b border-neutral-100">
                  <td className="px-2 py-2">
                    <div className="font-medium">{r.variety}</div>
                    <div className="text-xs text-neutral-500">
                      {r.inA && r.inB
                        ? t('varieties.bothPrincipal')
                        : r.inA
                          ? t('varieties.onlyA', { a: metaA.borvidek } as never)
                          : t('varieties.onlyB', { b: metaB.borvidek } as never)}
                    </div>
                  </td>
                  <td
                    className={`px-2 py-2 text-right tabular-nums ${suitClass(r.baseA)}`}
                  >
                    {r.baseA != null ? r.baseA.toFixed(2) : '—'}
                  </td>
                  <td
                    className={`px-2 py-2 text-right tabular-nums ${suitClass(r.baseB)}`}
                  >
                    {r.baseB != null ? r.baseB.toFixed(2) : '—'}
                  </td>
                  <td
                    className={`px-2 py-2 text-right tabular-nums ${suitClass(r.futA)}`}
                  >
                    {r.futA != null ? r.futA.toFixed(2) : '—'}
                  </td>
                  <td
                    className={`px-2 py-2 text-right tabular-nums ${suitClass(r.futB)}`}
                  >
                    {r.futB != null ? r.futB.toFixed(2) : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-2 text-xs text-neutral-500">{t('varieties.scale')}</p>
      </div>

      <p className="border-t border-neutral-200 pt-4 text-sm text-neutral-600">
        {t('footnote.before')}{' '}
        <Link href="/methods" className="text-amber-700 hover:underline">
          {t('footnote.methodsLink')}
        </Link>
        {t('footnote.after')}
      </p>
    </section>
  );
}
