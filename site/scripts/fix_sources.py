#!/usr/bin/env python3
"""Rewrite description JSONs with verified source titles + URLs."""
import json, glob, sys, shutil, os
sys.stdout.reconfigure(encoding='utf-8')

# URL -> verified title  (or tuple (new_url, title) if URL needs replacement)
TITLES = {
    "https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1481431/full":
        "Lakatos & Nagy 2025 — Temperature indices for Hungarian wine regions (Frontiers Plant Sci.)",
    "https://en.wikipedia.org/wiki/Badacsony_wine_region":
        "Badacsony wine region — Wikipedia",
    "https://tastehungary.com/journal/badacsony-pdo-a-guide-to-the-wine-region/":
        "Badacsony PDO: A Guide to the Wine Region — Taste Hungary",
    "https://winesofhungary.hu/grape-varieties/white-grape-varieties-white-wine-styles/keknyelu":
        "Kéknyelű grape variety — Wines of Hungary",
    "https://worldoffinewine.com/news-features/wine-hungary-keknyelu":
        "Kéknyelű: A late Lake Balaton comeback — World of Fine Wine",
    "https://winesofhungary.hu/wine-regio/balatonboglar-wine-district":
        ("https://winesofhungary.hu/wine-tourism/balatonboglar-wine-district",
         "Balatonboglár Wine District — Wines of Hungary"),
    "https://en.wikipedia.org/wiki/Balatonbogl%C3%A1r_wine_region":
        "Balatonboglár wine region — Wikipedia",
    "https://www.falstaff.com/en/regions/hungary-balatonboglar":
        "Wine Region Balatonboglár — Falstaff",
    "https://tastehungary.com/journal/lake-balaton-pgi-a-guide-to-the-wine-region/":
        "Lake Balaton PGI: A Guide to the Wine Region — Taste Hungary",
    "https://orszagkostolo.gov.hu/regiosvedetteredet/balaton-felvidek/?lang=en":
        "Balaton-felvidék PDO — Wines of Hungary (Országkóstoló)",
    "https://tastehungary.com/journal/kal-basin-kali-medence-pdo-a-guide-to-the-wine-region/":
        "Kál Basin (Káli Medence) PDO: A Guide to the Wine Region — Taste Hungary",
    "https://whc.unesco.org/en/tentativelists/6269/":
        "Balaton Uplands Cultural Landscape — UNESCO World Heritage Tentative List",
    "https://tastehungary.com/journal/land-of-fire-and-salt-hungarys-volcanic-wine-regions/":
        "Land of Fire and Salt: Hungary's Volcanic Wine Regions — Taste Hungary",
    "https://tastehungary.com/journal/baltonfured-csopak-pdo-a-guide-to-the-wine-region/":
        "Balatonfüred-Csopak PDO: A Guide to the Wine Region — Taste Hungary",
    "https://winesofhungary.hu/wine-regions/balatonfured-csopak-wine-district":
        ("https://bor.hu/en/balatonfured-csopaki-wine-district/",
         "Balatonfüred-Csopaki Wine District — Magyar Bor (bor.hu)"),
    "https://bor.hu/en/balatonfured-csopaki-wine-district/":
        "Balatonfüred-Csopaki Wine District — Magyar Bor (bor.hu)",
    "http://www.winesofa.eu/articles/csopak-is-olaszrizling":
        "Csopak is Olaszrizling — Winesofa (Csopak Codex explained)",
    "https://bor.hu/bukki-borvidek/":
        "Bükki borvidék — Magyar Bor (bor.hu)",
    "https://hu.wikipedia.org/wiki/B%C3%BCkki_borvid%C3%A9k":
        "Bükki borvidék — Wikipédia (HU)",
    "https://hungarianwines.eu/bukk-a-wine-region-to-be-discovered/":
        "Bükk – a wine region to be discovered — Hungarianwines.eu",
    "https://www.researchgate.net/publication/385969140_First_Experience_of_Late_Pruning_on_Kekfrankos_Grapevine_Vitis_vinifera_L_in_Eger_Wine_Region_Hungary":
        "Misik et al. 2024 — Late pruning on Kékfrankos in Eger (ResearchGate)",
    "https://link.springer.com/article/10.1007/s00704-025-05510-2":
        "Analysis of detected and future drought conditions, Great Hungarian Plain (Theor. Appl. Climatol. 2025)",
    "https://ishs.org/ishs-article/816_2/":
        "Importance of sandy soils during the Hungarian phylloxera epidemic and today — ISHS Acta Hort.",
    "http://vinotravel.hu/en/wine-regions/csongrad-wine-district/17":
        "Csongrád Wine District — Vinotravel.hu",
    "https://dkmtwine.com/en/2022/05/01/csongradi-borvidek-2/":
        "Csongrádi borvidék — DKMT Wine (2022)",
    "https://www.mdpi.com/2311-7524/10/11/1223":
        "Misik et al. 2024 — First experience of late pruning on Kékfrankos in Eger (Horticulturae)",
    "https://ives-openscience.eu/wp-content/uploads/2020/07/B-lo-et-al_Focus-on-Terroir-Studies.pdf":
        "Bíró et al. — Focus on terroir studies in the Eger wine region (IVES Open Science PDF)",
    "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022XC0405(03)":
        "Eger PDO single document (EUR-Lex 52022XC0405(03))",
    "https://winesofhungary.hu/upper-hungary/eger-wine-district":
        "Eger Wine District — Wines of Hungary",
    "https://orszagkostolo.gov.hu/regiosvedetteredet/etyek-buda/?lang=en":
        "Etyek-Buda PDO — Wines of Hungary (Országkóstoló)",
    "https://cluboenologique.com/story/etyek-sparkling-wine-rise-hungary/":
        "Etyek wines: A sparkling wine revolution is bubbling over in Hungary — Club Oenologique",
    "https://tastehungary.com/journal/etyek-limestone-and-bubbles/":
        "Etyek Wine Region: Where Limestone and Cool Weather Equal Bubbles — Taste Hungary",
    "https://winesofhungary.hu/upper-pannon/etyek-buda-wine-district":
        "Etyek-Buda Wine District — Wines of Hungary",
    "https://boraszat.kormany.hu/hajos-baja":
        "Hajós-Baja PDO product specification — boraszat.kormany.hu",
    "https://winesofhungary.hu/wine-regions/hajos-baja-wine-district":
        ("https://winesofhungary.hu/wine-tourism/hajos-baja-wine-district",
         "Hajós-Baja Wine District — Wines of Hungary"),
    "https://www.boraszportal.hu/magyarorszag-borvidekei/hajos-bajai-borvidek-16":
        "Hajós-Bajai borvidék bemutatása — Borászportál.hu",
    "https://www.hajosbaja.hu/":
        "Hajós-Bajai Borvidék — official borvidék website",
    "https://winesofhungary.hu/wine-regions/kunsag-wine-district":
        ("https://winesofhungary.hu/magazine/kunsag-wine-district-home-of-award-winning-roses-and-many-hidden-treasures",
         "Kunság Wine District: home of award-winning rosés — Wines of Hungary"),
    "https://tastehungary.com/journal/kunsag-pdo-vineyards-rising-from-the-sand/":
        "Kunság PDO: Vineyards Rising From The Sand — Taste Hungary",
    "https://www.researchgate.net/publication/316005136":
        "Kovács, Hoyk & Farkas 2017 — Homokhátság: aridification in the Carpathian Basin (Eur. Countryside)",
    "https://bor.hu/matrai-borvidek/":
        "Mátrai borvidék — Magyar Bor (bor.hu)",
    "https://www.winetourism.com/wine-appellation/matra/":
        "Matra Wine Region Guide — WineTourism.com",
    "https://hungarianwines.eu/matra-guide-vineyard-of-the-mountains-2/":
        ("https://hungarianwines.eu/matra-vineyard-of-the-mountains-full/",
         "Mátra – vineyard of the mountains — Hungarianwines.eu"),
    "https://winesofhungary.hu/magazine/the-new-home-of-kekfrankos-the-matra-wine-district":
        "The new home of Kékfrankos: the Mátra Wine District — Wines of Hungary",
    "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022XC0411(02)":
        "Mór/Móri PDO product specification (EUR-Lex 52022XC0411(02))",
    "https://tastehungary.com/journal/ezerjo-the-hungarian-wine-of-a-thousand-blessings/":
        "Ezerjó: The Hungarian Wine of a Thousand Blessings — Taste Hungary",
    "https://nimbus.elte.hu/tanszek/docs/BSc/2011/MesterhazyIldiko_2011.pdf":
        "Mesterházy I. (2011) — A Móri borvidék éghajlati adottságai (ELTE BSc szakdolgozat)",
    "https://www.wine-searcher.com/regions-mor":
        "Mor — Hungarian Wine Region | Wine-Searcher",
    "https://tastehungary.com/journal/nagy-somlo-pdo-a-guide-to-the-wine-region/":
        "Nagy Somló PDO: A Guide to the Wine Region — Taste Hungary",
    "https://klimapolitikaiintezet.hu/elemzes/soproni-zalai-borvidek-eghajlatvaltozas":
        "Az éghajlatváltozás eddigi nyertesei a Soproni és a Zalai borvidék? — Klímapolitikai Intézet",
    "https://winesofhungary.hu/wine-tourism/somlo-wine-district":
        "Somló Wine District — Wines of Hungary",
    "https://orszagkostolo.gov.hu/regiosvedetteredet/nagy-somlo/":
        "Nagy-Somló OEM — Országkóstoló (Agrárminisztérium)",
    "https://www.mdpi.com/2072-4292/14/14/3463":
        "Bertalan-Balázs et al. 2022 — Vineyard erosion in Neszmély (Remote Sensing)",
    "https://orszagkostolo.gov.hu/regiosvedetteredet/neszmely/?lang=en":
        "Neszmély PDO — Wines of Hungary (Országkóstoló)",
    "https://winesofhungary.hu/wine-regions/neszmely-wine-district":
        ("https://winesofhungary.hu/wine-tourism/neszmely-wine-district",
         "Neszmély Wine District — Wines of Hungary"),
    "https://hilltop.hu/en/wine-region":
        "Our Wine Region — Neszmély — Hilltop Winery",
    "https://winesofhungary.hu/wine-regions/upper-pannon-wine-region":
        "Upper Pannon Wine Region — Wines of Hungary",
    "https://hu.wikipedia.org/wiki/Pannonhalmi_borvid%C3%A9k":
        "Pannonhalmi borvidék — Wikipédia (HU)",
    "https://apatsagipinceszet.hu/?lang=en":
        "Pannonhalma Archabbey Winery — official site (apatsagipinceszet.hu)",
    "https://bbj.hu/budapest/gastronomy/drinks/a-pilgrims-progress-to-worship-wine-at-pannonhalma/":
        "A Pilgrim's Progress to Worship Wine at Pannonhalma — Budapest Business Journal",
    "https://tastehungary.com/journal/pecs-pdo-a-guide-to-the-wine-region/":
        "Pécs PDO – A Guide to the Wine Region — Taste Hungary",
    "https://bor.hu/en/pecsi-wine-district/":
        "Pécsi Wine District — Magyar Bor (bor.hu)",
    "https://borespiac.hu/2025/06/06/cirfandli-kostolosorozat-a-pecsi-kutatointezetben-tematikus-borbiralat-a-kutatasi-tetelekbol-vii/":
        "Cirfandli kóstolósorozat a Pécsi Kutatóintézetben — Bor és Piac (2025-06)",
    "https://www.mdpi.com/2225-1154/9/2/25":
        "Pieczka et al. 2021 — Climate Vulnerability and Adaptation in Szekszárd (MDPI Climate)",
    "https://tastehungary.com/journal/sopron-pdo-a-guide-to-the-wine-region/":
        "Sopron PDO – A Guide to the Wine Region — Taste Hungary",
    "https://www.the-buyer.net/tasting/wine/longhi-wines-sopron-hungary":
        "Sophia Longhi on Sopron – Hungary's oldest wine region — The Buyer",
    "https://www.winetourism.com/wine-appellation/sopron/":
        "Sopron Wine Region — WineTourism.com",
    "https://tastehungary.com/journal/szekszard-pdo-a-guide-to-the-wine-region/":
        "Szekszárd PDO: A Guide to the Wine Region — Taste Hungary",
    "https://hungarianwines.eu/szekszardi-bikaver-regulation/":
        "Szekszárdi Bikavér regulation — Hungarianwines.eu",
    "https://eu-cap-network.ec.europa.eu/good-practice/enhancing-kekfrankos-grape-varieties-climate-resistant-wine-production-hungary_en":
        "Enhancing Kékfrankos grapes for climate-resistant wine production in Hungary — EU CAP Network",
    "https://www.nature.com/articles/s41538-025-00468-x":
        "Magyar et al. 2025 — Long-term compositional profiling of historical Tokaji aszú wines (npj Sci. Food)",
    "https://akjournals.com/view/journals/446/20/1/article-p113.xml":
        "Szám et al. 2024 — Study of drought periods in the Tokaj-Hegyalja wine region (Prog. Agric. Eng. Sci.)",
    "https://winesoftokaj.hu/en/tokaj/soils":
        "Tokaj soils — Wines of Tokaj (official regional site)",
    "https://en.wikipedia.org/wiki/Tokaj_wine_region":
        "Tokaj wine region — Wikipedia",
    "https://bor.hu/tolnai-borvidek/":
        "Tolnai borvidék — Magyar Bor (bor.hu)",
    "https://www.boraszportal.hu/magyarorszag-borvidekei/tolnai-borvidek-13":
        "Tolnai borvidék bemutatása — Borászportál.hu",
    "https://tuzkobirtok.hu/en/":
        "Tűzkő Birtok (Bátaapáti, Tolna) — official winery website",
    "https://tastehungary.com/journal/villany-pdo-a-guide-to-the-wine-region/":
        "Villány PDO: A Guide to the Wine Region — Taste Hungary",
    "https://winesofhungary.hu/wine-regions/villany-wine-district":
        ("https://winesofhungary.hu/wine-tourism/villany-wine-district",
         "Villány Wine District — Wines of Hungary"),
    "https://www.thedrinksbusiness.com/2016/12/is-villany-the-new-home-of-cabernet-franc/":
        "Is Villány the new home of Cabernet Franc? — The Drinks Business (2016)",
    "https://www.wine-searcher.com/regions-villany":
        "Villany — Hungarian Wine Region | Wine-Searcher",
    "https://tastehungary.com/journal/zala-wine-region/":
        "Zala Wine Region — Taste Hungary",
    "https://www.aloki.hu/pdf/1602_20292042.pdf":
        "Szenteleki et al. — Shift in the annual growth cycle of grapevines in West Hungary (Aloki PDF)",
    "https://bor.hu/en/zalai-wine-district/":
        "Zalai Wine District — Magyar Bor (bor.hu)",
}

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# scripts is in site/scripts; we want C:/Bor-szőlő/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # site/
ROOT = os.path.dirname(ROOT)  # C:/Bor-szőlő/
print("ROOT =", ROOT)

dirpath = os.path.join(ROOT, "analysis", "curated", "descriptions")
files = sorted(glob.glob(os.path.join(dirpath, "*.json")))
agg = {}
total_changed = 0
total_url_changed = 0
unmapped = set()
for fn in files:
    if os.path.basename(fn) == "descriptions.json":
        continue
    with open(fn, encoding='utf-8') as f:
        d = json.load(f)
    new_sources = []
    for s in d.get('top_sources', []):
        url = s['url']
        old_title = s['title']
        if url in TITLES:
            v = TITLES[url]
            if isinstance(v, tuple):
                new_url, new_title = v
                if new_url != url:
                    total_url_changed += 1
            else:
                new_url, new_title = url, v
        else:
            new_url, new_title = url, old_title
            unmapped.add(url)
        if new_title != old_title or new_url != url:
            total_changed += 1
        new_sources.append({"title": new_title, "url": new_url})
    d['top_sources'] = new_sources
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    agg[d['slug']] = d

# aggregate
with open(os.path.join(dirpath, 'descriptions.json'), 'w', encoding='utf-8') as f:
    json.dump(agg, f, ensure_ascii=False, indent=2)

# copy to site
site_pub = os.path.join(ROOT, "site", "public", "data")
dst_dir = os.path.join(site_pub, "descriptions")
os.makedirs(dst_dir, exist_ok=True)
for fn in files:
    bn = os.path.basename(fn)
    if bn == "descriptions.json":
        continue
    shutil.copy(fn, os.path.join(dst_dir, bn))
shutil.copy(os.path.join(dirpath, 'descriptions.json'), os.path.join(site_pub, 'descriptions.json'))
shutil.copy(os.path.join(dirpath, 'descriptions.json'), os.path.join(dst_dir, 'descriptions.json'))

print(f"Updated {total_changed} sources across {len(files)-0} files; URL replacements: {total_url_changed}")
if unmapped:
    print("UNMAPPED URLs:")
    for u in unmapped:
        print(" -", u)
