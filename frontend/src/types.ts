export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info'
export type EventStatus = 'open' | 'investigating' | 'resolved'

export interface SecurityEvent {
  id: string
  timestamp: string
  severity: Severity
  title: string
  description: string
  source: string
  category: string
  status: EventStatus
  host?: string
  ip?: string
}

export interface Metrics {
  total_events: number
  open_events: number
  critical_count: number
  high_count: number
  medium_count: number
  low_count: number
  resolved_last_24h: number
  mttr_minutes: number
}
