import type { Metadata } from 'next';
import Link from 'next/link';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import DistrictMapClient from '@/components/DistrictMapClient';
import { BORVIDEK_LIST } from '@/lib/district-meta';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Magyar Borvidék Klímaatlasz'
    : 'Hungarian Wine Climate Atlas';
  const description = isHu
    ? 'A 22 magyar borvidék klímakitettsége, fajtaalkalmasság és betegségkockázatok — megfigyelésektől 2100-ig.'
    : 'Climate exposure, variety suitability and disease threats for all 22 Hungarian wine districts — observations to 2100.';
  return {
    title: { absolute: title },
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

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: 'home' });

  const headlines = [
    { key: 'fd', href: '/threats/flavescence-doree' },
    { key: 'tokaj', href: '/districts/tokaji' },
    { key: 'villany', href: '/districts/villanyi' },
    { key: 'coverage', href: '/methods' },
  ] as const;

  return (
    <section className="space-y-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
          {t('title')}
        </h1>
        <p className="mt-3 max-w-3xl text-base text-neutral-600 sm:text-lg">
          {t('intro')}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {headlines.map((h) => (
          <Link
            key={h.key}
            href={`/${locale}${h.href}`}
            className="block rounded-lg border border-neutral-200 bg-white p-4 transition hover:border-neutral-400 hover:shadow"
          >
            <p className="text-3xl font-bold tabular-nums">
              {t(`headlines.${h.key}.big`)}
            </p>
            <p className="mt-1 text-xs text-neutral-600">
              {t(`headlines.${h.key}.label`)}
            </p>
          </Link>
        ))}
      </div>

      <div>
        <h2 className="mb-3 text-2xl font-semibold">{t('mapTitle')}</h2>
        <p className="mb-3 text-sm text-neutral-600">{t('mapSubtitle')}</p>
        <div className="h-[360px] w-full overflow-hidden rounded-lg border border-neutral-200 sm:h-[480px]">
          <DistrictMapClient />
        </div>
      </div>

      <div>
        <h2 className="mb-3 text-2xl font-semibold">{t('browseTitle')}</h2>
        <p className="mb-4 text-sm text-neutral-600">{t('browseSubtitle')}</p>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
          {[...BORVIDEK_LIST]
            .sort((a, b) => a.borvidek.localeCompare(b.borvidek))
            .map((d) => (
              <Link
                key={d.slug}
                href={`/${locale}/districts/${d.slug}`}
                className="rounded border border-neutral-200 bg-white p-2 text-sm transition hover:border-neutral-400 hover:shadow"
              >
                {d.borvidek}
              </Link>
            ))}
        </div>
      </div>

      <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
        <p>
          {t.rich('draftNotice', {
            strong: (chunks) => <strong>{chunks}</strong>,
            methodsLink: (chunks) => (
              <Link href={`/${locale}/methods`} className="underline">
                {chunks}
              </Link>
            ),
          })}
        </p>
      </div>
    </section>
  );
}
