// Pure SVG sparkline — no client JS needed, safe in RSC.

export type SparklineProps = {
  data: number[];
  width?: number;
  height?: number;
  stroke?: string;
};

export default function Sparkline({
  data,
  width = 120,
  height = 28,
  stroke = '#7a1d2e',
}: SparklineProps) {
  const clean = data.filter((v) => Number.isFinite(v));
  if (clean.length < 2) return null;
  const lo = Math.min(...clean);
  const hi = Math.max(...clean);
  const span = hi - lo || 1;
  const n = clean.length;
  const pts = clean
    .map((v, i) => {
      const x = (i / (n - 1)) * width;
      const y = height - ((v - lo) / span) * height;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className="block"
      aria-hidden="true"
    >
      <polyline
        points={pts}
        fill="none"
        stroke={stroke}
        strokeWidth={1.5}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}
