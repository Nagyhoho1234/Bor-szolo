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
    ? 'Mit jelentenek a számok'
    : 'What the numbers mean';
  const description = isHu
    ? 'Winkler, Huglin, hűvös éjjelek és a többi szőlészeti klímaindex — közérthető magyarázatok.'
    : 'Winkler, Huglin, cool nights and the other viticultural climate indices — explained in plain language.';
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

export default async function IndicesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'methods.indices' });
  const tTop = await getTranslations({ locale, namespace: 'methods' });

  const strongRich = { strong: (chunks: React.ReactNode) => <strong>{chunks}</strong> };

  return (
    <article className="prose prose-neutral max-w-3xl">
      <p className="text-sm">
        <Link href={`/${locale}/methods`}>{tTop('backToOverview')}</Link>
      </p>
      <h1>{t('title')}</h1>

      <p>{t('intro')}</p>

      <h2>{t('h2Winkler')}</h2>
      <p>{t.rich('winklerBody', strongRich)}</p>

      <h2>{t('h2Huglin')}</h2>
      <p>{t.rich('huglinBody', strongRich)}</p>

      <h2>{t('h2Frost')}</h2>
      <p>{t.rich('frostBody', strongRich)}</p>

      <h2>{t('h2Heat')}</h2>
      <p>{t.rich('heatBody', strongRich)}</p>

      <h2>{t('h2Rain')}</h2>
      <p>{t.rich('rainBody', strongRich)}</p>

      <h2>{t('h2Dryness')}</h2>
      <p>{t.rich('drynessBody', strongRich)}</p>

      <h2>{t('h2CoolNights')}</h2>
      <p>{t.rich('coolNightsBody', strongRich)}</p>

      <h2>{t('h2Suitability')}</h2>
      <p>{t('suitabilityBody1')}</p>
      <p>{t('suitabilityBody2')}</p>

      <details className="not-prose mt-8 rounded border border-neutral-300 bg-neutral-50 p-4 text-sm">
        <summary className="cursor-pointer font-semibold">
          {t('formulasSummary')}
        </summary>
        <div className="prose prose-sm mt-3 max-w-none">
          <p>{t('formulasIntro')}</p>
          <ul>
            <li>
              {t.rich('formulaWinkler', {
                strong: (chunks) => <strong>{chunks}</strong>,
                em: (chunks) => <em>{chunks}</em>,
              })}
            </li>
            <li>
              {t.rich('formulaHuglin', strongRich)}
            </li>
            <li>{t.rich('formulaFrost', strongRich)}</li>
            <li>{t.rich('formulaHot', strongRich)}</li>
            <li>{t.rich('formulaPrecip', strongRich)}</li>
            <li>
              {t.rich('formulaDryness', {
                strong: (chunks) => <strong>{chunks}</strong>,
                faoLink: (chunks) => (
                  <a
                    href="https://www.fao.org/3/x0490e/x0490e00.htm"
                    target="_blank"
                    rel="noreferrer"
                  >
                    {chunks}
                  </a>
                ),
              })}
            </li>
            <li>{t.rich('formulaCoolNight', strongRich)}</li>
          </ul>
          <p>
            {t.rich('etccdiBody', {
              link: (chunks) => (
                <a
                  href="https://www.climdex.org/learn/indices/"
                  target="_blank"
                  rel="noreferrer"
                >
                  {chunks}
                </a>
              ),
            })}
          </p>
          <p>
            {t.rich('suitabilityFormula', {
              em: (chunks) => <em>{chunks}</em>,
            })}
          </p>
        </div>
      </details>
    </article>
  );
}
