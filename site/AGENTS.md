<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

## Hard-won site gotchas (read before editing)

### Stack quirks
- **luma.gl 9.x WebGL adapter must be imported explicitly.** `<DeckGL>` crashes at runtime with `Cannot read properties of undefined (reading 'maxTextureDimension2D')` if you don't `import { webgl2Adapter } from '@luma.gl/webgl'` and pass `deviceProps={{ adapters: [webgl2Adapter] }}` to the component. Already done in `src/components/DistrictMap.tsx`.
- **Tailwind typography plugin** is required for the `prose` class to render markdown nicely. Activated via `@plugin "@tailwindcss/typography";` at the top of `src/app/globals.css`. Without it the research dossier on district pages renders as one wall of text with no spacing.
- **Sapling browser extension hydration warning.** Sapling injects `sapling-installed="true"` on `<body>` before React loads. `suppressHydrationWarning` is set on both `<html>` and `<body>` in `src/app/layout.tsx` to silence it. Don't remove.
- **Path contains `ő`** (`C:\Bor-szőlő\site\`). Causes some C-based libraries (notably `netCDF4`) to crash. Stick to JS/TS for site-side work; do all NetCDF reads in `analysis/` instead.
- **Static export** (`output: 'export'`) — no middleware, no server actions, no on-request data fetches. Read curated JSON files from `public/data/` at build time using `fs` in Server Components (the existing pattern).

### Chart UX contract — static-by-default, click-to-interact
**The user explicitly does NOT want interactive controls visible inline on the page.** Every inline chart must use `staticView={true}` or equivalent (no Tooltip, no Legend, no toggle chips, `pointer-events-none`). Wrap every chart in `<ChartModal>` (`src/components/ChartModal.tsx`) and pass the **interactive copy** as the `expanded` prop. Click the inline static copy → modal opens → modal copy is fully interactive.

Components with `staticView` support today:
- `ClimateTrendChart`
- `VarietySuitabilityBars`
- `ThreatRanking`

There must be **only one** style of climate line chart on the district detail page: the **bottom IndexCard 2×3 dashboard**, each card wrapped in `ChartModal` whose `expanded` slot is the interactive `ClimateTrendChart`. Do **not** add a separate top-level "climate trajectory" grid above it — the user has explicitly objected to having two kinds of charts.

### District map colours
The map at `src/components/DistrictMap.tsx` uses a **22-colour qualitative palette hashed by district name**, NOT a regional/borrégió grouping. The borrégió layer was deleted from the site entirely (`/regions/` pages, `BORREGIO_COLORS`, `BORREGIO_LIST` exports) — do not reintroduce it.

### User-facing content tone (the user has corrected me on this twice)
- **Methods pages** (`src/app/[locale]/methods/*`) are visitor-friendly explainer content, NOT a journal methods section. No pipeline-script names (s00–s09), no DOI-style inline citations, no Hargreaves-vs-Penman jargon, no ETCCDI verbatim definitions, no "what we did NOT model" lists. Plain English, "you/we" voice, analogies, ~250–500 words per page. Formulas live in a collapsed `<details>` drawer at the bottom of `methods/indices` only. Page titles can be visitor-friendly ("About the data" / "What the numbers mean" / "How sure are we?") but URLs stay the same.
- **No JSON / parquet / manifest.json links in user-facing source boxes.** Those file references belong on the Downloads page only. Citation boxes elsewhere should link **publishers and DOIs**, not internal data files.
- **Use `https://doi.org/<DOI>` for academic citations**, never publisher-direct URLs (Springer / Wiley / Elsevier paywall and rot under URL reorganisation). Mark `(paywalled)` after the link if the reader can't get full text.
- **Real source titles only.** Run any title through WebFetch before committing — the bootstrap pass produced ~110 fake titles that took a full audit pass to fix. The Frontiers 2025 paper is **Lakatos & Nagy 2025**, not Kovács / Zhao et al. (project CLAUDE.md flags this citation drift).
- **Don't render the `hail_caveat` field from `descriptions/*.json` on district pages.** The field stays in the JSON for the Methods/Uncertainty page reference, but the long disclaimer reads like a methods footnote on a public site. Stripped from the district detail page on 2026-04-07.
- **No "Please cite..." lines** — the citation block IS the cite.
- **Research dossier markdown** at the bottom of each district page must be processed via `processResearchMarkdown` (`src/lib/research-markdown.ts`) before rendering. The processor strips the `> Reading guide` blockquote, all `[OBSERVED]`/`[PROJECTED]`/`[HU-AGGREGATE]`/`[N-HU ANALOGUE]`/`[OBSERVED + PROJECTED]` etc. inline meta-tags, and converts inline `> Sources (§N): [title](url)` blockquotes into superscript numeric markers `[1] [2]` linking to a single References section appended at the bottom of the dossier.

### Variety chart data contract
`VarietySuitabilityBars` reads `suitability_long.json` and renders **two sub-charts under one shared period dropdown**: principal varieties (`in_principal_varieties === true`) and climate-hedge candidates (`in_principal_varieties === false`). The parent must pass **all** suitability rows for the district preserving `in_principal_varieties` — pre-filtering breaks the lower chart silently. See project root `CLAUDE.md` for the full contract.

### Build verification
Always run `npm run build` from `C:/Bor-szőlő/site/` before reporting "done". The build is ~3-4s compile + ~1s static generation, total ~5s. Acceptable: 158-170 static pages depending on which routes exist. Common failure modes:
- TypeScript errors on Recharts `Tooltip` `formatter` prop in newer versions — don't annotate `(v: number)`, just `(v)` and let inference work.
- `Map` JS class collision with the imported `Map` component from `react-map-gl/maplibre` — never `new Map<...>()` in `DistrictMap.tsx`; use a plain object cache.
- Type-narrowing failures in `.filter` predicates — fall back to a post-filter `as` cast rather than `(x): x is T => ...` with non-trivial types.

### Curated data sync
Curated parquet/JSON live in `analysis/curated/` and are mirrored into `site/public/data/` by `site/scripts/sync_curated.mjs`. **Run that script after any change to `analysis/curated/`.** It wipes the destination first, so anything written directly into `site/public/data/` outside the sync flow gets deleted on the next run.
