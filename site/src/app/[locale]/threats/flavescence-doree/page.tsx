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
    ? 'Aranyszínű sárgaság (flavescence dorée) — magyar borvidékek'
    : 'Flavescence dorée — the existential threat to Hungarian vines';
  const description = isHu
    ? 'A kabócával terjedő gyógyíthatatlan szőlőbetegség — kockázat, terjedés és védekezés a magyar borvidékeken.'
    : 'The incurable leafhopper-borne phytoplasma disease — spread, risk and containment across Hungarian wine districts.';
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

export default async function FlavescenceDoreePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'threats.fd' });
  return (
    <article className="prose prose-neutral max-w-3xl space-y-4">
      <header className="not-prose">
        <p className="text-sm uppercase tracking-wider text-red-700">
          {t('kicker')}
        </p>
        <h1 className="mt-1 text-4xl font-bold">{t('title')}</h1>
        <p className="mt-2 text-lg text-neutral-700">
          {t.rich('lede', { em: (chunks) => <em>{chunks}</em> })}
        </p>
      </header>

      <h2>{t('h2Status')}</h2>
      <p>
        {t.rich('statusBody', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>

      <h2>{t('h2Background')}</h2>
      <p>
        {t.rich('backgroundBody1', {
          em: (chunks) => <em>{chunks}</em>,
        })}
      </p>
      <p>
        {t.rich('backgroundBody2', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>

      <h2>{t('h2Climate')}</h2>
      <p>
        {t.rich('climateBody', {
          em: (chunks) => <em>{chunks}</em>,
          indicesLink: (chunks) => (
            <Link href={`/${locale}/methods/indices`}>{chunks}</Link>
          ),
          compareLink: (chunks) => (
            <Link href={`/${locale}/compare`}>{chunks}</Link>
          ),
        })}
      </p>

      <h2>{t('h2Sources')}</h2>
      <ul className="text-sm">
        <li>
          NÉBIH (National Food Chain Safety Office) press releases, 2025 — Trade
          Magazin English coverage:{' '}
          <a
            href="https://trademagazin.hu/en/nebih-az-intenziv-felderites-ujabb-fd-vel-fertozott-teruleteket-tart-fel/"
            target="_blank"
            rel="noreferrer"
          >
            &quot;Nébih: Intensive reconnaissance revealed new areas infected with FD&quot;
          </a>
          .
        </li>
        <li>
          <a
            href="https://www.vinetur.com/en/2025122294408/flavescence-doree-hits-21-of-22-hungarian-wine-regions-threatening-270-million-liter-industry.html"
            target="_blank"
            rel="noreferrer"
          >
            Vinetur (Dec 2025): &quot;Flavescence Dorée Hits 21 of 22 Hungarian Wine
            Regions, Threatening 270 Million-Liter Industry&quot;
          </a>
          .
        </li>
        <li>
          <a
            href="https://magazine.wein.plus/news/gold-yellow-yellowing-is-taking-on-massive-proportions-in-hungary-21-out-of-22-growing-regions-are-threatened"
            target="_blank"
            rel="noreferrer"
          >
            wein.plus (2025): &quot;Gold-yellow yellowing is taking on massive
            proportions in Hungary&quot;
          </a>
          .
        </li>
        <li>
          <a
            href="https://thegrapereset.com/bites/phytoplasma-disease-threatens-the-heart-of-hungarian-wine-country"
            target="_blank"
            rel="noreferrer"
          >
            The Grape Reset: &quot;Phytoplasma Disease Threatens the Heart of
            Hungarian Wine Country&quot;
          </a>
          .
        </li>
        <li>
          AGES Austria —{' '}
          <a
            href="https://www.ages.at/en/plant/plant-health/pests-from-a-to-z/flavescence-doree"
            target="_blank"
            rel="noreferrer"
          >
            Flavescence dorée disease profile
          </a>
          .
        </li>
      </ul>

      <p className="not-prose mt-4 rounded border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900">
        {t.rich('draftNote', {
          strong: (chunks) => <strong>{chunks}</strong>,
          code: (chunks) => <code>{chunks}</code>,
        })}
      </p>
    </article>
  );
}
