// Process research-dossier markdown for the district detail pages.
//
// The source markdowns under research/districts/*.md are research-author
// notes with three artefacts that look bad rendered on a public site:
//
//   1. A "Reading guide" blockquote at the top that explains the
//      [OBSERVED]/[PROJECTED]/[HU-AGGREGATE] tagging convention.
//   2. Inline `[OBSERVED]`, `[PROJECTED]`, `[HU-AGGREGATE]`, `[N-HU ANALOGUE]`,
//      `[OBSERVED + PROJECTED]`, `[OBSERVED, N-HU ANALOGUE]` etc. tags scattered
//      through the prose.
//   3. `> Sources (§1): [title](url) · [title](url)` blockquotes at the end of
//      every numbered section. These should become numbered footnotes that link
//      to a single References section at the bottom of the page.
//
// This module strips (1) and (2) and converts (3) into [1] [2] [3] markers
// that link to anchors `#ref1`, `#ref2`, ... in a References section emitted
// by the caller.

export type Reference = { n: number; title: string; url: string };

export type ProcessedResearch = {
  body: string;
  references: Reference[];
};

export function processResearchMarkdown(raw: string): ProcessedResearch {
  let text = raw;

  // 1. Strip the "Reading guide" blockquote — typically a single multi-line
  //    blockquote starting with `> **Reading guide.**` or `> Reading guide.`
  text = text.replace(
    /^>\s*\*?\*?Reading guide[\s\S]*?(?=\n\s*\n|\n---|\n##|$)/m,
    '',
  );

  // 2. Strip inline meta-tags. These are square-bracketed UPPERCASE labels
  //    that are NOT markdown links (i.e. not followed by `(`). We allow
  //    digits, spaces, slashes, +, , and -.
  //    Examples to remove:
  //       [OBSERVED]
  //       [PROJECTED]
  //       [HU-AGGREGATE]
  //       [N-HU ANALOGUE]
  //       [OBSERVED + PROJECTED]
  //       [OBSERVED + emergent]
  //       [OBSERVED, N-HU ANALOGUE]
  //       [N-HU ANALOGUE / HU-AGGREGATE]
  //
  //    The negative lookahead `(?!\()` protects markdown links like
  //    `[Wines of Hungary](https://...)`.
  text = text.replace(
    /\[((?:OBSERVED|PROJECTED|EMERGENT|HU-AGGREGATE|N-HU ANALOGUE|FORECAST|SCENARIO|HISTORICAL|MODELLED|EXTRAPOLATED|emergent|aggregate)[A-Za-z0-9\s+,\-/]*)\](?!\()/g,
    '',
  );

  // Tidy up doubled spaces left by tag removal
  text = text.replace(/[ \t]{2,}/g, ' ').replace(/\s+([.;,])/g, '$1');

  // 3. Process inline source blockquotes. Each looks like:
  //       > Sources (§1): [Title](url) · [Title2](url2)
  //    or > Sources: [Title](url); [Title2](url2)
  //    or > Source: [Title](url)
  //    They can span multiple lines if the original was wrapped.
  //
  //    We collect every (title, url) into a deduplicated `references` list
  //    (first-seen wins for title) and replace the whole blockquote with
  //    inline numeric markers `[1, 2, 3]` linking to `#refN`.
  const references: Reference[] = [];
  const urlToN = new Map<string, number>();

  function registerLink(title: string, url: string): number {
    let n = urlToN.get(url);
    if (n != null) return n;
    n = references.length + 1;
    urlToN.set(url, n);
    references.push({ n, title: title.trim(), url });
    return n;
  }

  // Match a `> Sources(...)?: ...` blockquote that may span several `> ` lines.
  text = text.replace(
    /(^>\s*Sources?\b[^\n]*(?:\n>\s*[^\n]*)*)/gm,
    (block) => {
      // Extract every [title](url) inside the block
      const linkRe = /\[([^\]]+?)\]\(([^)]+?)\)/g;
      const nums: number[] = [];
      let m: RegExpExecArray | null;
      while ((m = linkRe.exec(block)) !== null) {
        nums.push(registerLink(m[1], m[2]));
      }
      if (nums.length === 0) return ''; // unparseable, drop it
      const markers = nums
        .map((n) => `[\\[${n}\\]](#ref${n})`)
        .join(' ');
      // Render the marker as a small superscript-ish line, NOT a blockquote.
      return `<sup class="text-xs text-neutral-500">Sources: ${markers}</sup>`;
    },
  );

  // 4. Final tidy: collapse 3+ blank lines, trim leading/trailing whitespace
  text = text.replace(/\n{3,}/g, '\n\n').trim();

  return { body: text, references };
}
