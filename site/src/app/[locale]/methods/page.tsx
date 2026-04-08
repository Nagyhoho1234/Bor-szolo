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
    ? 'Hogyan készült a klímaatlasz'
    : 'How the climate atlas was built';
  const description = isHu
    ? 'Az adatok forrása, a számított indexek és a bizonytalanságok — közérthetően.'
    : 'Where the data come from, what the indices mean and how sure we are — in plain language.';
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

export default async function MethodsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'methods.overview' });
  const tTop = await getTranslations({ locale, namespace: 'methods' });
  return (
    <article className="prose prose-neutral max-w-3xl">
      <h1>{tTop('title')}</h1>

      <p>{t('intro')}</p>

      <h2>{t('h2Find')}</h2>
      <p>
        {t.rich('findBody', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>

      <h2>{t('h2Numbers')}</h2>
      <p>
        {t.rich('numbersBody', {
          dataLink: (chunks) => (
            <Link href={`/${locale}/methods/data-sources`}>{chunks}</Link>
          ),
        })}
      </p>

      <h2>{t('h2How')}</h2>
      <ul>
        <li>
          {t.rich('howCurious', {
            strong: (chunks) => <strong>{chunks}</strong>,
            mapLink: (chunks) => (
              <Link href={`/${locale}`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('howCompare', {
            strong: (chunks) => <strong>{chunks}</strong>,
            compareLink: (chunks) => (
              <Link href={`/${locale}/compare`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('howNumber', {
            strong: (chunks) => <strong>{chunks}</strong>,
            indicesLink: (chunks) => (
              <Link href={`/${locale}/methods/indices`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('howSure', {
            strong: (chunks) => <strong>{chunks}</strong>,
            uncertaintyLink: (chunks) => (
              <Link href={`/${locale}/methods/uncertainty`}>{chunks}</Link>
            ),
          })}
        </li>
      </ul>

      <h2>{t('h2Limits')}</h2>
      <p>
        {t.rich('limitsBody', {
          em: (chunks) => <em>{chunks}</em>,
        })}
      </p>

      <h2>{t('h2Depth')}</h2>
      <ul>
        <li>
          {t.rich('depthData', {
            link: (chunks) => (
              <Link href={`/${locale}/methods/data-sources`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('depthIndices', {
            link: (chunks) => (
              <Link href={`/${locale}/methods/indices`}>{chunks}</Link>
            ),
          })}
        </li>
        <li>
          {t.rich('depthUncertainty', {
            link: (chunks) => (
              <Link href={`/${locale}/methods/uncertainty`}>{chunks}</Link>
            ),
          })}
        </li>
      </ul>
    </article>
  );
}
