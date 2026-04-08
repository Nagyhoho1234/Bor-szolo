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
  const title = isHu ? 'Mennyire bízhatunk benne' : 'How sure are we?';
  const description = isHu
    ? 'A klímaprojekciók bizonytalansága, modellek közötti eltérések és mit jelent ez a borvidékeknek.'
    : 'Climate-projection uncertainty, model spread and what it means for the wine districts.';
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

export default async function UncertaintyPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'methods.uncertainty' });
  const tTop = await getTranslations({ locale, namespace: 'methods' });
  return (
    <article className="prose prose-neutral max-w-3xl">
      <p className="text-sm">
        <Link href={`/${locale}/methods`}>{tTop('backToOverview')}</Link>
      </p>
      <h1>{t('title')}</h1>

      <p>{t('intro')}</p>

      <h2>{t('h2Models')}</h2>
      <p>
        {t.rich('modelsBody', {
          em: (chunks) => <em>{chunks}</em>,
        })}
      </p>

      <h2>{t('h2Emissions')}</h2>
      <p>
        {t.rich('emissionsBody', {
          em: (chunks) => <em>{chunks}</em>,
        })}
      </p>

      <h2>{t('h2Coarse')}</h2>
      <p>
        {t.rich('coarseBody', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>

      <h2>{t('h2Grape')}</h2>
      <p>{t('grapeBody')}</p>

      <h2>{t('h2Validation')}</h2>
      <p>{t('validationBody1')}</p>
      <p>
        {t.rich('validationBody2', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>
      <p>
        {t.rich('validationBody3', {
          strong: (chunks) => <strong>{chunks}</strong>,
        })}
      </p>
      <p className="text-sm">
        {t.rich('validationFooter', {
          briefLink: (chunks) => (
            <Link href={`/${locale}/synthesis/policy-brief`}>{chunks}</Link>
          ),
        })}
      </p>

      <h2>{t('h2NotModel')}</h2>
      <p>
        {t.rich('notModelBody', {
          threatsLink: (chunks) => (
            <Link href={`/${locale}/threats`}>{chunks}</Link>
          ),
        })}
      </p>

      <h2>{t('h2OneSentence')}</h2>
      <p>{t('oneSentenceBody')}</p>
    </article>
  );
}
