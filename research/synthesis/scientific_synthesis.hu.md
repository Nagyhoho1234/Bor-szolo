# Klímaváltozás és Magyarország huszonkét borvidéke: a borvidéki szintű bizonyítékelemzések szintézise (1971–2100)

**Szintézis dátuma:** 2026-04-07
**Hatókör:** Magyarország mind a 22 OEM-borvidéke
**Bizonyítékbázis:** 22 borvidéki szintű bizonyítékelemzés (`research/districts/*.md`; ~123 000 szó; ~1 200 forrás)
**Olvasási konvenció:** Minden ténymegállapítás **[OBSERVED]**, **[PROJECTED]** vagy **[HU-AGGREGATE]** címkét kap; a vitatott megállapításokat külön jelöljük.

---

## Absztrakt

Magyarország 22 oltalom alatt álló eredetmegjelöléssel (OEM) rendelkező borvidéknek ad otthont, amelyek négy makrorégióban (Tokaj, Felső-Magyarország, Dunántúl és Alföld) oszlanak el, és kontinentális éghajlati gradienst fognak át Sopron szub-alpin peremétől Kunság homokos alföldi belsejéig. Ez a szintézis 22 borvidéki szintű bizonyítékelemzést konszolidál, hogy elkészítse az első integrált, országos, OEM-felbontású auditot a szőlészet megfigyelt és előrevetített klímaváltozási hatásairól. A központi kvantitatív horgony Lakatos & Nagy (2025, *Frontiers in Plant Science* 16:1481431), amely a FORESEE 4.2 torzításkorrigált, 14 EURO-CORDEX regionális klímamodellből álló ensemble-jét alkalmazza RCP4.5 és RCP8.5 forgatókönyvek mellett mind a 22 borvidékre, négy bioklimatikus index segítségével (AGST, GDD-Winkler, Huglin-index, BEDD). Három megállapítás emelkedik ki. Először, az országos felmelegedési gradiens **megfordítja az ország hagyományos szőlészeti rangsorát**: Csongrád, Kunság, Tokaj, Eger, Bükk és Mátra (történelmileg „hűvös" vagy „közepes" északi és keleti borvidékek) gyorsabban melegszenek, mint a déli pannon borvidékek (Villány, Pécs és Szekszárd). Kunság mutatja a legnagyobb előrevetített GDD-emelkedést (**+581,65 °C·nap**), Bükk a legnagyobb BEDD-emelkedést (**+258,49 °C·nap**), Csongrád AGST-emelkedése meghaladja a **+2,5 °C**-ot, Eger pedig a legnagyobb Huglin-növekedést mutatja (**+566,15 °C**); Sopron az ellenkező véglet, a legkisebb GDD-emelkedéssel (**+66,16 °C·nap** történelmi; **+475,98 °C·nap** előrevetített). Másodszor, a megfigyelt kémiai jelzés — 55–60 g/L mustcukor-többlet a hűvös borvidékek fehérborainál, 1,5–2,5 g/L összes-savveszteség Chardonnay-ban 1980–2020 között, alkoholkúszás ~12 %-ról ≥14 tf%-ra a zászlóshajó vörösboroknál — már most újraírja a regionális borstílusokat. Harmadszor, **a hatás kiinduló hőmérséklet szerint kettéválik**: a hűvös éghajlatú borvidékek (Sopron, Etyek-Buda, Nagy-Somló, Mór, Balaton) „kétélű fegyverrel" néznek szembe, amelyben a melegedés javítja az érést, de erodálja az identitást, míg a forró borvidékek (Csongrád, Kunság, Hajós-Baja) a hőstresszes fenolos szétkapcsolódás, a szélsőséges hőhullámok és a Homokhátság 2–5 m-es talajvízszint-csökkenése által vezérelt egzisztenciális életképességi kérdésekkel szembesülnek. Hét kutatási prioritást azonosítunk, amelyek élén a Lakatos & Nagy-féle kiegészítő táblázatok borvidéki szintű kinyerésének sürgős szüksége, Tokajon kívül a szisztematikus fenológiai sorozatok, a Balaton csatolt tó–szőlő mezoklíma-leskálázása, valamint a Móri-szél statisztikai klimatológiája áll.

---

## 1. Bevezetés

Magyarországon mintegy 61 000 ha szőlőterületet művelnek (2023; szemben a 2018. évi 69 000 ha-ral), amelyek **22 oltalom alatt álló borvidékbe (borvidék)** szerveződnek, és ezek hat makrorégióba csoportosulnak: Tokaj, Felső-Magyarország (Bükk, Eger, Mátra), Felső-Pannon (Mór, Etyek-Buda, Neszmély, Pannonhalma, Sopron), Balaton (Badacsony, Balaton-felvidék, Balatonfüred-Csopak, Balatonboglár, Nagy-Somló, Zala), Pannon (Pécs, Szekszárd, Tolna, Villány) és a Duna/Alföld (Csongrád-Csanád, Hajós-Baja, Kunság). Összességében a globális bortermelésnek csak ~1–2 %-át adják, mégis aránytalanul nagy kulturális, tudományos és genetikai értéket hordoznak: Tokaj a világ legrégebbi zárt borvidéke (1737) és UNESCO-világörökségi kultúrtáj; a Pécsi Egyetem szőlő-génbankja ~1 500 tételt őriz (a világ hatodik legnagyobbja); a somlói Juhfark gyakorlatilag csak egyetlen erodált bazaltbütyök 500 ha-ján létezik; és a magyar endemikus fajták — Furmint, Hárslevelű, Kéknyelű, Juhfark, Cirfandli, Ezerjó, Királyleányka és Kadarka — máshol nem rendelkeznek jelentős kereskedelmi otthonnal.

A magyarországi nemzeti éves átlaghőmérséklet **+1,15 °C-kal emelkedett 1907 és 2017 között**, és jelenleg **+0,057 °C évenként melegszik 2000 óta — ami közel kétszerese a globális átlagnak** [`etyek-budai.md`; `pannonhalmi.md`; OMSZ]. A Kárpát-medence elismert európai felmelegedési hotspot (Spinoni et al. 2015). A szőlészet — amely belsőleg klímafüggő földhasználat, amelynek gazdasági értéke szorosan kapcsolódik szűk hőmérséklet-, savasság-, pH-, cukor- és fenolablakokhoz — számára ez egyszerre jelent közvetlen hőstresszt és másodlagos zavart az OEM-alapú eredetvédelmi architektúrában, amely borvidéki szinten határozza meg a bor identitását.

A közelmúltig a magyar klímahatás-szőlészeti kutatás töredezett volt: elszigetelt fenológiai sorozatok (Sopron, Zala), birtokszintű termelői tanúvallomások, valamint országos vagy európai aggregátumok, amelyek átlagoltak az ország valós belső gradiensein. Lakatos L. & Nagy R. (2025), *Assessment of historical and future changes in temperature indices for winegrape suitability in Hungarian wine regions (1971–2100)*, *Frontiers in Plant Science* 16:1481431 megjelenése az első integrált, fizikai alapú, torzításkorrigált reanalízist nyújtotta borvidéki felbontásban mind a 22 borvidékre. Ez a szintézis központi horgonya; minden borvidéki elemzés helyi terroir-, fajta-, fenológiai, kémiai, kártevő-, aszály-, adaptációs és gazdasági bizonyítékkal egészíti ki.

A szintézis célja, hogy (i) konszolidálja az országos jelzést a Lakatos & Nagy-féle keretben, (ii) ütköztesse megfigyelt fenológiai és kémiai adatokkal, (iii) fajtaspecifikus **sérülékenységi taxonómiát** építsen a magyar endemikus cultivarokra alapozva, (iv) összehasonlító adaptációs leltárt állítson össze, és (v) a 22 borvidéki elemzés során kijelölt ~250 egyedi tudáshézagot országos kutatási menetrenddé desztillálja.

## 2. Módszerek

Ez egy **narratív meta-szintézis** 22 borvidéki szintű bizonyítékelemzésről (`research/districts/*.md`, szintézis dátuma 2026-04-07). A borvidéki elemzések közös, 15 szakaszos sablont követtek (profil; terroir; alapklíma; megfigyelt trendek; fenológia; kémia; szenzorika; biotikus stresszorok; abiotikus szélsőségek; közvetett hatások; projekciók; adaptáció; gazdaság; tudáshézagok; források), és összességében ~1 200 szakmailag lektorált, ügynökségi és termelői forrást idéznek. Itt új külső irodalmat nem vezetünk be.

**A borvidéki elemzésekben visszatérő kulcsfontosságú adatforrások:**

- **Lakatos L. & Nagy R. (2025)**, *Frontiers in Plant Science* 16:1481431 — a mértékadó friss, országos indexreanalízis, a FORESEE 4.2 alapján (28 torzításkorrigált klímamodell, köztük 14 EURO-CORDEX futtatás), RCP4.5 és RCP8.5 forgatókönyvek, 1971–2000, 2021–2050 és 2071–2100 időszeletek, AGST, GDD-Winkler, Huglin-index és BEDD számítása mind a 22 borvidékre. Néhány borvidéki fájl (különösen Tokaj és a Balaton OEM-ek) ugyanezt a cikket „Kovács et al. 2025" néven idézi; a DOI azonos, és az eltérés a borvidéki elemzési fázis bibliográfiai zavarát tükrözi. Ez a szintézis a két hivatkozást egyenértékűnek tekinti, és egységesen **Lakatos & Nagy (2025)**-re szabványosít.
- **OMSZ** (Országos Meteorológiai Szolgálat) állomási és rácsos termékek.
- **FORESEE 4.0 / 4.2** torzításkorrigált klímaadatbázis (ELTE).
- **EURO-CORDEX** CMIP5 regionális leskálázási ensemble; torzításkorrekció-értékelés: Mihaljević & Bíró (2025, *Sci. Tot. Environ.*).
- **CARPATCLIM** Kárpát-régiós reanalízis (hivatkozott történelmi állomáskitöltésre).
- **Klímapolitikai Intézet (2023, 2024)** technikai jelentések — a dunántúli hűvös borvidékek széles körben idézett „**+55 – +60 g/L mustcukor-többlet**" számának forrása (Sopron-Zala aggregátum 1961–1990 vs. közelmúlt).
- **Termelői tanúvallomás** — NAIK-SZBKI Tarcal, Pécsi Egyetem Borászati Intézete, Csopak Kódex-termelők, Kreinbacher/Tornai (Somló), Misik et al. egri késői metszési kísérletek, Frittmann et al. (Kunság), Tűzkő/Antinori (Tolna).

A megállapításokat **[OBSERVED]** címkével jelöljük, ha műszeres, fenológiai vagy kémiai adatokon nyugszanak; **[PROJECTED]** címkével, ha az EURO-CORDEX/FORESEE ensemble-ből származnak; **[HU-AGGREGATE]** címkével, ha az egyetlen szakmailag lektorált szám országos, és analógia alapján került át egy borvidékre. A vitatott megállapításokat a §10-ben külön jelöljük.

---

## 3. Eredmények — Az országos felmelegedési gradiens

### 3.1 A Lakatos & Nagy (2025)-féle rangsor

Lakatos & Nagy négy bioklimatikus indexet számít mind a 22 borvidékre, jelentik az 1971–2000 referenciaértékeket és a 2021–2050, valamint 2071–2100 időszak változásait RCP4.5 és RCP8.5 alatt. A nyílt hozzáférésű cikk az országos tartományokat és néhány nevesített borvidéki szélsőértéket tesz közzé; a teljes borvidékenkénti táblázatok csak kiegészítő anyagként érhetők el. A 22 borvidéki elemzés között a visszakereshető numerikus főpontok (**[OBSERVED + PROJECTED, RCP8.5, 1986–2005 → 2081–2100, ha nem jelezzük másként]**):

| Index | Magyarországi tartomány | Legnagyobb | Legkisebb | Országos átlag |
|---|---|---|---|---|
| **GDD-Winkler (°C·nap)** — *megfigyelt történelmi emelkedés* | +66,16 – +173,96 | **Tokaj +173,96** | **Sopron +66,16** | +122,48 |
| **GDD-Winkler (°C·nap)** — *előrevetített évszázadvég* | +475,98 – +581,65 | **Kunság +581,65** | **Sopron +475,98** | +537,23 |
| **BEDD (°C·nap)** — *előrevetített évszázadvég* | +182,71 – +258,49 | **Bükk +258,49** | **Szekszárd +182,71** | +204,26 |
| **Huglin-index (°C)** — *előrevetített évszázadvég* | +461,58 – +566,15 | **Eger +566,15** | **Sopron +461,58** | +523,8 |
| **AGST (°C)** — *előrevetített évszázadvég* | +2,44 – +2,96 | **Tokaj +2,96** | **Sopron +2,44** | ~+2,7 |
| **AGST (°C)** — *Csongrád-Csanád-specifikus főérték* | > **+2,5 °C** | — | — | — |
| **AGST (°C)** — *Pannonhalma-specifikus főérték* | **+2,3 °C** (a legkisebb valamennyi borvidék között) | — | — | — |

[`bukki.md`; `kunsagi.md`; `tokaji.md`; `soproni.md`; `matrai.md`; `pannonhalmi.md`; `csongradi.md`; `tolnai.md`]

Ábrajavaslat 1: **1. ábra — Borvidékenkénti rangsorolt GDD-Winkler növekedés**, 1986–2005 → 2081–2100 RCP8.5. Vízszintes sávdiagram 22 sávval, Sopron (+475,98) alulról Kunság (+581,65) tetejéig rendezve, makrorégió szerint színezve (Tokaj / Felső-HU / Felső-Pannon / Balaton / Pannon / Duna), az országos átlaggal (+537,23) mint referenciavonallal.

### 3.2 Az ellentmondásos észak-dél megállapítás

A stratégiailag legfontosabb egyetlen projekció, hogy **az északi magyar borvidékek (Tokaj, Eger, Bükk, Mátra) gyorsabban melegszenek, mint a déliek (Villány, Pécs, Szekszárd)**, megfordítva az ország hagyományos szőlészeti rangsorát. Ez mind a négy indexen látszik: Tokaj mutatja a legnagyobb történelmi GDD-emelkedést (**+173,96 °C·nap**) és a legnagyobb előrevetített AGST-emelkedést (**+2,96 °C**); Bükk a legnagyobb előrevetített BEDD-emelkedést (**+258,49 °C·nap**), mert a hűvösebb alapja több termodinamikai tartalékot hagy; Eger a legnagyobb előrevetített Huglin-emelkedést (**+566,15 °C**); Kunság (Alföld, már most is forró) a legnagyobb előrevetített abszolút GDD-emelkedést (**+581,65 °C·nap**), ami a homokfelszíni konvektív erősítését és kontinentális kitettségét tükrözi [`bukki.md`; `tokaji.md`; `kunsagi.md`]. Ezzel szemben Pannonhalma mutatja a legkisebb előrevetített AGST-emelkedést (**+2,3 °C**), Sopron pedig a legkisebb abszolút emelkedést mindegyik indexen [`pannonhalmi.md`; `soproni.md`].

**Mechanizmus.** A borvidéki elemzések három tényezőt hoznak fel. (i) *Kontinentalitás*: az északi és keleti magyar borvidékek távolabb vannak a Sopron és az alpesi perem által élvezett atlanti mérséklő hatástól, és nyári hőjük ugyanazon sugárzási kényszer mellett gyorsabban halmozódik fel. (ii) *Termikus tartalék*: a hűvösebb alapállapotok nagyobb távolságot hagynak a Jones-féle AGST-osztályküszöbökig; különösen a BEDD-index kumulatív és Bükkben alultelített, így adott hőmérséklet-változás nagyobb BEDD-változást okoz. (iii) *Tó- és Duna-pufferelés*: Sopron, Pannonhalma, Neszmély és a balatoni borvidékek jelentős termikus pufferelést kapnak a Fertőtől, a Dunától vagy magától a Balatontól, ami tömöríti a helyi válaszreakciót [`soproni.md`; `balaton-felvideki.md`; `balatonfured-csopaki.md`].

**Vitatott pontok.** Lakatos & Nagy csak aggregált országos vizualizációkat tesz közzé; a borvidékenkénti numerikus táblázatok nem szerepelnek a főszövegben, és több borvidéki elemzés ezt explicite a verifikáció akadályaként jelöli meg (különösen `csongradi.md` 3. tudáshézag a csongrádi AGST-ről; `bukki.md` 3. hézag a BEDD-ről; `etyek-budai.md` 2. hézag; `balaton-felvideki.md` 12. hézag). A pontos rangsor tehát a kiegészítő táblázatoktól függ, amelyeket ki kellene nyerni és önálló nyílt adatállományként újra közzétenni; ez a tudáshézag-prioritás A a §11-ben.

---

## 4. Eredmények — Fenológia, hozam és kémia

### 4.1 Fenológia

**[OBSERVED]** A legjobban publikált magyar fenológiai sorozat továbbra is Kovács, Puskás & Pozsgai (2016, Springer) a **Sopron/Zala 1986–2015 vs. 1956–1985** összehasonlításához: rügyfakadás ~**8 nappal korábban**, virágzás ~**7 nappal korábban**, érésfordulat ~**8 nappal korábban**, szüret ~**11 nappal korábban**, a tenyészidőszak melegedése ~+1,2 °C [`bukki.md`; `soproni.md`]. Magyar **Chardonnay és Pinot Noir** esetében az 1981–1990 → 2011–2020 közötti szüreti dátumelőzés ~**10–20 nap** (összhangban a franciacortai Chardonnay ~25 napos jelzésével és a champagne-i ~0,9 g L⁻¹ TA / +0,7 tf% jellel) [`etyek-budai.md`]. **Tokajban** a 2024-es forró júliusi évjárat szürete **augusztus elején kezdődött — a történelmi normánál nagyjából egy hónappal korábban** [`tokaji.md`]. A Balaton déli partján a Chardonnay és a Merlot ma már rendszeresen **március utolsó hetében fakad ki**, ami történelmileg áprilishoz kötődött [`balatonboglari.md`].

**A Sopron-Zala páron kívül a többi 20 borvidék egyikére sincs szisztematikus fenológiai sorozat a jelen vizsgált szakirodalomban.** Bükk, Mátra, Nagy-Somló, Mór, Balaton-felvidék, Pannonhalma, Villány, Pécs, Szekszárd, Tolna, Hajós-Baja, Kunság és Csongrád tudáshézagai mind a megfelelő fájlokban vannak jelölve. Ez a **legnagyobb egyetlen országos adathézag**, amelyet a §11-ben azonosítunk.

**Fagy–fenológia szétkapcsolódás.** Mivel a rügyfakadás gyorsabban előrehúzódik, mint az utolsó tavaszi fagyok dátuma, **a nettó tavaszi fagykockázat nem csökkent a felmelegedéssel arányosan** [`csongradi.md`; `kunsagi.md`; `hajos-bajai.md`; `bukki.md`; `etyek-budai.md`]. A **2024. áprilisi fagyesemény** országos természeti kísérlet volt, amely megerősítette ezt: a hideg levegő az északi megyékben −2 °C vagy alacsonyabb szintre hatolt be; Kunság, Mátra és Tokaj szenvedte el az országos legnagyobb csökkenéseket (akár egyharmadával kevesebb termés az alföldi szőlőkön); Bükk súlyosan elvesztette az alsó-teraszos szőlőit; Eger jelentős Bikavér-mennyiségeket veszített; Felső-Pannon jelentős területet veszített; Etyek-Buda a fagyzugokban 20–60 %-os helyi terméskiesést jegyzett; Mór és maga Tokaj elkerülte a legrosszabbat. A 2024-es országos szüret egy évtized leggyengébb volt (~3,75 Mt) [`tokaji.md`; `kunsagi.md`; `bukki.md`; `etyek-budai.md`; `mori.md`; `csongradi.md`].

### 4.2 Cukor, savasság, pH, alkohol

**[OBSERVED]** Következetes kémiai jelzés rajzolódik ki minden olyan borvidéken, ahol termelői vagy publikált adat áll rendelkezésre:

- **Sopron-Zala hűvös borvidéki Olaszrizling:** **+55 – +60 g L⁻¹ mustcukor-többlet** 1961–1990 alap → közelmúlt évtizedek (Klímapolitikai Intézet 2023), ami **+3,2–3,5 tf% potenciális alkoholnak** felel meg. A történelmi identitás ~11,0–11,5 % ABV roppanós Olaszrizling volt; a közelmúlt borai rendszeresen 12,5–13,5 % ABV vagy magasabb értéken állnak [`zalai.md`].
- **Etyek-budai Chardonnay 1980–2020:** a szüreti összes savasság **1,5–2,5 g L⁻¹-rel csökkent** (~9–10 g L⁻¹-ről 6,5–8 g L⁻¹ felé); analóg a champagne-i ~−0,9 g L⁻¹ TA és +0,7 tf% potenciális alkohol 1980 óta tartó jelzésével [`etyek-budai.md`].
- **Balatonfüred-csopaki Olaszrizling:** TA ~1,0–1,5 g L⁻¹-rel csökkent (borkősavként); pH ~0,1–0,15 egységgel emelkedett. A Csopak Kódex 5,5 g L⁻¹-es minimum TA-ja de facto **klímastressz-indikátorrá** vált — a termelői tételek egyre nagyobb hányada nem éri el a Kódex TA-küszöbét forró évjáratokban [`balatonfured-csopaki.md`].
- **Móri Ezerjó:** a korábban ~11–11,5 tf%-os borok most rendszeresen **12,5–13,5 tf%-ot** érnek el [`mori.md`].
- **Villányi Franc:** az 1990-es évek–2000-es évek eleji „bársonyos, kékgyümölcsös, fűszeres, 13 tf%, 10–15 éves érlelés" referenciastílus részben átadta a helyét a **sűrű, opulens, sötétgyümölcsös, 14,5 %+ »Villányi Ördögkatlan« stílusnak**. A Villányi Franc 2014-es OEM-reformja kifejezetten szigorította az érés-, tölgyfa- és extrakciós paramétereket a drift ellensúlyozására — ez az egyik legkorábbi európai OEM-reform, amit kifejezetten a klímaindukált stílusváltás váltott ki [`villanyi.md`].
- **Kunsági fehérek (Cserszegi fűszeres, Olaszrizling, Bianca):** az 1980-as években ~19–21 °Bx / 6–7 g L⁻¹ TA alap; a közelmúlt forró évjáratai mindkét tengelyt **ugyanabba** az irányba tolják, strukturális tömegbor-költségszorítást hajtva [`kunsagi.md`].
- **Tokaji aszú:** Magyar et al. (2025, *npj Science of Food*) az 1999–2019 évjáratok kompozíciós profilozása alapján kimutatja, hogy a borkémia az éves csapadékot, napsütéses órákat és hőmérsékletet követi — ez az első hosszú távú *kémiai* megerősítése annak, hogy az éghajlati változékonyság rávésődik a tokaji bor összetételére [`tokaji.md`].

### 4.3 Fenolos és antocianin hőösszeomlás vörösekben

**[OBSERVED + MECHANIZMUS]** Mori et al. (2007, *J. Exp. Bot.*) klasszikus megállapítása — amely szerint a T<sub>max</sub> ≈ 35 °C-os bogyók **kevesebb mint fele annyi antocianint** halmoznak fel, mint a T<sub>max</sub> ≈ 25 °C-os bogyók, részben csökkent bioszintézis, részben fokozott lebomlás révén — ma közvetlenül megfigyelhető jelzés a magyar vörösekben. Explicite hivatkoznak rá: `hajos-bajai.md`, `csongradi.md`, `kunsagi.md`, `szekszardi.md`, `tolnai.md` és `villanyi.md`:

- **Kadarka** (vékony héjú, természetesen antocianin-szegény) mutatja a legkifejezettebb színinstabilitást: a halvány siller-stílusú vörösek ma Hajós-Bajában és Csongrádon az alapértelmezettek [`hajos-bajai.md`; `csongradi.md`].
- **Cabernet Sauvignon és Merlot** több színt megőriz, de acilált, kevésbé reaktív antocianin-formák felé tolódik — vizuálisan tompább borok stabil, de kevésbé élénk színnel [`hajos-bajai.md`].
- A **Kékfrankos** szín pozitívan korrelál a tengerszint feletti magassággal Egerben: a Nagy-Eged magashegyi blokkok következetesen felülmúlják a völgyi helyszíneket, összhangban a ~0,6–0,65 °C / 100 m-es hőmérsékleti gradienssel mint *de facto* adaptációval [`egri.md`].
- **Cukor/fenolos szétkapcsolódás** (cukorérés a tannin/antocianin érés előtt) a központi klíma-minőség probléma az összes pannon és alföldi vörös borvidéken [`villanyi.md`; `szekszardi.md`; `csongradi.md`; `kunsagi.md`]. Ez vezetett Misik et al. (2025, MDPI Horticulturae) Eger Kékfrankoson végzett késői metszési / csúcsi lombtalanítási kísérleteihez, amelyek kimutatták, hogy a késő szezonális kezelés ~2 héttel késleltetheti a rügyfakadást és a virágzást, és a cukor–antocianin görbét alacsonyabb alkoholtartalmú, jobb színű borok felé tolhatja [`egri.md`].

---

## 5. Eredmények — A magyar őshonos fajták identitáskockázati taxonómiája

Magyarország OEM-rendszere szorosabban kötődik — bármely más európai borországhoz képest, kivéve Burgundiát és a Moselt — az őshonos cultivarokhoz, amelyeknek máshol nincs jelentős kereskedelmi otthona. A klímaváltozás tehát *fajtakihalási kockázatot* jelent, ami Nyugat-Európa nagy részén csak *stílusdrift kockázat*.

**1. táblázat — A magyar őshonos cultivarok fajtaspecifikus sérülékenysége**

| Fajta | Borvidék(ek) | Összterület | Éghajlati kitettség | Veszélyeztetett stílus | Státus |
|---|---|---|---|---|---|
| **Furmint** (aszú kontextus) | Tokaj | — | Nemespenész-megbízhatóság csökken; száraz-bor pivot már ~1/3 a szüretből | Botritizált édes bor | Kettős pálya (édes le, száraz fel); Ausztriába exportálva mint klímafedezet [`tokaji.md`] |
| **Hárslevelű** | Tokaj + egyebek | — | Ugyanaz, mint a Furmint édes kontextusban | Botritizált / késői szüret | Száraz-bor pivoton keresztül túlél [`tokaji.md`] |
| **Ezerjó** | **Mór** (szellemi otthon), Kunság tömegtermelés | **Összesen 1 655 ha** (a **>14 000 ha-os 1970-es csúcshoz** képest, amikor HU 4. legtöbbet telepített fajtája); Mór a **minőségi** központ | Korai rügyfakadású, vékony héjú, hőérzékeny | Könnyű, roppanós száraz fehér ~11 tf% | Országos összeomlás 1970→2024 (−88 %); a móri identitás egzisztenciális kockázatban [`mori.md`] |
| **Cirfandli** (Zierfandler) | **Pécs** (Magyarország egyetlen kereskedelmi otthona) | **13,9 ha, −40 % 5 év alatt** 2024-ig | Paradox módon *javul* termikus alapon (PTE főborász: „2/10 kiemelkedő évjárat → 6/10"), de a szélsőséges hő jobban károsítja a gyümölcs szerkezetét, mint a nemzetközi fajtákét | Késői szüret, félszáraz, botritizált | Területösszeomlás javuló érettség ellenére; a klíma *segíti* a szőlőkémiát, de a gazdasági/fajta-trend összeomlóban [`pecsi.md`] |
| **Juhfark** | **Nagy-Somló** | **~80–150 ha a globális ~100–170 ha-ból** (a világkészlet ≥80 %-a) | A történelmi érési nehézséget ma a melegedés *enyhíti* — rövid távú haszonélvező —, de a fajta **USP-je a hasító savassága**, amely most strukturálisan erodálódik | „Kovakő"-ízű, magas savú, mineral, érlelhető száraz fehér | Újjáéledés (Kreinbacher et al. ~2005-től) az évjárati érési ablak idején; a stílusdrift most a fő hosszú távú kockázat; **nincs sehol hűvösklíma-menedék** [`nagy-somloi.md`] |
| **Kéknyelű** | **Badacsony** | **~45–47 ha** (az 1990-es évek közepének ~1 ha-járól; a borvidéki terület ~3 %-a). 2025-ben Hungarikummá nyilvánítva | Alacsony hozamú endemikus, nőivarú virág; Budai zölddel vagy a Rózsakő kereszttel kell közé ültetni | Mineral száraz fehér, alkalmanként botritizált | Majdnem kihalásból lábadozik, klímaérzékeny [`badacsonyi.md`] |
| **Olaszrizling** (Welschriesling) | Mind a hat balatoni OEM; Mór; Pécs; Szekszárd | Országosan domináns fehér | Hőtűrőbb, mint az aromás fehérek, de a stílus laposabb, teltebb test felé drifttel | Könnyű, roppanós, mineral | Stílusdrift az egész Balaton mentén; TA-csúszás a Csopak Kódex küszöbök alá [`balatonfured-csopaki.md`; `balatonboglari.md`; `balaton-felvideki.md`] |
| **Kékfrankos** (Blaufränkisch) | Sopron, Eger (Bikavér), Szekszárd, Villány | HU domináns vörös | Antocianinveszteség ~35 °C felett; magassággal korrelált szín (Nagy-Eged) | Középsúlyú száraz vörös | Regionálisan differenciált; egri magassági puffer [`egri.md`; `soproni.md`] |
| **Kadarka** | Szekszárd, Hajós-Baja, Csongrád | Kevés | Vékony héj, alacsony antocianin; forró évjárati színösszeomlás | Paprikás száraz vörös | Stílusvesztés halvány siller irányba [`szekszardi.md`; `hajos-bajai.md`; `csongradi.md`] |

Ábrajavaslat 2: **2. ábra — Veszélyeztetett fajtaidentitás**, (a) panel: teljes telepített terület 1970 vs. 2024 a hat legkitettebb őshonos cultivar esetében (Ezerjó, Cirfandli, Juhfark, Kéknyelű, Kadarka, Kékfrankos); (b) panel: földrajzi koncentráció (a magyar összterület %-a egy borvidéken); (c) panel: kvalitatív termikus kitettségi hőtérkép.

### 5.1 Stílusszintű identitáskövetkezmények

- **Tokaj** — Magyarország egyetlen legkitettebb zászlóshajó stílusa az aszú. A melegebb, szárazabb őszök egyre megbízhatatlanabbá teszik a nemespenész-képződést; a **száraz Furmint és Hárslevelű** felé történő strukturális pivot ma a **tokaji szüret ~1/3-át** teszi ki, egy olyan kereskedelmi kategória, amely 25 éve alig létezett [`tokaji.md`].
- **Pannon vörösek** — Villányi Franc alkoholkúszás ~13 tf%-ról ≥14,5 tf%-ra; a 2014-es OEM-reform korai európai szabályozási válasz [`villanyi.md`].
- **Etyek-budai pezsgőalap** — a savveszteség (−1,5 – −2,5 g L⁻¹ TA Chardonnay-ban 1980–2020 között) közvetlenül fenyegeti a borvidék *raison d'être*-jét mint Magyarország pezsgőalap-szívcentrumát. Lakatos & Nagy nem jelöli Etyek-Budát termikusan „javuló"-nak, mert itt a melegedés egyértelműen *egyértelmű degradációs jelzés* ennek a stílusnak [`etyek-budai.md`].
- **Balatoni Olaszrizling** — Csopak Kódex-megfelelés mint klímastressz-indikátor; stílusdrift teltebb test, alacsonyabb frissesség felé [`balatonfured-csopaki.md`; `balaton-felvideki.md`].
- **Csongrád/Kunság tömeg-fehérek és homoki vörösek** — strukturális költségszorítás, amikor a must hígítása és savasítása elkerülhetetlenné válik [`csongradi.md`; `kunsagi.md`].

---

## 6. Eredmények — Biotikus és abiotikus stresszorok

### 6.1 Inváziós kártevők areabővülése

**[OBSERVED — országos]**

- ***Drosophila suzukii*** (pettyes szárnyú muslica): **első magyarországi rekord 2012** (Somogy megye; Kiss et al.). Számos lágygyümölcs mellett szőlőt is támad; kritikusan **elősegíti a savas rothadás kitöréseit**, mivel a bogyókon sebeket hoz létre, amelyeket a *D. melanogaster* és rothadó mikrobák kihasználnak (Ioriatti et al. 2018). Közvetlen fenyegetés a késői szüretre és aszú-munkafolyamatokra, ahol a bogyók az őszig fent maradnak [`tokaji.md`; `balaton-felvideki.md`].
- ***Halyomorpha halys*** (márványos büdöspoloska): **első magyarországi rekord 2013** (Budapest; Vétek et al.); megerősítve **2017-re Magyarországon széles körben elterjedt**; *Vitis vinifera*-n táplálkozik; nagyon alacsony fertőzési arány mellett is „büdöspoloska-felhangot" okoz a kész borban [`tokaji.md`].
- ***Scaphoideus titanus***: a **Flavescence dorée fitoplazma** vektora, már jelen van Magyarországon; a felmelegedéssel járó areabővülés az elsődleges *betegség*-kockázat [`tokaji.md`].

Borvidéki szintű, a szőlőveszteségeket a három taxonra számszerűsítő kárfelmérések nem állnak rendelkezésre. Ez egy országos kártevő-/betegség-megfigyelési hézag (§11).

### 6.2 Gombabetegség-nyomás

- A **lisztharmat** és a **peronoszpóra** várhatóan intenzívebb, de változékonyabb éveket mutat a melegebb, nedvesebb tavaszok és a forróbb, szárazabb nyarak alatt. A Csopak Kódex szintetikus fungicid tilalma kulcsfontosságú üzemeltetési korláttá teszi a peronoszpóra-kezelést a Balaton partmenti borvidékein [`balatonfured-csopaki.md`].
- A ***Botrytis cinerea*** kettős szerepű szervezet. A tokaji aszú (nemespenész) és a pécsi késői szüretű Cirfandli *eszköze*; másutt *teher*. A `tokaji.md`-ben hivatkozott Bene et al. (2023) bizonyítékot szolgáltat arra, hogy **„a *B. cinerea* életaktivitása a klímaváltozás hatására folyamatosan változik"**, ami mind a savasítási kinetikát, mind a biokémiai profilt megváltoztatja — ami azt jelenti, hogy még ha a nemespenész be is kötődik, az eredményül kapott aszú nem feltétlenül ízlik úgy, mint a történelmi évjáratok.
- A **Bianca** fehér hibrid fő génre alapozott *P. viticola*-rezisztenciát hordoz, de a patogén evolúció Magyarországon már létrehozott egy *Plasmopara*-izolátumot, amely képes ezt a rezisztenciát leküzdeni [`szekszardi.md`] — korai figyelmeztetés arra, hogy a rezisztencia-alapú adaptáció véges számú évet vesz.

### 6.3 Aszály, hőhullámok és talajvíz

- **Tokaj-hegyaljai aszályklimatológia (Kiss et al. 2024, Markov-modell-analízis OMSZ-adatokon 2002–2020):** rövid, rendkívül intenzív csapadékok és hosszabb aszályos időszakok egyre gyakoribbá válnak; a meredek lejtős szőlészet felerősíti a lefolyási veszteségeket [`tokaji.md`].
- **2022-es balatoni vízháztartási szélsőség** — a Balaton vízgyűjtő valaha mért legszárazabb január–júliusa; **1921 óta a legrosszabb negatív vízháztartási esemény** (~100 éves visszatérési idő). A tó 2022 nyarán ~300 millió m³-t veszített párolgásra; a vízszint ~70 cm-rel esett; a felszíni hőmérsékletek meghaladták a 28 °C-ot; a tóvízhőmérsékleti hőhullámok, amelyek az 1990-es években ritkák voltak, ma **akár 100 napig/év** tartanak [`balaton-felvideki.md`; `balatonfured-csopaki.md`].
- **Homokhátsági talajvízszint-csökkenés** — a Duna-Tisza köze talajvízszintje **átlagosan 2–5 m-rel, helyileg 6–10 m-rel csökkent az 1970-es évek óta** (Pálfai, Ladányi et al., Homokhátság aridifikációs irodalom). Ez a legsúlyosabb hidrológiai klímaváltozási jelzés Magyarországon, és közvetlenül érinti Kunságot, nyugati peremén Hajós-Baját és keleti peremén Csongrádot [`kunsagi.md`; `hajos-bajai.md`; `csongradi.md`].
- **Balaton felszíni vízmelegedés:** +0,07 °C évenként 21. századi trend → ~+1,7 °C kumulatívan 2000–2025 között; +2,2 °C ~150 év alatt, ennek nagy része az utóbbi 30–40 évben [`badacsonyi.md`; `balaton-felvideki.md`].
- **Hőhullámok:** Magyarország-szerte az intenzív hőnapok száma **+250–300 %-kal** nőtt 1956–1985 és 1986–2015 között (Sopron-analóg). A kiemelkedő forró évjáratok: 2003, 2012, 2015, 2017, 2019, 2021, 2022, 2023, 2024 [`balatonfured-csopaki.md`; `bukki.md`].
- **Jéggyakoriság és -trend** országos adathézag: egyetlen borvidéki fájl sem jelent szakmailag lektorált, több évtizedes trendelemzést. Az OMSZ jégpárna- és radar-archívumok a nyilvánvaló források [`tokaji.md`; `zalai.md`; és mások].

---

## 7. Eredmények — Jövőbeli projekciók (Lakatos & Nagy 2025 / EURO-CORDEX / FORESEE 4.2)

**[PROJECTED — 14 EURO-CORDEX RCM ensemble, RCP4.5 és RCP8.5, 1971–2000 alap, 2021–2050 és 2071–2100 horizont]**

- **Winkler-osztály váltás:** a magyar borvidékek 1971–2000-ben túlnyomórészt **II. régió („közepes")** voltak, ma már többnyire **III. régió („meleg")**, és a vetítések szerint 2071–2100-ra túlnyomórészt **IV. régióvá („forró")** válnak — az RCP8.5 forró vége **V. régiót** is elér [`balaton-felvideki.md`; `etyek-budai.md`; `tokaji.md`].
- **Tenyészidőszaki hőmérséklet-emelkedés:** **+1,0 °C (optimista modell, RCP4.5) – >+4,0 °C (forró vég RCP8.5)** 2071–2100-ig. A borvidékspecifikus évszázadvégi AGST-emelkedések **+2,44 °C-tól (Sopron) +2,96 °C-ig (Tokaj)** terjednek; Csongrád explicite >+2,5 °C [`balaton-felvideki.md`; `csongradi.md`; `tokaji.md`; `tolnai.md`].
- **GDD-Winkler évszázadvégi emelkedés:** **+475,98 °C·nap (Sopron) – +581,65 °C·nap (Kunság)**, országos átlag +537,23 [`kunsagi.md`; `soproni.md`].
- **Huglin-index évszázadvégi emelkedés:** **+461,58 °C (Sopron) – +566,15 °C (Eger)**, országos átlag +523,8 [`bukki.md`; `soproni.md`].
- **BEDD évszázadvégi emelkedés:** **+182,71 °C·nap (Szekszárd) – +258,49 °C·nap (Bükk)**, országos átlag +204,26 [`bukki.md`].
- **Fajtaalkalmasság-veszteség:** az **alacsony hőigényű fehér fajták** esetében — ezek közé tartozik Tokaj zászlóshajója, a Furmint és a Hárslevelű klasszikus édesbor-kontextusban, és strukturálisan a teljes hűvös borvidéki (Sopron, Etyek-Buda, Mór, Nagy-Somló, Balaton) fehér portfólió — **az alkalmasság az évszázad végére ~29 %-kal csökkenhet** [`tokaji.md`; több más fájl].
- **Csapadék:** RCP4.5 alatt az éves csapadékváltozások 20 % alatt maradnak; RCP8.5 alatt a változások robusztusabbak és a hegyvidéki területeken a legnagyobbak. Észak-Magyarországon nedvesebb telek, szárazabb nyár közepek, közel állandó vagy enyhén csökkenő éves összegek (Mihaljević & Bíró 2025) [`tokaji.md`; `bukki.md`].
- **Regionális gradiens és inverzió:** **Az északi magyar borvidékek melegednek a leggyorsabban**, és a hagyományos termikus rangsor megfordul (ld. §3). A Lakatos & Nagy szerzők explicite javasolják **az OEM-határok és az azon belüli területhasználati struktúra módosítását** — politikailag érzékeny, de tudományosan alátámasztott lehetőség [`balaton-felvideki.md`].

Ábrajavaslat 3: **3. ábra — Az évszázadvégi Winkler-osztályok borvidékenkénti előrejelzése RCP8.5 alatt**, Magyarország térképe 22 borvidéki poligonnal, amelyeket az előrevetített 2071–2100 Winkler-régiójuk (II, III, IV, V) színkóddal jelöl, és nyilak jelzik az 1971–2000 → 2071–2100 osztályváltást a leginkább érintett borvidékekre.

---

## 8. Eredmények — Adaptációs leltár a 22 borvidéken

### 8.1 Aktív kutatás és fajtakísérletek

- **Tokaji Borvidék Kutatóintézet (Tarcal):** a quasi-univerzális **Teleki 5C** alanyt összehasonlító benchmarkelés **140 Ruggeri, 1103 Paulsen és 110 Richter** alanyokkal, Furmintra és Hárslevelűre oltva; műanyag árnyékolóháló a bogyóérés alatt; intelligens talajművelés és tápanyagkezelés [`tokaji.md`].
- **Eger (Misik et al. 2025, MDPI Horticulturae):** **késői metszés** plusz **csúcsi lombtalanítás az érésfordulat után** Kékfrankoson ~2 héttel késlelteti a rügyfakadást és a virágzást, eltolja a cukor–antocianin görbét, és alacsonyabb alkoholtartalmú, jobban megőrzött színű borokat eredményez [`egri.md`].
- **Pécsi Egyetem Szőlőbirtoka:** otthont ad a világ 6. legnagyobb szőlő-génbankjának (~1 500 tétel), beleértve ritka magyar örökségeket — stratégiai genetikai erőforrás-tartalék az adaptációhoz [`pecsi.md`].
- **NAIK-SZBKI Badacsony:** nemesítette a **Rózsakövet** (Kéknyelű × Budai zöld) a Kéknyelű beporzási problémájának megoldására — terroir-megőrző nemesítési válasz, ma 45–47 ha-on és növekszik [`badacsonyi.md`].

### 8.2 Szabályozási válaszok

- **Csopak Kódex (2013-tól, Balatonfüred-Csopak):** **önkéntes, magán terroir-kódex**, amely szigorúbb, mint maga az OEM-specifikáció, csak Olaszrizlingre és Furmintra alkalmazandó, minimum 5,5 g L⁻¹ TA, maximum 4 g L⁻¹ RS, kötelező hozamkorlátokkal és minimum tőkekorral. A `balatonfured-csopaki.md` kifejezetten úgy írja le, hogy „klíma-ellenállóképességi protokoll terroir-kódex formájában" — a legvilágosabb intézményi válasz bármely magyar borvidék részéről a klímaindukált stíluserózióra.
- **Villányi Franc OEM-reform (2014):** szigorította az érési, tölgy- és extrakciós paramétereket az alkohol- és extrakciós kúszás ellensúlyozására [`villanyi.md`].
- **Kunsági Bianca telepítés:** a magyar Bianca ~90 %-a Kunságban van; a fő génre alapozott *P. viticola*-rezisztencia lehetővé teszi **2–4 permetezést/szezonban a 8–14 helyett** a *V. vinifera* fehérek esetében; a Bianca a borvidék egyetlen legfontosabb klíma-adaptációs eszköze [`kunsagi.md`].

### 8.3 Fajtahelyettesítés és mediterrán technológiaimport

- **Tolna (Tűzkő Birtok / Antinori):** Marchese Piero Antinori 2000-ben megvásárolta Tűzkőt; a birtok Magyarország legvilágosabb esete egyetlen külföldi befektető birtokának **mediterrán technológiaimport-csatornaként** való működésére, alkalmazva éjszakai szüretet, hűtött láncú szállítást, fordított ozmózisos alkoholmentesítést, csepegtető öntözést, valamint egy fehér portfóliót (Grüner Veltliner, Pinot Grigio, Tramini, Chardonnay, Sauvignon Blanc), amely már önmagában klíma-adaptív fedezet. A hihető következő lépés mediterrán fehérek (Vermentino, Viognier) az Antinori csoport tapasztalatán belül vannak [`tolnai.md`].
- **Mátra:** Syrah, Tempranillo és Gamay kísérletek termelői szinten; még nem OEM-regisztráltak [`matrai.md` borvidéki szintézisen keresztül].
- **Furmint-export:** **Ausztria kifejezetten klímafedezetként kezdett Furmintot telepíteni**, ironikus módon átvéve Tokaj zászlóshajófajtáját akkor, amikor maga Tokaj újragondolja termékportfólióját [`tokaji.md`].
- **PIWI-fajták:** Bianca, Souvignier Gris és Solaris megfontolás tárgya Bükkben és Kunságban a permetigény csökkentésére [`bukki.md`; `kunsagi.md`].

### 8.4 Identitásvédelem vs. adaptáció kompromisszum

A borvidéki fájlok ismételten felhozzák az **identitásvédelem** (őshonos fajták és hagyományos stílusok megőrzése) és az **adaptáció** (helyettesítésük vagy módosításuk) közötti feszültséget. A szélsőséges esetek:

- Nagy-Somló Juhfark: 80–150 ha a globális ~100–170 ha-ból. **A somlói stílusdrift világszerte a fajta stílusdriftje.** Nincs hűvösklíma-menedék [`nagy-somloi.md`].
- Móri Ezerjó: Mór egy olyan fajta „szellemi otthona", amely országosan már összeomlott >14 000 ha-ról (1970) 1 655 ha-ra (közelmúlt) [`mori.md`].
- Pécsi Cirfandli: 13,9 ha, −40 % 5 év alatt, termelői jelentésű minőségjavulás ellenére 2/10-ről 6/10 évjáratra. A gazdasági trend és az éghajlati trend **szétkapcsolódik** [`pecsi.md`].
- Tokaji aszú: a nemespenész megbízhatósága csökken még akkor is, amikor a Furmint és a Hárslevelű maguk viszonylag aszálytűrők maradnak [`tokaji.md`].

---

## 9. Diszkusszió

### 9.1 Kétélű fegyver a hűvös éghajlatú borvidékeknek; egzisztenciális kérdés a forró borvidékeknek

A 22 borvidéki elemzés egységes üzenete, hogy **a klímaváltozás nem egyenletes degradációt okoz a magyar szőlészetben; két minőségileg különböző krízist produkál**.

A **hűvös éghajlatú borvidékek** (Sopron, Etyek-Buda, Mór, Nagy-Somló, Pannonhalma, Neszmély, Zala, Balaton északi part, és kisebb mértékben Bükk és Eger) **kétélű fegyverrel** néznek szembe: a melegedés növeli az érés megbízhatóságát, és megmenti a történelmileg marginális, későn érő cultivarokat (Juhfark, Cirfandli, Ezerjó) a krónikus éretlen-évjárat problémától, ugyanakkor erodálja azt a **hűvösséget**, amelyre ezek a borvidékek a roppanós savasságért, mérsékelt alkoholtartalomért és klasszikus szerkezetért kiépítették hírnevüket. Etyek-Buda a legtisztább példa: a melegedés **egyértelműen degradációs jelzés** a pezsgőalap szempontjából, mert a borvidék *raison d'être*-je a hűvössége [`etyek-budai.md`]. Nagy-Somló Juhfark rövid távon érési biztosítást nyer, de hosszú távon elveszítheti a hasító savasságot, amely *ténylegesen* a piaci identitása [`nagy-somloi.md`]. A pécsi Cirfandli a legvilágosabb termelői által számszerűsített „nyertes" az adatállományban (2/10 → 6/10 kiemelkedő évjárat), a hektárszáma mégis összeomlik [`pecsi.md`]. A „klímanyertes" minősítés ezekre a borvidékekre tehát feltételes: a szőlőkémián nyernek, a stílusidentitáson vesztenek, és nem világos, melyik tengely dominál évszázad közepén.

A **forró borvidékek** (Csongrád, Kunság, Hajós-Baja, valamint Villány és Szekszárd forró vége) alapvetően másfajta problémával szembesülnek: **egzisztenciális életképesség**. Az antocianin hőösszeomlás ≥35 °C-nál, a cukor/fenolos szétkapcsolódás, a pH mikrobiológiai stabilitási küszöb fölé emelkedése, a 2–5 m-es Homokhátsági talajvízszint-csökkenés, valamint az öntözési infrastruktúra nélküli csapadékfüggő kistermelői szerkezet együttesen arra a kérdésre vezetnek, hogy nem *„milyen borstílus?"*, hanem *„lehetséges-e még itt kereskedelmi szőlészetet folytatni?"*. Csongrád telepített területe már ~2 500 ha-ról ~1 500–2 000 ha-ra zsugorodott két évtized alatt [`csongradi.md`]; a borvidéki elemzés az őszinte hosszú távú forgatókönyvet kifejezetten **„szabályozott visszavonulásként"** fogalmazza meg, a legszárazabb Homokhátsági magok fokozatos szőlőfelhagyásával.

### 9.2 Szabályozási szűk keresztmetszetek

Három szűk keresztmetszet visszatérő:

1. **Az öntözés jogilag korlátozott.** A magyar vízjog a szőlőöntözést a gyakorlatban valóban nehézzé teszi. Minden vízre vonatkozó borvidéki elemzés (`tokaji.md`, `csongradi.md`, `kunsagi.md`, `tolnai.md`, `balatonfured-csopaki.md`) ezt jelöli meg az adaptáció legnagyobb szakpolitikai akadályaként. A magyar szőlészeti kutatóközösség lényegében egyhangú abban, hogy enyhíteni kell az öntözési jogi feltételeket.
2. **OEM-merevség vs. szükséges fajtaváltások.** Az OEM-ek meghatározzák az engedélyezett cultivarokat; klímanyomás alatt ezek a cultivarok éghajlatilag szuboptimálissá válhatnak, miközben jogilag továbbra is az OEM meghatározó elemei maradnak. Lakatos & Nagy (2025) explicite javasolják az OEM-határok és az azon belüli területhasználati struktúra módosítását. A Villányi Franc 2014-es reformja és a Csopak Kódex a két magyar példa arra, hogy a szabályozás a klíma elé megy; a szélesebb OEM-architektúra nem.
3. **A tó mezoklímáját az EURO-CORDEX 12 km nem oldja fel.** A hat balatoni OEM tóindukált termikus pufferelésen és páratartalom-szabályozáson múlik, amely rácson aluli skálán működik. Amíg a FORESEE / EURO-CORDEX ensemble-ök nem leskálázottak a Balaton és a Fertő mezoklímájára, a Badacsony, Balaton-felvidék, Balatonfüred-Csopak, Balatonboglár, Nagy-Somló és Sopron projekciói továbbra is nem kvantifikált pufferelési bizonytalanságot hordoznak.

---

## 10. Vitatott megállapítások

A borvidéki elemzések ismételten öt kiemelt vitatott megállapítást jelölnek, ahol további munkára van szükség, mielőtt a szintézis megszilárdítható lenne:

1. **Bene et al. (2023) Tokaj polifenol-nem-trend.** A globális melegedés-hajtja-a-fenolokat elvárással szemben ez a tokaji-specifikus botritizált-bor tanulmány *nem* talál kimutatható klímavezérelt polifenolnövekedést, és a teljes <200 mg L⁻¹-es Furmint-fenolos szintet szándékos borászati választásnak tulajdonítja. Vagy (a) valódi terroir-specifikus kivétel, (b) egy valós klímajelzést elfedő stilisztikai műtermék, vagy (c) mintavételi műtermék. Független replikációra van szükség [`tokaji.md`].
2. **„Klímanyertesek" minősítés hűvös borvidékek esetén.** A pécsi Cirfandli (2/10 → 6/10), nagy-somlói Juhfark, bükki Kékfrankos és egri Bikavér eseteket klímaváltozási érés-biztosítás haszonélvezőiként hivatkozzák, miközben a megfelelő hektárszámok és identitásmutatók összeomlóban vagy kockázatban vannak. Nyitott kérdés, hogy ezek a borvidékek évszázad közepén és végén **nettó nyertesek vagy vesztesek** [`pecsi.md`; `nagy-somloi.md`; `bukki.md`; `egri.md`].
3. **A száraz-bor pivot Tokajon — klímavezérelt vagy piacvezérelt?** Mindkét erő ugyanarra mutat (az alacsonyabb őszi páratartalom a száraz stílusoknak kedvez; a globális fogyasztói piacok a száraz Furmint/Hárslevelűt jutalmazzák az édes aszú rovására). Az irodalom felcserélhetően kezeli őket. Szétválasztásuk elengedhetetlen az adaptációs tervezéshez [`tokaji.md`].
4. **A borvidékenkénti Lakatos & Nagy (2025) táblázatok nem szerepelnek a nyílt hozzáférésű főszövegben.** A kiemelt borvidék-specifikus számok (Csongrád > +2,5 °C AGST, Bükk +258,49 °C BEDD, Kunság +581,65 °C·nap GDD, Sopron +66,16 és +475,98 GDD, Tokaj +173,96 és +2,96 °C AGST, Eger +566,15 Huglin, Pannonhalma +2,3 °C) megbízhatóan szerepelnek a borvidéki elemzésekben, de a többi borvidék értékei kiegészítő anyagtól függenek, amelyeket még nem nyertek ki nyilvános adatállományba. A nem-szélsőséges borvidékek rangsorolása tehát ideiglenes [`csongradi.md`; `bukki.md`; `etyek-budai.md`; `balaton-felvideki.md`].
5. **Móri-szél trend.** A móri borvidék teljes reziliencianarratívája egy állandó szellőztető szélen nyugszik, amelynek statisztikai klimatológiáját szőlőmagasságban **soha nem publikálták**. A globális modellek „stilling"-je csendes, elsőrendű degradációja lenne a borvidék adaptív kapacitásának — és jelenleg nem mérhető [`mori.md`].

---

## 11. Tudáshézagok és országos kutatási menetrend

Minden borvidéki elemzés 5–12 egyénileg jelölt tudáshézaggal zárul; ezek konszolidálásával prioritásba rendezett országos kutatási menetrendet kapunk.

**A prioritás — Adatközzététel és reanalízis**
1. **A Lakatos & Nagy (2025) AGST / GDD / Huglin / BEDD táblázatainak borvidékenkénti kinyerése és közzététele** mind a 22 borvidékre, évtizedes felbontással, RCP4.5 és RCP8.5 alatt, nyílt adatállományként. Ezt legalább 8 borvidéki fájl kiemelt prioritásként jelöli, és azonnal felszabadítaná a borvidéki szintű döntéshozatalt.
2. **Szisztematikus fenológiai sorozatok a 20 olyan borvidékre, ahol nincs publikált több évtizedes nyilvántartás** (azaz mindenütt, Sopron/Zala és Tokaj kivételével). Célváltozók: rügyfakadás, virágzás, érésfordulat, szüret a borvidék meghatározó cultivarai számára. Egy NAIK-SZBKI, PTE Pécs, Egri Kutatóintézet és termelői nyilvántartások (különösen a Kreinbacher/Tornai/Fekete/Somlói Apátsági archívumok Somlón és az Antinori/Tűzkő-nyilvántartások Tolnán) alapú föderált erőfeszítés a hézag nagy részét ~3 év alatt feltöltené.

**B prioritás — Mezoskála és helyi klimatológia**
3. **Csatolt tó–szőlő mezoklíma-leskálázás a Balatonra** (és a Fertőre/Neusiedler See-re Sopron esetében). Az EURO-CORDEX 12 km nem oldja fel a tó pufferelését, amely hat OEM alapját képezi.
4. **A Móri-szél statisztikai klimatológiája szőlőmagasságban** — irányrózsák, sebességeloszlások, több évtizedes trend. Kritikus, tekintettel a szél központi szerepére Mór reziliencianarratívájában.
5. **OMSZ jégklimatológia a borvidékekre** — gyakoriság és trend, jégpárna- és radararchívumok felhasználásával.
6. **Helyi OMSZ állomásreanalízis** a tokaji alaphőmérsékleti ellentmondás (9,8 °C 1961–1990 vs. ~14 °C közelmúlt) és más borvidékek analóg referencia-időszakbeli kérdéseinek feloldására.

**C prioritás — Biológiai monitoring**
7. **Borvidéki szintű kártevő- és betegségmegfigyelés** a *Drosophila suzukii*, *Halyomorpha halys* és *Scaphoideus titanus* (Flavescence dorée vektora) számára. Országos jelenlét megerősítve; borvidéki szintű kárfelmérések mindenhol hiányoznak.
8. **Szőlőkémiai idősorok** (°Brix, pH, TA, YAN, antocianinok, terpének, tiolok) a borvidékmeghatározó fajtákra — szinte minden borvidéki elemzésben hézagként jelölt. Kritikus a somlói Juhfark (amelynek USP-je a savasság), a móri Ezerjó, a pécsi Cirfandli, a balatoni Olaszrizling, az egri/soproni/szekszárdi Kékfrankos és a tokaji Furmint/Hárslevelű esetében.
9. **Talaj-víz-egyensúly modellezés, amely a Homokhátság talajvízszint-csökkenését a szőlő gyökérzónájának vízhiányához köti** parcella-szinten Kunság, Hajós-Baja és Csongrád esetében.
10. **Kvantitatív talajerózió-mérések** tokaji meredek lejtős szőlőkön intenzívebb konvektív csapadék alatt.

**D prioritás — OEM-architektúra és adaptációs politika**
11. **Az OEM-határ és az engedélyezett fajtalista módosításának szisztematikus értékelése** klíma-adaptációs eszközként — közvetlenül Lakatos & Nagy (2025)-től származó ajánlás.
12. **Csopak Kódex megfelelési arány idősora** mint valós klíma-kompatibilitási stressz-indikátor [`balatonfured-csopaki.md`].

---

## 12. Következtetések

A klímaváltozás nem egyenletesen zavarja meg a magyar szőlészetet. A 22 borvidéken **térben megfordított, fajtaspecifikusan célzott, stilisztikailag kettéváló** hatásokat termel. Az országos felmelegedési gradiens **északon és keleten a legerősebb** (Csongrád, Kunság, Tokaj, Eger, Bükk, Mátra) és **nyugaton a leggyengébb** (Sopron, Pannonhalma) — az ország hagyományos szőlészeti rangsorának fordítottja. Az előrevetített egyetlen legnagyobb abszolút változások: Kunság GDD **+581,65 °C·nap**, Bükk BEDD **+258,49 °C·nap**, Eger Huglin **+566,15 °C**, Tokaj AGST **+2,96 °C**, Csongrád AGST **> +2,5 °C**; a legkisebbek: Sopron GDD **+66,16 °C·nap** (történelmi) / **+475,98 °C·nap** (előrevetített), és Pannonhalma AGST **+2,3 °C**.

A megfigyelt kémiai jelzés — 55–60 g L⁻¹ mustcukor-többlet a hűvös borvidékek fehérborainál, −1,5 – −2,5 g L⁻¹ TA Chardonnay-ban 1980–2020 között, alkoholkúszás ~12 %-ról ≥14,5 tf%-ra a zászlóshajó pannon vörösöknél, Mori-mechanizmusú antocianinösszeomlás Kadarkában és Kékfrankosban — már most beíródik a magyar borstílusokba, és korai szabályozási válaszokat vált ki Csopakon (2013-as önkéntes Kódex), Villányban (2014-es Villányi Franc OEM-reform) és Kunságban (Bianca-helyettesítés). A fajtakihalási taxonómia egyedülállóan éles: Magyarország őshonos cultivarainak az országon kívül nincs hűvösklíma-menedékük (Somlói Juhfark, Móri Ezerjó, Pécsi Cirfandli, Badacsonyi Kéknyelű), és hektárszámuk vagy összeomlóban van (Ezerjó, Cirfandli), vagy egyetlen erodált bazaltbütykön koncentrálódik (Juhfark).

Két stratégiai következtetés adódik. Először: a politikailag legérzékenyebb, de tudományosan legmegalapozottabb adaptációs eszköz **az OEM-architektúra módosítása**, hogy lehetővé tegye a fajta- és stílusváltást az eredetvédett státusz elvesztése nélkül — ezt az ajánlást közvetlenül Lakatos & Nagy (2025) tette, és a borvidéki elemzések visszhangozzák. Másodszor: **az öntözési jogi korlátozások enyhítése** a legtöbbet kért szakpolitikai változtatás a magyar szőlészeti kutatóközösségben, és aránytalanul nagy hasznot hozna a leginkább kitett borvidékeknek (Csongrád, Kunság, Hajós-Baja, Tolna, forró Villány).

A 22 itt konszolidált borvidéki elemzést pillanatfelvételként kell olvasni — részletes, keresztreferált, és őszinte azzal kapcsolatban, ami ismert, vitatott és hiányzó. A §11 kutatási menetrendje ezt a pillanatfelvételt operatív klíma-adaptációs döntéstámogató rendszerré alakítaná a magyar bor számára.

---

## Hivatkozások

*A 22 borvidéki bizonyítékelemzésből konszolidálva és deduplikálva (`C:\Bor-szőlő\research\districts\`). A hiperlinkek a kiinduló borvidéki fájlokban megőrződnek.*

### Központi horgony

- **Lakatos L. & Nagy R. (2025).** Assessment of historical and future changes in temperature indices for winegrape suitability in Hungarian wine regions (1971–2100). *Frontiers in Plant Science* 16: 1481431. doi:10.3389/fpls.2025.1481431. (Egyes borvidéki fájlokban „Kovács et al. 2025" néven is idézve; a DOI azonos.) [Frontiers](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1481431/full) · [PMC11842426](https://pmc.ncbi.nlm.nih.gov/articles/PMC11842426/)

### Éghajlat és hidrológia

- Spinoni J. et al. (2015). Heat and cold waves trends in the Carpathian Region from 1961 to 2010. *Int. J. Climatol.*
- Mihaljević B. & Bíró L. (2025). Evaluation of different bias-corrected EURO-CORDEX databases and the expected future changes in precipitation over Hungary. *Sci. Tot. Environ.*
- Kiss T. et al. (2024). Study of drought periods in the Tokaj-Hegyalja wine region. *Prog. Agric. Eng. Sci.* 20(1): 113.
- Pálfai I., Ladányi Z. et al. — Homokhátsági aridifikációs irodalom: talajvízszint-csökkenés 2–5 m (helyileg 6–10 m) az 1970-es évek óta a Duna-Tisza közén.
- OMSZ — Országos Meteorológiai Szolgálat rácsos és állomási termékek.
- FORESEE 4.0 / 4.2 torzításkorrigált klímaadatbázis (ELTE).
- EURO-CORDEX CMIP5 regionális leskálázási ensemble.
- CARPATCLIM Kárpát-régiós reanalízis.
- Klímapolitikai Intézet (2023, 2024). Technikai jelentések a magyarországi klímaváltozásról, hűvös borvidéki cukortöbblet- és felmelegedési ráta-kvantifikációval.

### Szőlészet, fenológia, kémia

- Kovács E., Puskás J. & Pozsgai A. (2016). Positive Effects of Climate Change on the Field of Sopron Wine-Growing Region in Hungary. *Springer*. — a legközelebbi publikált többévtizedes magyar fenológiai sorozat (Sopron/Zala 1956–1985 vs. 1986–2015).
- Szenteleki K. et al. (2009). Wine Quantity and Quality Variations in Relation to Climatic Factors in the Tokaj (Hungary) Winegrowing Region. *Am. J. Enol. Vitic.* 60(3): 312–321.
- Bene Z. et al. (2023). Impact of climate change on the (poly)phenol composition of botrytization in the Tokaj wine region. *Auctores Online.*
- Magyar I. et al. (2025). Long-term compositional profiling of historical Tokaji aszú wines. *npj Science of Food.*
- Misik et al. (2024/2025). Late pruning and apical defoliation on Eger Kékfrankos. *MDPI Horticulturae.*
- Mesterházy I. et al. (2018, 2022). Hungarian phenology and quadratic dryness–yield model. *MDPI Climate.*
- Mori K., Goto-Yamamoto N., Kitayama M. & Hashizume K. (2007). Loss of anthocyanins in red-wine grape under high temperature. *J. Exp. Bot.* 58(8): 1935–1945.
- Lakatos L. et al. *Possible methods of adaptation to the effects of climate change in the Tokaj Wine Region.* IVES Open Science.

### Biotikus stresszorok

- Kiss A. et al. (2012). First record of *Drosophila suzukii* in Hungary.
- Ioriatti C. et al. (2018). Invasive *Drosophila suzukii* facilitates *Drosophila melanogaster* infestation and sour rot outbreaks in the vineyards. *R. Soc. Open Sci.*
- Vétek G. et al. (2014). First record of the brown marmorated stink bug, *Halyomorpha halys*, in Hungary. *Zootaxa* 3780.
- *The invasive brown marmorated stink bug ... is now widespread in Hungary.* *Entomologia Generalis* (2017).
- Salinari F. et al. — Effect of climate change on infection of grapevine by downy and powdery mildew.

### Áttekintő és szakpolitikai munkák

- Ahmed M., Seleiman M. F. et al. A Review of the Potential Climate Change Impacts and Adaptation Options for European Viticulture. *Appl. Sci.* 10: 3092.
- The Impact of Climate Change on Eastern European Viticulture: Smart Irrigation and Water Management. *Horticulturae* 11(11): 1282.
- Adaptation to Climate Change in Viticulture: The Role of Varietal Selection. *Plants* 14(1): 104.
- Kovács E. et al. (2025). The Impact of Climate Change on Wine Tourism from the Perspective of Hungarian Organic Wineries. *European Countryside.*
- Gaál M. et al. Hungarian wine regions modelling. *Applied Ecology and Environmental Research.*

### Ipari és intézményi források

- Csopak Kódex (2013-tól) — önkéntes magán terroir-/minőségi kódex, Balatonfüred-Csopak OEM.
- Villányi Franc OEM-reform (2014) — érés, tölgy és extrakció szigorítása.
- Wines of Hungary, bor.hu, Taste Hungary — borvidéki adatlapok és fajtaleírások, amelyeket a terroir- és termelői tényekhez használtunk.
- OMSZ éghajlat portal — https://omsz.met.hu/eghajlat/
- NAIK-SZBKI Tarcal (Tokaji Borvidék Kutatóintézet) — alany- és árnyékolási kísérletek.
- Pécsi Egyetem Szőlőbirtoka (PTE Szőlészeti és Borászati Kutatóintézet) — génbank, Cirfandli-kísérletek.
- Tokaji Borvidék / Wines of Tokaj — https://winesoftokaj.hu
- Tűzkő Birtok / Antinori — https://tuzkobirtok.hu/en/

### Forrás borvidéki fájlok (22)

A szintézis minden állítása visszavezethető a megfelelő borvidéki elemzésre (`C:\Bor-szőlő\research\districts\`):
`badacsonyi.md`, `balaton-felvideki.md`, `balatonboglari.md`, `balatonfured-csopaki.md`, `bukki.md`, `csongradi.md`, `egri.md`, `etyek-budai.md`, `hajos-bajai.md`, `kunsagi.md`, `matrai.md`, `mori.md`, `nagy-somloi.md`, `neszmelyi.md`, `pannonhalmi.md`, `pecsi.md`, `soproni.md`, `szekszardi.md`, `tokaji.md`, `tolnai.md`, `villanyi.md`, `zalai.md`.

---

*Szintézis összeállítva 2026-04-07. Narratív meta-szintézis 22 borvidéki szintű bizonyítékelemzésről (~123 000 szó, ~1 200 forrás), amely az első OEM-felbontású klímahatás-audit a magyar szőlészetről. A bizonyítékok végig [OBSERVED] / [PROJECTED] / [HU-AGGREGATE] címkével jelölve. Központi kvantitatív horgony: Lakatos L. & Nagy R. (2025), Frontiers in Plant Science 16:1481431.*
