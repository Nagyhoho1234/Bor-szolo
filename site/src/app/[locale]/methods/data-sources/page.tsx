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
  const title = isHu ? 'Az adatokról' : 'About the data';
  const description = isHu
    ? 'A klímaatlasz adatforrásai — FORESEE, World Bank CCKP, HungaroMet és az indexek származtatása.'
    : 'Data sources behind the atlas — FORESEE, World Bank CCKP, HungaroMet and how the indices are derived.';
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

export default async function DataSourcesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'methods.data' });
  const tTop = await getTranslations({ locale, namespace: 'methods' });
  return (
    <article className="prose prose-neutral max-w-3xl">
      <p className="text-sm">
        <Link href={`/${locale}/methods`}>{tTop('backToOverview')}</Link>
      </p>
      <h1>{t('title')}</h1>

      <p>{t('intro')}</p>

      <h2>{t('h2Foresee')}</h2>
      <p>
        {t('foreseeBody')}{' '}
        <a href="https://nimbus.elte.hu/FORESEE/" target="_blank" rel="noreferrer">
          {t('foreseeLink')}
        </a>
      </p>

      <h2>{t('h2WB')}</h2>
      <p>
        {t.rich('wbBody', {
          link: (chunks) => (
            <a
              href="https://climateknowledgeportal.worldbank.org/"
              target="_blank"
              rel="noreferrer"
            >
              {chunks}
            </a>
          ),
        })}
      </p>

      <h2>{t('h2HungaroMet')}</h2>
      <p>
        {t.rich('hungaroMetBody', {
          link: (chunks) => (
            <a href="https://odp.met.hu/" target="_blank" rel="noreferrer">
              {chunks}
            </a>
          ),
        })}
      </p>

      <h2>{t('h2BuiltOn')}</h2>
      <p>
        {t.rich('builtOnBody', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>

      <h2>{t('h2NotDo')}</h2>
      <p>
        {t.rich('notDoBody', {
          em: (chunks) => <em>{chunks}</em>,
          link: (chunks) => (
            <Link href={`/${locale}/downloads`}>{chunks}</Link>
          ),
        })}
      </p>

      <hr />

      <h2 className="text-base">{t('furtherReading')}</h2>
      <ul className="text-sm">
        <li>
          Dobor, L. et al. (2015). Bridging the gap between climate models and
          impact studies: the FORESEE Database. <em>Geoscience Data Journal</em>.{' '}
          <a href="https://doi.org/10.1002/gdj3.22" target="_blank" rel="noreferrer">
            Open access
          </a>
          .
        </li>
        <li>
          Lakatos, M. &amp; Nagy, J. (2025). Historical and future temperature
          changes in Hungarian wine regions, 1971–2100.{' '}
          <em>Frontiers in Plant Science</em>.{' '}
          <a
            href="https://doi.org/10.3389/fpls.2025.1481431"
            target="_blank"
            rel="noreferrer"
          >
            Open access
          </a>
          .
        </li>
        <li>
          Tonietto, J. &amp; Carbonneau, A. (2004). A multicriteria climatic
          classification system for grape-growing regions worldwide.{' '}
          <em>Agricultural and Forest Meteorology</em>.
        </li>
        <li>
          Allen, R.G. et al. (1998). Crop evapotranspiration — FAO Irrigation
          and Drainage Paper 56.{' '}
          <a href="https://www.fao.org/3/x0490e/x0490e00.htm" target="_blank" rel="noreferrer">
            FAO open report
          </a>
          .
        </li>
        <li>
          OpenStreetMap contributors —{' '}
          <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">
            ODbL licence
          </a>
          .
        </li>
      </ul>
    </article>
  );
}
