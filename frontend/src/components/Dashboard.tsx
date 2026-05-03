import type { Metrics, SecurityEvent } from '../types'
import AlertList from './AlertList'
import MetricsPanel from './MetricsPanel'

interface Props {
  events: SecurityEvent[]
  metrics: Metrics | null
}

export default function Dashboard({ events, metrics }: Props) {
  return (
    <main className="dashboard">
      {metrics && <MetricsPanel metrics={metrics} />}
      <AlertList events={events} />
    </main>
  )
}
