'use client';

import { useEffect, useMemo, useState } from 'react';
import Map from 'react-map-gl/maplibre';
import DeckGL from '@deck.gl/react';
import { GeoJsonLayer } from '@deck.gl/layers';
import type { PickingInfo } from '@deck.gl/core';
// luma.gl 9.x requires the WebGL device adapter to be imported explicitly
// so deck.gl can find it. Without this, the runtime crashes with
// "Cannot read properties of undefined (reading 'maxTextureDimension2D')"
// in WebGLCanvasContext.getMaxDrawingBufferSize.
import { webgl2Adapter } from '@luma.gl/webgl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { useRouter, usePathname } from 'next/navigation';
import { slugify } from '@/lib/district-meta';

// Official Hungarian wine-region color scheme, transcribed from
// `Borvidekterkep.png`. Each borrégió has its own colour family; districts
// within a family share a hue and differ in shade so they remain visually
// distinct while signalling the regional grouping.
//
//   Észak-Dunántúl  → cool purples / lavenders
//   Balaton          → greens
//   Pannon           → pinks → wine reds
//   Duna             → yellows / oranges / cream
//   Észak-Mo.        → bright oranges / yellow (volcanic ridge)
//   Tokaj            → dark brown
const DISTRICT_COLORS: Record<string, [number, number, number]> = {
  // Észak-Dunántúl (lavenders / purples)
  Soproni:                [184, 181, 214],
  Pannonhalmi:            [180, 158, 203],
  Neszmélyi:              [220, 212, 232],
  Móri:                   [210, 201, 221],
  'Etyek-Budai':          [200, 183, 220],

  // Balaton (greens)
  'Nagy-Somlói':          [46, 107, 62],
  Zalai:                  [111, 165, 87],
  'Balaton-felvidéki':    [136, 184, 149],
  Balatonfelvidéki:       [136, 184, 149], // user spelling without hyphen
  Badacsonyi:             [74, 155, 98],
  'Balatonfüred-Csopaki': [171, 207, 161],
  Balatonboglári:         [183, 205, 85],

  // Pannon (pinks → wine reds)
  Tolnai:                 [240, 175, 195],
  Szekszárdi:             [220, 110, 145],
  Pécsi:                  [165, 30, 55],
  Villányi:               [125, 25, 50],

  // Duna (yellows / orange / cream)
  'Hajós-Bajai':          [255, 240, 175],
  Csongrádi:              [240, 155, 75],
  Kunsági:                [255, 235, 200],

  // Észak-Magyarországi (orange / dark orange / yellow)
  Mátrai:                 [240, 145, 55],
  Egri:                   [220, 90, 50],
  Bükki:                  [255, 230, 50],

  // Tokaj
  Tokaji:                 [120, 70, 40],
};
// Fallback if a district name doesn't appear in the table (shouldn't happen
// with our 22 known borvidék but defensive).
const FALLBACK_COLOR: [number, number, number] = [153, 153, 153];

function colorForDistrict(borvidek: string): [number, number, number] {
  return DISTRICT_COLORS[borvidek] ?? FALLBACK_COLOR;
}

const HUNGARY_VIEW = {
  longitude: 19.5,
  latitude: 47.15,
  zoom: 6.3,
  pitch: 0,
  bearing: 0,
};

type DistrictProps = {
  borvidek: string;
  borregio?: string;
  n_settlements: number;
  area_km2: number;
};

export type DistrictMapProps = {
  geojsonUrl?: string;
  /** Values keyed by borvidek name for choropleth colouring */
  metricValues?: Record<string, number>;
  locale?: string;
  clickable?: boolean;
  lowColor?: [number, number, number];
  highColor?: [number, number, number];
  /** Optional label shown under the hover value */
  metricLabel?: string;
};

export default function DistrictMap({
  geojsonUrl = '/data/wine_districts.geojson',
  metricValues,
  locale: localeProp,
  clickable = true,
  lowColor = [253, 231, 37],
  highColor = [68, 1, 84],
  metricLabel,
}: DistrictMapProps) {
  // Derive the active locale from the URL when no prop is passed, so the
  // component navigates to /hu/districts/... when the user is on /hu/.
  const pathname = usePathname() ?? '';
  const pathLocale = pathname.startsWith('/hu') ? 'hu' : 'en';
  const locale = localeProp ?? pathLocale;
  const [fc, setFc] = useState<GeoJSON.FeatureCollection | null>(null);
  const [hover, setHover] = useState<{
    x: number;
    y: number;
    props: DistrictProps;
  } | null>(null);
  const router = useRouter();

  useEffect(() => {
    let alive = true;
    fetch(geojsonUrl)
      .then((r) => r.json())
      .then((j) => {
        if (alive) setFc(j);
      })
      .catch(() => {});
    return () => {
      alive = false;
    };
  }, [geojsonUrl]);

  const normMetric = useMemo(() => {
    if (!metricValues) return null;
    const vals = Object.values(metricValues).filter((v) => Number.isFinite(v));
    if (vals.length === 0) return null;
    const lo = Math.min(...vals);
    const hi = Math.max(...vals);
    const span = hi - lo || 1;
    const norm: Record<string, number> = {};
    for (const [k, v] of Object.entries(metricValues)) {
      norm[k] = (v - lo) / span;
    }
    return norm;
  }, [metricValues]);

  const layers = useMemo(() => {
    if (!fc) return [];
    return [
      new GeoJsonLayer<DistrictProps>({
        id: 'wine-districts',
        data: fc as unknown as GeoJSON.FeatureCollection,
        filled: true,
        stroked: true,
        pickable: true,
        autoHighlight: true,
        highlightColor: [255, 255, 255, 60],
        getFillColor: (f: GeoJSON.Feature) => {
          const p = (f.properties ?? {}) as DistrictProps;
          if (normMetric && p.borvidek in normMetric) {
            const t = normMetric[p.borvidek];
            const r = Math.round(lowColor[0] + (highColor[0] - lowColor[0]) * t);
            const g = Math.round(lowColor[1] + (highColor[1] - lowColor[1]) * t);
            const b = Math.round(lowColor[2] + (highColor[2] - lowColor[2]) * t);
            return [r, g, b, 210];
          }
          const [r, g, b] = colorForDistrict(p.borvidek);
          return [r, g, b, 190];
        },
        getLineColor: [40, 40, 40, 230],
        lineWidthMinPixels: 1,
        onHover: (info: PickingInfo) => {
          if (info.object && info.x != null && info.y != null) {
            const f = info.object as GeoJSON.Feature;
            setHover({
              x: info.x,
              y: info.y,
              props: (f.properties ?? {}) as DistrictProps,
            });
          } else {
            setHover(null);
          }
        },
        onClick: (info: PickingInfo) => {
          if (!clickable || !info.object) return;
          const f = info.object as GeoJSON.Feature;
          const p = (f.properties ?? {}) as DistrictProps;
          const slug = slugify(p.borvidek);
          router.push(`/${locale}/districts/${slug}`);
        },
      }),
    ];
  }, [fc, normMetric, lowColor, highColor, clickable, locale, router]);

  return (
    <div className="relative h-full w-full">
      <DeckGL
        initialViewState={HUNGARY_VIEW}
        controller
        layers={layers}
        deviceProps={{ adapters: [webgl2Adapter] }}
        style={{ position: 'absolute', inset: '0' }}
      >
        <Map
          mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
          reuseMaps
        />
      </DeckGL>
      {hover && (
        <div
          className="pointer-events-none absolute z-10 max-w-[80vw] rounded bg-neutral-900/90 px-2 py-1 text-xs text-white shadow"
          style={{
            left: Math.min(hover.x + 12, (typeof window !== 'undefined' ? window.innerWidth : 1024) - 180),
            top: hover.y + 12,
          }}
        >
          <div className="font-semibold">{hover.props.borvidek}</div>
          <div className="text-neutral-300">
            {hover.props.area_km2?.toFixed(0)} km² · {hover.props.n_settlements}{' '}
            settlements
          </div>
          {metricValues && hover.props.borvidek in metricValues && (
            <div>
              {metricValues[hover.props.borvidek].toFixed(1)}
              {metricLabel ? ` ${metricLabel}` : ''}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
