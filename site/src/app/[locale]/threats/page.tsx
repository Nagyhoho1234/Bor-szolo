import type { Metadata } from 'next';
import Link from 'next/link';
import { getTranslations } from 'next-intl/server';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Klíma- és betegségfenyegetések a magyar szőlőtermesztésben'
    : 'Climate and disease threats to Hungarian viticulture';
  const description = isHu
    ? 'Aranyszínű sárgaság, hőhullám, aszály, fagy — a négy fő veszélyforrás a magyar borvidékeken.'
    : 'Flavescence dorée, heat, drought and frost — the four headline threats to Hungarian wine districts.';
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

const THREAT_SLUGS = [
  { slug: 'flavescence-doree', key: 'fd', severity: 'catastrophic', severityColor: 'bg-red-600' },
  { slug: 'heat', key: 'heat', severity: 'high', severityColor: 'bg-orange-500' },
  { slug: 'drought', key: 'drought', severity: 'high', severityColor: 'bg-amber-500' },
  { slug: 'frost', key: 'frost', severity: 'medium', severityColor: 'bg-blue-500' },
] as const;

export default async function ThreatsOverviewPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'threats' });
  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-4xl font-bold">{t('indexTitle')}</h1>
        <p className="mt-2 max-w-3xl text-neutral-700">{t('indexSubtitle')}</p>
      </header>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {THREAT_SLUGS.map((it) => (
          <Link
            key={it.slug}
            href={`/${locale}/threats/${it.slug}`}
            className="block rounded-lg border border-neutral-200 bg-white p-5 transition hover:border-neutral-400 hover:shadow"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-wider text-neutral-500">
                  {t(`cards.${it.key}.flag`)}
                </p>
                <h2 className="mt-1 text-xl font-bold">
                  {t(`cards.${it.key}.title`)}
                </h2>
              </div>
              <span
                className={`rounded px-2 py-0.5 text-xs font-semibold uppercase text-white ${it.severityColor}`}
              >
                {t(`severity.${it.severity}`)}
              </span>
            </div>
            <p className="mt-3 text-sm text-neutral-700">
              {t(`cards.${it.key}.summary`)}
            </p>
          </Link>
        ))}
      </div>
      <p className="rounded border border-amber-200 bg-amber-50 p-3 text-xs text-amber-900">
        {t.rich('draftWarning', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>
    </section>
  );
}
