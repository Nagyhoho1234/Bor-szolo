import { ImageResponse } from 'next/og';

// Default Open Graph image for the site root. Next.js generates this at
// build time and emits a static PNG into the output bundle. Page-level
// `metadata.openGraph.images` entries reference '/opengraph-image' which
// resolves to this file.

// Required for `output: 'export'` — Next refuses to emit dynamic image
// route handlers into the static bundle without this.
export const dynamic = 'force-static';
export const runtime = 'nodejs';
export const alt = 'Hungarian Wine Climate Atlas';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '72px 80px',
          background:
            'linear-gradient(135deg, #4c0519 0%, #7f1d1d 45%, #b45309 100%)',
          color: 'white',
          fontFamily: 'sans-serif',
        }}
      >
        <div
          style={{
            display: 'flex',
            fontSize: 26,
            letterSpacing: 6,
            textTransform: 'uppercase',
            opacity: 0.85,
          }}
        >
          Magyar Borvidék Klímaatlasz
        </div>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 18,
          }}
        >
          <div
            style={{
              fontSize: 86,
              fontWeight: 800,
              lineHeight: 1.05,
              letterSpacing: -2,
            }}
          >
            Hungarian Wine
          </div>
          <div
            style={{
              fontSize: 86,
              fontWeight: 800,
              lineHeight: 1.05,
              letterSpacing: -2,
            }}
          >
            Climate Atlas
          </div>
          <div
            style={{
              fontSize: 32,
              maxWidth: 980,
              lineHeight: 1.3,
              opacity: 0.92,
              marginTop: 18,
            }}
          >
            22 wine districts · variety suitability · disease &amp; heat threats
            · observations to 2100
          </div>
        </div>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-end',
            fontSize: 22,
            opacity: 0.8,
          }}
        >
          <span>Tokaj · Eger · Villány · Szekszárd · Sopron · Balaton</span>
          <span>EN · HU</span>
        </div>
      </div>
    ),
    { ...size },
  );
}
