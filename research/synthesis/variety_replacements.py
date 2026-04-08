"""
Variety-replacement analysis for the 22 Hungarian wine districts under
climate projections at four horizons (≈ +20, +40, +60, +80 years from 2026)
and two RCP scenarios.

Input: analysis/curated/variety_match/suitability_long.parquet
       analysis/config/grape_envelopes.csv

For each district × future (period, scenario) combination, identifies the
top 3–4 REPLACEMENT candidate varieties to plant in place of declining
principal varieties. Ranking: prefers high future suitability, positive
delta vs 1991–2020, and high-confidence climate envelopes.

Outputs
-------
  research/synthesis/variety_replacements.csv    — machine-readable
  research/synthesis/variety_replacements.md     — human-readable report
"""
from __future__ import annotations

import sys
import io
from pathlib import Path

import pandas as pd

# Force UTF-8 stdout (the project path contains ő)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(r"C:\Bor-szőlő")
PARQUET = ROOT / "analysis" / "curated" / "variety_match" / "suitability_long.parquet"
ENVELOPES = ROOT / "analysis" / "config" / "grape_envelopes.csv"
OUT_DIR = ROOT / "research" / "synthesis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Horizon mapping — now using 20-year bins for both RCPs
# (from 2026 reference year, the user-facing labels are approximate)
HORIZONS = [
    ("Near term (2021–2040)", "2021-2040", "rcp45", "moderate"),
    ("Near term (2021–2040)", "2021-2040", "rcp85", "high"),
    ("≈ +20y (2041–2060)", "2041-2060", "rcp45", "moderate"),
    ("≈ +20y (2041–2060)", "2041-2060", "rcp85", "high"),
    ("≈ +40y (2061–2080)", "2061-2080", "rcp45", "moderate"),
    ("≈ +40y (2061–2080)", "2061-2080", "rcp85", "high"),
    ("≈ +60y (2081–2100)", "2081-2100", "rcp45", "moderate"),
    ("≈ +60y (2081–2100)", "2081-2100", "rcp85", "high"),
]

# Ranking thresholds
MIN_FUTURE_SUITABILITY = 0.55   # a replacement must be ≥ this under future climate
AT_RISK_DELTA = -0.20           # currently-principal varieties dropping by this much = at risk
TOP_N_REPLACEMENTS = 4


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_parquet(PARQUET)
    envelopes = pd.read_csv(ENVELOPES)
    return df, envelopes


def district_replacement_candidates(
    df: pd.DataFrame,
    district: str,
    period: str,
    scenario: str,
    top_n: int = TOP_N_REPLACEMENTS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns (at_risk_df, replacements_df) for one district at one horizon.

    at_risk_df: currently-principal varieties whose suitability is dropping hard.
    replacements_df: top_n candidate varieties that could fill the gap.
    """
    future = df[
        (df.borvidek == district)
        & (df.period == period)
        & (df.scenario == scenario)
    ].copy()

    # At-risk = principal varieties losing ground
    at_risk = future[
        (future.in_principal_varieties)
        & (future.delta_vs_1991_2020 <= AT_RISK_DELTA)
    ].sort_values("delta_vs_1991_2020").reset_index(drop=True)

    # Candidate pool = varieties with adequate future suitability
    candidates = future[future.suitability >= MIN_FUTURE_SUITABILITY].copy()

    # Scoring: rank by (future suitability, delta, confidence bonus)
    conf_bonus = {"high": 0.05, "medium": 0.0, "low": -0.05}
    candidates["score"] = (
        candidates["suitability"]
        + 0.25 * candidates["delta_vs_1991_2020"].clip(lower=-1, upper=1)
        + candidates["confidence"].map(conf_bonus).fillna(0)
    )

    # Prefer varieties that are NOT already declining principal varieties
    # (those are the ones we want to replace, not recommend as replacements).
    # Keep: (a) non-principal new varieties, (b) principal varieties that are holding up (delta >= 0)
    at_risk_names = set(at_risk["variety"])
    candidates = candidates[~candidates["variety"].isin(at_risk_names)]

    candidates = candidates.sort_values(
        ["score", "suitability"], ascending=[False, False]
    ).head(top_n).reset_index(drop=True)

    return at_risk, candidates


def build_long_replacements(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (district, horizon, rank) containing the replacement pick."""
    rows = []
    for district in sorted(df.borvidek.unique()):
        for label, period, scenario, emissions_level in HORIZONS:
            at_risk, repls = district_replacement_candidates(
                df, district, period, scenario
            )
            for rank, r in enumerate(repls.itertuples(index=False), 1):
                novel = "new" if not r.in_principal_varieties else "expand"
                rows.append({
                    "borvidek": district,
                    "horizon_label": label,
                    "period": period,
                    "scenario": scenario,
                    "emissions_level": emissions_level,
                    "rank": rank,
                    "variety": r.variety,
                    "variety_en": r.variety_en,
                    "colour": r.colour,
                    "future_suitability": round(float(r.suitability), 3),
                    "delta_vs_1991_2020": round(float(r.delta_vs_1991_2020), 3),
                    "confidence": r.confidence,
                    "limiting_factor": r.limiting_factor,
                    "status": novel,
                    "huglin_mean": round(float(r.huglin_mean), 0),
                    "winkler_mean": round(float(r.winkler_mean), 0),
                })
    return pd.DataFrame(rows)


def build_markdown(df: pd.DataFrame, replacements: pd.DataFrame) -> str:
    lines: list[str] = []
    lines.append("# Variety replacement analysis — 22 Hungarian wine districts")
    lines.append("")
    lines.append(
        "**Generated from** `analysis/curated/variety_match/suitability_long.parquet` "
        "(38 varieties × 22 districts × 4 periods × 3 scenarios)."
    )
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append(
        "For each district and each future (period, scenario) combination, "
        "identifies (a) currently principal varieties whose suitability drops by "
        f"≥ |{abs(AT_RISK_DELTA)}| relative to 1991–2020 [**at-risk**], and (b) top "
        f"{TOP_N_REPLACEMENTS} candidate varieties with future suitability ≥ "
        f"{MIN_FUTURE_SUITABILITY} [**replacements**]. Candidates are ranked by a "
        "composite score: `suitability + 0.25·delta + confidence_bonus` where "
        "high-confidence envelopes get +0.05 and low-confidence −0.05. Varieties "
        "already classified as at-risk are excluded from their own replacement list."
    )
    lines.append("")
    lines.append("### Horizon mapping")
    lines.append("")
    lines.append("| User horizon | Period | Scenario | Emissions |")
    lines.append("|---|---|---|---|")
    for label, period, scenario, emis in HORIZONS:
        lines.append(f"| {label} | {period} | {scenario.upper()} | {emis} |")
    lines.append("")
    lines.append(
        "Note: only two 30-year future bins exist in the dataset. +20y and +40y both "
        "fall in 2041–2070; +60y and +80y both fall in 2071–2100. Where the user asks "
        "for four time steps, we present them as two time bins × two emissions "
        "scenarios (moderate RCP4.5 + high RCP8.5)."
    )
    lines.append("")
    lines.append(
        "**Status tag:** `new` = variety not currently in the district's principal "
        "list (i.e. needs to be planted); `expand` = variety already principal in the "
        "district and climate-robust under the future scenario (expand plantings)."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-district sections
    for district in sorted(df.borvidek.unique()):
        region = df[df.borvidek == district]["borregio"].iloc[0]
        lines.append(f"## {district} ({region})")
        lines.append("")

        # Current principal varieties summary
        current = df[
            (df.borvidek == district)
            & (df.period == "1991-2020")
            & (df.scenario == "observed")
            & (df.in_principal_varieties)
        ][["variety", "variety_en", "colour", "suitability"]].sort_values(
            "suitability", ascending=False
        )
        if not current.empty:
            current_list = ", ".join(
                f"{r.variety} ({r.suitability:.2f})" for r in current.itertuples(index=False)
            )
            lines.append(f"**Current principal varieties (1991–2020 observed):** {current_list}")
            lines.append("")

        # For each horizon, list at-risk + replacements
        for label, period, scenario, emis in HORIZONS:
            at_risk, repls = district_replacement_candidates(df, district, period, scenario)
            lines.append(f"### {label} — {period} {scenario.upper()}")
            lines.append("")

            if not at_risk.empty:
                lines.append("**At-risk current varieties:**")
                lines.append("")
                lines.append("| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |")
                lines.append("|---|---|---|---|")
                for r in at_risk.itertuples(index=False):
                    lines.append(
                        f"| {r.variety} ({r.variety_en}) "
                        f"| {r.suitability:.2f} "
                        f"| {r.delta_vs_1991_2020:+.2f} "
                        f"| {r.limiting_factor} |"
                    )
                lines.append("")
            else:
                lines.append("*No principal varieties cross the at-risk threshold under this scenario.*")
                lines.append("")

            if not repls.empty:
                lines.append(f"**Top {len(repls)} replacement candidates:**")
                lines.append("")
                lines.append("| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |")
                lines.append("|---|---|---|---|---|---|---|---|")
                for i, r in enumerate(repls.itertuples(index=False), 1):
                    status = "new" if not r.in_principal_varieties else "expand"
                    lines.append(
                        f"| {i} "
                        f"| **{r.variety}** "
                        f"| {r.variety_en} "
                        f"| {r.colour} "
                        f"| {r.suitability:.2f} "
                        f"| {r.delta_vs_1991_2020:+.2f} "
                        f"| {r.confidence} "
                        f"| {status} |"
                    )
                lines.append("")
            else:
                lines.append(
                    f"*No varieties meet the future-suitability floor "
                    f"({MIN_FUTURE_SUITABILITY}) under this scenario.* "
                    "This usually means the climate has moved outside the "
                    "envelope of every variety currently in the dataset — "
                    "consider consulting Mediterranean/southern-Iberian "
                    "variety envelopes not yet in `grape_envelopes.csv`."
                )
                lines.append("")

        lines.append("---")
        lines.append("")

    # Hungary-wide summary: which varieties appear most often as replacements?
    lines.append("## Hungary-wide climate-adapted variety rankings")
    lines.append("")
    lines.append(
        "Varieties ranked by the number of (district × horizon) slots in which "
        "they were recommended as a top-4 replacement:"
    )
    lines.append("")
    counts = replacements.groupby(["variety", "variety_en", "colour"]).size().reset_index(
        name="recommendations"
    ).sort_values("recommendations", ascending=False).head(15)
    lines.append("| Variety | EN | Colour | Slots recommended |")
    lines.append("|---|---|---|---|")
    for r in counts.itertuples(index=False):
        lines.append(f"| **{r.variety}** | {r.variety_en} | {r.colour} | {r.recommendations} |")
    lines.append("")

    # Breakdown by horizon
    lines.append("### Top 5 replacements per horizon (Hungary-wide)")
    lines.append("")
    for label, period, scenario, _ in HORIZONS:
        subset = replacements[
            (replacements.period == period) & (replacements.scenario == scenario)
        ]
        lines.append(f"**{label} — {period} {scenario.upper()}**")
        top5 = subset.groupby(["variety", "variety_en", "colour"]).size().reset_index(
            name="count"
        ).sort_values("count", ascending=False).head(5)
        if not top5.empty:
            for r in top5.itertuples(index=False):
                lines.append(f"- {r.variety} ({r.variety_en}, {r.colour}) — {r.count}/22 districts")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    print(f"Loading {PARQUET}")
    df, envelopes = load_data()
    print(f"  {len(df)} rows, {df.borvidek.nunique()} districts, "
          f"{df.variety.nunique()} varieties")

    print("Building replacement recommendations...")
    replacements = build_long_replacements(df)
    print(f"  {len(replacements)} recommendations")

    csv_path = OUT_DIR / "variety_replacements.csv"
    replacements.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  wrote {csv_path}")

    md = build_markdown(df, replacements)
    md_path = OUT_DIR / "variety_replacements.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  wrote {md_path} ({len(md)} chars)")

    # Quick Hungary-wide summary to stdout
    print()
    print("=== Top 10 climate-adapted varieties (Hungary-wide) ===")
    counts = replacements.groupby(["variety", "variety_en", "colour"]).size().reset_index(
        name="n"
    ).sort_values("n", ascending=False).head(10)
    for r in counts.itertuples(index=False):
        print(f"  {r.variety:25s} ({r.variety_en:25s}) {r.colour:5s} -> {r.n:3d} slots")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
