import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Compare wine districts by climate risk',
  description:
    'Side-by-side risk ranking of Hungarian wine districts (placeholder page).',
  openGraph: {
    title: 'Compare wine districts by climate risk',
    description:
      'Side-by-side risk ranking of Hungarian wine districts (placeholder page).',
    type: 'website',
    locale: 'en_US',
    images: ['/opengraph-image'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Compare wine districts by climate risk',
    description:
      'Side-by-side risk ranking of Hungarian wine districts (placeholder page).',
  },
};

export default function CompareRiskPage() {
  return (
    <section>
      <h1 className="text-3xl font-bold">Compare: Risk</h1>
      <p className="mt-2 text-neutral-600">Placeholder.</p>
    </section>
  );
}
