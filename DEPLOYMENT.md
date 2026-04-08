# Deployment

The Hungarian Wine Climate Atlas is a **static-export Next.js 16 site** —
the build output is a folder of HTML/CSS/JS/JSON/PDF files that can be
served from any static host. There is no server, no database, no API.

## Quick deploy paths (in order of simplicity)

### 1. Cloudflare Pages (recommended — free, global CDN)

1. Push this repo to GitHub (see `README.md` Quick Start).
2. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick the repo.
3. Build settings:
   - **Framework preset:** `Next.js (Static HTML Export)`
   - **Build command:** `cd site && npm install && npm run build`
   - **Build output directory:** `site/out`
   - **Root directory:** *(leave empty)*
   - **Node version:** `20` or `22` (set via `NODE_VERSION` environment variable if needed)
4. Save and deploy. First build takes ~3–5 minutes.
5. Cloudflare gives you a `*.pages.dev` URL immediately. Add a custom domain in the Pages → Custom Domains tab.

### 2. Vercel

1. Import the GitHub repo at <https://vercel.com/new>.
2. Project settings:
   - **Framework Preset:** `Next.js`
   - **Root Directory:** `site`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `out`
   - **Install Command:** `npm install` (default)
3. Deploy. Vercel auto-detects the static export.
4. Add a custom domain in Project → Settings → Domains.

### 3. Netlify

1. New site from Git → pick the repo.
2. Build settings:
   - **Base directory:** `site`
   - **Build command:** `npm run build`
   - **Publish directory:** `site/out`
3. Deploy.

### 4. GitHub Pages (cheapest, but no preview deploys)

1. Add a GitHub Actions workflow at `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy to GitHub Pages
   on:
     push:
       branches: [main]
   permissions:
     contents: read
     pages: write
     id-token: write
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with: { node-version: '22' }
         - run: cd site && npm ci && npm run build
         - uses: actions/upload-pages-artifact@v3
           with: { path: site/out }
     deploy:
       needs: build
       runs-on: ubuntu-latest
       environment: { name: github-pages, url: "${{ steps.deployment.outputs.page_url }}" }
       steps:
         - id: deployment
           uses: actions/deploy-pages@v4
   ```
2. In the repo settings → Pages → Source → "GitHub Actions".
3. Push to `main`. The action builds and deploys.

### 5. Self-hosted (any static web server)

The contents of `site/out/` are a complete static bundle. Copy them to any
nginx / Caddy / Apache / `python -m http.server` document root and serve.

## Pre-deploy checklist

Before pushing your first deploy live:

- [ ] **Domain configured.** Update the `metadataBase` constant in `site/src/app/layout.tsx` from `https://example.com` to your real production domain. The same URL also lives at the top of `site/src/app/sitemap.ts` and `site/src/app/robots.ts` — search-and-replace all three.
- [ ] **Build verified.** Run `cd site && npm run build` locally and confirm the output `site/out/sitemap.xml`, `site/out/robots.txt`, `site/out/opengraph-image` are all present.
- [ ] **Curated data is up-to-date.** If you regenerated any pipeline outputs, run `cd site && node scripts/sync_curated.mjs` first to mirror the latest `analysis/curated/` into `site/public/data/`.
- [ ] **Per-district PDFs.** If you regenerated the variety match or normals data, re-run `python analysis/src/s10_generate_district_pdfs.py` to refresh the 22 PDFs in `site/public/pdfs/`.
- [ ] **Memory.md and CLAUDE.md not exposed.** They are excluded by `.gitignore`, but double-check no copy ended up under `site/public/`.

## Build size and performance

| Asset | Size | Notes |
|---|---|---|
| `site/out/` total | ~133 MB | Including 28 MB of curated JSON data and 22 PDFs |
| Largest single page (HTML) | ~440 KB | District detail page with embedded research dossier (gzips to ~100 KB) |
| Largest JS chunk | ~1 MB | deck.gl + maplibre + WebGL adapter; lazy-loaded only on the landing page |
| Static pages | 1,091 | EN + HU mirrors of every route |

The build takes 4–6 seconds on a modern laptop after the first run. Cold builds with a clean `node_modules/` take ~3 minutes (mostly `npm install`).

## Updating the data

When new climate data arrives or you correct an envelope:

1. Edit the relevant file under `analysis/config/` or re-run a pipeline step under `analysis/src/`.
2. Run `python analysis/src/s07_publish_curated.py` to refresh the manifest + checksums.
3. Run `cd site && node scripts/sync_curated.mjs` to mirror to `site/public/data/`.
4. Run `python analysis/src/s10_generate_district_pdfs.py` if PDFs need refreshing.
5. Commit and push. Your CI / Cloudflare Pages / Vercel will pick up the change and rebuild.

## DOI minting (Zenodo)

After your first GitHub release:

1. Connect the repository to Zenodo at <https://zenodo.org/account/settings/github/>.
2. Toggle the repo to "On".
3. Cut a release on GitHub (e.g. `v1.0.0`).
4. Zenodo auto-archives the release and assigns a DOI using the metadata in `.zenodo.json`.
5. Add the DOI badge to `README.md`.

## Troubleshooting

**`Cannot read properties of undefined (reading 'maxTextureDimension2D')`**
The luma.gl 9.x WebGL adapter wasn't imported. Check that
`src/components/DistrictMap.tsx` imports `webgl2Adapter` from `@luma.gl/webgl`
and passes it to `<DeckGL deviceProps={{ adapters: [webgl2Adapter] }}>`.

**`Page "/[locale]/foo/[bar]/[baz]/page" is missing param ... in "generateStaticParams()"`**
Leaf routes with two or more dynamic segments at once must enumerate the
parent `[locale]` segment too. Cross-product `locales × your-pairs` in
`generateStaticParams()`.

**Hydration warning about `sapling-installed`**
The Sapling browser extension injects an attribute on `<body>` before React
hydrates. The fix (already applied in `src/app/layout.tsx`) is to add
`suppressHydrationWarning` on both `<html>` and `<body>`.

**`prose` Tailwind class renders as one wall of text**
The `@tailwindcss/typography` plugin must be activated via
`@plugin "@tailwindcss/typography";` at the top of `site/src/app/globals.css`.
