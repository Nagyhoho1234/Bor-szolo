import type { Metadata } from 'next';
import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import { BORVIDEK_LIST } from '@/lib/district-meta';
import {
  loadDescriptions,
  localizeDescription,
  type DistrictDescription,
} from '@/lib/data';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'A 22 magyar borvidék'
    : 'All 22 Hungarian wine districts';
  const description = isHu
    ? 'Böngéssze a 22 magyar borvidéket — terület, főfajták és klímakockázati áttekintés.'
    : 'Browse all 22 Hungarian wine districts — area, principal varieties and climate-risk overview.';
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

export default async function DistrictsIndexPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'districts' });
  const descriptions = (await loadDescriptions().catch(
    () => ({}) as Record<string, DistrictDescription>,
  )) as Record<string, DistrictDescription>;

  const sorted = [...BORVIDEK_LIST].sort((a, b) =>
    a.borvidek.localeCompare(b.borvidek),
  );

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">{t('indexTitle')}</h1>
        <p className="mt-2 text-neutral-600">{t('indexSubtitle')}</p>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {sorted.map((d) => {
          const desc = localizeDescription(descriptions[d.slug], locale);
          return (
            <Link
              key={d.slug}
              href={`/${locale}/districts/${d.slug}`}
              className="group block rounded-lg border border-neutral-200 bg-white p-5 transition hover:border-neutral-400 hover:shadow"
            >
              <p className="text-xl font-semibold group-hover:text-blue-700">
                {desc?.name_hu ?? d.borvidek}
              </p>
              <p className="text-xs text-neutral-500">
                {desc?.name_en ?? d.nameEn}
              </p>
              {desc?.tagline && (
                <p className="mt-2 text-sm italic leading-snug text-neutral-700">
                  {desc.tagline}
                </p>
              )}
              <div className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs text-neutral-600">
                <span>
                  {d.nSettlements} {t('settlements')}
                </span>
                <span>{d.areaKm2.toFixed(0)} km²</span>
              </div>
              {desc?.flagship_wines?.length ? (
                <p className="mt-2 text-xs text-neutral-700">
                  <span className="font-semibold">{t('flagshipLabel')}: </span>
                  {desc.flagship_wines.join(' · ')}
                </p>
              ) : (
                <p className="mt-2 line-clamp-1 text-xs text-neutral-600">
                  {d.principalVarieties.slice(0, 5).join(' · ')}
                </p>
              )}
              {desc?.climate_threat_headline && (
                <p className="mt-2 line-clamp-2 border-t border-neutral-100 pt-2 text-xs text-amber-700">
                  ⚠ {desc.climate_threat_headline}
                </p>
              )}
            </Link>
          );
        })}
      </div>
    </section>
  );
}
