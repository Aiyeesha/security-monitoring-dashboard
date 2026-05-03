import { useCallback, useEffect, useState } from 'react'
import './App.css'
import Dashboard from './components/Dashboard'
import type { Metrics, SecurityEvent } from './types'

export default function App() {
  const [events, setEvents] = useState<SecurityEvent[]>([])
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [connected, setConnected] = useState(false)

  const refresh = useCallback(async () => {
    const [evRes, mRes] = await Promise.all([
      fetch('/api/events'),
      fetch('/api/metrics'),
    ])
    setEvents(await evRes.json())
    setMetrics(await mRes.json())
  }, [])

  useEffect(() => {
    refresh()
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${proto}://${window.location.host}/ws/events`)
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = () => refresh()
    return () => ws.close()
  }, [refresh])

  return (
    <div className="app">
      <header className="app-header">
        <h1>&#x1F6E1;&#xFE0F; Security Monitoring Dashboard</h1>
        <span className={`live-badge ${connected ? 'on' : 'off'}`}>
          {connected ? '● LIVE' : '○ OFFLINE'}
        </span>
      </header>
      <Dashboard events={events} metrics={metrics} />
    </div>
  )
}
