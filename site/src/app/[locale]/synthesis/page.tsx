import type { Metadata } from 'next';
import Link from 'next/link';
import fs from 'node:fs';
import path from 'node:path';
import { getTranslations, setRequestLocale } from 'next-intl/server';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Szintézis: a magyar bor klímahelyzete'
    : 'Synthesis: the Hungarian wine climate outlook';
  const description = isHu
    ? 'A teljes adatbázis legfontosabb tanulságai egy helyen — kutatóknak és döntéshozóknak.'
    : 'The headline takeaways from the full dataset — for researchers and for decision-makers.';
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

function getSynthesisDate(): string {
  // Read the freshest mtime of the two synthesis briefs as the
  // human-readable "as of" date for the hub caveat. Falls back to
  // today if the files cannot be stat'd at build time.
  try {
    const root = path.join(process.cwd(), '..', 'research', 'synthesis');
    const files = ['scientific_synthesis.md', 'decision_support_brief.md'];
    const stamps = files
      .map((f) => {
        try {
          return fs.statSync(path.join(root, f)).mtime;
        } catch {
          return null;
        }
      })
      .filter((d): d is Date => d != null);
    if (stamps.length === 0) return new Date().toISOString().slice(0, 10);
    const newest = stamps.reduce((a, b) => (a > b ? a : b));
    return newest.toISOString().slice(0, 10);
  } catch {
    return new Date().toISOString().slice(0, 10);
  }
}

export default async function SynthesisHubPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: 'synthesis.hub' });
  const asOf = getSynthesisDate();

  const englishOnlyTag =
    locale === 'hu' ? (
      <span className="ml-2 text-xs font-normal text-neutral-500">
        ({t('englishOnly')})
      </span>
    ) : null;

  return (
    <article className="prose prose-neutral max-w-3xl">
      <h1>{t('title')}</h1>
      <p>{t('intro')}</p>

      <div className="not-prose mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
        <Link
          href={`/${locale}/synthesis/scientific`}
          className="block rounded-lg border border-neutral-200 bg-white p-5 shadow-sm transition hover:border-neutral-400 hover:shadow-md"
        >
          <div className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
            {t('scientific.kicker')}
          </div>
          <h2 className="mt-1 text-lg font-semibold text-neutral-900">
            {t('scientific.title')}
            {englishOnlyTag}
          </h2>
          <p className="mt-2 text-sm text-neutral-700">
            {t('scientific.description')}
          </p>
          <p className="mt-3 text-xs text-neutral-500">{t('scientific.meta')}</p>
        </Link>

        <Link
          href={`/${locale}/synthesis/policy-brief`}
          className="block rounded-lg border border-neutral-200 bg-white p-5 shadow-sm transition hover:border-neutral-400 hover:shadow-md"
        >
          <div className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
            {t('policy.kicker')}
          </div>
          <h2 className="mt-1 text-lg font-semibold text-neutral-900">
            {t('policy.title')}
            {englishOnlyTag}
          </h2>
          <p className="mt-2 text-sm text-neutral-700">
            {t('policy.description')}
          </p>
          <p className="mt-3 text-xs text-neutral-500">{t('policy.meta')}</p>
        </Link>
      </div>

      <p className="mt-8 text-xs text-neutral-500">
        {t('caveat', { date: asOf })}
      </p>
    </article>
  );
}
