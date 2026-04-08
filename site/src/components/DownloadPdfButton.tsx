import { getTranslations } from 'next-intl/server';

/**
 * One-page investor briefing PDF download button.
 *
 * Server Component — renders a plain anchor with the `download` attribute,
 * pointing at `/pdfs/<slug>.pdf` (generated at build time by
 * `analysis/src/s10_generate_district_pdfs.py`).
 *
 * The text comes from the `downloadPdf.button` translation key so it works
 * in both EN and HU locales.
 */
export default async function DownloadPdfButton({
  slug,
  locale,
}: {
  slug: string;
  locale: string;
}) {
  const t = await getTranslations({ locale, namespace: 'downloadPdf' });
  return (
    <a
      href={`/pdfs/${slug}.pdf`}
      download
      className="inline-flex items-center gap-1.5 rounded-md border border-neutral-300 bg-white px-3 py-1.5 text-xs font-semibold text-neutral-800 shadow-sm transition hover:border-neutral-400 hover:bg-neutral-50"
      aria-label={t('button')}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        className="h-3.5 w-3.5"
        aria-hidden="true"
      >
        <path
          fillRule="evenodd"
          d="M10 3a.75.75 0 0 1 .75.75v7.69l2.22-2.22a.75.75 0 1 1 1.06 1.06l-3.5 3.5a.75.75 0 0 1-1.06 0l-3.5-3.5a.75.75 0 1 1 1.06-1.06l2.22 2.22V3.75A.75.75 0 0 1 10 3Zm-6.25 12a.75.75 0 0 1 .75.75v.75c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-.75a.75.75 0 0 1 1.5 0v.75A1.75 1.75 0 0 1 15.25 18.5H4.75A1.75 1.75 0 0 1 3 16.75v-.75a.75.75 0 0 1 .75-.75Z"
          clipRule="evenodd"
        />
      </svg>
      {t('button')}
    </a>
  );
}
