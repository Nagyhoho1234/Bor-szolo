'use client';

import dynamic from 'next/dynamic';

// Client-side wrapper for the deck.gl + maplibre map. The map module weighs
// ~1 MB and would otherwise be eagerly bundled into every page that imports
// from `@/components/...`. Wrapping it in a Client Component lets us use
// `ssr: false` (forbidden in Server Components) so the chunk only loads in
// the browser, on the landing page.
const DistrictMap = dynamic(() => import('@/components/DistrictMap'), {
  ssr: false,
  loading: () => (
    <div className="flex h-full w-full items-center justify-center bg-neutral-100 text-sm text-neutral-500">
      Loading map…
    </div>
  ),
});

export default function DistrictMapClient() {
  return <DistrictMap />;
}
