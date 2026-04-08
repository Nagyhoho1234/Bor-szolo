import type { Metadata } from 'next';
import Link from 'next/link';
import fs from 'node:fs';
import path from 'node:path';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { processResearchMarkdown } from '@/lib/research-markdown';
import { getTranslations, setRequestLocale } from 'next-intl/server';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Tudományos szintézis — magyar borvidékek klímakitettsége'
    : 'Scientific synthesis: Hungarian wine-district climate exposure';
  const description = isHu
    ? 'A teljes adatbázis tudományos összefoglalása — indexek, projekciók, bizonytalanságok és hivatkozások.'
    : 'A research-grade synthesis of the full dataset — indices, projections, uncertainty and citations.';
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

function loadBrief(locale: string): string | null {
  const root = path.join(process.cwd(), '..', 'research', 'synthesis');
  // When locale is "hu", prefer the Hungarian translation if it exists,
  // and fall back to the English original.
  const candidates =
    locale === 'hu'
      ? ['scientific_synthesis.hu.md', 'scientific_synthesis.md']
      : ['scientific_synthesis.md'];
  for (const c of candidates) {
    try {
      const p = path.join(root, c);
      if (fs.existsSync(p)) return fs.readFileSync(p, 'utf-8');
    } catch {
      /* ignore */
    }
  }
  return null;
}

export default async function ScientificSynthesisPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: 'synthesis.page' });

  const raw = loadBrief(locale);
  if (!raw) {
    return (
      <article className="prose prose-neutral max-w-3xl">
        <p>
          <Link href={`/${locale}/synthesis`}>{t('back')}</Link>
        </p>
        <p>{t('missing')}</p>
      </article>
    );
  }

  const { body, references } = processResearchMarkdown(raw);

  return (
    <article className="max-w-3xl">
      <p className="mb-4 text-sm">
        <Link
          href={`/${locale}/synthesis`}
          className="text-blue-700 hover:underline"
        >
          {t('back')}
        </Link>
      </p>

      <div className="prose prose-neutral max-w-3xl prose-headings:scroll-mt-20 prose-h1:text-3xl prose-h2:text-2xl prose-h3:text-xl prose-a:text-blue-700 prose-a:no-underline hover:prose-a:underline">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
        >
          {body}
        </ReactMarkdown>
      </div>

      {references.length > 0 && (
        <div className="mt-10 border-t border-neutral-200 pt-4">
          <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-neutral-700">
            {t('references')} ({references.length})
          </h2>
          <ol className="space-y-1 text-xs text-neutral-700">
            {references.map((r) => (
              <li
                key={r.n}
                id={`ref${r.n}`}
                className="grid grid-cols-[2rem_1fr] gap-1 scroll-mt-20"
              >
                <span className="text-neutral-500 tabular-nums">[{r.n}]</span>
                <a
                  href={r.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-700 hover:underline break-all"
                >
                  {r.title}
                </a>
              </li>
            ))}
          </ol>
        </div>
      )}
    </article>
  );
}
