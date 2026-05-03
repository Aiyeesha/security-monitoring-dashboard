import type { SecurityEvent, Severity } from '../types'

const SEV_BG: Record<Severity, string> = {
  critical: '#dc2626',
  high:     '#ea580c',
  medium:   '#ca8a04',
  low:      '#2563eb',
  info:     '#475569',
}

export default function AlertList({ events }: { events: SecurityEvent[] }) {
  return (
    <section className="alert-section">
      <div className="alert-section-header">
        <h2>Security Events</h2>
        <span className="alert-count">{events.length} events</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Severity</th>
            <th>Event</th>
            <th>Source</th>
            <th>Host / IP</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {events.map((ev) => (
            <tr key={ev.id}>
              <td style={{ whiteSpace: 'nowrap', color: '#94a3b8' }}>
                {new Date(ev.timestamp).toLocaleTimeString()}
              </td>
              <td>
                <span className="sev-badge" style={{ background: SEV_BG[ev.severity] }}>
                  {ev.severity.toUpperCase()}
                </span>
              </td>
              <td>
                <div className="event-title">{ev.title}</div>
                <div className="event-desc">{ev.description}</div>
              </td>
              <td style={{ color: '#94a3b8' }}>{ev.source}</td>
              <td style={{ color: '#94a3b8', fontSize: '0.78rem' }}>
                {ev.host ?? '—'}
                {ev.ip && <div style={{ color: '#475569' }}>{ev.ip}</div>}
              </td>
              <td>
                <span className={`status-pill ${ev.status}`}>{ev.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
