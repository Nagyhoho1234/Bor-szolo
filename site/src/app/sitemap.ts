import type { MetadataRoute } from 'next';
import { BORVIDEK_LIST, slugify } from '@/lib/district-meta';

// Required for `output: 'export'` — without this, Next.js refuses to emit
// the sitemap into the static bundle.
export const dynamic = 'force-static';

// TODO at deploy time: replace https://example.com with the real production
// domain. All URLs in a sitemap must be absolute, and the host must match
// the host the file is served from or crawlers will reject it.
const SITE_URL = 'https://example.com';
const LOCALES = ['en', 'hu'] as const;

// Hand-picked compare pairs (must stay in sync with
// src/app/[locale]/compare/[a]/[b]/page.tsx COMPARE_PAIRS)
const COMPARE_PAIRS: Array<[string, string]> = [
  ['tokaji', 'egri'],
  ['tokaji', 'villanyi'],
  ['egri', 'matrai'],
  ['soproni', 'tokaji'],
  ['csongradi', 'soproni'],
  ['villanyi', 'szekszardi'],
  ['badacsonyi', 'balatonfured-csopaki'],
];

// All distinct principal varieties across the 22 districts (must stay in
// sync with src/app/[locale]/varieties/[variety]/page.tsx)
const ALL_VARIETIES = Array.from(
  new Set(BORVIDEK_LIST.flatMap((d) => d.principalVarieties)),
).sort();

// Static routes under /[locale]/ — relative paths, no leading slash.
const STATIC_PATHS = [
  '', // landing page
  'districts',
  'varieties',
  'compare',
  'compare/risk',
  'compare/suitability',
  'threats',
  'threats/flavescence-doree',
  'threats/heat',
  'threats/drought',
  'threats/frost',
  'methods',
  'methods/data-sources',
  'methods/indices',
  'methods/uncertainty',
  'synthesis',
  'synthesis/policy-brief',
  'synthesis/scientific',
  'about',
  'downloads',
] as const;

type Entry = MetadataRoute.Sitemap[number];

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  const entries: Entry[] = [];

  for (const locale of LOCALES) {
    // Static routes
    for (const p of STATIC_PATHS) {
      const url = p
        ? `${SITE_URL}/${locale}/${p}`
        : `${SITE_URL}/${locale}`;
      const isLanding = p === '';
      const isMethodsOrSynthesis =
        p.startsWith('methods') || p.startsWith('synthesis');
      entries.push({
        url,
        lastModified,
        changeFrequency: isLanding ? 'weekly' : 'monthly',
        priority: isLanding ? 1.0 : isMethodsOrSynthesis ? 0.7 : 0.5,
      });
    }

    // District detail pages (22)
    for (const d of BORVIDEK_LIST) {
      entries.push({
        url: `${SITE_URL}/${locale}/districts/${d.slug}`,
        lastModified,
        changeFrequency: 'monthly',
        priority: 0.9,
      });
    }

    // Variety detail pages (~38)
    for (const v of ALL_VARIETIES) {
      entries.push({
        url: `${SITE_URL}/${locale}/varieties/${slugify(v)}`,
        lastModified,
        changeFrequency: 'monthly',
        priority: 0.5,
      });
    }

    // Compare pair pages (7)
    for (const [a, b] of COMPARE_PAIRS) {
      entries.push({
        url: `${SITE_URL}/${locale}/compare/${a}/${b}`,
        lastModified,
        changeFrequency: 'monthly',
        priority: 0.5,
      });
    }
  }

  return entries;
}
