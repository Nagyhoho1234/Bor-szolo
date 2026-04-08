// District + region metadata. Compiled once from
// analysis/config/districts.yml + analysis/curated/wine_districts.geojson.
//
// This is a pure TypeScript module (no runtime data loading) so it can be
// safely imported from Server Components, generateStaticParams, and the
// client bundle.

export type Borregio =
  | 'Balaton'
  | 'Felső-Pannon'
  | 'Duna'
  | 'Felső-Magyarországi'
  | 'Pannon'
  | 'Tokaj';

export type BorvidekMeta = {
  borvidek: string; // Hungarian name, exact spelling
  borregio: Borregio;
  slug: string; // URL slug, lowercase ASCII
  nameEn: string; // English display name
  nSettlements: number;
  areaKm2: number;
  centroid: [number, number]; // [lon, lat]
  principalVarieties: string[];
  flagshipStyles: string[];
  notes: string;
};

export type BorregioMeta = {
  borregio: Borregio;
  slug: string;
  nameEn: string;
};

// ----- slugify helper -----
// Strip diacritics, collapse anything non-alphanumeric to hyphens.
export function slugify(s: string): string {
  return s
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // combining marks
    .replace(/ő|Ő/g, 'o')
    .replace(/ű|Ű/g, 'u')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// ----- BORREGIO -----
export const BORREGIO_LIST: BorregioMeta[] = [
  { borregio: 'Balaton', slug: 'balaton', nameEn: 'Balaton' },
  { borregio: 'Felső-Pannon', slug: 'felso-pannon', nameEn: 'Upper Pannonia' },
  { borregio: 'Duna', slug: 'duna', nameEn: 'Danube' },
  {
    borregio: 'Felső-Magyarországi',
    slug: 'felso-magyarorszagi',
    nameEn: 'Upper Hungary',
  },
  { borregio: 'Pannon', slug: 'pannon', nameEn: 'Pannonia' },
  { borregio: 'Tokaj', slug: 'tokaj', nameEn: 'Tokaj' },
];

// Tailwind-friendly hex palette (viridis-adjacent)
export const BORREGIO_COLORS: Record<Borregio, string> = {
  Balaton: '#2563eb', // deep blue (lake)
  'Felső-Pannon': '#0d9488', // teal
  Duna: '#65a30d', // lime-green (plains)
  'Felső-Magyarországi': '#9333ea', // purple
  Pannon: '#dc2626', // red (reds country)
  Tokaj: '#d97706', // amber (aszú)
};

// ----- BORVIDEK (22) -----
export const BORVIDEK_LIST: BorvidekMeta[] = [
  {
    borvidek: 'Badacsonyi',
    borregio: 'Balaton',
    slug: 'badacsonyi',
    nameEn: 'Badacsony',
    nSettlements: 12,
    areaKm2: 217.6,
    centroid: [17.5048, 46.8663],
    principalVarieties: [
      'Olaszrizling',
      'Kéknyelű',
      'Szürkebarát',
      'Rajnai rizling',
      'Rizlingszilváni',
      'Budai zöld',
      'Furmint',
    ],
    flagshipStyles: ['mineral white', 'Kéknyelű', 'volcanic Olaszrizling'],
    notes:
      'Volcanic basalt hills on the north shore of Lake Balaton; the historic home of Kéknyelű and powerful, mineral whites.',
  },
  {
    borvidek: 'Balatonboglári',
    borregio: 'Balaton',
    slug: 'balatonboglari',
    nameEn: 'Balatonboglar',
    nSettlements: 42,
    areaKm2: 1194.7,
    centroid: [17.6411, 46.5864],
    principalVarieties: [
      'Chardonnay',
      'Királyleányka',
      'Olaszrizling',
      'Cabernet sauvignon',
      'Merlot',
      'Kékfrankos',
      'Pinot noir',
    ],
    flagshipStyles: ['fresh white', 'Chardonnay', 'light red'],
    notes:
      'South-shore Balaton district with gentler slopes; a broad mix of international whites and lighter reds, much of it from cooperatives.',
  },
  {
    borvidek: 'Balatonfelvidéki',
    borregio: 'Balaton',
    slug: 'balatonfelvideki',
    nameEn: 'Balaton Uplands',
    nSettlements: 23,
    areaKm2: 488.7,
    centroid: [17.3655, 46.8917],
    principalVarieties: [
      'Olaszrizling',
      'Szürkebarát',
      'Tramini',
      'Rajnai rizling',
      'Sauvignon blanc',
      'Chardonnay',
      'Muscat ottonel',
    ],
    flagshipStyles: ['aromatic white', 'Olaszrizling'],
    notes:
      'Cool, hilly district north-west of Lake Balaton with mixed volcanic and limestone soils; primarily white wines.',
  },
  {
    borvidek: 'Balatonfüred-Csopaki',
    borregio: 'Balaton',
    slug: 'balatonfured-csopaki',
    nameEn: 'Balatonfüred-Csopak',
    nSettlements: 26,
    areaKm2: 471.3,
    centroid: [17.9089, 46.9784],
    principalVarieties: [
      'Olaszrizling',
      'Rajnai rizling',
      'Furmint',
      'Szürkebarát',
      'Tramini',
      'Sauvignon blanc',
    ],
    flagshipStyles: ['Csopak Olaszrizling', 'mineral white'],
    notes:
      'North-shore Balaton district famous for tightly-defined, terroir-driven Olaszrizling under the Csopak Kódex appellation rules.',
  },
  {
    borvidek: 'Bükki',
    borregio: 'Felső-Magyarországi',
    slug: 'bukki',
    nameEn: 'Bükk',
    nSettlements: 23,
    areaKm2: 1010.3,
    centroid: [20.7315, 48.0773],
    principalVarieties: [
      'Olaszrizling',
      'Leányka',
      'Királyleányka',
      'Chardonnay',
      'Müller-Thurgau',
      'Cserszegi fűszeres',
    ],
    flagshipStyles: ['fresh white'],
    notes:
      'Small cool district on the southern flank of the Bükk mountains; crisp whites in an Egri-adjacent style.',
  },
  {
    borvidek: 'Csongrádi',
    borregio: 'Duna',
    slug: 'csongradi',
    nameEn: 'Csongrád',
    nSettlements: 19,
    areaKm2: 1894.4,
    centroid: [20.1426, 46.3936],
    principalVarieties: [
      'Kékfrankos',
      'Kadarka',
      'Olaszrizling',
      'Cserszegi fűszeres',
      'Generosa',
    ],
    flagshipStyles: ['light red', 'sandy-soil white'],
    notes:
      'Hot, sandy district along the Tisza in the south-east; phylloxera-free sands grow light reds and easy-drinking whites.',
  },
  {
    borvidek: 'Egri',
    borregio: 'Felső-Magyarországi',
    slug: 'egri',
    nameEn: 'Eger',
    nSettlements: 19,
    areaKm2: 569.2,
    centroid: [20.3408, 47.9029],
    principalVarieties: [
      'Kékfrankos',
      'Kadarka',
      'Cabernet franc',
      'Cabernet sauvignon',
      'Merlot',
      'Pinot noir',
      'Olaszrizling',
      'Leányka',
      'Hárslevelű',
    ],
    flagshipStyles: ['Egri Bikavér', 'Egri Csillag', 'Pinot noir'],
    notes:
      "Famous for Egri Bikavér (Bull's Blood) red blend and the white Egri Csillag blend; volcanic tuff soils, cool nights, long aging in tuff cellars.",
  },
  {
    borvidek: 'Etyek-Budai',
    borregio: 'Felső-Pannon',
    slug: 'etyek-budai',
    nameEn: 'Etyek-Buda',
    nSettlements: 26,
    areaKm2: 921.5,
    centroid: [18.6968, 47.4056],
    principalVarieties: [
      'Chardonnay',
      'Sauvignon blanc',
      'Királyleányka',
      'Olaszrizling',
      'Pinot noir',
      'Zöld veltelíni',
    ],
    flagshipStyles: ['sparkling base', 'fresh Chardonnay'],
    notes:
      'Cool limestone district close to Budapest; the principal source of base wine for Hungarian sparkling (pezsgő) and crisp Chardonnay.',
  },
  {
    borvidek: 'Hajós-Bajai',
    borregio: 'Duna',
    slug: 'hajos-bajai',
    nameEn: 'Hajós-Baja',
    nSettlements: 17,
    areaKm2: 1085.2,
    centroid: [18.9778, 46.2395],
    principalVarieties: [
      'Kadarka',
      'Kékfrankos',
      'Cabernet sauvignon',
      'Olaszrizling',
      'Chardonnay',
    ],
    flagshipStyles: ['Hajós red', 'sandy red'],
    notes:
      'Loess and sandy district between the Danube and the Bács hills; traditional Kadarka and crisp whites from cellar villages.',
  },
  {
    borvidek: 'Kunsági',
    borregio: 'Duna',
    slug: 'kunsagi',
    nameEn: 'Kunság',
    nSettlements: 110,
    areaKm2: 8232.1,
    centroid: [19.5608, 47.0173],
    principalVarieties: [
      'Kékfrankos',
      'Kadarka',
      'Cserszegi fűszeres',
      'Olaszrizling',
      'Generosa',
      'Arany sárfehér',
      'Bianca',
    ],
    flagshipStyles: ['bulk white', 'light red'],
    notes:
      "Hungary's largest wine district by area; sandy Great Plain producing high volumes, with a focus on light, fruity wines and resistant new varieties.",
  },
  {
    borvidek: 'Mátrai',
    borregio: 'Felső-Magyarországi',
    slug: 'matrai',
    nameEn: 'Mátra',
    nSettlements: 35,
    areaKm2: 1173.8,
    centroid: [19.6736, 47.7499],
    principalVarieties: [
      'Olaszrizling',
      'Rizlingszilváni',
      'Hárslevelű',
      'Tramini',
      'Chardonnay',
      'Sauvignon blanc',
      'Cserszegi fűszeres',
    ],
    flagshipStyles: ['aromatic white', 'fresh Olaszrizling'],
    notes:
      "Hungary's second-largest district, on the southern slopes of the Mátra; predominantly whites at moderate altitude.",
  },
  {
    borvidek: 'Móri',
    borregio: 'Felső-Pannon',
    slug: 'mori',
    nameEn: 'Mór',
    nSettlements: 6,
    areaKm2: 250.4,
    centroid: [18.2676, 47.3685],
    principalVarieties: [
      'Ezerjó',
      'Tramini',
      'Rajnai rizling',
      'Chardonnay',
      'Leányka',
    ],
    flagshipStyles: ['Móri Ezerjó', 'aromatic white'],
    notes:
      'Small cool district between the Vértes and Bakony hills; historic home of Ezerjó.',
  },
  {
    borvidek: 'Nagy-Somlói',
    borregio: 'Balaton',
    slug: 'nagy-somloi',
    nameEn: 'Somló',
    nSettlements: 10,
    areaKm2: 167.7,
    centroid: [17.2526, 47.1843],
    principalVarieties: [
      'Juhfark',
      'Olaszrizling',
      'Furmint',
      'Hárslevelű',
      'Tramini',
    ],
    flagshipStyles: ['Juhfark', 'volcanic mineral white'],
    notes:
      'Tiny volcanic single-hill district; the historic home of Juhfark and famously long-lived, austere mineral whites.',
  },
  {
    borvidek: 'Neszmélyi',
    borregio: 'Felső-Pannon',
    slug: 'neszmelyi',
    nameEn: 'Neszmély',
    nSettlements: 28,
    areaKm2: 887.7,
    centroid: [18.3459, 47.631],
    principalVarieties: [
      'Olaszrizling',
      'Cserszegi fűszeres',
      'Sauvignon blanc',
      'Chardonnay',
      'Irsai Olivér',
      'Királyleányka',
    ],
    flagshipStyles: ['fresh aromatic white'],
    notes:
      'Danube-side district producing fresh, fruity whites, heavily focused on aromatic and modern international varieties.',
  },
  {
    borvidek: 'Pannonhalmi',
    borregio: 'Felső-Pannon',
    slug: 'pannonhalmi',
    nameEn: 'Pannonhalma',
    nSettlements: 16,
    areaKm2: 501.9,
    centroid: [17.7034, 47.5716],
    principalVarieties: [
      'Olaszrizling',
      'Rajnai rizling',
      'Tramini',
      'Sauvignon blanc',
      'Királyleányka',
      'Chardonnay',
    ],
    flagshipStyles: ['monastic white blend', 'Riesling'],
    notes:
      'Small district centred on the millennium-old Benedictine abbey; almost exclusively whites in a cool, fresh style.',
  },
  {
    borvidek: 'Pécsi',
    borregio: 'Pannon',
    slug: 'pecsi',
    nameEn: 'Pécs',
    nSettlements: 34,
    areaKm2: 847.1,
    centroid: [18.302, 46.0725],
    principalVarieties: [
      'Cirfandli',
      'Olaszrizling',
      'Chardonnay',
      'Pinot blanc',
      'Cabernet sauvignon',
      'Kékfrankos',
    ],
    flagshipStyles: ['Cirfandli', 'fresh white'],
    notes:
      'South-western Pannon district on the slopes of the Mecsek; a rare home of Cirfandli (Zierfandler) and a mix of whites and reds.',
  },
  {
    borvidek: 'Soproni',
    borregio: 'Felső-Pannon',
    slug: 'soproni',
    nameEn: 'Sopron',
    nSettlements: 18,
    areaKm2: 507.4,
    centroid: [16.6512, 47.4858],
    principalVarieties: [
      'Kékfrankos',
      'Zweigelt',
      'Cabernet sauvignon',
      'Merlot',
      'Zöld veltelíni',
      'Sauvignon blanc',
    ],
    flagshipStyles: ['Soproni Kékfrankos', 'light red'],
    notes:
      "Western border district sharing terroir with Austria's Burgenland; the spiritual home of Hungarian Kékfrankos (Blaufränkisch).",
  },
  {
    borvidek: 'Szekszárdi',
    borregio: 'Pannon',
    slug: 'szekszardi',
    nameEn: 'Szekszárd',
    nSettlements: 15,
    areaKm2: 621.9,
    centroid: [18.6935, 46.3171],
    principalVarieties: [
      'Kadarka',
      'Kékfrankos',
      'Cabernet franc',
      'Cabernet sauvignon',
      'Merlot',
      'Syrah',
    ],
    flagshipStyles: ['Szekszárdi Bikavér', 'Kadarka', 'Bordeaux-style red'],
    notes:
      "Loess-soil southern district producing the other classic Bikavér style and some of Hungary's finest Kadarka; warm, dry summers.",
  },
  {
    borvidek: 'Tokaji',
    borregio: 'Tokaj',
    slug: 'tokaji',
    nameEn: 'Tokaj',
    nSettlements: 27,
    areaKm2: 873.1,
    centroid: [21.4202, 48.2525],
    principalVarieties: [
      'Furmint',
      'Hárslevelű',
      'Sárgamuskotály',
      'Kabar',
      'Zéta',
      'Kövérszőlő',
    ],
    flagshipStyles: ['aszú', 'late harvest', 'dry Furmint', 'szamorodni'],
    notes:
      'UNESCO World Heritage region on volcanic soils at the confluence of the Tisza and Bodrog; world-famous for botrytised aszú dessert wines and increasingly for dry Furmint.',
  },
  {
    borvidek: 'Tolnai',
    borregio: 'Pannon',
    slug: 'tolnai',
    nameEn: 'Tolna',
    nSettlements: 58,
    areaKm2: 2139.5,
    centroid: [18.5395, 46.5406],
    principalVarieties: [
      'Kékfrankos',
      'Cabernet sauvignon',
      'Merlot',
      'Chardonnay',
      'Olaszrizling',
      'Rajnai rizling',
    ],
    flagshipStyles: ['structured red', 'fresh white'],
    notes:
      'Lesser-known Pannon district to the north of Szekszárd, with similar loess soils; producing increasing volumes of varietal reds and whites.',
  },
  {
    borvidek: 'Villányi',
    borregio: 'Pannon',
    slug: 'villanyi',
    nameEn: 'Villány',
    nSettlements: 17,
    areaKm2: 273.6,
    centroid: [18.2736, 45.8856],
    principalVarieties: [
      'Cabernet franc',
      'Cabernet sauvignon',
      'Merlot',
      'Kékfrankos',
      'Portugieser',
      'Pinot noir',
    ],
    flagshipStyles: ['Villányi Franc', 'Bordeaux-style red'],
    notes:
      "Hungary's warmest district, on the south-facing slopes of the Villány hills; internationally known for Cabernet Franc (Villányi Franc DHC) and powerful Bordeaux-style reds.",
  },
  {
    borvidek: 'Zalai',
    borregio: 'Balaton',
    slug: 'zalai',
    nameEn: 'Zala',
    nSettlements: 37,
    areaKm2: 925.1,
    centroid: [16.9173, 46.6309],
    principalVarieties: [
      'Olaszrizling',
      'Cserszegi fűszeres',
      'Királyleányka',
      'Tramini',
      'Chardonnay',
    ],
    flagshipStyles: ['aromatic white', 'Cserszegi fűszeres'],
    notes:
      'Cool, wet south-western district producing mostly aromatic whites; partially overlaps the Balaton-felvidék hills.',
  },
];

// ----- Lookup helpers -----
const BORVIDEK_BY_SLUG = new Map(BORVIDEK_LIST.map((d) => [d.slug, d]));
const BORVIDEK_BY_NAME = new Map(BORVIDEK_LIST.map((d) => [d.borvidek, d]));
const BORREGIO_BY_SLUG = new Map(BORREGIO_LIST.map((r) => [r.slug, r]));

export function getBorvidekBySlug(slug: string): BorvidekMeta | undefined {
  return BORVIDEK_BY_SLUG.get(slug);
}

export function getBorvidekByName(name: string): BorvidekMeta | undefined {
  return BORVIDEK_BY_NAME.get(name);
}

export function getBorregioBySlug(slug: string): BorregioMeta | undefined {
  return BORREGIO_BY_SLUG.get(slug);
}

export function getDistrictsInRegion(regio: Borregio): BorvidekMeta[] {
  return BORVIDEK_LIST.filter((d) => d.borregio === regio);
}

// 5 nearest neighbours by centroid great-circle distance (simple haversine)
export function getNearestDistricts(
  slug: string,
  k: number = 5
): BorvidekMeta[] {
  const me = getBorvidekBySlug(slug);
  if (!me) return [];
  const [lon0, lat0] = me.centroid;
  const R = 6371;
  const toRad = (x: number) => (x * Math.PI) / 180;
  const dist = (a: [number, number]) => {
    const dLat = toRad(a[1] - lat0);
    const dLon = toRad(a[0] - lon0);
    const s =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(toRad(lat0)) *
        Math.cos(toRad(a[1])) *
        Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(s));
  };
  return BORVIDEK_LIST.filter((d) => d.slug !== slug)
    .map((d) => ({ d, km: dist(d.centroid) }))
    .sort((a, b) => a.km - b.km)
    .slice(0, k)
    .map((x) => x.d);
}

// ----- Variety list (38, from suitability_long) -----
export const VARIETY_LIST: {
  variety: string;
  slug: string;
  colour: 'red' | 'white';
}[] = [
  { variety: 'Arany sárfehér', slug: 'arany-sarfeher', colour: 'white' },
  { variety: 'Bianca', slug: 'bianca', colour: 'white' },
  { variety: 'Budai zöld', slug: 'budai-zold', colour: 'white' },
  { variety: 'Cabernet franc', slug: 'cabernet-franc', colour: 'red' },
  { variety: 'Cabernet sauvignon', slug: 'cabernet-sauvignon', colour: 'red' },
  { variety: 'Chardonnay', slug: 'chardonnay', colour: 'white' },
  { variety: 'Cirfandli', slug: 'cirfandli', colour: 'white' },
  { variety: 'Cserszegi fűszeres', slug: 'cserszegi-fuszeres', colour: 'white' },
  { variety: 'Ezerjó', slug: 'ezerjo', colour: 'white' },
  { variety: 'Furmint', slug: 'furmint', colour: 'white' },
  { variety: 'Generosa', slug: 'generosa', colour: 'white' },
  { variety: 'Hárslevelű', slug: 'harslevelu', colour: 'white' },
  { variety: 'Irsai Olivér', slug: 'irsai-oliver', colour: 'white' },
  { variety: 'Juhfark', slug: 'juhfark', colour: 'white' },
  { variety: 'Kabar', slug: 'kabar', colour: 'white' },
  { variety: 'Kadarka', slug: 'kadarka', colour: 'red' },
  { variety: 'Királyleányka', slug: 'kiralyleanyka', colour: 'white' },
  { variety: 'Kékfrankos', slug: 'kekfrankos', colour: 'red' },
  { variety: 'Kéknyelű', slug: 'keknyelu', colour: 'white' },
  { variety: 'Kövérszőlő', slug: 'koverszolo', colour: 'white' },
  { variety: 'Leányka', slug: 'leanyka', colour: 'white' },
  { variety: 'Merlot', slug: 'merlot', colour: 'red' },
  { variety: 'Muscat ottonel', slug: 'muscat-ottonel', colour: 'white' },
  { variety: 'Müller-Thurgau', slug: 'muller-thurgau', colour: 'white' },
  { variety: 'Olaszrizling', slug: 'olaszrizling', colour: 'white' },
  { variety: 'Pinot blanc', slug: 'pinot-blanc', colour: 'white' },
  { variety: 'Pinot noir', slug: 'pinot-noir', colour: 'red' },
  { variety: 'Portugieser', slug: 'portugieser', colour: 'red' },
  { variety: 'Rajnai rizling', slug: 'rajnai-rizling', colour: 'white' },
  { variety: 'Rizlingszilváni', slug: 'rizlingszilvani', colour: 'white' },
  { variety: 'Sauvignon blanc', slug: 'sauvignon-blanc', colour: 'white' },
  { variety: 'Syrah', slug: 'syrah', colour: 'red' },
  { variety: 'Szürkebarát', slug: 'szurkebarat', colour: 'white' },
  { variety: 'Sárgamuskotály', slug: 'sargamuskotaly', colour: 'white' },
  { variety: 'Tramini', slug: 'tramini', colour: 'white' },
  { variety: 'Zweigelt', slug: 'zweigelt', colour: 'red' },
  { variety: 'Zéta', slug: 'zeta', colour: 'white' },
  { variety: 'Zöld veltelíni', slug: 'zold-veltelini', colour: 'white' },
];

const VARIETY_BY_SLUG = new Map(VARIETY_LIST.map((v) => [v.slug, v]));
export function getVarietyBySlug(slug: string) {
  return VARIETY_BY_SLUG.get(slug);
}

// ----- Index metadata (the 9 viticulture indices) -----
export const INDEX_META: Record<
  string,
  { label: string; units: string; description: string }
> = {
  winkler_gdd: {
    label: 'Winkler GDD',
    units: '°C·days',
    description:
      'Growing degree days base 10°C, April–October (Winkler index / heat summation).',
  },
  huglin_index: {
    label: 'Huglin Index',
    units: '°C·days',
    description: 'Huglin heliothermal index, April–September.',
  },
  spring_frost_days: {
    label: 'Spring frost days',
    units: 'days',
    description: 'Days with Tmin < 0°C between 1 March and 31 May.',
  },
  last_spring_frost_doy: {
    label: 'Last spring frost (DOY)',
    units: 'day of year',
    description: 'Day of year of the last spring frost (Tmin < 0°C).',
  },
  heat_days_t35: {
    label: 'Heat days ≥35°C',
    units: 'days',
    description: 'Days with Tmax ≥ 35°C, April–October.',
  },
  extreme_heat_days_t38: {
    label: 'Extreme heat days ≥38°C',
    units: 'days',
    description: 'Days with Tmax ≥ 38°C, April–October.',
  },
  growing_season_precip: {
    label: 'Growing-season precip',
    units: 'mm',
    description: 'Total precipitation April–October.',
  },
  hargreaves_pet: {
    label: 'Hargreaves PET',
    units: 'mm',
    description:
      'Hargreaves–Samani reference evapotranspiration, April–October.',
  },
  p_minus_pet: {
    label: 'P − PET (drought)',
    units: 'mm',
    description:
      'Growing-season water balance: precipitation minus Hargreaves PET.',
  },
  cool_night_index: {
    label: 'Cool night index',
    units: '°C',
    description: 'Mean minimum temperature in September.',
  },
};
