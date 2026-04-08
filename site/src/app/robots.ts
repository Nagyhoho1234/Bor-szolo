import type { MetadataRoute } from 'next';

// Required for `output: 'export'` — without this, Next.js refuses to emit
// route handlers into the static bundle.
export const dynamic = 'force-static';

// TODO at deploy time: replace https://example.com with the real production
// domain. The sitemap URL must be absolute and reachable from the deployed
// site, otherwise crawlers will silently drop it.
const SITE_URL = 'https://example.com';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/' }],
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
