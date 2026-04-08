'use client';

import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useTranslations } from 'next-intl';

export type ChartModalProps = {
  title?: string;
  /** The thumbnail/inline rendering shown in the page flow. */
  children: ReactNode;
  /**
   * The large rendering shown when the modal is opened. If omitted, falls
   * back to the same children. Useful when the same chart can render at
   * larger sizes.
   */
  expanded?: ReactNode;
};

export default function ChartModal({
  title,
  children,
  expanded,
}: ChartModalProps) {
  const [open, setOpen] = useState(false);
  const t = useTranslations('common');

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [open]);

  return (
    <>
      <div
        className="group relative cursor-zoom-in"
        onClick={() => setOpen(true)}
        title={t('clickToEnlarge')}
      >
        {children}
        <div className="pointer-events-none absolute right-2 top-2 rounded bg-neutral-900/70 px-1.5 py-0.5 text-[10px] font-medium text-white opacity-0 transition group-hover:opacity-100">
          {t('clickToEnlarge')} ⤢
        </div>
      </div>
      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/80 p-2 sm:p-4"
          onClick={() => setOpen(false)}
        >
          <div
            className="relative max-h-[95vh] w-full max-w-5xl overflow-auto rounded-lg bg-white p-3 shadow-2xl sm:max-h-[92vh] sm:p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="sticky top-0 z-10 mb-3 flex items-center justify-between gap-2 bg-white pb-2">
              {title ? (
                <h3 className="truncate text-base font-semibold sm:text-lg">{title}</h3>
              ) : (
                <span />
              )}
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="shrink-0 rounded border border-neutral-300 px-3 py-1 text-sm hover:bg-neutral-100"
              >
                {t('close')} ✕
              </button>
            </div>
            <div className="min-h-[60vh]">{expanded ?? children}</div>
          </div>
        </div>
      )}
    </>
  );
}
