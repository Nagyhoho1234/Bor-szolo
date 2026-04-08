'use client';

import { useState } from 'react';

export type ProgressiveDisclosureProps = {
  title?: string;
  tier1: React.ReactNode;
  tier2?: React.ReactNode;
  tier3?: React.ReactNode;
  moreLabel?: string;
  lessLabel?: string;
  defaultOpen?: boolean;
};

export default function ProgressiveDisclosure({
  title,
  tier1,
  tier2,
  tier3,
  moreLabel = 'More detail',
  lessLabel = 'Less',
  defaultOpen = false,
}: ProgressiveDisclosureProps) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <section className="my-6 rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
      {title && (
        <h2 className="mb-3 text-lg font-semibold text-neutral-900">
          {title}
        </h2>
      )}
      <div className="space-y-3">{tier1}</div>
      {tier2 && (
        <div className="mt-4">
          <button
            type="button"
            className="text-xs font-medium text-blue-700 underline-offset-2 hover:underline"
            onClick={() => setOpen((o) => !o)}
          >
            {open ? lessLabel : moreLabel}
          </button>
          {open && (
            <div className="mt-3 border-t border-neutral-100 pt-3">
              {tier2}
            </div>
          )}
        </div>
      )}
      {tier3 && (
        <div className="mt-4 border-t border-neutral-100 pt-3 text-[11px] text-neutral-500">
          {tier3}
        </div>
      )}
    </section>
  );
}
