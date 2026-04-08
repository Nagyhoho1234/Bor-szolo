import type { Metadata } from 'next';
import Link from 'next/link';
import fs from 'node:fs';
import path from 'node:path';
import { getTranslations } from 'next-intl/server';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu ? 'Adatok letöltése' : 'Download the data';
  const description = isHu
    ? 'A klímaatlasz teljes adatkészlete CSV, JSON és parquet formátumban — szabadon felhasználható.'
    : 'The full atlas dataset in CSV, JSON and parquet — open and free to reuse.';
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

type ManifestFile = {
  path: string;
  type: string;
  size_bytes: number;
  sha256?: string;
  rows?: number;
  columns?: string[];
};

type Manifest = {
  bundle_name: string;
  version: string;
  generated_at: string;
  license: string;
  citation_required: string[];
  files: ManifestFile[];
  totals?: Record<string, unknown>;
  draft_flags?: string[];
};

function loadManifest(): Manifest | null {
  try {
    const p = path.join(process.cwd(), 'public', 'data', 'manifest.json');
    return JSON.parse(fs.readFileSync(p, 'utf-8')) as Manifest;
  } catch {
    return null;
  }
}

function fmtBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} kB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}

function groupBy(files: ManifestFile[]): Record<string, ManifestFile[]> {
  const groups: Record<string, ManifestFile[]> = {};
  for (const f of files) {
    const top = f.path.includes('/') ? f.path.split('/')[0] : '(root)';
    (groups[top] ||= []).push(f);
  }
  return groups;
}

export default async function DownloadsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'downloads' });
  const manifest = loadManifest();

  const entryItems = ['entryManifest', 'entryChecksums', 'entryReadme', 'entryGeoJson'];

  return (
    <article className="prose prose-neutral max-w-4xl">
      <h1>{t('title')}</h1>
      <p>{t('intro')}</p>

      <h2>{t('h2Entry')}</h2>
      <ul>
        {entryItems.map((key) => (
          <li
            key={key}
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{ __html: t.raw(key) as string }}
          />
        ))}
      </ul>

      {manifest && (
        <>
          <h2>
            {t('bundleHeading')}{' '}
            <code>
              {manifest.bundle_name} {manifest.version}
            </code>
          </h2>
          <p className="text-sm text-neutral-600">
            {t('generatedAt', {
              date: manifest.generated_at,
              count: manifest.files.length,
            })}
          </p>
          <p className="text-sm">{manifest.license}</p>
          <h3>{t('citationRequired')}</h3>
          <ul className="text-sm">
            {manifest.citation_required.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>

          {Object.entries(groupBy(manifest.files)).map(([group, files]) => (
            <section key={group}>
              <h3>
                <code>{group}/</code> ({t('filesCount', { count: files.length })})
              </h3>
              <ul className="text-sm">
                {files.map((f) => (
                  <li key={f.path}>
                    <a href={`/data/${f.path}`}>{f.path}</a>{' '}
                    <span className="text-neutral-500">
                      — {f.type}, {fmtBytes(f.size_bytes)}
                      {f.rows !== undefined ? `, ${f.rows} ${t('rows')}` : ''}
                    </span>
                  </li>
                ))}
              </ul>
            </section>
          ))}

          {manifest.draft_flags && manifest.draft_flags.length > 0 && (
            <>
              <h3>{t('draftFlags')}</h3>
              <ul className="text-sm">
                {manifest.draft_flags.map((d, i) => (
                  <li key={i}>{d}</li>
                ))}
              </ul>
            </>
          )}
        </>
      )}

      {!manifest && (
        <p
          className="rounded border border-amber-300 bg-amber-50 p-3 text-sm"
          // eslint-disable-next-line react/no-danger
          dangerouslySetInnerHTML={{ __html: t.raw('manifestMissing') as string }}
        />
      )}

      <h2>{t('h2Verify')}</h2>
      <pre className="overflow-x-auto text-xs">
        <code>{`# Linux / macOS
curl -O https://<this-host>/data/SHA256SUMS.txt
curl -O https://<this-host>/data/manifest.json
# fetch each file from manifest, then:
sha256sum -c SHA256SUMS.txt`}</code>
      </pre>

      <p className="text-sm">
        {t.rich('verifyHint', {
          methodsLink: (chunks) => (
            <Link href={`/${locale}/methods`}>{chunks}</Link>
          ),
          uncertaintyLink: (chunks) => (
            <Link href={`/${locale}/methods/uncertainty`}>{chunks}</Link>
          ),
        })}
      </p>
    </article>
  );
}
