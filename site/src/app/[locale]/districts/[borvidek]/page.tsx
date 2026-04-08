import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import fs from 'node:fs';
import path from 'node:path';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { processResearchMarkdown } from '@/lib/research-markdown';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import {
  BORVIDEK_LIST,
  getBorvidekBySlug,
  getNearestDistricts,
  INDEX_META,
} from '@/lib/district-meta';
import {
  loadIndicesAnnual,
  loadNormals,
  loadSuitabilityByDistrict,
  loadHeadlineWinnersLosers,
  loadDescription,
  loadReplacements,
  loadOdpMetAssignments,
  loadOdpMetStation,
  localizeDescription,
} from '@/lib/data';
import HungaroMetPanel from '@/components/HungaroMetPanel';
import IndexCard from '@/components/IndexCard';
import ClimateTrendChart from '@/components/ClimateTrendChart';
import VarietySuitabilityBars from '@/components/VarietySuitabilityBars';
import VarietyReplacements from '@/components/VarietyReplacements';
import ChartModal from '@/components/ChartModal';
import ThreatCard from '@/components/ThreatCard';
import ProgressiveDisclosure from '@/components/ProgressiveDisclosure';
import DownloadPdfButton from '@/components/DownloadPdfButton';

export function generateStaticParams() {
  return BORVIDEK_LIST.map((d) => ({ borvidek: d.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; borvidek: string }>;
}): Promise<Metadata> {
  const { locale, borvidek: slug } = await params;
  const meta = getBorvidekBySlug(slug);
  if (!meta) return {};
  const isHu = locale === 'hu';
  const descRaw = await loadDescription(slug);
  const desc = descRaw ? localizeDescription(descRaw, locale) : null;
  const huName = desc?.name_hu ?? meta.borvidek;
  const enName = desc?.name_en ?? meta.nameEn;
  const title = isHu
    ? `${huName} borvidék — klímakitettség és fajták`
    : `${enName} — Hungarian wine district climate profile`;
  const fallbackEn = `${enName}: ${meta.principalVarieties.slice(0, 3).join(', ')}. Climate exposure, variety suitability and disease threats to 2100.`;
  const fallbackHu = `${huName}: ${meta.principalVarieties.slice(0, 3).join(', ')}. Klímakitettség, fajtaalkalmasság és betegségkockázat 2100-ig.`;
  const tagline = desc?.tagline?.trim();
  const description = (tagline && tagline.length <= 158
    ? tagline
    : isHu
      ? fallbackHu
      : fallbackEn
  ).slice(0, 158);
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      type: 'website',
      locale: isHu ? 'hu_HU' : 'en_US',
      images: ['/opengraph-image'],
    },
    twitter: { card: 'summary_large_image', title, description },
  };
}

// Read the user's research markdown for this district, if any.
// Tries the canonical site slug, then a hyphen-fallback (e.g. site uses
// "balatonfelvideki" but the file may be "balaton-felvideki.md").
// When locale is "hu", prefers <slug>.hu.md and falls back to the English
// <slug>.md if no Hungarian version exists yet.
function loadResearch(slug: string, locale: string): string | null {
  const root = path.join(process.cwd(), '..', 'research', 'districts');
  const hyphenated = slug.replace(
    /(felvideki|bajai|csopaki|budai|somloi)$/,
    '-$1',
  );
  const isHu = locale === 'hu';
  const candidates = isHu
    ? [
        `${slug}.hu.md`,
        `${hyphenated}.hu.md`,
        `${slug}.md`,
        `${hyphenated}.md`,
      ]
    : [`${slug}.md`, `${hyphenated}.md`];
  for (const c of candidates) {
    try {
      const p = path.join(root, c);
      if (fs.existsSync(p)) return fs.readFileSync(p, 'utf-8');
    } catch {
      /* ignore */
    }
  }
  return null;
}

const DASHBOARD_INDICES: Array<{
  key: keyof typeof INDEX_META;
  worseWhenHigher: boolean;
}> = [
  { key: 'winkler_gdd', worseWhenHigher: true },
  { key: 'huglin_index', worseWhenHigher: true },
  { key: 'spring_frost_days', worseWhenHigher: true },
  { key: 'heat_days_t35', worseWhenHigher: true },
  { key: 'growing_season_precip', worseWhenHigher: false },
  { key: 'p_minus_pet', worseWhenHigher: false },
];

export default async function DistrictDetailPage({
  params,
}: {
  params: Promise<{ locale: string; borvidek: string }>;
}) {
  const { locale, borvidek: slug } = await params;
  setRequestLocale(locale);
  const meta = getBorvidekBySlug(slug);
  if (!meta) notFound();

  const t = await getTranslations({ locale, namespace: 'districts.detail' });
  const tCommon = await getTranslations({ locale, namespace: 'common' });
  const tThreats = await getTranslations({ locale, namespace: 'threats' });

  // Load everything (server-side fs reads, so this is instant at build time)
  const [baseNormals, futNormals, suitability, headlines, indicesRcp85, descriptionRaw, replacements, odpAssignments, odpStationRows] =
    await Promise.all([
      loadNormals('1991-2020', 'observed'),
      loadNormals('2081-2100', 'rcp85'),
      loadSuitabilityByDistrict(slug),
      loadHeadlineWinnersLosers(),
      loadIndicesAnnual('rcp85'),
      loadDescription(slug),
      loadReplacements(slug),
      loadOdpMetAssignments(),
      loadOdpMetStation(slug),
    ]);
  // Pick HU fields when locale is hu, falling back to EN where missing
  const description = localizeDescription(descriptionRaw, locale);

  // HungaroMet station observations (2020-2024) for the credibility panel.
  // Authoritative assignment lives in the assignments CSV; if no row exists
  // there, the district has no nearby station and we render nothing.
  const odpAssignment = odpAssignments.find((a) => a.borvidek === meta.borvidek) ?? null;
  const odpRows = odpAssignment
    ? odpStationRows
        .filter(
          (r) =>
            r.borvidek === meta.borvidek &&
            r.tmean_c != null &&
            r.precip_mm != null &&
            Number.isFinite(r.tmean_c) &&
            Number.isFinite(r.precip_mm),
        )
        .map((r) => ({ year: r.year, tmean_c: r.tmean_c, precip_mm: r.precip_mm }))
    : [];

  const baseRows = baseNormals.filter((r) => r.borvidek === meta.borvidek);
  const futRows = futNormals.filter((r) => r.borvidek === meta.borvidek);
  const headline = headlines.find((h) => h.borvidek === meta.borvidek);

  const get = (rows: typeof baseRows, idx: string) =>
    rows.find((r) => r.index === idx);

  const baseWinkler = get(baseRows, 'winkler_gdd')?.mean ?? null;
  const futWinkler = get(futRows, 'winkler_gdd')?.mean ?? null;
  const winklerDelta =
    baseWinkler != null && futWinkler != null ? futWinkler - baseWinkler : null;

  // Approximate mean-temperature delta via cool_night_index change (proxy)
  // plus heat-days change tracer. For the headline tile, we use Huglin delta
  // as a temperature-summed proxy converted back to approximate degrees via
  // the rule of thumb (delta HI / 6 months / 30 days ≈ mean-T delta).
  const baseHuglin = get(baseRows, 'huglin_index')?.mean ?? null;
  const futHuglin = get(futRows, 'huglin_index')?.mean ?? null;
  const approxTempDelta =
    baseHuglin != null && futHuglin != null
      ? (futHuglin - baseHuglin) / 180
      : null;

  // Flagship variety = first principal in the list that exists in the data
  const flagshipName = meta.principalVarieties[0];
  const baseSuit = suitability.find(
    (r) =>
      r.variety === flagshipName &&
      r.period === '1991-2020' &&
      r.scenario === 'observed'
  );
  const futSuit = suitability.find(
    (r) =>
      r.variety === flagshipName &&
      r.period === '2081-2100' &&
      r.scenario === 'rcp85'
  );
  const flagshipDelta =
    baseSuit && futSuit ? futSuit.suitability - baseSuit.suitability : null;

  // All suitability rows for this district across every (period, scenario)
  // combination AND every variety (principal + climate-hedge candidates).
  // The bar component splits them into the principal-varieties chart and
  // the top-N climate-adapted-candidates chart based on
  // in_principal_varieties.
  const varietyRows = suitability
    .map((r) => ({
      variety: r.variety,
      period: r.period,
      scenario: r.scenario,
      suitability: r.suitability,
      colour: (r.colour as 'red' | 'white') ?? 'white',
      in_principal_varieties: r.in_principal_varieties,
    }));

  // Index dashboard tiles — paired baseline/future values
  const dashboardTiles = DASHBOARD_INDICES.map(({ key, worseWhenHigher }) => {
    const b = get(baseRows, key as string)?.mean ?? null;
    const f = get(futRows, key as string)?.mean ?? null;
    const risk = get(futRows, key as string)?.risk_flag ?? null;
    const sparkSeries = indicesRcp85
      .filter((r) => r.borvidek === meta.borvidek)
      .sort((a, b) => a.year - b.year)
      .map((r) => r[key as keyof typeof r] as number)
      .filter((v) => Number.isFinite(v));
    return {
      key,
      label: INDEX_META[key].label,
      units: INDEX_META[key].units,
      baseline: b,
      future: f,
      sparkSeries,
      riskFlag: risk,
      worseWhenHigher,
    };
  });

  // Peers
  const peers = getNearestDistricts(slug, 5);
  const peerRows = peers.map((p) => {
    const pb = baseNormals.find(
      (r) => r.borvidek === p.borvidek && r.index === 'winkler_gdd'
    )?.mean;
    const pf = futNormals.find(
      (r) => r.borvidek === p.borvidek && r.index === 'winkler_gdd'
    )?.mean;
    return {
      borvidek: p.borvidek,
      slug: p.slug,
      winklerNow: pb ?? null,
      winklerFuture: pf ?? null,
      winklerDelta: pb != null && pf != null ? pf - pb : null,
    };
  });

  // Threat flag detection
  const futHeat = get(futRows, 'heat_days_t35');
  const futFrost = get(futRows, 'spring_frost_days');
  const futDrought = get(futRows, 'p_minus_pet');
  const heatRisk = futHeat?.risk_flag?.includes('heat') ?? false;
  const frostRisk = futFrost?.risk_flag?.includes('frost') ?? false;
  const droughtRisk = futDrought?.risk_flag?.includes('drought') ?? false;

  const research = loadResearch(slug, locale);

  return (
    <article className="space-y-6">
      {/* Header strip */}
      <header className="space-y-2">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <h1 className="text-3xl font-bold tracking-tight text-neutral-900 sm:text-4xl">
            {description?.name_hu ?? meta.borvidek}
          </h1>
          <DownloadPdfButton slug={slug} locale={locale} />
        </div>
        <p className="text-neutral-600">
          {description?.name_en ?? meta.nameEn}
        </p>
        {description?.tagline && (
          <p className="text-base italic text-neutral-700 sm:text-lg">{description.tagline}</p>
        )}
        <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm text-neutral-500">
          <span>
            <strong className="text-neutral-800">{meta.areaKm2}</strong>{' '}
            {tCommon('units.km2')}
          </span>
          <span>
            <strong className="text-neutral-800">{meta.nSettlements}</strong>{' '}
            {t('settlements')}
          </span>
          {description?.flagship_wines?.length ? (
            <span>
              {t('flagshipLabel')}: {description.flagship_wines.join(' · ')}
            </span>
          ) : (
            <span>
              {t('principalLabel')}: {meta.principalVarieties.slice(0, 3).join(', ')}
            </span>
          )}
        </div>
      </header>

      {/* Description hero panel: elevator pitch + key facts + climate verdict */}
      {description && (
        <section className="rounded-lg border border-neutral-200 bg-gradient-to-br from-neutral-50 to-white p-4 shadow-sm sm:p-6">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-4">
              <p className="text-base leading-relaxed text-neutral-800">
                {description.elevator_pitch}
              </p>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-semibold text-neutral-700">{t('grapesAndWines')}: </span>
                  <span className="text-neutral-700">{description.principal_grapes_summary}</span>
                </div>
                <div>
                  <span className="font-semibold text-neutral-700">{t('terroir')}: </span>
                  <span className="text-neutral-700">{description.terroir_summary}</span>
                </div>
                <div>
                  <span className="font-semibold text-neutral-700">{t('climateToday')}: </span>
                  <span className="text-neutral-700">{description.climate_today}</span>
                </div>
                <div className="rounded border-l-4 border-amber-400 bg-amber-50 p-3">
                  <p className="text-xs font-semibold uppercase tracking-wide text-amber-800">
                    {t('climateThreat')}
                  </p>
                  <p className="mt-1 text-sm text-amber-900">
                    {description.climate_threat_headline}
                  </p>
                </div>
                <div className="rounded border-l-4 border-blue-400 bg-blue-50 p-3">
                  <p className="text-xs font-semibold uppercase tracking-wide text-blue-800">
                    {t('varietyWinnersLosers')}
                  </p>
                  <p className="mt-1 text-sm text-blue-900">
                    {description.climate_winner_loser}
                  </p>
                </div>
              </div>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold uppercase tracking-wide text-neutral-500">
                {t('keyFacts')}
              </h3>
              <dl className="space-y-2 text-sm">
                {description.key_facts.map((f, i) => (
                  <div key={i} className="border-b border-neutral-100 pb-1.5 last:border-0">
                    <dt className="text-xs uppercase tracking-wide text-neutral-500">
                      {f.label}
                    </dt>
                    <dd className="text-neutral-800">{f.value}</dd>
                  </div>
                ))}
              </dl>
              {description.top_sources?.length > 0 && (
                <div className="mt-4">
                  <h3 className="mb-2 text-sm font-semibold uppercase tracking-wide text-neutral-500">
                    {t('topSources')}
                  </h3>
                  <ul className="space-y-1 text-xs">
                    {description.top_sources.slice(0, 5).map((s, i) => (
                      <li key={i}>
                        <a
                          href={s.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-700 hover:underline"
                        >
                          {s.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Extreme weather outlook (CCKP CMIP6 — rx1day, cdd, frost, tnn, gsl) */}
      {description?.climate_extremes_outlook && (
        <section className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm sm:p-6">
          <h2 className="mb-2 text-lg font-semibold">{t('extremeOutlook')}</h2>
          <p className="text-sm text-neutral-700">
            {description.climate_extremes_outlook.summary}
          </p>
          <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4 sm:gap-3 lg:grid-cols-7">
            {[
              ['rx1day_mm', t('extremeMetrics.rx1day'), 'mm'],
              ['rx5day_mm', t('extremeMetrics.rx5day'), 'mm'],
              ['cdd_days', t('extremeMetrics.cdd'), tCommon('units.days')],
              ['cwd_days', t('extremeMetrics.cwd'), tCommon('units.days')],
              ['frost_days', t('extremeMetrics.frost'), tCommon('units.days')],
              ['tnn_c', t('extremeMetrics.tnn'), '°C'],
              ['growing_season_length_days', t('extremeMetrics.gsl'), tCommon('units.days')],
            ].map(([k, label, units]) => {
              const m = description.climate_extremes_outlook!.metrics;
              const hist = m[`${k}_hist_1995_2014`];
              const fut = m[`${k}_ssp585_2080_2099`];
              if (hist == null && fut == null) return null;
              return (
                <div key={k} className="rounded border border-neutral-200 bg-neutral-50 p-2">
                  <div className="text-[11px] uppercase leading-tight tracking-wide text-neutral-500 sm:text-[10px]">
                    {label}
                  </div>
                  <div className="mt-1 text-sm font-semibold tabular-nums text-neutral-900">
                    {hist != null ? hist.toFixed(1) : '—'}
                    <span className="text-neutral-400"> → </span>
                    {fut != null ? fut.toFixed(1) : '—'}
                  </div>
                  <div className="text-[11px] text-neutral-500 sm:text-[10px]">{units}</div>
                </div>
              );
            })}
          </div>
          <p className="mt-3 text-[11px] text-neutral-500">
            {t('source')}:{' '}
            <a
              href={description.climate_extremes_outlook.source_url}
              target="_blank"
              rel="noreferrer"
              className="text-blue-700 hover:underline"
            >
              {description.climate_extremes_outlook.source}
            </a>
          </p>
        </section>
      )}

      {/* HungaroMet station observations — credibility anchor for FORESEE projections */}
      {odpAssignment && odpRows.length > 0 && (
        <HungaroMetPanel
          locale={locale}
          stationName={odpAssignment.station_name}
          distanceKm={odpAssignment.distance_km}
          rows={odpRows}
        />
      )}

      {/* Headline tile row */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
          <div className="text-xs uppercase tracking-wide text-neutral-500">
            {t('headline.tempDelta')}
          </div>
          <div className="mt-1 text-3xl font-semibold text-neutral-900">
            {approxTempDelta != null
              ? `${approxTempDelta > 0 ? '+' : ''}${approxTempDelta.toFixed(1)} °C`
              : '—'}
          </div>
          <div className="text-xs text-neutral-500">{t('headlineSubtitle')}</div>
        </div>
        <div className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
          <div className="text-xs uppercase tracking-wide text-neutral-500">
            {t('headline.gddDelta')}
          </div>
          <div className="mt-1 text-3xl font-semibold text-neutral-900">
            {winklerDelta != null
              ? `${winklerDelta > 0 ? '+' : ''}${winklerDelta.toFixed(0)} GDD`
              : '—'}
          </div>
          <div className="text-xs text-neutral-500">
            {baseWinkler?.toFixed(0)} → {futWinkler?.toFixed(0)}
          </div>
        </div>
        <div className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
          <div className="text-xs uppercase tracking-wide text-neutral-500">
            {t('headline.flagshipDelta')} ({flagshipName})
          </div>
          <div className="mt-1 text-3xl font-semibold text-neutral-900">
            {flagshipDelta != null
              ? `${flagshipDelta > 0 ? '+' : ''}${flagshipDelta.toFixed(2)}`
              : '—'}
          </div>
          <div className="text-xs text-neutral-500">
            {baseSuit?.suitability.toFixed(2)} →{' '}
            {futSuit?.suitability.toFixed(2)}
          </div>
        </div>
      </div>

      {/* What's grown here */}
      <section className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
        <h2 className="mb-2 text-lg font-semibold">{t('whatsGrown')}</h2>
        <p className="text-sm text-neutral-700">{meta.notes}</p>
        <p className="mt-2 text-xs text-neutral-500">
          {t('principalVarieties')}: {meta.principalVarieties.join(', ')}
        </p>
      </section>

      {/* Indices dashboard — click any card to open the interactive chart */}
      <section className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
        <h2 className="mb-2 text-lg font-semibold">{t('indicesDashboard')}</h2>
        <p className="mb-3 text-xs text-neutral-500">
          {t('indicesDashboardSubtitle')}
        </p>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {dashboardTiles.map((d) => (
            <ChartModal
              key={d.key}
              title={`${meta.borvidek} — ${d.label}`}
              expanded={
                <ClimateTrendChart
                  borvidek={meta.borvidek}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  index={d.key as any}
                  label={d.label}
                  units={d.units}
                />
              }
            >
              <IndexCard
                label={d.label}
                units={d.units}
                baseline={d.baseline}
                future={d.future}
                sparkSeries={d.sparkSeries}
                riskFlag={d.riskFlag}
                worseWhenHigher={d.worseWhenHigher}
              />
            </ChartModal>
          ))}
        </div>
      </section>

      {/* Variety suitability */}
      <section className="rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
        <h2 className="mb-3 text-lg font-semibold">{t('variety')}</h2>
        <ChartModal
          title={`${meta.borvidek} — variety suitability`}
          expanded={<VarietySuitabilityBars rows={varietyRows} />}
        >
          <VarietySuitabilityBars rows={varietyRows} staticView />
        </ChartModal>
        {headline && (
          <div className="mt-3 text-xs text-neutral-500">
            {t('biggestWinner')}:{' '}
            <strong>{headline.biggest_winner_variety}</strong> (
            {headline.winner_delta.toFixed(2)}) · {t('biggestLoser')}:{' '}
            <strong>{headline.biggest_loser_variety}</strong> (
            {headline.loser_delta.toFixed(2)})
          </div>
        )}
      </section>

      {/* Climate-adapted variety replacement recommendations */}
      <VarietyReplacements
        doc={replacements}
        borvidek={meta.borvidek}
        locale={locale}
      />

      {/* Threats */}
      <section className="space-y-3">
        <h2 className="text-lg font-semibold">{t('threats')}</h2>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          <ThreatCard
            title={tThreats('cards.fd.title')}
            severity="high"
            description={t('threatFdDescription')}
            href={`/${locale}/threats/flavescence-doree`}
            draft
            draftWarning={t('threatFdDraftWarning')}
          />
          {frostRisk && (
            <ThreatCard
              title={tThreats('cards.frost.title')}
              severity="medium"
              description={t('threatFrostDescription', { flag: futFrost?.risk_flag ?? '' })}
              href={`/${locale}/threats/frost`}
            />
          )}
          {droughtRisk && (
            <ThreatCard
              title={tThreats('cards.drought.title')}
              severity="high"
              description={t('threatDroughtDescription', {
                value: futDrought?.mean?.toFixed(0) ?? '—',
              })}
              href={`/${locale}/threats/drought`}
            />
          )}
          {heatRisk && (
            <ThreatCard
              title={tThreats('cards.heat.title')}
              severity="high"
              description={t('threatHeatDescription', {
                value: futHeat?.mean?.toFixed(1) ?? '—',
              })}
              href={`/${locale}/threats/drought`}
            />
          )}
        </div>
      </section>

      {/* Peers */}
      <ProgressiveDisclosure
        title={t('peers')}
        tier1={
          <div>
            <table className="w-full text-sm">
              <thead className="text-left text-xs text-neutral-500">
                <tr>
                  <th className="py-1">{t('peerCols.district')}</th>
                  <th className="py-1">{t('peerCols.winklerNow')}</th>
                  <th className="py-1">{t('peerCols.winklerFuture')}</th>
                  <th className="py-1">{t('peerCols.delta')}</th>
                </tr>
              </thead>
              <tbody>
                {peerRows.map((p) => (
                  <tr key={p.slug} className="border-t border-neutral-100">
                    <td className="py-1">
                      <Link
                        href={`/${locale}/districts/${p.slug}`}
                        className="underline-offset-2 hover:underline"
                      >
                        {p.borvidek}
                      </Link>
                    </td>
                    <td className="py-1">{p.winklerNow?.toFixed(0) ?? '—'}</td>
                    <td className="py-1">
                      {p.winklerFuture?.toFixed(0) ?? '—'}
                    </td>
                    <td className="py-1">
                      {p.winklerDelta != null
                        ? (p.winklerDelta > 0 ? '+' : '') +
                          p.winklerDelta.toFixed(0)
                        : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        }
      />

      {/* Research dossier — long-form synthesis from research/districts/<slug>.md */}
      {research && (() => {
        const { body, references } = processResearchMarkdown(research);
        return (
          <section className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm sm:p-6">
            <h2 className="mb-3 text-xl font-semibold sm:text-2xl">{t('researchTitle')}</h2>
            <p className="mb-4 text-sm text-neutral-600">
              {t('researchSubtitle')}
            </p>
            <div className="prose prose-neutral max-w-none prose-headings:scroll-mt-20 prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg prose-a:text-blue-700 prose-a:no-underline hover:prose-a:underline">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
              >
                {body}
              </ReactMarkdown>
            </div>
            {references.length > 0 && (
              <div className="mt-8 border-t border-neutral-200 pt-4">
                <h3 className="mb-2 text-sm font-semibold uppercase tracking-wide text-neutral-700">
                  {t('references')} ({references.length})
                </h3>
                <ol className="space-y-1 text-xs text-neutral-700">
                  {references.map((r) => (
                    <li
                      key={r.n}
                      id={`ref${r.n}`}
                      className="grid grid-cols-[2rem_1fr] gap-1 scroll-mt-20"
                    >
                      <span className="text-neutral-500 tabular-nums">
                        [{r.n}]
                      </span>
                      <a
                        href={r.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-blue-700 hover:underline break-all"
                      >
                        {r.title}
                      </a>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </section>
        );
      })()}

    </article>
  );
}
