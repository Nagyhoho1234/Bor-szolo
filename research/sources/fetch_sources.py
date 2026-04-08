"""
fetch_sources.py
================

Pipeline that:
  1. Extracts every source URL from the 22 district synthesis Markdown files
     in C:\\Bor-szolo\\research\\districts\\*.md
  2. Deduplicates URLs across all files
  3. Downloads each source (HTML/PDF/other) to a local cache, named by SHA1
  4. Converts each downloaded source to a standalone Markdown file
  5. Builds a JSON index and a human-readable INDEX.md
  6. Logs failures (and skips known auth-gated aggregators)

Run:
    python fetch_sources.py            # full pipeline
    python fetch_sources.py --help     # see options
    python fetch_sources.py --dry-run  # just list URLs, no download
    python fetch_sources.py --workers 8

Idempotent: re-running will not re-download already-cached sources.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import logging
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Optional third-party imports (we degrade gracefully and tell the user)
# ---------------------------------------------------------------------------
_MISSING: list[str] = []

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore
    _MISSING.append("requests")

try:
    from markdownify import markdownify as _md_from_html  # type: ignore
    _HTML_BACKEND = "markdownify"
except ImportError:
    try:
        import html2text  # type: ignore
        _HTML_BACKEND = "html2text"
    except ImportError:
        _HTML_BACKEND = None
        _MISSING.append("markdownify (or html2text)")

try:
    import fitz  # type: ignore  # PyMuPDF
    _PDF_BACKEND = "pymupdf"
except ImportError:
    try:
        from pdfminer.high_level import extract_text as _pdfminer_extract  # type: ignore
        _PDF_BACKEND = "pdfminer"
    except ImportError:
        _PDF_BACKEND = None
        _MISSING.append("pymupdf (or pdfminer.six)")

try:
    from tqdm import tqdm  # type: ignore
except ImportError:
    tqdm = None  # type: ignore
    _MISSING.append("tqdm")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(r"C:\Bor-szőlő")
DISTRICTS_DIR = PROJECT_ROOT / "research" / "districts"
SOURCES_DIR = PROJECT_ROOT / "research" / "sources"
RAW_DIR = SOURCES_DIR / "raw"
MD_DIR = SOURCES_DIR / "md"
INDEX_JSON = SOURCES_DIR / "index.json"
INDEX_MD = SOURCES_DIR / "INDEX.md"
FAILURES_LOG = SOURCES_DIR / "failures.log"

UA_PRIMARY = (
    "BorSzoloResearchBot/1.0 (+wine-district climate study; "
    "academic use; contact: research@example.org)"
)
UA_FALLBACK = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

REQUEST_TIMEOUT = 30          # seconds
MAX_WORKERS_DEFAULT = 8
PER_DOMAIN_DELAY = 1.0        # seconds between hits to the same domain

# Domains that are known landing pages requiring login / paid access.
# We treat these as auth_required and skip the download.
AUTH_GATED_DOMAINS = {
    "sci-hub.se", "sci-hub.ru", "sci-hub.st",
    "z-lib.org", "libgen.is", "libgen.rs",
    "academia.edu", "www.academia.edu",
    "jstor.org", "www.jstor.org",
    "ieeexplore.ieee.org",  # most papers gated
}

# URL extraction regexes
RE_MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
RE_BARE_URL = re.compile(
    r"(?<![\(\[])\bhttps?://[^\s)<>\]\"']+",
)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
def _setup_logging() -> logging.Logger:
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("fetch_sources")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s",
                                          datefmt="%H:%M:%S"))
        logger.addHandler(sh)
    return logger


LOG = _setup_logging()


# Per-domain rate-limiting lock
_domain_locks: dict[str, threading.Lock] = {}
_domain_last_hit: dict[str, float] = {}
_domain_dict_lock = threading.Lock()


def _domain_throttle(url: str) -> None:
    """Sleep just enough to respect PER_DOMAIN_DELAY for this URL's host."""
    host = urlparse(url).netloc.lower()
    with _domain_dict_lock:
        lock = _domain_locks.setdefault(host, threading.Lock())
    with lock:
        last = _domain_last_hit.get(host, 0.0)
        now = time.time()
        wait = PER_DOMAIN_DELAY - (now - last)
        if wait > 0:
            time.sleep(wait)
        _domain_last_hit[host] = time.time()


# ---------------------------------------------------------------------------
# URL extraction
# ---------------------------------------------------------------------------
def extract_urls_from_file(path: Path) -> list[str]:
    """Pull every http(s) URL out of a single district markdown file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    found: list[str] = []

    # Markdown links anywhere in the file
    for m in RE_MD_LINK.finditer(text):
        found.append(m.group(2))

    # Bare URLs anywhere (covers §15 plain text and inline citations)
    for m in RE_BARE_URL.finditer(text):
        found.append(m.group(0))

    # Normalize trailing junk like .,;) often left from sentence-end URLs
    cleaned: list[str] = []
    for u in found:
        u = u.rstrip(".,;:)]>")
        # Drop trailing markdown asterisks/parens
        u = u.rstrip("*")
        if u:
            cleaned.append(u)
    return cleaned


def collect_all_urls() -> dict[str, list[str]]:
    """Return {url: [district_filenames_that_cited_it]} sorted."""
    mapping: dict[str, set[str]] = {}
    md_files = sorted(DISTRICTS_DIR.glob("*.md"))
    LOG.info("Scanning %d district files in %s", len(md_files), DISTRICTS_DIR)
    for f in md_files:
        for u in extract_urls_from_file(f):
            mapping.setdefault(u, set()).add(f.name)
    LOG.info("Found %d unique URLs across %d files", len(mapping), len(md_files))
    return {u: sorted(d) for u, d in sorted(mapping.items())}


# ---------------------------------------------------------------------------
# Download / cache
# ---------------------------------------------------------------------------
def url_sha1(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


def guess_extension(url: str, content_type: Optional[str]) -> str:
    """Decide a file extension for the cached raw blob."""
    path = urlparse(url).path.lower()
    if path.endswith(".pdf"):
        return ".pdf"
    if content_type:
        ct = content_type.split(";")[0].strip().lower()
        if ct == "application/pdf":
            return ".pdf"
        if ct in ("text/html", "application/xhtml+xml"):
            return ".html"
        if ct.startswith("text/"):
            return ".txt"
    # Generic fallback: assume html (most web pages)
    return ".html"


def is_auth_gated(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return host in AUTH_GATED_DOMAINS


def _existing_raw_for(sha: str) -> Optional[Path]:
    """Return existing raw cache file for this sha1 if any."""
    if not RAW_DIR.exists():
        return None
    for p in RAW_DIR.glob(sha + ".*"):
        if p.is_file() and p.stat().st_size > 0:
            return p
    return None


def download_one(url: str) -> dict:
    """
    Try to download a single URL. Returns a result dict that always
    contains: url, sha1, status (ok|auth_required|failed|cached),
              raw_path (or None), http_status, size, content_type, error.
    """
    sha = url_sha1(url)
    result: dict = {
        "url": url,
        "sha1": sha,
        "status": "failed",
        "raw_path": None,
        "http_status": None,
        "size": 0,
        "content_type": None,
        "error": None,
    }

    if is_auth_gated(url):
        result["status"] = "auth_required"
        result["error"] = "domain in AUTH_GATED_DOMAINS"
        return result

    existing = _existing_raw_for(sha)
    if existing is not None:
        result["status"] = "cached"
        result["raw_path"] = str(existing)
        result["size"] = existing.stat().st_size
        # ext to content-type-ish
        result["content_type"] = (
            "application/pdf" if existing.suffix == ".pdf" else "text/html"
        )
        return result

    if requests is None:
        result["error"] = "requests not installed"
        return result

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for attempt, ua in enumerate((UA_PRIMARY, UA_FALLBACK), start=1):
        try:
            _domain_throttle(url)
            resp = requests.get(
                url,
                headers={
                    "User-Agent": ua,
                    "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
                    "Accept-Language": "en,hu;q=0.8",
                },
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                stream=False,
            )
            result["http_status"] = resp.status_code
            result["content_type"] = resp.headers.get("Content-Type")
            if resp.status_code == 200 and resp.content:
                ext = guess_extension(url, result["content_type"])
                raw_path = RAW_DIR / f"{sha}{ext}"
                raw_path.write_bytes(resp.content)
                result["raw_path"] = str(raw_path)
                result["size"] = len(resp.content)
                result["status"] = "ok"
                return result
            else:
                result["error"] = f"HTTP {resp.status_code}"
        except requests.RequestException as exc:  # type: ignore[attr-defined]
            result["error"] = f"{type(exc).__name__}: {exc}"
        except Exception as exc:  # pragma: no cover - last-ditch
            result["error"] = f"{type(exc).__name__}: {exc}"

        if attempt == 1:
            time.sleep(0.8)  # brief pause before UA fallback retry

    return result


# ---------------------------------------------------------------------------
# Conversion to Markdown
# ---------------------------------------------------------------------------
def _html_to_md(html_bytes: bytes) -> tuple[str, str]:
    """Return (title, markdown_body) from raw HTML bytes."""
    # Decode best-effort
    try:
        html = html_bytes.decode("utf-8")
    except UnicodeDecodeError:
        html = html_bytes.decode("latin-1", errors="replace")

    # Extract <title>
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""

    if _HTML_BACKEND == "markdownify":
        md = _md_from_html(html, heading_style="ATX")
    elif _HTML_BACKEND == "html2text":
        h = html2text.HTML2Text()
        h.body_width = 0
        h.ignore_images = True
        md = h.handle(html)
    else:
        # last-ditch: strip tags crudely
        md = re.sub(r"<[^>]+>", "", html)

    return title, md.strip()


def _pdf_to_md(pdf_path: Path) -> tuple[str, str]:
    """Return (title, markdown_body) from a PDF on disk."""
    title = pdf_path.stem
    text = ""
    if _PDF_BACKEND == "pymupdf":
        try:
            doc = fitz.open(pdf_path)  # type: ignore[arg-type]
            try:
                meta_title = (doc.metadata or {}).get("title") or ""
                if meta_title.strip():
                    title = meta_title.strip()
                pages = []
                for i, page in enumerate(doc, start=1):
                    pages.append(f"\n\n## Page {i}\n\n{page.get_text()}")
                text = "".join(pages)
            finally:
                doc.close()
        except Exception as exc:  # pragma: no cover
            text = f"_PDF extraction failed: {exc}_"
    elif _PDF_BACKEND == "pdfminer":
        try:
            text = _pdfminer_extract(str(pdf_path)) or ""
        except Exception as exc:  # pragma: no cover
            text = f"_PDF extraction failed: {exc}_"
    else:
        text = "_No PDF backend installed (pip install pymupdf or pdfminer.six)_"

    return title, text.strip()


def convert_to_md(result: dict, districts: list[str]) -> Optional[Path]:
    """
    Convert a successfully downloaded raw file to a standalone Markdown file.
    Returns the path to the MD file (or None on failure).
    """
    raw_path_str = result.get("raw_path")
    if not raw_path_str:
        return None
    raw_path = Path(raw_path_str)
    if not raw_path.exists():
        return None

    MD_DIR.mkdir(parents=True, exist_ok=True)
    md_path = MD_DIR / f"{result['sha1']}.md"

    # Idempotency: skip if MD newer than raw
    if md_path.exists() and md_path.stat().st_mtime >= raw_path.stat().st_mtime:
        return md_path

    try:
        if raw_path.suffix == ".pdf":
            title, body = _pdf_to_md(raw_path)
        else:
            title, body = _html_to_md(raw_path.read_bytes())
    except Exception as exc:
        LOG.warning("Conversion failed for %s: %s", result["url"], exc)
        return None

    header_lines = [
        f"# Source: {result['url']}",
        "",
        f"**Original title:** {title or '(unknown)'}",
        f"**District(s):** {', '.join(districts)}",
        f"**Downloaded:** {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "---",
        "",
    ]
    md_path.write_text("\n".join(header_lines) + body + "\n", encoding="utf-8")
    return md_path


# ---------------------------------------------------------------------------
# Failure logging
# ---------------------------------------------------------------------------
_failures_lock = threading.Lock()


def log_failure(url: str, reason: str) -> None:
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(timezone.utc).isoformat()}\t{url}\t{reason}\n"
    with _failures_lock:
        with FAILURES_LOG.open("a", encoding="utf-8") as fh:
            fh.write(line)


# ---------------------------------------------------------------------------
# Index builders
# ---------------------------------------------------------------------------
def write_json_index(records: list[dict]) -> None:
    INDEX_JSON.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_markdown_index(records: list[dict]) -> None:
    """Group sources by district, with internal links to local MD copies."""
    by_district: dict[str, list[dict]] = {}
    for r in records:
        for d in r.get("districts", []):
            by_district.setdefault(d, []).append(r)

    lines: list[str] = []
    lines.append("# Research Sources Index")
    lines.append("")
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_")
    lines.append("")
    lines.append(f"Total unique sources: **{len(records)}**")
    ok = sum(1 for r in records if r["status"] in ("ok", "cached"))
    fail = sum(1 for r in records if r["status"] == "failed")
    auth = sum(1 for r in records if r["status"] == "auth_required")
    lines.append(f"- Downloaded OK: **{ok}**")
    lines.append(f"- Failed: **{fail}**")
    lines.append(f"- Auth-gated (skipped): **{auth}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    for district in sorted(by_district):
        lines.append(f"## {district}")
        lines.append("")
        for r in sorted(by_district[district], key=lambda x: x["url"]):
            md_rel = r.get("md_path")
            if md_rel:
                # Relative link from sources/ to md/<sha>.md
                rel = Path(md_rel).relative_to(SOURCES_DIR).as_posix()
                lines.append(f"- [{r['url']}]({rel})  _(status: {r['status']})_")
            else:
                lines.append(f"- {r['url']}  _(status: {r['status']})_")
        lines.append("")

    INDEX_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline(workers: int, dry_run: bool) -> int:
    if _MISSING and not dry_run:
        LOG.error("Missing required packages: %s", ", ".join(_MISSING))
        LOG.error("Install with: pip install requests markdownify pymupdf tqdm")
        return 2

    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)

    url_map = collect_all_urls()
    urls = list(url_map.keys())

    if dry_run:
        for u in urls:
            print(u)
        LOG.info("Dry run: %d URLs (no download).", len(urls))
        return 0

    LOG.info("Downloading %d unique URLs with %d workers...", len(urls), workers)

    records: list[dict] = []
    iterator: object

    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_url = {pool.submit(download_one, u): u for u in urls}
        if tqdm is not None:
            iterator = tqdm(cf.as_completed(future_to_url),
                            total=len(future_to_url),
                            desc="download", unit="src")
        else:
            iterator = cf.as_completed(future_to_url)

        for fut in iterator:  # type: ignore[assignment]
            url = future_to_url[fut]
            try:
                res = fut.result()
            except Exception as exc:  # pragma: no cover
                res = {
                    "url": url, "sha1": url_sha1(url), "status": "failed",
                    "raw_path": None, "http_status": None, "size": 0,
                    "content_type": None, "error": f"executor: {exc}",
                }

            res["districts"] = url_map[url]

            if res["status"] in ("ok", "cached"):
                md_path = convert_to_md(res, res["districts"])
                res["md_path"] = str(md_path) if md_path else None
            else:
                res["md_path"] = None
                reason = res.get("error") or res["status"]
                log_failure(url, f"{res['status']}: {reason}")

            records.append(res)

    LOG.info("Writing index.json and INDEX.md ...")
    write_json_index(records)
    write_markdown_index(records)

    ok = sum(1 for r in records if r["status"] in ("ok", "cached"))
    fail = sum(1 for r in records if r["status"] == "failed")
    auth = sum(1 for r in records if r["status"] == "auth_required")
    LOG.info("Done. ok=%d failed=%d auth_required=%d total=%d",
             ok, fail, auth, len(records))
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Fetch and convert all research sources cited in district MD files.",
    )
    p.add_argument("--workers", type=int, default=MAX_WORKERS_DEFAULT,
                   help=f"parallel download workers (default {MAX_WORKERS_DEFAULT})")
    p.add_argument("--dry-run", action="store_true",
                   help="just print URLs that would be fetched and exit")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    return run_pipeline(workers=max(1, args.workers), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
