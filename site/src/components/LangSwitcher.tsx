'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { locales } from '@/lib/i18n';

export type LangSwitcherProps = {
  currentLocale: string;
};

export default function LangSwitcher({ currentLocale }: LangSwitcherProps) {
  const pathname = usePathname() ?? '/';
  const stripped = pathname.replace(/^\/(en|hu)(?=\/|$)/, '') || '/';

  return (
    <span className="flex gap-2 text-xs">
      {locales.map((loc) => (
        <Link
          key={loc}
          href={`/${loc}${stripped === '/' ? '' : stripped}`}
          className={loc === currentLocale ? 'font-semibold underline' : 'text-neutral-500'}
        >
          {loc.toUpperCase()}
        </Link>
      ))}
    </span>
  );
}
