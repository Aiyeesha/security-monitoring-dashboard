import type { Metrics } from '../types'

const SEV_COLORS = {
  total:    '#64748b',
  open:     '#f59e0b',
  critical: '#ef4444',
  high:     '#f97316',
  resolved: '#22c55e',
  mttr:     '#3b82f6',
}

export default function MetricsPanel({ metrics }: { metrics: Metrics }) {
  const cards = [
    { label: 'Total Events',    value: metrics.total_events,     color: SEV_COLORS.total },
    { label: 'Open Alerts',     value: metrics.open_events,      color: SEV_COLORS.open },
    { label: 'Critical',        value: metrics.critical_count,   color: SEV_COLORS.critical },
    { label: 'High',            value: metrics.high_count,       color: SEV_COLORS.high },
    { label: 'Resolved (24h)',  value: metrics.resolved_last_24h,color: SEV_COLORS.resolved },
    { label: 'MTTR (min)',      value: metrics.mttr_minutes,     color: SEV_COLORS.mttr },
  ]
  return (
    <section className="metrics-panel">
      {cards.map((c) => (
        <div key={c.label} className="metric-card" style={{ borderTopColor: c.color }}>
          <span className="metric-value" style={{ color: c.color }}>{c.value}</span>
          <span className="metric-label">{c.label}</span>
        </div>
      ))}
    </section>
  )
}
