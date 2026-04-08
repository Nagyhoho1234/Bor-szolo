# Threats verification — main-thread WebSearch findings

## Flavescence dorée (FD) — verified facts

**First Hungarian detection:** August 2013, southwest Hungary (likely Zalai
borvidék, around Zalaszentgrót).
- Source: 2025 wine industry coverage, e.g.
  https://www.vinetur.com/en/2025122294408/flavescence-doree-hits-21-of-22-hungarian-wine-regions-threatening-270-million-liter-industry.html

**2025 status:** Confirmed in 21 of 22 Hungarian wine regions including Tokaj,
Eger, Zala, Pannonhalma. Sources do NOT explicitly identify which one of the
22 borvidék remains free of confirmed cases — leave that field blank in the
timeline CSV rather than guess.
- Sources:
  - https://magazine.wein.plus/news/gold-yellow-yellowing-is-taking-on-massive-proportions-in-hungary-21-out-of-22-growing-regions-are-threatened
  - https://thegrapereset.com/bites/phytoplasma-disease-threatens-the-heart-of-hungarian-wine-country
  - https://trademagazin.hu/en/mar-a-pannonhalmi-borvideken-is-megjelent-a-szolo-aranyszinu-sargasag-betegsege/
  - https://www.vinetur.com/en/2025122294408/...

**Government response:** ~3.8 BHUF (~USD 11M) emergency aid package
allocated to inspections, pesticide programs, and grower compensation; >200
inspection teams deployed.

**Quote (2025):** Winemaker Dorottya Bussay: "From next year, we won't have a
single vine left; we'll have to uproot everything."

**Vector:** *Scaphoideus titanus* (American grapevine leafhopper). Climate
linkage: warmer winters increase overwintering survival.

## Variety envelope facts confirmed

**Kékfrankos / Blaufränkisch:** vigorous, early budding, late ripening; needs
relatively warm climate. Hungarian sites are ~1 °C warmer than Austrian
Burgenland on average → fuller riper Hungarian Kékfrankos.
- Source: https://winencsy.com/blaufrankisch-or-kekfrankos-what-is-the-difference/

**Eger wine region Huglin classification (Tonietto & Carbonneau 2004):** falls
in **HI−1 Temperate to HI+1 Temperate-warm** band.
- Source: https://ives-openscience.eu/wp-content/uploads/2020/07/B-lo-et-al_Focus-on-Terroir-Studies.pdf

**Furmint:** late-ripening; dry-wine harvest in September; sweet aszú harvest
mid-October or later. Tokaj microclimate: bitter cold winters, cool dry
springs, hot summers, long Indian summer ripening.
- Source: https://en.wikipedia.org/wiki/Furmint

## To do in polish pass

- Update `flavescence_doree_timeline.csv` row for first detection (year 2013, district Zalai, status `phytoplasma_detected`)
- Update 2025 row to NOT name the unaffected district
- Verify the Frontiers 2025 paper's specific claim of GDD per-decade trends per district
- Verify EU Pesticides Database approval/expiry dates for the 25 listed actives (lower priority)
- Verify 2017 Tokaj trunk disease prevalence numbers (lower priority)
