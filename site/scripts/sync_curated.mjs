#!/usr/bin/env node
/*
 * sync_curated.mjs
 *
 * Recursively copies the curated data bundle from
 *   C:\Bor-szőlő\analysis\curated\
 * into
 *   site/public/data/
 *
 * Design decision (documented in-code so the choice is auditable):
 *   parquet-wasm works but requires shipping the ~2 MB wasm blob and dealing
 *   with Next.js static-export + bundler quirks. Since our total parquet
 *   payload is ~1 MB across 37 files and the browser only ever needs to read
 *   a handful of rows per page, we convert every parquet file to a sibling
 *   `.json` file at sync time via a short Python (pyarrow) helper. The
 *   browser then only needs `fetch + JSON.parse`.
 *
 * The original .parquet files are ALSO copied so that the /downloads page
 * can still link them for analysts.
 */

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SITE_ROOT = path.resolve(__dirname, '..');
const SRC = path.resolve(SITE_ROOT, '..', 'analysis', 'curated');
const DST = path.resolve(SITE_ROOT, 'public', 'data');

const SKIP = new Set(['.gitkeep']);
const SKIP_EXT = new Set(['.lock']);

async function walk(dir) {
  const out = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      out.push(...(await walk(full)));
    } else {
      if (SKIP.has(e.name)) continue;
      if (SKIP_EXT.has(path.extname(e.name))) continue;
      out.push(full);
    }
  }
  return out;
}

async function copyFile(src, dst) {
  await fs.mkdir(path.dirname(dst), { recursive: true });
  await fs.copyFile(src, dst);
  const s = await fs.stat(dst);
  return s.size;
}

function parquetToJson(parquetPath, jsonPath) {
  // Uses the local Python (pyarrow) to dump a parquet file to a JSON array.
  // We go through sys.argv so we never pass the UTF-8 path as a Python string
  // literal inside -c, which sometimes trips Windows consoles.
  const py = `
import sys, json
import pyarrow.parquet as pq
src, dst = sys.argv[1], sys.argv[2]
tbl = pq.read_table(src)
records = tbl.to_pylist()
def clean(v):
    if v is None:
        return None
    if isinstance(v, float):
        if v != v:  # NaN
            return None
    return v
for r in records:
    for k, v in list(r.items()):
        r[k] = clean(v)
with open(dst, 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, separators=(',', ':'))
`;
  const res = spawnSync('python', ['-c', py, parquetPath, jsonPath], {
    encoding: 'utf-8',
    env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
  });
  if (res.status !== 0) {
    throw new Error(
      `parquet->json failed for ${parquetPath}\nstdout: ${res.stdout}\nstderr: ${res.stderr}`
    );
  }
}

async function main() {
  console.log('[sync] src:', SRC);
  console.log('[sync] dst:', DST);
  // wipe and recreate
  await fs.rm(DST, { recursive: true, force: true });
  await fs.mkdir(DST, { recursive: true });

  const files = await walk(SRC);
  let nCopied = 0;
  let nJson = 0;
  let totalBytes = 0;

  for (const src of files) {
    const rel = path.relative(SRC, src);
    const dst = path.join(DST, rel);
    const sz = await copyFile(src, dst);
    totalBytes += sz;
    nCopied++;

    if (path.extname(src).toLowerCase() === '.parquet') {
      const jsonDst = dst.replace(/\.parquet$/i, '.json');
      parquetToJson(src, jsonDst);
      const js = await fs.stat(jsonDst);
      totalBytes += js.size;
      nJson++;
    }
  }

  console.log(
    `[sync] copied ${nCopied} files, wrote ${nJson} parquet->json siblings, total ${(
      totalBytes /
      1024 /
      1024
    ).toFixed(2)} MB`
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
