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
  const title = isHu ? 'A projektről' : 'About this atlas';
  const description = isHu
    ? 'Ki, miért és hogyan készítette a Magyar Borvidék Klímaatlaszt — kapcsolat és háttér.'
    : 'Who built the Hungarian Wine Climate Atlas, why, and how — context and contact.';
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

export default async function AboutPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'about' });
  return (
    <article className="prose prose-neutral max-w-3xl">
      <h1>{t('title')}</h1>
      <p>
        {t.rich('intro', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>

      <h2>{t('h2What')}</h2>
      <ul>
        <li>
          {t.rich('whatBrowse', {
            link: (chunks) => (
              <Link href={`/${locale}/districts`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('whatCompare', {
            link: (chunks) => (
              <Link href={`/${locale}/compare`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('whatVarieties', {
            link: (chunks) => (
              <Link href={`/${locale}/varieties`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('whatThreats', {
            link: (chunks) => (
              <Link href={`/${locale}/threats`}>{chunks}</Link>
            ),
            fdLink: (chunks) => (
              <Link href={`/${locale}/threats/flavescence-doree`}>
                {chunks}
              </Link>
            ),
          })}
        </li>
        <li>
          {t.rich('whatDownloads', {
            link: (chunks) => (
              <Link href={`/${locale}/downloads`}>{chunks}</Link>
            ),
          })}
        </li>
      </ul>

      <h2>{t('h2Methodology')}</h2>
      <p>
        {t.rich('methodologyBody', {
          methodsLink: (chunks) => (
            <Link href={`/${locale}/methods`}>{chunks}</Link>
          ),
          sourcesLink: (chunks) => (
            <Link href={`/${locale}/methods/data-sources`}>{chunks}</Link>
          ),
          indicesLink: (chunks) => (
            <Link href={`/${locale}/methods/indices`}>{chunks}</Link>
          ),
          uncertaintyLink: (chunks) => (
            <Link href={`/${locale}/methods/uncertainty`}>{chunks}</Link>
          ),
        })}
      </p>

      <h2>{t('h2Sources')}</h2>
      <ul>
        <li>
          <a
            href="https://nimbus.elte.hu/FORESEE/"
            target="_blank"
            rel="noreferrer"
          >
            FORESEE database — ELTE Department of Meteorology
          </a>
        </li>
        <li>
          <a
            href="https://climateknowledgeportal.worldbank.org/"
            target="_blank"
            rel="noreferrer"
          >
            World Bank Climate Change Knowledge Portal (CMIP6)
          </a>
        </li>
        <li>
          <a href="https://odp.met.hu/" target="_blank" rel="noreferrer">
            HungaroMet Open Data Portal
          </a>
        </li>
        <li>
          <a
            href="https://doi.org/10.3389/fpls.2025.1481431"
            target="_blank"
            rel="noreferrer"
          >
            Lakatos &amp; Nagy 2025 — Hungarian wine-region temperature
            indices, Frontiers in Plant Science
          </a>
        </li>
      </ul>

      <h2>{t('h2License')}</h2>
      <p>
        {t.rich('licenseBody', {
          em: (chunks) => <em>{chunks}</em>,
        })}
      </p>

      <h2>{t('h2Repro')}</h2>
      <p>
        {t.rich('reproBody', {
          link: (chunks) => (
            <Link href={`/${locale}/downloads`}>{chunks}</Link>
          ),
        })}
      </p>
    </article>
  );
}
