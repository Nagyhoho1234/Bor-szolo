import type { Metadata } from 'next';
import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import { BORVIDEK_LIST, slugify } from '@/lib/district-meta';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const isHu = locale === 'hu';
  const title = isHu
    ? 'Szőlőfajták a magyar borvidékeken'
    : 'Grape varieties across Hungarian wine districts';
  const description = isHu
    ? 'Furmint, Kadarka, Kékfrankos és társaik — hol főfajták és hogyan változik alkalmasságuk 2100-ig.'
    : 'Furmint, Kadarka, Kékfrankos and the rest — where each grape is principal and how its suitability shifts to 2100.';
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

type VarietyRow = { name: string; slug: string; districts: string[] };

const VARIETY_ROWS: VarietyRow[] = (() => {
  const map = new Map<string, Set<string>>();
  for (const d of BORVIDEK_LIST) {
    for (const v of d.principalVarieties) {
      if (!map.has(v)) map.set(v, new Set());
      map.get(v)!.add(d.borvidek);
    }
  }
  return Array.from(map.entries())
    .map(([name, ds]) => ({
      name,
      slug: slugify(name),
      districts: Array.from(ds).sort(),
    }))
    .sort((a, b) => b.districts.length - a.districts.length || a.name.localeCompare(b.name));
})();

export default async function VarietiesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'varieties' });
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">{t('indexTitle')}</h1>
        <p className="mt-2 text-neutral-600">
          {t('indexSubtitle', { count: VARIETY_ROWS.length })}
        </p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead className="bg-neutral-100 text-left">
            <tr>
              <th className="p-2 font-semibold">{t('tableHeader.variety')}</th>
              <th className="p-2 font-semibold">{t('tableHeader.nDistricts')}</th>
              <th className="p-2 font-semibold">{t('tableHeader.districts')}</th>
            </tr>
          </thead>
          <tbody>
            {VARIETY_ROWS.map((v) => (
              <tr key={v.slug} className="border-b border-neutral-200">
                <td className="p-2 font-medium">
                  <Link
                    href={`/${locale}/varieties/${v.slug}`}
                    className="text-blue-700 hover:underline"
                  >
                    {v.name}
                  </Link>
                </td>
                <td className="p-2 tabular-nums">{v.districts.length}</td>
                <td className="p-2 text-xs text-neutral-600">
                  {v.districts.join(' · ')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
