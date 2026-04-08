'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

type Option = { slug: string; label: string };

export default function DistrictPickerForm({
  locale,
  options,
  defaultA,
  defaultB,
  labels,
}: {
  locale: string;
  options: Option[];
  defaultA: string;
  defaultB: string;
  labels: {
    heading: string;
    subtitle: string;
    districtA: string;
    districtB: string;
    submit: string;
    sameWarning: string;
  };
}) {
  const router = useRouter();
  const [a, setA] = useState(defaultA);
  const [b, setB] = useState(defaultB);
  const same = a === b;

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (same) return;
    router.push(`/${locale}/compare/${a}/${b}`);
  }

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-lg border border-neutral-200 bg-neutral-50 p-4"
    >
      <div className="text-sm font-semibold text-neutral-900">
        {labels.heading}
      </div>
      <p className="mt-1 text-sm text-neutral-600">{labels.subtitle}</p>
      <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-end">
        <label className="flex flex-1 flex-col text-xs uppercase tracking-wide text-neutral-500">
          {labels.districtA}
          <select
            value={a}
            onChange={(e) => setA(e.target.value)}
            className="mt-1 rounded border border-neutral-300 bg-white px-2 py-2 text-sm text-neutral-900"
          >
            {options.map((o) => (
              <option key={o.slug} value={o.slug}>
                {o.label}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-1 flex-col text-xs uppercase tracking-wide text-neutral-500">
          {labels.districtB}
          <select
            value={b}
            onChange={(e) => setB(e.target.value)}
            className="mt-1 rounded border border-neutral-300 bg-white px-2 py-2 text-sm text-neutral-900"
          >
            {options.map((o) => (
              <option key={o.slug} value={o.slug}>
                {o.label}
              </option>
            ))}
          </select>
        </label>
        <button
          type="submit"
          disabled={same}
          className="rounded bg-amber-700 px-4 py-2 text-sm font-semibold text-white hover:bg-amber-800 disabled:cursor-not-allowed disabled:bg-neutral-400"
        >
          {labels.submit}
        </button>
      </div>
      {same && (
        <p className="mt-2 text-xs text-rose-600">{labels.sameWarning}</p>
      )}
    </form>
  );
}
