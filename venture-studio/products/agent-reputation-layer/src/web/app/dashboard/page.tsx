'use client'

import { useState, useEffect } from 'react'
import { Search, Shield, TrendingUp, Users, Activity } from 'lucide-react'
import Link from 'next/link'

interface Agent {
  id: string
  did: string
  name: string
  type: string
  reputation: {
    overall: number
    confidence: number
    breakdown: {
      transactionHistory: number
      protocolCompliance: number
      communityTrust: number
      verificationLevel: number
    }
  }
  verificationStatus: {
    level: string
  }
}

export default function DashboardPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalAgents: 0,
    avgScore: 0,
    verifiedAgents: 0,
    totalSignals: 0,
  })

  useEffect(() => {
    fetchAgents()
    fetchStats()
  }, [])

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents?perPage=10')
      const data = await response.json()
      setAgents(data.data || [])
    } catch (error) {
      console.error('Failed to fetch agents:', error)
      // Use mock data for demo
      setAgents([
        {
          id: '1',
          did: 'did:artl:abc123',
          name: 'Research Agent Pro',
          type: 'autonomous',
          reputation: {
            overall: 847,
            confidence: 0.87,
            breakdown: {
              transactionHistory: 210,
              protocolCompliance: 245,
              communityTrust: 198,
              verificationLevel: 194,
            },
          },
          verificationStatus: { level: 'enterprise' },
        },
        {
          id: '2',
          did: 'did:artl:def456',
          name: 'Data Processor X',
          type: 'service',
          reputation: {
            overall: 723,
            confidence: 0.72,
            breakdown: {
              transactionHistory: 185,
              protocolCompliance: 198,
              communityTrust: 175,
              verificationLevel: 165,
            },
          },
          verificationStatus: { level: 'domain' },
        },
        {
          id: '3',
          did: 'did:artl:ghi789',
          name: 'Code Review Bot',
          type: 'autonomous',
          reputation: {
            overall: 612,
            confidence: 0.58,
            breakdown: {
              transactionHistory: 145,
              protocolCompliance: 168,
              communityTrust: 155,
              verificationLevel: 144,
            },
          },
          verificationStatus: { level: 'email' },
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    // Mock stats for demo
    setStats({
      totalAgents: 1247,
      avgScore: 684,
      verifiedAgents: 892,
      totalSignals: 45632,
    })
  }

  const getRiskColor = (score: number) => {
    if (score >= 800) return 'text-emerald-400'
    if (score >= 500) return 'text-amber-400'
    return 'text-red-400'
  }

  const getRiskBg = (score: number) => {
    if (score >= 800) return 'bg-emerald-500/20'
    if (score >= 500) return 'bg-amber-500/20'
    return 'bg-red-500/20'
  }

  const getVerificationBadge = (level: string) => {
    const colors: Record<string, string> = {
      none: 'bg-slate-700 text-slate-300',
      email: 'bg-blue-500/20 text-blue-400',
      domain: 'bg-purple-500/20 text-purple-400',
      enterprise: 'bg-emerald-500/20 text-emerald-400',
      kyc: 'bg-amber-500/20 text-amber-400',
    }
    return colors[level] || colors.none
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-500">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">ARTL Dashboard</h1>
                <p className="text-sm text-slate-400">Agent Reputation & Trust Layer</p>
              </div>
            </div>
            <nav className="flex gap-4">
              <Link href="/" className="text-sm text-slate-400 hover:text-white">
                Home
              </Link>
              <Link href="/dashboard" className="text-sm text-white">
                Dashboard
              </Link>
              <Link href="/dashboard/lookup" className="text-sm text-slate-400 hover:text-white">
                Lookup
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Stats */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { label: 'Total Agents', value: stats.totalAgents.toLocaleString(), icon: Users },
            { label: 'Average Score', value: stats.avgScore, icon: TrendingUp },
            { label: 'Verified Agents', value: stats.verifiedAgents.toLocaleString(), icon: Shield },
            { label: 'Trust Signals', value: stats.totalSignals.toLocaleString(), icon: Activity },
          ].map((stat) => (
            <div
              key={stat.label}
              className="rounded-xl bg-slate-900 p-6 ring-1 ring-white/10"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-500/20">
                  <stat.icon className="h-6 w-6 text-indigo-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">{stat.label}</p>
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Search */}
        <div className="mt-8">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by DID, name, or identifier..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-xl bg-slate-900 py-4 pl-12 pr-4 text-white placeholder-slate-500 ring-1 ring-white/10 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        {/* Agents Table */}
        <div className="mt-8 rounded-xl bg-slate-900 ring-1 ring-white/10">
          <div className="px-6 py-4 border-b border-slate-800">
            <h2 className="text-lg font-semibold text-white">Top Agents</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-800/50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase">Agent</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase">Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase">Confidence</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase">Status</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {loading ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-8 text-center text-slate-400">
                      Loading...
                    </td>
                  </tr>
                ) : (
                  agents.map((agent) => (
                    <tr key={agent.id} className="hover:bg-slate-800/50">
                      <td className="px-6 py-4">
                        <div>
                          <p className="font-medium text-white">{agent.name}</p>
                          <p className="text-sm text-slate-500">{agent.did.slice(0, 20)}...</p>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="inline-flex items-center rounded-full bg-slate-800 px-2.5 py-0.5 text-xs font-medium text-slate-300">
                          {agent.type}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <span className={`text-lg font-bold ${getRiskColor(agent.reputation.overall)}`}>
                            {agent.reputation.overall}
                          </span>
                          <span className="text-xs text-slate-500">/1000</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className="h-2 w-16 rounded-full bg-slate-800">
                            <div
                              className="h-2 rounded-full bg-indigo-500"
                              style={{ width: `${agent.reputation.confidence * 100}%` }}
                            />
                          </div>
                          <span className="text-sm text-slate-400">
                            {Math.round(agent.reputation.confidence * 100)}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getVerificationBadge(
                            agent.verificationStatus.level
                          )}`}
                        >
                          {agent.verificationStatus.level}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <Link
                          href={`/dashboard/lookup?did=${encodeURIComponent(agent.did)}`}
                          className="text-sm font-medium text-indigo-400 hover:text-indigo-300"
                        >
                          View →
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  )
}
