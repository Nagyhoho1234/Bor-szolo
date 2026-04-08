'use client';

import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  useReactTable,
  type ColumnDef,
  type SortingState,
} from '@tanstack/react-table';
import { useMemo, useState } from 'react';
import Link from 'next/link';
import { slugify } from '@/lib/district-meta';

export type RankingRow = {
  borvidek: string;
  borregio: string;
  winklerNow: number | null;
  winklerFuture: number | null;
  winklerDelta: number | null;
  heatDaysFuture: number | null;
  droughtFuture: number | null;
  winner: string;
  loser: string;
};

export type RankingTableProps = {
  data: RankingRow[];
  locale: string;
  searchPlaceholder?: string;
  labels: {
    borvidek: string;
    borregio: string;
    winklerNow: string;
    winklerFuture: string;
    winklerDelta: string;
    heatDaysFuture: string;
    droughtFuture: string;
    winner: string;
    loser: string;
  };
};

function fmt(v: number | null | undefined, d = 0): string {
  if (v == null || !Number.isFinite(v)) return '—';
  return v.toFixed(d);
}

export default function RankingTable({
  data,
  locale,
  labels,
  searchPlaceholder = 'Search…',
}: RankingTableProps) {
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'winklerDelta', desc: true },
  ]);
  const [query, setQuery] = useState('');

  const columns = useMemo<ColumnDef<RankingRow>[]>(
    () => [
      {
        accessorKey: 'borvidek',
        header: labels.borvidek,
        cell: ({ getValue }) => {
          const name = getValue<string>();
          return (
            <Link
              className="font-medium text-neutral-900 underline-offset-2 hover:underline"
              href={`/${locale}/districts/${slugify(name)}`}
            >
              {name}
            </Link>
          );
        },
      },
      {
        accessorKey: 'winklerNow',
        header: labels.winklerNow,
        cell: ({ getValue }) => fmt(getValue<number | null>(), 0),
      },
      {
        accessorKey: 'winklerFuture',
        header: labels.winklerFuture,
        cell: ({ getValue }) => fmt(getValue<number | null>(), 0),
      },
      {
        accessorKey: 'winklerDelta',
        header: labels.winklerDelta,
        cell: ({ getValue }) => {
          const v = getValue<number | null>();
          return (
            <span className={v && v > 0 ? 'text-red-600' : ''}>
              {fmt(v, 0)}
            </span>
          );
        },
      },
      {
        accessorKey: 'heatDaysFuture',
        header: labels.heatDaysFuture,
        cell: ({ getValue }) => fmt(getValue<number | null>(), 1),
      },
      {
        accessorKey: 'droughtFuture',
        header: labels.droughtFuture,
        cell: ({ getValue }) => fmt(getValue<number | null>(), 0),
      },
      { accessorKey: 'winner', header: labels.winner },
      { accessorKey: 'loser', header: labels.loser },
    ],
    [locale, labels]
  );

  const table = useReactTable({
    data,
    columns,
    state: { sorting, globalFilter: query },
    onSortingChange: setSorting,
    onGlobalFilterChange: setQuery,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <div className="w-full">
      <input
        type="text"
        placeholder={searchPlaceholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="mb-3 w-full max-w-xs rounded border border-neutral-300 px-2 py-1 text-sm sm:w-56"
      />
      <p className="mb-2 text-[11px] text-neutral-500 sm:hidden">
        ← swipe the table sideways to see all columns →
      </p>
      <div className="max-h-[70vh] overflow-auto rounded border border-neutral-200">
        <table className="w-full min-w-[720px] border-collapse text-sm">
          <thead className="sticky top-0 z-10 bg-neutral-50">
            {table.getHeaderGroups().map((hg) => (
              <tr key={hg.id} className="border-b border-neutral-200 text-left">
                {hg.headers.map((h, i) => (
                  <th
                    key={h.id}
                    className={`cursor-pointer select-none px-2 py-2 font-medium hover:bg-neutral-100 ${
                      i === 0
                        ? 'sticky left-0 z-20 bg-neutral-50 shadow-[1px_0_0_0_#e5e5e5]'
                        : ''
                    }`}
                    onClick={h.column.getToggleSortingHandler()}
                  >
                    {h.isPlaceholder
                      ? null
                      : flexRender(h.column.columnDef.header, h.getContext())}
                    {{ asc: ' ↑', desc: ' ↓' }[
                      h.column.getIsSorted() as string
                    ] ?? ''}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                className="border-b border-neutral-100 hover:bg-neutral-50"
              >
                {row.getVisibleCells().map((cell, i) => (
                  <td
                    key={cell.id}
                    className={`px-2 py-1.5 ${
                      i === 0
                        ? 'sticky left-0 z-10 bg-white shadow-[1px_0_0_0_#e5e5e5]'
                        : ''
                    }`}
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
