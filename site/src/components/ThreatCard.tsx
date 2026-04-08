import Link from 'next/link';

export type ThreatCardProps = {
  title: string;
  severity?: 'low' | 'medium' | 'high';
  description?: string;
  href?: string;
  /** If true, renders the DRAFT data warning badge */
  draft?: boolean;
  draftWarning?: string;
};

const SEVERITY_STYLES: Record<string, string> = {
  low: 'bg-emerald-100 text-emerald-800',
  medium: 'bg-amber-100 text-amber-800',
  high: 'bg-red-100 text-red-800',
};

export default function ThreatCard({
  title,
  severity = 'medium',
  description,
  href,
  draft,
  draftWarning,
}: ThreatCardProps) {
  const badge = SEVERITY_STYLES[severity] ?? SEVERITY_STYLES.medium;
  const body = (
    <div className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm transition hover:border-neutral-300">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-neutral-900">{title}</h3>
        <span
          className={`rounded px-1.5 py-0.5 text-[10px] font-medium uppercase ${badge}`}
        >
          {severity}
        </span>
      </div>
      {description && (
        <p className="mt-2 text-sm text-neutral-600">{description}</p>
      )}
      {draft && (
        <p className="mt-2 rounded bg-amber-50 px-2 py-1 text-[11px] text-amber-800">
          Draft: {draftWarning ?? 'source not yet verified.'}
        </p>
      )}
    </div>
  );
  if (href) {
    return (
      <Link href={href} className="block no-underline">
        {body}
      </Link>
    );
  }
  return body;
}
