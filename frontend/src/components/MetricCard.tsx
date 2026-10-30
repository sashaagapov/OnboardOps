type MetricCardProps = {
  label: string;
  value: number | string;
  tone?: "default" | "success" | "progress" | "warning";
};

export function MetricCard({ label, value, tone = "default" }: MetricCardProps) {
  return (
    <article className={`metric-card metric-card--${tone}`} aria-label={`${label}: ${value}`}>
      <p className="metric-card__label">{label}</p>
      <strong className="metric-card__value">{value}</strong>
    </article>
  );
}
