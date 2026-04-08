import type { Metadata } from 'next';
import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import { BORVIDEK_LIST, slugify } from '@/lib/district-meta';

// All varieties that appear as a principal variety in any district
const ALL_VARIETIES = Array.from(
  new Set(BORVIDEK_LIST.flatMap((d) => d.principalVarieties)),
).sort();

export function generateStaticParams() {
  return ALL_VARIETIES.map((v) => ({ variety: slugify(v) }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; variety: string }>;
}): Promise<Metadata> {
  const { locale, variety: slug } = await params;
  const variety = ALL_VARIETIES.find((v) => slugify(v) === slug);
  if (!variety) return {};
  const isHu = locale === 'hu';
  const grownIn = BORVIDEK_LIST.filter((d) =>
    d.principalVarieties.includes(variety),
  );
  const title = isHu
    ? `${variety} — szőlőfajta a magyar borvidékeken`
    : `${variety} — Hungarian wine grape variety`;
  const districts = grownIn
    .slice(0, 4)
    .map((d) => d.borvidek)
    .join(', ');
  const description = isHu
    ? `${variety}: főfajta ${grownIn.length} magyar borvidéken (${districts}…). Klímaalkalmasság ma és 2100-ban.`
    : `${variety}: principal in ${grownIn.length} Hungarian wine districts (${districts}…). Climate suitability today and in 2100.`;
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

export default async function VarietyDetailPage({
  params,
}: {
  params: Promise<{ variety: string; locale: string }>;
}) {
  const { variety: slug, locale } = await params;
  const t = await getTranslations({ locale, namespace: 'varieties.detail' });
  const variety = ALL_VARIETIES.find((v) => slugify(v) === slug);
  if (!variety) {
    return (
      <section>
        <h1 className="text-3xl font-bold">{t('notFound')}</h1>
        <Link
          href={`/${locale}/varieties`}
          className="mt-2 inline-block text-blue-600 hover:underline"
        >
          {t('backToAll')}
        </Link>
      </section>
    );
  }
  const grownIn = BORVIDEK_LIST.filter((d) =>
    d.principalVarieties.includes(variety),
  );
  return (
    <section className="space-y-6">
      <div>
        <p className="text-sm uppercase tracking-wider text-neutral-500">
          {t('kicker')}
        </p>
        <h1 className="text-4xl font-bold">{variety}</h1>
        <p className="mt-1 text-neutral-600">
          {t('principalIn', { count: grownIn.length })}
        </p>
      </div>
      <div>
        <h2 className="mb-3 text-xl font-semibold">{t('grownAsPrincipal')}</h2>
        <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {grownIn.map((d) => (
            <li key={d.slug}>
              <Link
                href={`/${locale}/districts/${d.slug}`}
                className="block rounded border border-neutral-200 bg-white p-3 hover:border-neutral-400"
              >
                <span className="font-medium">{d.borvidek}</span>
                <span className="ml-2 text-xs text-neutral-500">
                  {d.borregio}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
      <p className="text-sm text-neutral-600">
        {t.rich('envelopeNote', {
          code: (chunks) => <code className="text-xs">{chunks}</code>,
          methodsLink: (chunks) => (
            <Link
              href={`/${locale}/methods/indices`}
              className="text-blue-600 hover:underline"
            >
              {chunks}
            </Link>
          ),
        })}
      </p>
    </section>
  );
}
