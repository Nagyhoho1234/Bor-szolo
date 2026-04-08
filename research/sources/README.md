# Research Sources Fetcher

`fetch_sources.py` builds a local, offline-readable copy of every web source
cited in the 22 district synthesis files under
`C:\Bor-szőlő\research\districts\*.md`.

## What it does

1. **Extracts URLs** from every district markdown file. It picks up both
   inline `[text](https://…)` markdown links and bare URLs in the §15 Sources
   sections.
2. **Deduplicates** the URL list across all districts.
3. **Downloads** every unique source (HTML or PDF) to
   `research/sources/raw/<sha1>.<ext>`. Files are named by the SHA1 of the
   URL so the cache survives URL collisions and is trivially idempotent.
4. **Converts** each download to a standalone markdown file at
   `research/sources/md/<sha1>.md` with a header block:
   ```
   # Source: <original URL>
   **Original title:** ...
   **District(s):** badacsonyi, tokaji, ...
   **Downloaded:** 2026-04-07
   ---
   <converted body>
   ```
   - HTML is converted with `markdownify` (or `html2text` if that is what
     you have installed).
   - PDFs are converted with `PyMuPDF` (`fitz`) — or `pdfminer.six` as a
     fallback — and emitted page-by-page.
5. **Writes two indexes:**
   - `research/sources/index.json` — machine-readable: URL, sha1, raw path,
     md path, citing districts, status, HTTP code, byte size.
   - `research/sources/INDEX.md` — human-readable, grouped by district, with
     clickable links to the local `md/` copies.
6. **Logs failures** to `research/sources/failures.log` (timestamp, URL,
   reason). The pipeline never crashes on a single bad URL — it retries
   once with a different User-Agent, then logs and moves on.
7. **Skips known auth-gated aggregators** (Sci-Hub, JSTOR, Academia.edu,
   IEEE Xplore, Libgen, Z-Lib) and marks them as `auth_required` instead of
   wasting time on landing pages.

## Required Python packages

```bash
pip install requests markdownify pymupdf tqdm
```

Alternative drop-ins (the script auto-detects whichever is installed):

- HTML conversion: `markdownify` *or* `html2text`
- PDF conversion: `pymupdf` *or* `pdfminer.six`

`requests` and `tqdm` are required.

Python 3.10 or newer.

## How to run

From any working directory:

```bash
python C:\Bor-szőlő\research\sources\fetch_sources.py
```

Useful flags:

```bash
python fetch_sources.py --dry-run            # just list every URL it would fetch
python fetch_sources.py --workers 4          # tune parallelism (default 8)
python fetch_sources.py --help
```

The script is **idempotent**: re-running will skip URLs already cached
successfully and only re-convert a markdown file if its raw blob is newer.
You can safely Ctrl-C and resume.

Expect roughly **one hour** for the full ~1,200-source download on a
typical home connection (politeness throttle is ~1 s per domain, 8 workers).

## Output structure

```
research/sources/
├── fetch_sources.py        # this script
├── README.md               # this file
├── index.json              # machine index of every URL
├── INDEX.md                # human index, grouped by district
├── failures.log            # one line per failure (timestamp, URL, reason)
├── raw/
│   ├── 0123abcd….html      # raw cached HTML
│   ├── 4567ef89….pdf       # raw cached PDF
│   └── …
└── md/
    ├── 0123abcd….md        # converted, with provenance header
    └── …
```

## Politeness & limits

- User-Agent identifies the script as a research bot, with a fallback to
  a generic browser UA on retry.
- 8 concurrent connections maximum (configurable via `--workers`).
- ~1-second delay between requests to the same domain.
- 30-second timeout per request.
- One retry per URL (with the fallback UA), then logged as failed.

## Known limitations

- **Paywalls and bot walls.** Some publishers (Elsevier, Wiley, Taylor &
  Francis, certain news sites) return 403/Captcha pages. Those land in
  `failures.log` with the HTTP status code; you can manually fetch them
  and drop the file into `raw/` using the same `<sha1>.<ext>` filename, then
  re-run the script to regenerate the markdown.
- **JavaScript-rendered pages.** The script uses plain `requests`, no
  headless browser. Pages whose content is built client-side (some modern
  SPAs) will save an empty shell.
- **PDFs with images / scanned PDFs.** Text extraction only — no OCR.
  Scan-only PDFs will produce empty markdown bodies.
- **HTML cleanup.** The conversion preserves nav menus, footers, etc.
  This is intentional (lossless caching) — downstream summarization can
  filter further.
- **Sci-Hub etc.** are deliberately not used; we mark gated aggregator
  domains as `auth_required` instead.
- **URL trailing-punctuation heuristics** trim trailing `.,;:)]>*` which is
  almost always correct for prose but could in principle truncate a
  legitimate URL ending in punctuation.
