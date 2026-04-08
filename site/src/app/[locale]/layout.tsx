import { NextIntlClientProvider } from 'next-intl';
import { getMessages, getTranslations, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { locales } from '@/lib/i18n';
import LangSwitcher from '@/components/LangSwitcher';

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!(locales as readonly string[]).includes(locale)) notFound();
  setRequestLocale(locale);
  const messages = await getMessages();
  const tNav = await getTranslations({ locale, namespace: 'nav' });
  const tF = await getTranslations({ locale, namespace: 'footer' });

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <header className="border-b border-neutral-200">
        <nav className="mx-auto flex max-w-6xl items-center gap-3 overflow-x-auto px-3 py-3 text-sm whitespace-nowrap sm:gap-6 sm:px-4 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          <Link href={`/${locale}`} className="shrink-0 font-semibold">
            {tNav('brand')}
          </Link>
          <Link href={`/${locale}/districts`} className="shrink-0">{tNav('districts')}</Link>
          <Link href={`/${locale}/compare`} className="shrink-0">{tNav('compare')}</Link>
          <Link href={`/${locale}/varieties`} className="shrink-0">{tNav('varieties')}</Link>
          <Link href={`/${locale}/threats`} className="shrink-0">{tNav('threats')}</Link>
          <Link href={`/${locale}/methods`} className="shrink-0">{tNav('methods')}</Link>
          <Link href={`/${locale}/synthesis`} className="shrink-0">{tNav('synthesis')}</Link>
          <Link href={`/${locale}/about`} className="shrink-0">{tNav('about')}</Link>
          <Link href={`/${locale}/downloads`} className="shrink-0">{tNav('downloads')}</Link>
          <span className="ml-auto shrink-0 pl-2">
            <LangSwitcher currentLocale={locale} />
          </span>
        </nav>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6 sm:py-8">{children}</main>
      <footer className="mt-12 border-t border-neutral-200 bg-neutral-50">
        <div className="mx-auto max-w-6xl px-4 py-8 text-xs text-neutral-700">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <h3 className="mb-2 text-sm font-semibold text-neutral-900">
                {tF('climateData')}
              </h3>
              <ul className="space-y-1">
                <li>
                  <a
                    href="https://nimbus.elte.hu/FORESEE/"
                    target="_blank"
                    rel="noreferrer"
                    className="hover:underline"
                  >
                    FORESEE database (ELTE Department of Meteorology)
                  </a>{' '}
                  — {tF('foreseeDesc')}{' '}
                  <a
                    href="https://doi.org/10.1002/gdj3.22"
                    target="_blank"
                    rel="noreferrer"
                    className="hover:underline"
                  >
                    {tF('foreseeAuthor')}
                  </a>
                </li>
                <li>
                  <a
                    href="https://climateknowledgeportal.worldbank.org/"
                    target="_blank"
                    rel="noreferrer"
                    className="hover:underline"
                  >
                    World Bank Climate Change Knowledge Portal (CCKP)
                  </a>{' '}
                  — {tF('wbDesc')}
                </li>
                <li>
                  <a
                    href="https://odp.met.hu/"
                    target="_blank"
                    rel="noreferrer"
                    className="hover:underline"
                  >
                    HungaroMet Open Data Portal (odp.met.hu)
                  </a>{' '}
                  — {tF('hungaroMetDesc')}
                </li>
                <li>
                  <a
                    href="https://doi.org/10.3389/fpls.2025.1481431"
                    target="_blank"
                    rel="noreferrer"
                    className="hover:underline"
                  >
                    Lakatos & Nagy 2025 — Temperature indices for Hungarian wine
                    regions (Frontiers in Plant Science)
                  </a>{' '}
                  — {tF('lakatosDesc')}
                </li>
              </ul>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold text-neutral-900">
                {tF('wineRefs')}
              </h3>
              <ul className="space-y-1">
                <li>
                  <a href="https://winesofhungary.hu/" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('winesOfHungary')}
                  </a>
                </li>
                <li>
                  <a href="https://hungarianwines.eu/" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('hungarianWinesEu')}
                  </a>
                </li>
                <li>
                  <a href="https://tastehungary.com/journal/categories/wine/" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('tasteHungary')}
                  </a>
                </li>
                <li>
                  <a href="https://en.wikipedia.org/wiki/Hungarian_wine" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('wikipedia')}
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold text-neutral-900">
                {tF('threatsPesticides')}
              </h3>
              <ul className="space-y-1">
                <li>
                  <a href="https://portal.nebih.gov.hu/" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('nebih')}
                  </a>
                </li>
                <li>
                  <a href="https://food.ec.europa.eu/plants/pesticides/eu-pesticides-database_en" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('euPesticides')}
                  </a>
                </li>
                <li>
                  <a href="https://www.efsa.europa.eu/" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('efsa')}
                  </a>
                </li>
                <li>
                  <a href="https://www.eppo.int/" target="_blank" rel="noreferrer" className="hover:underline">
                    {tF('eppo')}
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold text-neutral-900">
                {tF('thisSite')}
              </h3>
              <ul className="space-y-1">
                <li>
                  <Link href={`/${locale}/methods`} className="hover:underline">
                    {tF('methodsLink')}
                  </Link>
                </li>
                <li>
                  <Link href={`/${locale}/downloads`} className="hover:underline">
                    {tF('downloadsLink')}
                  </Link>
                </li>
                <li>
                  <Link href={`/${locale}/about`} className="hover:underline">
                    {tF('aboutLink')}
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-6 border-t border-neutral-200 pt-4 text-[11px] text-neutral-500">
            <p>
              {tF.rich('copyright', {
                year: new Date().getFullYear(),
                foreseeLink: (chunks) => (
                  <a
                    href="https://nimbus.elte.hu/FORESEE/"
                    target="_blank"
                    rel="noreferrer"
                    className="underline"
                  >
                    {chunks}
                  </a>
                ),
                wbLink: (chunks) => (
                  <a
                    href="https://climateknowledgeportal.worldbank.org/"
                    target="_blank"
                    rel="noreferrer"
                    className="underline"
                  >
                    {chunks}
                  </a>
                ),
                methodsLink: (chunks) => (
                  <Link href={`/${locale}/methods`} className="underline">
                    {chunks}
                  </Link>
                ),
              })}
            </p>
          </div>
        </div>
      </footer>
    </NextIntlClientProvider>
  );
}
