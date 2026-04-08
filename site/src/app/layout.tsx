import type { Metadata } from 'next';
import './globals.css';

// TODO at deploy time: replace https://example.com with the real production
// domain (e.g. https://wine-climate.example.org). metadataBase is required for
// Open Graph / Twitter card image URLs to resolve to absolute URLs.
const SITE_URL = 'https://example.com';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Hungarian Wine Climate Atlas',
    template: '%s · Hungarian Wine Climate Atlas',
  },
  description:
    'Climate change exposure, variety suitability and disease threats for all 22 Hungarian wine districts — observations to 2100.',
  openGraph: {
    type: 'website',
    siteName: 'Hungarian Wine Climate Atlas',
    images: [
      {
        url: '/opengraph-image',
        width: 1200,
        height: 630,
        alt: 'Hungarian Wine Climate Atlas',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    images: ['/opengraph-image'],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className="min-h-screen bg-white text-neutral-900 antialiased"
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
