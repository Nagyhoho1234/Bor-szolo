import type { Metadata } from 'next';
import fs from 'node:fs';
import path from 'node:path';
import { getTranslations } from 'next-intl/server';
import RankingTable, { type RankingRow } from '@/components/RankingTable';
import { BORVIDEK_LIST } from '@/lib/district-meta';
import DistrictPickerForm from './DistrictPickerForm';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Borvidékek összehasonlítása'
    : 'Compare Hungarian wine districts';
  const description = isHu
    ? 'Hasonlítsa össze a magyar borvidékeket hőmérsékleti összegek, csapadék, fagy- és hőhullámkockázat szerint.'
    : 'Compare Hungarian wine districts head-to-head on heat sums, rainfall, frost risk and heat-stress days.';
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

type NormalsRow = {
  borvidek: string;
  borregio: string;
  index: string;
  mean: number;
  anomaly_vs_1991_2020: number | null;
};

type HeadlineRow = {
  borvidek: string;
  biggest_winner_variety: string;
  winner_delta: number;
  biggest_loser_variety: string;
  loser_delta: number;
};

function readJson<T>(p: string): T {
  return JSON.parse(fs.readFileSync(p, 'utf-8')) as T;
}

function pickMean(rows: NormalsRow[], borvidek: string, index: string): number | null {
  const r = rows.find((x) => x.borvidek === borvidek && x.index === index);
  return r ? r.mean : null;
}

export default async function ComparePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'compare' });
  const dataDir = path.join(process.cwd(), 'public', 'data');
  const baselineNormals = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_1991-2020_per_district.json'),
  );
  const futureNormals = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_2081-2100_rcp85_per_district.json'),
  );
  // headline is a CSV — parse it inline (small file, 22 rows)
  const csv = fs.readFileSync(
    path.join(dataDir, 'variety_match', 'headline_winners_losers.csv'),
    'utf-8',
  );
  const lines = csv.trim().split(/\r?\n/);
  const header = lines[0].split(',');
  const headline: HeadlineRow[] = lines.slice(1).map((line) => {
    const cells = line.split(',');
    const row: Record<string, string> = {};
    header.forEach((h, i) => (row[h.trim()] = cells[i]));
    return {
      borvidek: row.borvidek,
      biggest_winner_variety: row.biggest_winner_variety,
      winner_delta: parseFloat(row.winner_delta),
      biggest_loser_variety: row.biggest_loser_variety,
      loser_delta: parseFloat(row.loser_delta),
    };
  });

  const data: RankingRow[] = BORVIDEK_LIST.map((d) => {
    const winklerNow = pickMean(baselineNormals, d.borvidek, 'winkler_gdd');
    const winklerFuture = pickMean(futureNormals, d.borvidek, 'winkler_gdd');
    const heatDaysFuture = pickMean(futureNormals, d.borvidek, 'heat_days_t35');
    const droughtFuture = pickMean(futureNormals, d.borvidek, 'p_minus_pet');
    const h = headline.find((x) => x.borvidek === d.borvidek);
    return {
      borvidek: d.borvidek,
      borregio: d.borregio,
      winklerNow,
      winklerFuture,
      winklerDelta:
        winklerNow != null && winklerFuture != null
          ? winklerFuture - winklerNow
          : null,
      heatDaysFuture,
      droughtFuture,
      winner: h?.biggest_winner_variety ?? '—',
      loser: h?.biggest_loser_variety ?? '—',
    };
  });

  const pickerOptions = BORVIDEK_LIST.map((d) => ({
    slug: d.slug,
    label: d.borvidek,
  })).sort((x, y) => x.label.localeCompare(y.label, 'hu'));

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">{t('title')}</h1>
        <p className="mt-2 text-neutral-600">{t('subtitle')}</p>
      </div>
      <DistrictPickerForm
        locale={locale}
        options={pickerOptions}
        defaultA="tokaji"
        defaultB="egri"
        labels={{
          heading: t('picker.heading'),
          subtitle: t('picker.subtitle'),
          districtA: t('picker.districtA'),
          districtB: t('picker.districtB'),
          submit: t('picker.submit'),
          sameWarning: t('picker.sameWarning'),
        }}
      />
      <RankingTable
        data={data}
        locale={locale}
        searchPlaceholder={t('searchPlaceholder')}
        labels={{
          borvidek: t('columns.borvidek'),
          borregio: t('columns.borregio'),
          winklerNow: t('columns.winklerNow'),
          winklerFuture: t('columns.winklerFuture'),
          winklerDelta: t('columns.winklerDelta'),
          heatDaysFuture: t('columns.heatDaysFuture'),
          droughtFuture: t('columns.droughtFuture'),
          winner: t('columns.winner'),
          loser: t('columns.loser'),
        }}
      />
    </section>
  );
}
