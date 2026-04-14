type MetricCardProps = {
  label: string;
  value: string;
  subtext?: string;
};

export default function MetricCard({ label, value, subtext }: MetricCardProps) {
  return (
    <div className="card p-5">
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {subtext ? <p className="mt-2 text-sm text-white/60">{subtext}</p> : null}
    </div>
  );
}
