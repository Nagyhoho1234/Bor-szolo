# Threats Dataset — Hungarian Wine District Climate & Biotic Susceptibility

Curated CSVs feeding the "threats" section of the public wine-investor information site.
All files UTF-8, comma-separated, Hungarian district names preserved.

## Verification status — 2026-04-07 (re-verified Wave 11C, pesticides cleared Wave 11D)

This dataset was source-verified on **2026-04-07** using WebSearch against
primary regulatory and scientific sources. Each row now carries a
`verification_status` column with one of: `verified` / `partial` / `unverified`,
plus a `last_verified_date` column on `eu_pesticides_actives.csv`.

| File | Rows | Verified | Partial | Unverified |
|---|---|---|---|---|
| flavescence_doree_timeline.csv | 10 | 10 | 0 | 0 |
| trunk_diseases.csv | 8 | 3 | 5 | 0 |
| pest_disease_regulatory.csv | 26 | 19 | 7 | 0 |
| eu_pesticides_actives.csv | 28 | 26 | 2 | 0 |

Wave 11D (2026-04-07) cleared 12 of the 14 previously `partial` rows in
`eu_pesticides_actives.csv` by cross-referencing EUR-Lex Implementing
Regulations directly (rather than the JS-only EU Pesticides Database UI).
Notable updates: metrafenone renewed to 31 October 2039 (Reg 2024/2390),
spinosad renewed effective 1 April 2026 (Reg 2026/351), spirotetramat
moved to `not_approved` (approval expired 30 April 2024), and exact
initial-approval dates added for boscalid, fluxapyroxad, tebuconazole,
difenoconazole, cyflufenamid, deltamethrin, dithianon and Bt strains.
Sulphur and kaolin remain `partial` because no single primary source
gave the *current* expiry date with full confidence.

Wave 11C cleared the four previously fully-unverified threats rows
(2024 April frost, 2023 hail, black foot disease, Petri disease) to
`verified` or `partial` using Hungarian-language sources (HNT 2024 sectoral
report, NAK Országos Jégkármérséklő Rendszer reports, the 2003–2005
Phytopathol. Mediterr. HU multi-region trunk-disease survey).

`verified` = the row's key facts (year, regulation number, prevalence figure,
or status code) have been confirmed against the cited primary source.
`partial` = the substantive claim is correct but some secondary fields (exact
expiry date, prevalence percent, district list) could not be confirmed from
the public web without direct EU Pesticides Database UI access.
`unverified` = the row remains a domain-knowledge stub.

## Most-cited primary sources

1. **EPPO Global Database** — `gd.eppo.int`
   - Article 265: First record of *Scaphoideus titanus* in Hungary (2006)
   - Article 2673: First record of FD in Hungary (Lenti, Kerkateskánd, Zala, August 2013)
2. **EUR-Lex** — Commission Implementing Regulations:
   - 2018/1981 (copper compounds)
   - 2020/2087 (mancozeb non-renewal)
   - 2018/783, 2018/784, 2018/785 (neonicotinoid outdoor bans)
   - 2018/113 (acetamiprid renewal)
   - 2020/18 (chlorpyrifos non-renewal)
   - 2019/1090 (dimethoate non-renewal)
   - 2023/2660 (glyphosate re-approval)
3. **Phytoparasitica 45:21–32 (2017)** — Kovács et al., Tokaj GTD survey
   (Diplodia seriata 50–100% incidence).
4. **Phytopathol. Mediterr. 46:91–95 (2007)** — 2003–2005 esca survey across
   11 Hungarian wine regions.
5. **Trademagazin / NÉBIH press releases (2025)** — district-by-district FD
   confirmations during 2025 outbreak.
6. **Vinetur / The Grape Reset / wein.plus / Wine-Searcher (Oct–Dec 2025)** —
   coverage of "21 of 22 wine districts" announcement and 3.8 BHUF aid package.

## Key corrections from the previous draft

- **Scaphoideus titanus first record in Hungary: 2006**, not 2014 (EPPO
  Reporting Service Article 265). The vector was already in HU 7 years before
  the phytoplasma was first detected.
- **FD first detected in Hungary: end of August 2013** at Lenti and
  Kerkateskánd, Zala county — *not* 2018. EPPO Article 2673 is the
  authoritative source.
- **Diplodia seriata prevalence in Tokaj: 50–100%** in surveyed vineyards
  (Kovács et al. 2017) — was previously left blank.
- **Esca complex prevalence**: 34% of plantations in 2003–2005 HU survey,
  with 0.3–2.6% per-vine incidence; ALL vineyards over 12 years old affected.
- **Acetamiprid is renewed until 28 February 2033** (Reg 2018/113) — it is
  the *only* neonicotinoid still allowed outdoors in the EU and is the key
  remaining tool for Scaphoideus titanus / FD vector control.
- **Mancozeb expiry**: approval lapsed 4 January 2021, MS withdrawals by
  4 July 2021, final use-up grace period 4 January 2022 — three distinct
  dates, not a single 2022 cutoff.
- **Drosophila suzukii first HU record: 2012** near Táska (Somogy county).
- **Halyomorpha halys first HU record: 2013** in Budapest.

## Rows that could not be fully verified

- **The single FD-unaffected wine district (1 of 22)**: no consulted source
  named the unaffected district. Left unspecified rather than guessed.
- **2024 April frost** (Wave 11C update): now `verified` — affected districts
  per HNT 2024 ágazati gyorsjelentés are Eger, Mátra, Villány, Kunság,
  Hajós-Baja, Csongrád and parts of Dunántúl; ~5,000–6,000 ha total
  (~10% of HU vineyards), local damage up to 80%. National 2024 harvest fell
  to 3.73 Mq, the lowest in a decade.
- **2023 hail** (Wave 11C update): now `partial` — Országos Jégkármérséklő
  Rendszer (NAK) reports give national totals (30,678 ha all crops, 96 active
  generator-days) and name NW Balaton (late August) and Mád/Tokaji (July) as
  notable vineyard hail strikes, but no per-borvidék vineyard-only breakdown
  is published.
- **Black foot disease and Petri disease** (Wave 11C update): both now
  `partial` — the 2003–2005 Phytopathol. Mediterr. HU multi-region survey
  documents that on 2–4 year old vines, Cylindrocarpon sp., Phaeomoniella
  chlamydospora and Phaeoacremonium sp. were the most frequently isolated
  pathogens (i.e. the Petri/black foot complex is established in HU young
  plantings since 2003–2007). No subsequent black-foot–specific or
  Petri-specific Hungarian incidence study has been published; modern
  Dactylonectria-level molecular taxonomy is not yet covered in HU literature.
- **Sulphur and kaolin** in `eu_pesticides_actives.csv` remain `partial`
  after Wave 11D: sulphur's initial approval (Dir 2009/70/EC, 1 Jan 2010)
  and successive Reg 2017/555 / 2020/1511 / 2023/2592 extensions are
  confirmed, but the *current* expiry date is not pinned to a single
  primary source via WebSearch snippets. Kaolin (aluminium silicate /
  kaolin calcined) has an EFSA peer-review of renewal (EFSA Journal 7637,
  2022, RMS Greece) but the renewal Implementing Regulation has not been
  identified.

## Files

### `flavescence_doree_timeline.csv`
10 rows. Anchored on EPPO Reporting Service Articles 265 and 2673 plus the
2025 Trademagazin/NÉBIH district-by-district confirmations. The 2025 column
intentionally avoids guessing the single unaffected district.

### `trunk_diseases.csv`
8 rows. Esca and Botryosphaeria entries now carry hard prevalence numbers
from the 2017 Tokaj study and the 2003–2005 HU multi-region survey.

### `pest_disease_regulatory.csv`
26 rows. EU regulatory items (copper cap, mancozeb withdrawal, glyphosate
re-approval, neonicotinoid bans, chlorpyrifos, dimethoate, thiacloprid)
verified against EUR-Lex regulation numbers. First HU records added for
Drosophila suzukii (2012), Halyomorpha halys (2013), and S. titanus (2006).

### `eu_pesticides_actives.csv`
28 rows, 26 verified. After Wave 11D, all SDHI/DMI fungicides, the
pyrethroids, the spinosyn (spinosad, renewed 2026), the benzophenone
(metrafenone, renewed 2024), the dithiocarbamate alternative dithianon,
and the Bacillus thuringiensis biopesticide entry are pinned to specific
EUR-Lex Implementing Regulations. Spirotetramat was moved from
`approved` to `not_approved` (approval expired 30 April 2024 with no
renewal application). Sulphur and kaolin remain `partial`.
A `last_verified_date` column records the verification date per row.

## District name reference (Hungarian, UTF-8)
Badacsonyi, Balatonboglári, Balatonfüred-Csopaki, Balaton-felvidéki,
Nagy-Somlói, Zalai, Etyek-Budai, Móri, Neszmélyi, Pannonhalmi, Soproni,
Csongrádi, Hajós-Bajai, Kunsági, Bükki, Egri, Mátrai, Pécsi, Szekszárdi,
Tolnai, Villányi, Tokaji.
