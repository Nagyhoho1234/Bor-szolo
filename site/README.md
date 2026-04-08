# Hungarian Wine Districts Climate Atlas — site

Public bilingual (HU + EN) information site about Hungarian wine districts and
their climate change susceptibility. This is the static front-end; the data
backbone (parquet/arrow/geojson) is built separately under
`C:\Bor-szőlő\analysis\curated\` and synced into `public/data/` later.

## Stack

- Next.js 16 (App Router) with `output: 'export'` (fully static)
- TypeScript + Tailwind CSS v4
- next-intl for HU/EN i18n with `[locale]` route segment
- MapLibre GL JS + react-map-gl + deck.gl for the map overlays
- Recharts for time-series and bar charts
- TanStack Table for ranking views
- @next/mdx for narrative pages
- apache-arrow + parquet-wasm for browser-side parquet loading (not yet wired)

## Layout

```
src/
  app/
    layout.tsx              # html/body root
    page.tsx                # redirects / -> /en
    [locale]/
      layout.tsx            # nav, footer, NextIntlClientProvider
      page.tsx              # landing + DistrictMap
      regions/              # list + [region] detail
      districts/            # list + [borvidek] detail
      compare/              # overview + risk + suitability
      varieties/            # list + [variety] detail
      threats/              # overview + flavescence-doree, frost, drought
      methods/              # overview + data-sources, indices, uncertainty
      about/
      downloads/
  components/               # DistrictMap, IndexCard, ClimateTrendChart, ...
  lib/
    i18n.ts                 # next-intl getRequestConfig + locales
    data.ts                 # stub data loaders (return [])
  messages/
    en.json
    hu.json
  mdx-components.tsx        # required by @next/mdx
public/
  data/                     # synced from analysis/curated (currently empty)
scripts/
  sync_curated.mjs          # stub for the future sync step
```

## Locales

- `en` (default), `hu`
- All routes live under `/[locale]/...`. Visiting `/` redirects to `/en/`.
- Translations: `src/messages/{en,hu}.json`. Add keys with `nav.*`, `home.*`,
  `common.*` etc. and reference them via `useTranslations('home')` from
  `next-intl`.

## Deferred data layer

`src/lib/data.ts` exposes `loadDistricts()`, `loadIndex()`, and
`loadVarietyMatch()` as stubs that return empty arrays. When the curated
parquet/arrow assets exist under `analysis/curated/`, run

```bash
npm run sync:curated
```

to copy them into `public/data/`, then wire the loaders to read via
`apache-arrow` / `parquet-wasm`. The page components do not need to change.

## Commands

```bash
npm run dev            # local dev server
npm run build          # static export to ./out
npm run lint
npm run sync:curated   # stub today, real later
```

## Notes

- Static export means no middleware, no server actions, no on-demand image
  optimization. All routes are pre-rendered at build via `generateStaticParams`.
- Dynamic segments (`[region]`, `[borvidek]`, `[variety]`) currently emit a
  single `placeholder` page; replace `generateStaticParams` with the real
  district/variety lists once the data is wired.
- Next.js 16 uses Turbopack by default, which requires remark/rehype plugins
  to be passed as strings (see `next.config.mjs`).
