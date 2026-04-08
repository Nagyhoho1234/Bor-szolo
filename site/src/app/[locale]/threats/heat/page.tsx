import type { Metadata } from 'next';
import fs from 'node:fs';
import path from 'node:path';
import { getTranslations } from 'next-intl/server';
import ThreatRanking, { type ThreatBarRow } from '@/components/ThreatRanking';
import ChartModal from '@/components/ChartModal';
import { BORVIDEK_LIST } from '@/lib/district-meta';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Hőhullám-stressz a magyar borvidékeken'
    : 'Heat stress in Hungarian wine districts';
  const description = isHu
    ? 'Hőséges napok (>35 °C) ranglistája a 22 magyar borvidéken — ma és 2100-ban.'
    : 'Hot-day (>35 °C) ranking across the 22 Hungarian wine districts — today and in 2100.';
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
  index: string;
  mean: number;
};
type CckpRow = {
  borvidek: string;
  scenario: string;
  period: string;
  stat: string;
  value: number;
};

function readJson<T>(p: string): T {
  return JSON.parse(fs.readFileSync(p, 'utf-8')) as T;
}

function pickMean(
  rows: NormalsRow[],
  borvidek: string,
  index: string,
): number | null {
  const r = rows.find((x) => x.borvidek === borvidek && x.index === index);
  return r ? r.mean : null;
}

function pickCckp(
  rows: CckpRow[],
  borvidek: string,
  scenario: string,
  period: string,
): number | null {
  const r = rows.find(
    (x) =>
      x.borvidek === borvidek &&
      x.scenario === scenario &&
      x.period === period &&
      x.stat === 'mean',
  );
  return r ? r.value : null;
}

export default async function HeatStressPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'threats.heat' });
  const dataDir = path.join(process.cwd(), 'public', 'data');

  const baseline = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_1991-2020_per_district.json'),
  );
  const fut70_45 = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_2041-2060_rcp45_per_district.json'),
  );
  const fut70_85 = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_2041-2060_rcp85_per_district.json'),
  );
  const fut00_45 = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_2081-2100_rcp45_per_district.json'),
  );
  const fut00_85 = readJson<NormalsRow[]>(
    path.join(dataDir, 'normals', 'normals_2081-2100_rcp85_per_district.json'),
  );
  const cckp245 = readJson<CckpRow[]>(
    path.join(dataDir, 'cckp', 'cckp_cmip6_hd35_ssp245_per_district.json'),
  );
  const cckp585 = readJson<CckpRow[]>(
    path.join(dataDir, 'cckp', 'cckp_cmip6_hd35_ssp585_per_district.json'),
  );

  const INDEX = 'heat_days_t35';
  const data: ThreatBarRow[] = BORVIDEK_LIST.map((d) => ({
    borvidek: d.borvidek,
    baseline: pickMean(baseline, d.borvidek, INDEX),
    rcp45_2070: pickMean(fut70_45, d.borvidek, INDEX),
    rcp85_2070: pickMean(fut70_85, d.borvidek, INDEX),
    rcp45_2100: pickMean(fut00_45, d.borvidek, INDEX),
    rcp85_2100: pickMean(fut00_85, d.borvidek, INDEX),
    cckp_ssp245_2099: pickCckp(cckp245, d.borvidek, 'ssp245', '2080-2099'),
    cckp_ssp585_2099: pickCckp(cckp585, d.borvidek, 'ssp585', '2080-2099'),
  }));

  return (
    <article className="space-y-6">
      <header>
        <p className="text-sm uppercase tracking-wider text-red-700">
          {t('kicker')}
        </p>
        <h1 className="mt-1 text-4xl font-bold">{t('title')}</h1>
        <p className="mt-2 max-w-3xl text-neutral-700">{t('lede')}</p>
      </header>
      <ChartModal
        title={t('chartTitleShort')}
        expanded={
          <ThreatRanking
            rows={data}
            title={t('chartTitleFull')}
            units={t('units')}
            worseWhenHigher
          />
        }
      >
        <ThreatRanking
          rows={data}
          title={t('chartTitleFull')}
          units={t('units')}
          worseWhenHigher
          staticView
        />
      </ChartModal>
    </article>
  );
}
