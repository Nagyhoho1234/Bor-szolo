# Variety replacement analysis — 22 Hungarian wine districts

**Generated from** `analysis/curated/variety_match/suitability_long.parquet` (38 varieties × 22 districts × 4 periods × 3 scenarios).

## Method

For each district and each future (period, scenario) combination, identifies (a) currently principal varieties whose suitability drops by ≥ |0.2| relative to 1991–2020 [**at-risk**], and (b) top 4 candidate varieties with future suitability ≥ 0.55 [**replacements**]. Candidates are ranked by a composite score: `suitability + 0.25·delta + confidence_bonus` where high-confidence envelopes get +0.05 and low-confidence −0.05. Varieties already classified as at-risk are excluded from their own replacement list.

### Horizon mapping

| User horizon | Period | Scenario | Emissions |
|---|---|---|---|
| Near term (2021–2040) | 2021-2040 | RCP45 | moderate |
| Near term (2021–2040) | 2021-2040 | RCP85 | high |
| ≈ +20y (2041–2060) | 2041-2060 | RCP45 | moderate |
| ≈ +20y (2041–2060) | 2041-2060 | RCP85 | high |
| ≈ +40y (2061–2080) | 2061-2080 | RCP45 | moderate |
| ≈ +40y (2061–2080) | 2061-2080 | RCP85 | high |
| ≈ +60y (2081–2100) | 2081-2100 | RCP45 | moderate |
| ≈ +60y (2081–2100) | 2081-2100 | RCP85 | high |

Note: only two 30-year future bins exist in the dataset. +20y and +40y both fall in 2041–2070; +60y and +80y both fall in 2071–2100. Where the user asks for four time steps, we present them as two time bins × two emissions scenarios (moderate RCP4.5 + high RCP8.5).

**Status tag:** `new` = variety not currently in the district's principal list (i.e. needs to be planted); `expand` = variety already principal in the district and climate-robust under the future scenario (expand plantings).

---

## Badacsonyi (Balaton)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Rajnai rizling (1.00), Rizlingszilváni (1.00), Szürkebarát (1.00), Budai zöld (1.00), Furmint (0.82), Kéknyelű (0.82)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.18 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | expand |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.18 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Rizlingszilváni (Müller-Thurgau) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Tempranillo** | Tempranillo | red | 1.00 | +0.97 | medium | new |
| 2 | **Fiano** | Fiano | white | 1.00 | +0.97 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.67 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.67 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.18 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | expand |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Rizlingszilváni (Müller-Thurgau) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.97 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.97 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.65 | -0.35 | winkler |
| Rajnai rizling (Riesling) | 0.67 | -0.33 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.97 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.97 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Rizlingszilváni (Müller-Thurgau) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.97 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.97 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.11 | -0.89 | winkler |
| Rajnai rizling (Riesling) | 0.13 | -0.87 | winkler |
| Szürkebarát (Pinot gris) | 0.40 | -0.60 | winkler |
| Budai zöld (Budai zold) | 0.40 | -0.60 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.62 | -0.38 | winkler |
| Kéknyelű (Keknyelu) | 0.51 | -0.30 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |

---

## Balatonboglári (Balaton)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Chardonnay (1.00), Királyleányka (1.00), Kékfrankos (1.00), Pinot noir (1.00), Merlot (0.99), Cabernet sauvignon (0.74)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.64 | -0.36 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.58 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.58 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.26 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.26 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.58 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.58 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.26 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.26 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.55 | -0.45 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.58 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.58 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.26 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.26 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.26 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.26 | high | new |
| 3 | **Sangiovese** | Sangiovese | red | 1.00 | +0.25 | high | new |
| 4 | **Tempranillo** | Tempranillo | red | 1.00 | +0.26 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.54 | -0.46 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.58 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.58 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.26 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.26 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.15 | -0.85 | winkler |
| Királyleányka (Kiralyleanyka) | 0.44 | -0.56 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.66 | -0.34 | winkler |
| Chardonnay (Chardonnay) | 0.66 | -0.34 | winkler |
| Kékfrankos (Blaufränkisch) | 0.66 | -0.34 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.97 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.97 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.35 | -0.65 | winkler |
| Királyleányka (Kiralyleanyka) | 0.65 | -0.35 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.75 | -0.25 | winkler |
| Chardonnay (Chardonnay) | 0.75 | -0.25 | winkler |
| Kékfrankos (Blaufränkisch) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.97 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.97 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.00 | -1.00 | winkler |
| Királyleányka (Kiralyleanyka) | 0.05 | -0.95 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.15 | -0.85 | winkler |
| Chardonnay (Chardonnay) | 0.15 | -0.85 | winkler |
| Kékfrankos (Blaufränkisch) | 0.15 | -0.85 | winkler |
| Merlot (Merlot) | 0.39 | -0.60 | winkler |
| Cabernet sauvignon (Cabernet Sauvignon) | 0.47 | -0.27 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.97 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.97 | low | new |

---

## Balatonfelvidéki (Balaton)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Rajnai rizling (1.00), Szürkebarát (1.00), Tramini (1.00), Sauvignon blanc (1.00), Chardonnay (1.00), Muscat ottonel (1.00)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 2 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 4 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 2 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 4 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |
| Muscat ottonel (Muscat Ottonel) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.72 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.72 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 2 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 4 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |
| Muscat ottonel (Muscat Ottonel) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.72 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.72 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.35 | -0.65 | winkler |
| Tramini (Gewürztraminer) | 0.35 | -0.65 | winkler |
| Muscat ottonel (Muscat Ottonel) | 0.35 | -0.65 | winkler |
| Szürkebarát (Pinot gris) | 0.71 | -0.29 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.71 | -0.29 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.75 | -0.25 | winkler |
| Chardonnay (Chardonnay) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.70 | -0.30 | winkler |
| Tramini (Gewürztraminer) | 0.70 | -0.30 | winkler |
| Muscat ottonel (Muscat Ottonel) | 0.70 | -0.30 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.72 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.72 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.06 | -0.94 | winkler |
| Tramini (Gewürztraminer) | 0.06 | -0.94 | winkler |
| Muscat ottonel (Muscat Ottonel) | 0.06 | -0.94 | winkler |
| Szürkebarát (Pinot gris) | 0.28 | -0.72 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.28 | -0.72 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.48 | -0.52 | winkler |
| Chardonnay (Chardonnay) | 0.48 | -0.52 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |

---

## Balatonfüred-Csopaki (Balaton)

**Current principal varieties (1991–2020 observed):** Furmint (1.00), Olaszrizling (1.00), Rajnai rizling (1.00), Szürkebarát (1.00), Tramini (1.00), Sauvignon blanc (1.00)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.70 | -0.30 | winkler |
| Tramini (Gewürztraminer) | 0.70 | -0.30 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.55 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.55 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.25 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.25 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.55 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.55 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.25 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.25 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.49 | -0.51 | winkler |
| Tramini (Gewürztraminer) | 0.49 | -0.51 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.55 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.55 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.25 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.25 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.25 | high | new |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.25 | high | new |
| 3 | **Sangiovese** | Sangiovese | red | 1.00 | +0.25 | high | new |
| 4 | **Touriga Nacional** | Touriga Nacional | red | 0.98 | +0.53 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.32 | -0.68 | winkler |
| Tramini (Gewürztraminer) | 0.32 | -0.68 | winkler |
| Szürkebarát (Pinot gris) | 0.71 | -0.29 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.71 | -0.29 | winkler |
| Furmint (Furmint) | 0.75 | -0.25 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.95 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.95 | low | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.17 | -0.83 | winkler |
| Tramini (Gewürztraminer) | 0.17 | -0.83 | winkler |
| Szürkebarát (Pinot gris) | 0.46 | -0.54 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.46 | -0.54 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.65 | -0.35 | winkler |
| Furmint (Furmint) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.95 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.95 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.30 | -0.70 | winkler |
| Tramini (Gewürztraminer) | 0.30 | -0.70 | winkler |
| Szürkebarát (Pinot gris) | 0.63 | -0.37 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.63 | -0.37 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.73 | -0.27 | winkler |
| Furmint (Furmint) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.95 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.95 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.00 | -1.00 | winkler |
| Tramini (Gewürztraminer) | 0.00 | -1.00 | winkler |
| Szürkebarát (Pinot gris) | 0.03 | -0.97 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.03 | -0.97 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.13 | -0.87 | winkler |
| Furmint (Furmint) | 0.27 | -0.73 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.98 | +0.98 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.98 | +0.98 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.98 | +0.93 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 0.98 | +0.93 | low | new |

---

## Bükki (Felső-Magyarországi)

**Current principal varieties (1991–2020 observed):** Müller-Thurgau (1.00), Olaszrizling (0.81), Chardonnay (0.81), Cserszegi fűszeres (0.81), Leányka (0.81), Királyleányka (0.81)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 2 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 3 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | expand |
| 4 | **Tramini** | Gewürztraminer | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.19 | high | expand |
| 2 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.19 | high | new |
| 3 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.19 | high | new |
| 4 | **Chardonnay** | Chardonnay | white | 1.00 | +0.19 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 0.98 | +0.17 | high | expand |
| 2 | **Szürkebarát** | Pinot gris | white | 0.98 | +0.17 | high | new |
| 3 | **Sauvignon blanc** | Sauvignon Blanc | white | 0.98 | +0.17 | high | new |
| 4 | **Chardonnay** | Chardonnay | white | 0.98 | +0.17 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.51 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.51 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.51 | medium | new |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.51 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Müller-Thurgau (Müller-Thurgau) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.77 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.77 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Müller-Thurgau (Müller-Thurgau) | 0.59 | -0.41 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.77 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.77 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Müller-Thurgau (Müller-Thurgau) | 0.73 | -0.27 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.77 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.77 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Müller-Thurgau (Müller-Thurgau) | 0.07 | -0.93 | winkler |
| Leányka (Leanyka) | 0.32 | -0.49 | winkler |
| Királyleányka (Kiralyleanyka) | 0.32 | -0.49 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.43 | -0.38 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.52 | -0.29 | winkler |
| Chardonnay (Chardonnay) | 0.52 | -0.29 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |

---

## Csongrádi (Duna)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Cserszegi fűszeres (1.00), Generosa (1.00), Kékfrankos (1.00), Kadarka (0.78)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.66 | -0.34 | heat |
| Generosa (Generosa) | 0.66 | -0.34 | heat |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.71 | -0.29 | heat |
| Kékfrankos (Blaufränkisch) | 0.71 | -0.29 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Syrah** | Syrah | red | 0.87 | +0.09 | high | new |
| 2 | **Cabernet franc** | Cabernet Franc | red | 0.90 | -0.10 | high | new |
| 3 | **Sangiovese** | Sangiovese | red | 0.90 | -0.10 | high | new |
| 4 | **Tempranillo** | Tempranillo | red | 0.87 | +0.09 | medium | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.22 | high | new |
| 2 | **Merlot** | Merlot | red | 1.00 | +0.22 | high | new |
| 3 | **Syrah** | Syrah | red | 1.00 | +0.22 | high | new |
| 4 | **Furmint** | Furmint | white | 1.00 | +0.22 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.22 | -0.78 | winkler |
| Generosa (Generosa) | 0.22 | -0.78 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.26 | -0.74 | winkler |
| Kékfrankos (Blaufränkisch) | 0.26 | -0.74 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.91 | +0.65 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.91 | +0.65 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.91 | +0.36 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.91 | +0.33 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.22 | high | new |
| 2 | **Merlot** | Merlot | red | 1.00 | +0.22 | high | new |
| 3 | **Syrah** | Syrah | red | 1.00 | +0.22 | high | new |
| 4 | **Furmint** | Furmint | white | 1.00 | +0.22 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.22 | -0.78 | winkler |
| Generosa (Generosa) | 0.22 | -0.78 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.27 | -0.73 | winkler |
| Kékfrankos (Blaufränkisch) | 0.27 | -0.73 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.95 | +0.69 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.95 | +0.69 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.95 | +0.40 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.95 | +0.36 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.06 | -0.94 | winkler |
| Generosa (Generosa) | 0.06 | -0.94 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.08 | -0.92 | winkler |
| Kékfrankos (Blaufränkisch) | 0.08 | -0.92 | winkler |
| Kadarka (Kadarka) | 0.28 | -0.50 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.85 | +0.59 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.85 | +0.59 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.85 | +0.30 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.85 | +0.26 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.25 | -0.75 | winkler |
| Generosa (Generosa) | 0.25 | -0.75 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.31 | -0.69 | winkler |
| Kékfrankos (Blaufränkisch) | 0.31 | -0.69 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.74 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.74 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.45 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.41 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Olaszrizling (Welschriesling / Olaszrizling) | 0.00 | -1.00 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.00 | -1.00 | winkler |
| Generosa (Generosa) | 0.00 | -1.00 | winkler |
| Kékfrankos (Blaufränkisch) | 0.00 | -1.00 | winkler |
| Kadarka (Kadarka) | 0.02 | -0.76 | winkler |

*No varieties meet the future-suitability floor (0.55) under this scenario.* This usually means the climate has moved outside the envelope of every variety currently in the dataset — consider consulting Mediterranean/southern-Iberian variety envelopes not yet in `grape_envelopes.csv`.

---

## Egri (Felső-Magyarországi)

**Current principal varieties (1991–2020 observed):** Kékfrankos (1.00), Pinot noir (1.00), Olaszrizling (0.84), Leányka (0.84), Cabernet franc (0.84), Hárslevelű (0.53), Kadarka (0.53), Merlot (0.53), Cabernet sauvignon (0.40)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 2 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 3 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 4 | **Tramini** | Gewürztraminer | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.16 | high | expand |
| 2 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.16 | high | new |
| 3 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.16 | high | new |
| 4 | **Chardonnay** | Chardonnay | white | 1.00 | +0.16 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.64 | -0.36 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Fiano** | Fiano | white | 1.00 | +0.58 | medium | new |
| 2 | **Sangiovese** | Sangiovese | red | 1.00 | +0.37 | high | new |
| 3 | **Vermentino** | Vermentino | white | 1.00 | +0.37 | medium | new |
| 4 | **Verdejo** | Verdejo | white | 1.00 | +0.37 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.47 | high | expand |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.47 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.47 | medium | expand |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.47 | medium | expand |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.65 | -0.35 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.94 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.94 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.60 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.60 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.19 | -0.81 | winkler |
| Leányka (Leanyka) | 0.52 | -0.32 | winkler |
| Kékfrankos (Blaufränkisch) | 0.72 | -0.28 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.96 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.57 | -0.43 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.94 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.94 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.60 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.60 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.00 | -1.00 | winkler |
| Kékfrankos (Blaufränkisch) | 0.17 | -0.83 | winkler |
| Leányka (Leanyka) | 0.06 | -0.78 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.17 | -0.67 | winkler |
| Cabernet franc (Cabernet Franc) | 0.29 | -0.55 | winkler |
| Hárslevelű (Harslevelu) | 0.17 | -0.35 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.96 | medium | new |

---

## Etyek-Budai (Felső-Pannon)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Sauvignon blanc (1.00), Chardonnay (1.00), Zöld veltelíni (1.00), Királyleányka (1.00), Pinot noir (1.00)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.53 | -0.47 | winkler |
| Zöld veltelíni (Grüner Veltliner) | 0.73 | -0.27 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sangiovese** | Sangiovese | red | 1.00 | +0.25 | high | new |
| 2 | **Touriga Nacional** | Touriga Nacional | red | 0.94 | +0.63 | medium | new |
| 3 | **Aglianico** | Aglianico | red | 0.94 | +0.63 | medium | new |
| 4 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 0.94 | +0.34 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.75 | -0.25 | winkler |
| Pinot noir (Pinot Noir) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.69 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.69 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.43 | -0.57 | winkler |
| Zöld veltelíni (Grüner Veltliner) | 0.61 | -0.39 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.69 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.69 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.75 | -0.25 | winkler |
| Pinot noir (Pinot Noir) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 0.95 | +0.64 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 0.95 | +0.64 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.30 | -0.70 | winkler |
| Zöld veltelíni (Grüner Veltliner) | 0.49 | -0.51 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.76 | -0.24 | heat |
| Királyleányka (Kiralyleanyka) | 0.76 | -0.24 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.69 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.69 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.12 | -0.88 | winkler |
| Zöld veltelíni (Grüner Veltliner) | 0.21 | -0.79 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.39 | -0.61 | winkler |
| Királyleányka (Kiralyleanyka) | 0.39 | -0.61 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.61 | -0.39 | winkler |
| Chardonnay (Chardonnay) | 0.61 | -0.39 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.99 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.79 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.26 | -0.74 | winkler |
| Zöld veltelíni (Grüner Veltliner) | 0.35 | -0.65 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.63 | -0.37 | winkler |
| Királyleányka (Kiralyleanyka) | 0.63 | -0.37 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.74 | -0.26 | winkler |
| Chardonnay (Chardonnay) | 0.74 | -0.26 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.99 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.79 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Sauvignon blanc (Sauvignon Blanc) | 0.00 | -1.00 | winkler |
| Zöld veltelíni (Grüner Veltliner) | 0.00 | -1.00 | winkler |
| Királyleányka (Kiralyleanyka) | 0.00 | -1.00 | winkler |
| Pinot noir (Pinot Noir) | 0.00 | -1.00 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.07 | -0.93 | winkler |
| Chardonnay (Chardonnay) | 0.07 | -0.93 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.84 | +0.84 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.84 | +0.84 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.84 | +0.83 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.84 | +0.63 | medium | new |

---

## Hajós-Bajai (Duna)

**Current principal varieties (1991–2020 observed):** Kékfrankos (1.00), Olaszrizling (0.93), Chardonnay (0.93), Kadarka (0.64), Cabernet sauvignon (0.48)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.69 | -0.31 | heat |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.69 | -0.24 | heat |
| Chardonnay (Chardonnay) | 0.69 | -0.24 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sangiovese** | Sangiovese | red | 0.88 | +0.18 | high | new |
| 2 | **Vermentino** | Vermentino | white | 0.88 | +0.18 | medium | new |
| 3 | **Fiano** | Fiano | white | 0.88 | +0.18 | medium | new |
| 4 | **Verdejo** | Verdejo | white | 0.88 | +0.18 | medium | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sangiovese** | Sangiovese | red | 1.00 | +0.30 | high | new |
| 2 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 0.94 | +0.46 | high | expand |
| 3 | **Syrah** | Syrah | red | 0.94 | +0.46 | high | new |
| 4 | **Vermentino** | Vermentino | white | 1.00 | +0.30 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.50 | -0.50 | heat |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.50 | -0.44 | heat |
| Chardonnay (Chardonnay) | 0.50 | -0.44 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 0.92 | +0.45 | medium | new |
| 2 | **Syrah** | Syrah | red | 0.81 | +0.33 | high | new |
| 3 | **Tempranillo** | Tempranillo | red | 0.81 | +0.33 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 0.81 | +0.33 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.52 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.52 | high | new |
| 3 | **Merlot** | Merlot | red | 1.00 | +0.36 | high | new |
| 4 | **Tempranillo** | Tempranillo | red | 1.00 | +0.52 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.31 | -0.69 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.31 | -0.62 | winkler |
| Chardonnay (Chardonnay) | 0.31 | -0.62 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.97 | +0.91 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.97 | +0.91 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.97 | +0.76 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.97 | +0.65 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.17 | -0.83 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.17 | -0.76 | winkler |
| Chardonnay (Chardonnay) | 0.17 | -0.76 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.90 | +0.85 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.90 | +0.85 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.90 | +0.69 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.90 | +0.58 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.40 | -0.60 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.40 | -0.53 | winkler |
| Chardonnay (Chardonnay) | 0.40 | -0.53 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.95 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.95 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.79 | medium | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.52 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.00 | -1.00 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.00 | -0.93 | winkler |
| Chardonnay (Chardonnay) | 0.00 | -0.93 | winkler |
| Kadarka (Kadarka) | 0.07 | -0.57 | winkler |
| Cabernet sauvignon (Cabernet Sauvignon) | 0.09 | -0.39 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.58 | +0.52 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.58 | +0.52 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.58 | +0.36 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.58 | +0.26 | medium | new |

---

## Kunsági (Duna)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Cserszegi fűszeres (1.00), Generosa (1.00), Bianca (1.00), Kékfrankos (1.00), Arany sárfehér (0.73), Kadarka (0.73)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sangiovese** | Sangiovese | red | 1.00 | +0.25 | high | new |
| 2 | **Vermentino** | Vermentino | white | 1.00 | +0.25 | medium | new |
| 3 | **Fiano** | Fiano | white | 1.00 | +0.25 | medium | new |
| 4 | **Verdejo** | Verdejo | white | 1.00 | +0.25 | medium | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.45 | high | new |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.45 | high | new |
| 3 | **Merlot** | Merlot | red | 1.00 | +0.27 | high | new |
| 4 | **Tempranillo** | Tempranillo | red | 1.00 | +0.45 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.56 | -0.44 | heat |
| Generosa (Generosa) | 0.56 | -0.44 | heat |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.63 | -0.37 | heat |
| Kékfrankos (Blaufränkisch) | 0.63 | -0.37 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Syrah** | Syrah | red | 0.96 | +0.42 | high | new |
| 2 | **Touriga Nacional** | Touriga Nacional | red | 0.99 | +0.44 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 0.96 | +0.42 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 0.96 | +0.42 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.45 | high | new |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.45 | high | new |
| 3 | **Merlot** | Merlot | red | 1.00 | +0.27 | high | new |
| 4 | **Tempranillo** | Tempranillo | red | 1.00 | +0.45 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.36 | -0.64 | winkler |
| Generosa (Generosa) | 0.36 | -0.64 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.43 | -0.57 | winkler |
| Kékfrankos (Blaufränkisch) | 0.43 | -0.57 | winkler |
| Bianca (Bianca) | 0.57 | -0.43 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.96 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.96 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.78 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.64 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.22 | -0.78 | winkler |
| Generosa (Generosa) | 0.22 | -0.78 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.28 | -0.72 | winkler |
| Kékfrankos (Blaufränkisch) | 0.28 | -0.72 | winkler |
| Bianca (Bianca) | 0.39 | -0.61 | winkler |
| Arany sárfehér (Arany sarfeher) | 0.39 | -0.34 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.96 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.96 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.78 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.64 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.41 | -0.59 | winkler |
| Generosa (Generosa) | 0.41 | -0.59 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.49 | -0.51 | winkler |
| Kékfrankos (Blaufränkisch) | 0.49 | -0.51 | winkler |
| Bianca (Bianca) | 0.60 | -0.40 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.96 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.96 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.78 | medium | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.45 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Olaszrizling (Welschriesling / Olaszrizling) | 0.00 | -1.00 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.00 | -1.00 | winkler |
| Generosa (Generosa) | 0.00 | -1.00 | winkler |
| Kékfrankos (Blaufränkisch) | 0.00 | -1.00 | winkler |
| Bianca (Bianca) | 0.05 | -0.95 | winkler |
| Arany sárfehér (Arany sarfeher) | 0.05 | -0.68 | winkler |
| Kadarka (Kadarka) | 0.10 | -0.62 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.64 | +0.60 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.64 | +0.60 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.64 | +0.42 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.64 | +0.28 | medium | new |

---

## Mátrai (Felső-Magyarországi)

**Current principal varieties (1991–2020 observed):** Rizlingszilváni (0.97), Tramini (0.97), Olaszrizling (0.67), Sauvignon blanc (0.67), Chardonnay (0.67), Cserszegi fűszeres (0.67), Hárslevelű (0.31)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Pinot blanc** | Pinot Blanc | white | 0.94 | -0.03 | high | new |
| 2 | **Zöld veltelíni** | Grüner Veltliner | white | 0.94 | -0.03 | high | new |
| 3 | **Kékfrankos** | Blaufränkisch | red | 0.94 | -0.03 | high | new |
| 4 | **Zweigelt** | Zweigelt | red | 0.94 | -0.03 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Rajnai rizling** | Riesling | white | 1.00 | +0.03 | high | new |
| 2 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.03 | high | expand |
| 3 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.03 | high | new |
| 4 | **Tramini** | Gewürztraminer | white | 1.00 | +0.03 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.52 | -0.45 | winkler |
| Tramini (Gewürztraminer) | 0.52 | -0.45 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Kékfrankos** | Blaufränkisch | red | 1.00 | +0.03 | high | new |
| 2 | **Zweigelt** | Zweigelt | red | 1.00 | +0.03 | high | new |
| 3 | **Fiano** | Fiano | white | 0.90 | +0.61 | medium | new |
| 4 | **Sangiovese** | Sangiovese | red | 0.90 | +0.40 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.69 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.69 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.69 | medium | expand |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.69 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.58 | -0.39 | winkler |
| Tramini (Gewürztraminer) | 0.59 | -0.38 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.98 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.98 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.77 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.77 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.19 | -0.78 | winkler |
| Tramini (Gewürztraminer) | 0.21 | -0.76 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.99 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.54 | -0.42 | winkler |
| Tramini (Gewürztraminer) | 0.56 | -0.41 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.98 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.98 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.77 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.77 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rizlingszilváni (Müller-Thurgau) | 0.00 | -0.97 | winkler |
| Tramini (Gewürztraminer) | 0.00 | -0.97 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.07 | -0.60 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.19 | -0.48 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.24 | -0.43 | winkler |
| Chardonnay (Chardonnay) | 0.24 | -0.43 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 0.99 | +0.99 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.99 | +0.99 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 0.99 | +0.99 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.99 | +0.98 | medium | new |

---

## Móri (Felső-Pannon)

**Current principal varieties (1991–2020 observed):** Rajnai rizling (1.00), Tramini (1.00), Chardonnay (0.90), Leányka (0.90), Ezerjó (0.61)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | expand |
| 2 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 3 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 4 | **Tramini** | Gewürztraminer | white | 1.00 | +0.00 | high | expand |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.10 | high | new |
| 2 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.10 | high | new |
| 3 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.10 | high | new |
| 4 | **Chardonnay** | Chardonnay | white | 1.00 | +0.10 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 0.97 | +0.36 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.10 | high | new |
| 3 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.10 | high | new |
| 4 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.10 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.39 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.39 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.39 | medium | new |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.39 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.99 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.98 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.62 | -0.38 | winkler |
| Tramini (Gewürztraminer) | 0.62 | -0.38 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.99 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.98 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.99 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.98 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.05 | -0.95 | winkler |
| Tramini (Gewürztraminer) | 0.05 | -0.95 | winkler |
| Leányka (Leanyka) | 0.29 | -0.61 | winkler |
| Chardonnay (Chardonnay) | 0.50 | -0.40 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |

---

## Nagy-Somlói (Balaton)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Tramini (1.00), Furmint (0.80), Hárslevelű (0.80), Juhfark (0.80)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 0.99 | +0.19 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.00 | high | new |
| 4 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.20 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.65 | -0.35 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.86 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.86 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.20 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.60 | -0.40 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.86 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.86 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.21 | -0.79 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.91 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.63 | -0.37 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.86 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.86 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.00 | -1.00 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.28 | -0.72 | winkler |
| Hárslevelű (Harslevelu) | 0.28 | -0.52 | winkler |
| Juhfark (Juhfark) | 0.28 | -0.52 | winkler |
| Furmint (Furmint) | 0.52 | -0.28 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.91 | medium | new |

---

## Neszmélyi (Felső-Pannon)

**Current principal varieties (1991–2020 observed):** Irsai Olivér (1.00), Olaszrizling (0.86), Sauvignon blanc (0.86), Chardonnay (0.86), Cserszegi fűszeres (0.86), Királyleányka (0.86)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Pinot blanc** | Pinot Blanc | white | 1.00 | +0.00 | high | new |
| 2 | **Zöld veltelíni** | Grüner Veltliner | white | 1.00 | +0.00 | high | new |
| 3 | **Kékfrankos** | Blaufränkisch | red | 1.00 | +0.00 | high | new |
| 4 | **Zweigelt** | Zweigelt | red | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.14 | high | expand |
| 2 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.14 | high | new |
| 3 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.14 | high | expand |
| 4 | **Chardonnay** | Chardonnay | white | 1.00 | +0.14 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Irsai Olivér (Irsai Oliver) | 0.57 | -0.43 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Fiano** | Fiano | white | 1.00 | +0.70 | medium | new |
| 2 | **Touriga Nacional** | Touriga Nacional | red | 0.93 | +0.93 | medium | new |
| 3 | **Aglianico** | Aglianico | red | 0.93 | +0.93 | medium | new |
| 4 | **Sangiovese** | Sangiovese | red | 1.00 | +0.37 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.45 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.45 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.45 | medium | new |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.45 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Irsai Olivér (Irsai Oliver) | 0.55 | -0.45 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.80 | medium | new |
| 4 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.60 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Irsai Olivér (Irsai Oliver) | 0.26 | -0.74 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.66 | -0.20 | winkler |
| Királyleányka (Kiralyleanyka) | 0.66 | -0.20 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Irsai Olivér (Irsai Oliver) | 0.61 | -0.39 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +1.00 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.80 | medium | new |
| 4 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.60 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Irsai Olivér (Irsai Oliver) | 0.00 | -1.00 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.09 | -0.78 | winkler |
| Királyleányka (Kiralyleanyka) | 0.09 | -0.78 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.22 | -0.65 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.27 | -0.59 | winkler |
| Chardonnay (Chardonnay) | 0.27 | -0.59 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +1.00 | medium | new |
| 2 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 3 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 4 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |

---

## Pannonhalmi (Felső-Pannon)

**Current principal varieties (1991–2020 observed):** Rajnai rizling (1.00), Tramini (1.00), Olaszrizling (0.97), Sauvignon blanc (0.97), Chardonnay (0.97), Királyleányka (0.97)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.03 | high | expand |
| 2 | **Szürkebarát** | Pinot gris | white | 1.00 | +0.03 | high | new |
| 3 | **Sauvignon blanc** | Sauvignon Blanc | white | 1.00 | +0.03 | high | expand |
| 4 | **Chardonnay** | Chardonnay | white | 1.00 | +0.03 | high | expand |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.31 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.31 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.31 | medium | new |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.31 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.55 | -0.45 | winkler |
| Tramini (Gewürztraminer) | 0.55 | -0.45 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.87 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.87 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.48 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.48 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.31 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.31 | medium | new |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.31 | medium | new |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.31 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.48 | -0.52 | winkler |
| Tramini (Gewürztraminer) | 0.48 | -0.52 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.87 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.87 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.48 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.48 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.19 | -0.81 | winkler |
| Tramini (Gewürztraminer) | 0.19 | -0.81 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.53 | -0.44 | winkler |
| Királyleányka (Kiralyleanyka) | 0.53 | -0.44 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.74 | -0.23 | winkler |
| Chardonnay (Chardonnay) | 0.74 | -0.23 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.91 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.53 | -0.47 | winkler |
| Tramini (Gewürztraminer) | 0.53 | -0.47 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.87 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.87 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.48 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.48 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.00 | -1.00 | winkler |
| Tramini (Gewürztraminer) | 0.00 | -1.00 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.06 | -0.92 | winkler |
| Királyleányka (Kiralyleanyka) | 0.06 | -0.92 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.23 | -0.75 | winkler |
| Chardonnay (Chardonnay) | 0.23 | -0.75 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 0.97 | +0.97 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.97 | +0.97 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 0.97 | +0.97 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.97 | +0.88 | medium | new |

---

## Pécsi (Pannon)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Chardonnay (1.00), Pinot blanc (1.00), Kékfrankos (1.00), Cirfandli (0.88), Cabernet sauvignon (0.66)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.67 | -0.33 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.62 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.62 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.34 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.34 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.62 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.62 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.34 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.34 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.59 | -0.41 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.62 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.62 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.34 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.34 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.62 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.62 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.34 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.34 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.58 | -0.42 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.62 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.62 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.34 | high | expand |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.34 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.18 | -0.82 | winkler |
| Cirfandli (Zierfandler) | 0.34 | -0.54 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.55 | -0.45 | winkler |
| Chardonnay (Chardonnay) | 0.55 | -0.45 | winkler |
| Kékfrankos (Blaufränkisch) | 0.55 | -0.45 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.97 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.97 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.36 | -0.64 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.75 | -0.25 | winkler |
| Chardonnay (Chardonnay) | 0.75 | -0.25 | winkler |
| Kékfrankos (Blaufränkisch) | 0.75 | -0.25 | winkler |
| Cirfandli (Zierfandler) | 0.65 | -0.23 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.97 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.97 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot blanc (Pinot Blanc) | 0.01 | -0.99 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.12 | -0.88 | winkler |
| Chardonnay (Chardonnay) | 0.12 | -0.88 | winkler |
| Kékfrankos (Blaufränkisch) | 0.12 | -0.88 | winkler |
| Cirfandli (Zierfandler) | 0.02 | -0.86 | winkler |
| Cabernet sauvignon (Cabernet Sauvignon) | 0.42 | -0.24 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.95 | +0.95 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.95 | +0.95 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.95 | +0.92 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 0.95 | +0.92 | low | new |

---

## Soproni (Felső-Pannon)

**Current principal varieties (1991–2020 observed):** Sauvignon blanc (1.00), Zöld veltelíni (1.00), Kékfrankos (1.00), Zweigelt (1.00), Merlot (0.93), Cabernet sauvignon (0.70)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.07 | high | expand |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | new |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.07 | high | expand |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | new |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.96 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.96 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.61 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.58 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.07 | high | expand |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | new |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.96 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.96 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.61 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.58 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.39 | -0.61 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.69 | -0.31 | winkler |
| Kékfrankos (Blaufränkisch) | 0.75 | -0.25 | winkler |
| Zweigelt (Zweigelt) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.97 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.67 | -0.33 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.96 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.96 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.61 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.58 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Zöld veltelíni (Grüner Veltliner) | 0.12 | -0.88 | winkler |
| Sauvignon blanc (Sauvignon Blanc) | 0.23 | -0.77 | winkler |
| Kékfrankos (Blaufränkisch) | 0.43 | -0.57 | winkler |
| Zweigelt (Zweigelt) | 0.43 | -0.57 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.97 | medium | new |

---

## Szekszárdi (Pannon)

**Current principal varieties (1991–2020 observed):** Kékfrankos (1.00), Cabernet franc (0.96), Kadarka (0.67), Merlot (0.67), Cabernet sauvignon (0.50), Syrah (0.50)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.75 | -0.25 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sangiovese** | Sangiovese | red | 0.93 | +0.21 | high | new |
| 2 | **Vermentino** | Vermentino | white | 0.93 | +0.21 | medium | new |
| 3 | **Fiano** | Fiano | white | 0.93 | +0.21 | medium | new |
| 4 | **Verdejo** | Verdejo | white | 0.93 | +0.21 | medium | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 0.97 | +0.47 | high | expand |
| 2 | **Syrah** | Syrah | red | 0.97 | +0.47 | high | expand |
| 3 | **Sangiovese** | Sangiovese | red | 1.00 | +0.28 | high | new |
| 4 | **Merlot** | Merlot | red | 0.97 | +0.30 | high | expand |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.54 | -0.46 | heat |
| Cabernet franc (Cabernet Franc) | 0.75 | -0.20 | heat |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 0.94 | +0.44 | medium | new |
| 2 | **Syrah** | Syrah | red | 0.86 | +0.35 | high | expand |
| 3 | **Tempranillo** | Tempranillo | red | 0.86 | +0.35 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 0.86 | +0.35 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.50 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.50 | high | expand |
| 3 | **Merlot** | Merlot | red | 1.00 | +0.33 | high | expand |
| 4 | **Tempranillo** | Tempranillo | red | 1.00 | +0.50 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.36 | -0.64 | winkler |
| Cabernet franc (Cabernet Franc) | 0.55 | -0.41 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.93 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.93 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.76 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.66 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.12 | -0.88 | winkler |
| Cabernet franc (Cabernet Franc) | 0.23 | -0.72 | winkler |
| Kadarka (Kadarka) | 0.35 | -0.32 | winkler |
| Merlot (Merlot) | 0.35 | -0.32 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.90 | +0.83 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.90 | +0.83 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.90 | +0.67 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.90 | +0.57 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.43 | -0.57 | winkler |
| Cabernet franc (Cabernet Franc) | 0.63 | -0.32 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +0.93 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +0.93 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.76 | medium | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.50 | high | expand |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Kékfrankos (Blaufränkisch) | 0.00 | -1.00 | winkler |
| Cabernet franc (Cabernet Franc) | 0.03 | -0.93 | winkler |
| Kadarka (Kadarka) | 0.04 | -0.63 | winkler |
| Merlot (Merlot) | 0.04 | -0.63 | winkler |
| Cabernet sauvignon (Cabernet Sauvignon) | 0.05 | -0.45 | winkler |
| Syrah (Syrah) | 0.17 | -0.34 | winkler |

*No varieties meet the future-suitability floor (0.55) under this scenario.* This usually means the climate has moved outside the envelope of every variety currently in the dataset — consider consulting Mediterranean/southern-Iberian variety envelopes not yet in `grape_envelopes.csv`.

---

## Tokaji (Tokaj)

**Current principal varieties (1991–2020 observed):** Furmint (0.73), Hárslevelű (0.73), Sárgamuskotály (0.73), Kabar (0.73), Zéta (0.73), Kövérszőlő (0.73)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | new |
| 2 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 3 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |
| 4 | **Müller-Thurgau** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.27 | high | new |
| 2 | **Furmint** | Furmint | white | 1.00 | +0.27 | medium | expand |
| 3 | **Hárslevelű** | Harslevelu | white | 1.00 | +0.27 | medium | expand |
| 4 | **Kadarka** | Kadarka | red | 1.00 | +0.27 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 0.96 | +0.85 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 0.96 | +0.85 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 0.96 | +0.42 | high | new |
| 4 | **Syrah** | Syrah | red | 0.96 | +0.42 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.45 | high | new |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.45 | high | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.61 | medium | new |
| 4 | **Merlot** | Merlot | red | 1.00 | +0.27 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.88 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.88 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.45 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.45 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.92 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.88 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.88 | medium | new |
| 3 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.45 | high | new |
| 4 | **Syrah** | Syrah | red | 1.00 | +0.45 | high | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Hárslevelű (Harslevelu) | 0.17 | -0.56 | winkler |
| Kabar (Kabar) | 0.17 | -0.56 | winkler |
| Zéta (Zeta) | 0.17 | -0.56 | winkler |
| Kövérszőlő (Koverszolo) | 0.17 | -0.56 | winkler |
| Sárgamuskotály (Yellow Muscat / Muscat Lunel) | 0.21 | -0.52 | winkler |
| Furmint (Furmint) | 0.32 | -0.40 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.92 | medium | new |

---

## Tolnai (Pannon)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Rajnai rizling (1.00), Chardonnay (1.00), Kékfrankos (1.00), Merlot (0.80), Cabernet sauvignon (0.60)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.34 | -0.66 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.50 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.50 | medium | new |

### Near term (2021–2040) — 2021-2040 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.50 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.50 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.17 | -0.83 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.50 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.50 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.68 | -0.32 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.50 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.50 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.16 | -0.84 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.40 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.40 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.50 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.50 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.00 | -1.00 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.39 | -0.61 | winkler |
| Chardonnay (Chardonnay) | 0.39 | -0.61 | winkler |
| Kékfrankos (Blaufränkisch) | 0.39 | -0.61 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.86 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.86 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.16 | -0.84 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.68 | -0.32 | winkler |
| Chardonnay (Chardonnay) | 0.68 | -0.32 | winkler |
| Kékfrankos (Blaufränkisch) | 0.68 | -0.32 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.86 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 1.00 | +0.86 | low | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Rajnai rizling (Riesling) | 0.00 | -1.00 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.03 | -0.97 | winkler |
| Chardonnay (Chardonnay) | 0.03 | -0.97 | winkler |
| Kékfrankos (Blaufränkisch) | 0.03 | -0.97 | winkler |
| Merlot (Merlot) | 0.19 | -0.61 | winkler |
| Cabernet sauvignon (Cabernet Sauvignon) | 0.23 | -0.37 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.76 | +0.76 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.76 | +0.76 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.76 | +0.62 | medium | new |
| 4 | **Carignan** | Carignan / Mazuelo | red | 0.76 | +0.62 | low | new |

---

## Villányi (Pannon)

**Current principal varieties (1991–2020 observed):** Kékfrankos (1.00), Cabernet franc (1.00), Pinot noir (1.00), Portugieser (1.00), Merlot (0.79), Cabernet sauvignon (0.59)

### Near term (2021–2040) — 2021-2040 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.32 | -0.68 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sangiovese** | Sangiovese | red | 1.00 | +0.25 | high | new |
| 2 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 0.96 | +0.37 | high | expand |
| 3 | **Syrah** | Syrah | red | 0.96 | +0.37 | high | new |
| 4 | **Touriga Nacional** | Touriga Nacional | red | 0.96 | +0.48 | medium | new |

### Near term (2021–2040) — 2021-2040 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.41 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.41 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.52 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.52 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.16 | -0.84 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.41 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.41 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.52 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.52 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Cabernet sauvignon** | Cabernet Sauvignon | red | 1.00 | +0.41 | high | expand |
| 2 | **Syrah** | Syrah | red | 1.00 | +0.41 | high | new |
| 3 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.52 | medium | new |
| 4 | **Aglianico** | Aglianico | red | 1.00 | +0.52 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.16 | -0.84 | winkler |
| Kékfrankos (Blaufränkisch) | 0.70 | -0.30 | winkler |
| Portugieser (Portugieser / Kékoportó) | 0.70 | -0.30 | winkler |
| Cabernet franc (Cabernet Franc) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.88 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.68 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.01 | -0.99 | winkler |
| Kékfrankos (Blaufränkisch) | 0.40 | -0.60 | winkler |
| Portugieser (Portugieser / Kékoportó) | 0.40 | -0.60 | winkler |
| Cabernet franc (Cabernet Franc) | 0.60 | -0.40 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.88 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.68 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.24 | -0.76 | winkler |
| Kékfrankos (Blaufränkisch) | 0.70 | -0.30 | winkler |
| Portugieser (Portugieser / Kékoportó) | 0.70 | -0.30 | winkler |
| Cabernet franc (Cabernet Franc) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 3 | **Garnacha** | Grenache | red | 1.00 | +0.88 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.68 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Pinot noir (Pinot Noir) | 0.00 | -1.00 | winkler |
| Kékfrankos (Blaufränkisch) | 0.07 | -0.93 | winkler |
| Portugieser (Portugieser / Kékoportó) | 0.07 | -0.93 | winkler |
| Cabernet franc (Cabernet Franc) | 0.17 | -0.83 | winkler |
| Merlot (Merlot) | 0.25 | -0.54 | winkler |
| Cabernet sauvignon (Cabernet Sauvignon) | 0.31 | -0.29 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Mourvèdre** | Mourvèdre / Monastrell | red | 0.85 | +0.85 | medium | new |
| 2 | **Nero d'Avola** | Nero d'Avola | red | 0.85 | +0.85 | medium | new |
| 3 | **Garnacha** | Grenache | red | 0.85 | +0.72 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 0.85 | +0.53 | medium | new |

---

## Zalai (Balaton)

**Current principal varieties (1991–2020 observed):** Olaszrizling (1.00), Tramini (1.00), Chardonnay (1.00), Cserszegi fűszeres (1.00), Királyleányka (1.00)

### Near term (2021–2040) — 2021-2040 RCP45

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.06 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### Near term (2021–2040) — 2021-2040 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.06 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.90 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.90 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.54 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.52 | medium | new |

### ≈ +20y (2041–2060) — 2041-2060 RCP85

*No principal varieties cross the at-risk threshold under this scenario.*

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Merlot** | Merlot | red | 1.00 | +0.06 | high | new |
| 2 | **Olaszrizling** | Welschriesling / Olaszrizling | white | 1.00 | +0.00 | high | expand |
| 3 | **Rajnai rizling** | Riesling | white | 1.00 | +0.00 | high | new |
| 4 | **Rizlingszilváni** | Müller-Thurgau | white | 1.00 | +0.00 | high | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.74 | -0.26 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.90 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.90 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.54 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.52 | medium | new |

### ≈ +40y (2061–2080) — 2061-2080 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.26 | -0.74 | winkler |
| Királyleányka (Kiralyleanyka) | 0.63 | -0.37 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.65 | -0.35 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.75 | -0.25 | winkler |
| Chardonnay (Chardonnay) | 0.75 | -0.25 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.93 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP45

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.66 | -0.34 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Touriga Nacional** | Touriga Nacional | red | 1.00 | +0.90 | medium | new |
| 2 | **Aglianico** | Aglianico | red | 1.00 | +0.90 | medium | new |
| 3 | **Tempranillo** | Tempranillo | red | 1.00 | +0.54 | medium | new |
| 4 | **Fiano** | Fiano | white | 1.00 | +0.52 | medium | new |

### ≈ +60y (2081–2100) — 2081-2100 RCP85

**At-risk current varieties:**

| Variety | Future suitability | Δ vs 1991–2020 | Limiting factor |
|---|---|---|---|
| Tramini (Gewürztraminer) | 0.01 | -0.99 | winkler |
| Királyleányka (Kiralyleanyka) | 0.19 | -0.81 | winkler |
| Cserszegi fűszeres (Cserszegi fuszeres) | 0.30 | -0.70 | winkler |
| Olaszrizling (Welschriesling / Olaszrizling) | 0.38 | -0.62 | winkler |
| Chardonnay (Chardonnay) | 0.38 | -0.62 | winkler |

**Top 4 replacement candidates:**

| # | Variety | EN | Colour | Future suit. | Δ vs current | Conf. | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Garnacha** | Grenache | red | 1.00 | +1.00 | medium | new |
| 2 | **Mourvèdre** | Mourvèdre / Monastrell | red | 1.00 | +1.00 | medium | new |
| 3 | **Nero d'Avola** | Nero d'Avola | red | 1.00 | +1.00 | medium | new |
| 4 | **Assyrtiko** | Assyrtiko | white | 1.00 | +0.93 | medium | new |

---

## Hungary-wide climate-adapted variety rankings

Varieties ranked by the number of (district × horizon) slots in which they were recommended as a top-4 replacement:

| Variety | EN | Colour | Slots recommended |
|---|---|---|---|
| **Touriga Nacional** | Touriga Nacional | red | 71 |
| **Aglianico** | Aglianico | red | 68 |
| **Syrah** | Syrah | red | 60 |
| **Garnacha** | Grenache | red | 56 |
| **Cabernet sauvignon** | Cabernet Sauvignon | red | 56 |
| **Mourvèdre** | Mourvèdre / Monastrell | red | 56 |
| **Nero d'Avola** | Nero d'Avola | red | 50 |
| **Assyrtiko** | Assyrtiko | white | 33 |
| **Merlot** | Merlot | red | 29 |
| **Tempranillo** | Tempranillo | red | 28 |
| **Olaszrizling** | Welschriesling / Olaszrizling | white | 23 |
| **Fiano** | Fiano | white | 22 |
| **Rizlingszilváni** | Müller-Thurgau | white | 19 |
| **Rajnai rizling** | Riesling | white | 19 |
| **Carignan** | Carignan / Mazuelo | red | 13 |

### Top 5 replacements per horizon (Hungary-wide)

**Near term (2021–2040) — 2021-2040 RCP45**
- Rizlingszilváni (Müller-Thurgau, white) — 8/22 districts
- Rajnai rizling (Riesling, white) — 8/22 districts
- Olaszrizling (Welschriesling / Olaszrizling, white) — 7/22 districts
- Cabernet sauvignon (Cabernet Sauvignon, red) — 6/22 districts
- Touriga Nacional (Touriga Nacional, red) — 6/22 districts

**Near term (2021–2040) — 2021-2040 RCP85**
- Syrah (Syrah, red) — 10/22 districts
- Cabernet sauvignon (Cabernet Sauvignon, red) — 10/22 districts
- Olaszrizling (Welschriesling / Olaszrizling, white) — 9/22 districts
- Merlot (Merlot, red) — 9/22 districts
- Aglianico (Aglianico, red) — 6/22 districts

**≈ +20y (2041–2060) — 2041-2060 RCP45**
- Aglianico (Aglianico, red) — 16/22 districts
- Touriga Nacional (Touriga Nacional, red) — 16/22 districts
- Syrah (Syrah, red) — 13/22 districts
- Cabernet sauvignon (Cabernet Sauvignon, red) — 10/22 districts
- Fiano (Fiano, white) — 7/22 districts

**≈ +20y (2041–2060) — 2041-2060 RCP85**
- Merlot (Merlot, red) — 15/22 districts
- Cabernet sauvignon (Cabernet Sauvignon, red) — 11/22 districts
- Syrah (Syrah, red) — 11/22 districts
- Furmint (Furmint, white) — 7/22 districts
- Hárslevelű (Harslevelu, white) — 6/22 districts

**≈ +40y (2061–2080) — 2061-2080 RCP45**
- Aglianico (Aglianico, red) — 16/22 districts
- Touriga Nacional (Touriga Nacional, red) — 16/22 districts
- Cabernet sauvignon (Cabernet Sauvignon, red) — 11/22 districts
- Syrah (Syrah, red) — 10/22 districts
- Garnacha (Grenache, red) — 6/22 districts

**≈ +40y (2061–2080) — 2061-2080 RCP85**
- Garnacha (Grenache, red) — 19/22 districts
- Mourvèdre (Mourvèdre / Monastrell, red) — 19/22 districts
- Nero d'Avola (Nero d'Avola, red) — 17/22 districts
- Assyrtiko (Assyrtiko, white) — 13/22 districts
- Aglianico (Aglianico, red) — 5/22 districts

**≈ +60y (2081–2100) — 2081-2100 RCP45**
- Aglianico (Aglianico, red) — 12/22 districts
- Touriga Nacional (Touriga Nacional, red) — 12/22 districts
- Garnacha (Grenache, red) — 10/22 districts
- Mourvèdre (Mourvèdre / Monastrell, red) — 10/22 districts
- Nero d'Avola (Nero d'Avola, red) — 10/22 districts

**≈ +60y (2081–2100) — 2081-2100 RCP85**
- Garnacha (Grenache, red) — 20/22 districts
- Mourvèdre (Mourvèdre / Monastrell, red) — 20/22 districts
- Nero d'Avola (Nero d'Avola, red) — 16/22 districts
- Assyrtiko (Assyrtiko, white) — 11/22 districts
- Touriga Nacional (Touriga Nacional, red) — 5/22 districts
