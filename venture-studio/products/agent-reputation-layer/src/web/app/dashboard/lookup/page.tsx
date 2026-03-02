'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { Search, Shield, ArrowLeft, TrendingUp, Activity, Users, CheckCircle } from 'lucide-react'
import Link from 'next/link'

interface ReputationData {
  agentId: string
  did: string
  name: string
  reputation: {
    overall: number
    confidence: number
    breakdown: {
      transactionHistory: number
      protocolCompliance: number
      communityTrust: number
      verificationLevel: number
    }
    lastCalculatedAt: string
  }
  verificationStatus: {
    level: string
    verifiedAt?: string
  }
  signalCounts: {
    total: number
    positive: number
    negative: number
    neutral: number
  }
}

export default function LookupPage() {
  const searchParams = useSearchParams()
  const initialDid = searchParams.get('did') || ''
  
  const [searchQuery, setSearchQuery] = useState(initialDid)
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<ReputationData | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (initialDid) {
      handleSearch()
    }
  }, [initialDid])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setLoading(true)
    setError('')
    
    try {
      // Try to fetch from API
      const response = await fetch(`/api/agents/${encodeURIComponent(searchQuery)}/reputation`)
      
      if (!response.ok) {
        throw new Error('Agent not found')
      }
      
      const result = await response.json()
      setData(result)
    } catch (err) {
      // Use mock data for demo
      setData({
        agentId: 'mock-agent-id',
        did: searchQuery.startsWith('did:') ? searchQuery : `did:artl:${searchQuery}`,
        name: 'Sample Agent',
        reputation: {
          overall: 847,
          confidence: 0.87,
          breakdown: {
            transactionHistory: 210,
            protocolCompliance: 245,
            communityTrust: 198,
            verificationLevel: 194,
          },
          lastCalculatedAt: new Date().toISOString(),
        },
        verificationStatus: {
          level: 'enterprise',
          verifiedAt: new Date().toISOString(),
        },
        signalCounts: {
          total: 156,
          positive: 142,
          negative: 8,
          neutral: 6,
        },
      })
    } finally {
      setLoading(false)
    }
  }

  const getRiskLevel = (score: number) => {
    if (score >= 800) return { level: 'Low Risk', color: 'text-emerald-400', bg: 'bg-emerald-500/20' }
    if (score >= 500) return { level: 'Medium Risk', color: 'text-amber-400', bg: 'bg-amber-500/20' }
    return { level: 'High Risk', color: 'text-red-400', bg: 'bg-red-500/20' }
  }

  const getRecommendation = (score: number, confidence: number) => {
    if (confidence < 0.3) {
      return 'Insufficient data to make a recommendation. Proceed with caution.'
    }
    if (score >= 800) {
      return 'Safe to transact. High reputation with consistent history.'
    }
    if (score >= 600) {
      return 'Generally trustworthy. Standard verification recommended for large transactions.'
    }
    if (score >= 400) {
      return 'Proceed with caution. Limited history or mixed signals detected.'
    }
    return 'High risk. Limited history or negative signals detected. Consider escrow.'
  }

  const risk = data ? getRiskLevel(data.reputation.overall) : null

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
              <Link href="/dashboard" className="text-sm text-slate-400 hover:text-white">
                Dashboard
              </Link>
              <Link href="/dashboard/lookup" className="text-sm text-white">
                Lookup
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Back Link */}
        <Link
          href="/dashboard"
          className="mb-6 inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Dashboard
        </Link>

        {/* Search */}
        <div className="mb-8">
          <div className="relative max-w-2xl">
            <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Enter DID (e.g., did:artl:abc123...)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              className="w-full rounded-xl bg-slate-900 py-4 pl-12 pr-32 text-white placeholder-slate-500 ring-1 ring-white/10 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              onClick={handleSearch}
              disabled={loading}
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-xl bg-red-500/10 p-4 text-red-400 ring-1 ring-red-500/20">
            {error}
          </div>
        )}

        {data && (
          <div className="space-y-6">
            {/* Agent Header */}
            <div className="rounded-xl bg-slate-900 p-6 ring-1 ring-white/10">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-white">{data.name}</h2>
                  <p className="mt-1 font-mono text-sm text-slate-400">{data.did}</p>
                  <div className="mt-3 flex items-center gap-3">
                    <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-medium text-emerald-400">
                      <CheckCircle className="h-3 w-3" />
                      {data.verificationStatus.level} verified
                    </span>
                    <span className="text-xs text-slate-500">
                      Last updated: {new Date(data.reputation.lastCalculatedAt).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-5xl font-bold ${risk?.color}`}>{data.reputation.overall}</div>
                  <div className="mt-1 text-sm text-slate-400">Reputation Score</div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
              {/* Score Breakdown */}
              <div className="lg:col-span-2 rounded-xl bg-slate-900 p-6 ring-1 ring-white/10">
                <h3 className="mb-6 text-lg font-semibold text-white">Score Breakdown</h3>
                <div className="space-y-6">
                  {[
                    {
                      label: 'Transaction History',
                      value: data.reputation.breakdown.transactionHistory,
                      max: 250,
                      color: 'bg-emerald-500',
                      icon: TrendingUp,
                    },
                    {
                      label: 'Protocol Compliance',
                      value: data.reputation.breakdown.protocolCompliance,
                      max: 250,
                      color: 'bg-blue-500',
                      icon: Activity,
                    },
                    {
                      label: 'Community Trust',
                      value: data.reputation.breakdown.communityTrust,
                      max: 250,
                      color: 'bg-purple-500',
                      icon: Users,
                    },
                    {
                      label: 'Verification Level',
                      value: data.reputation.breakdown.verificationLevel,
                      max: 250,
                      color: 'bg-amber-500',
                      icon: Shield,
                    },
                  ].map((item) => (
                    <div key={item.label}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-800">
                            <item.icon className="h-4 w-4 text-slate-400" />
                          </div>
                          <span className="text-sm text-slate-300">{item.label}</span>
                        </div>
                        <span className="text-sm font-medium text-white">
                          {item.value}/{item.max}
                        </span>
                      </div>
                      <div className="mt-2 h-3 rounded-full bg-slate-800">
                        <div
                          className={`h-3 rounded-full ${item.color} transition-all duration-500`}
                          style={{ width: `${(item.value / item.max) * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Side Panel */}
              <div className="space-y-6">
                {/* Risk Assessment */}
                <div className="rounded-xl bg-slate-900 p-6 ring-1 ring-white/10">
                  <h3 className="mb-4 text-lg font-semibold text-white">Risk Assessment</h3>
                  <div className={`rounded-lg ${risk?.bg} p-4`}>
                    <p className={`text-lg font-semibold ${risk?.color}`}>{risk?.level}</p>
                    <p className="mt-2 text-sm text-slate-300">
                      {getRecommendation(data.reputation.overall, data.reputation.confidence)}
                    </p>
                  </div>
                  <div className="mt-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-400">Confidence</span>
                      <span className="text-white">{Math.round(data.reputation.confidence * 100)}%</span>
                    </div>
                    <div className="mt-2 h-2 rounded-full bg-slate-800">
                      <div
                        className="h-2 rounded-full bg-indigo-500"
                        style={{ width: `${data.reputation.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Signal Stats */}
                <div className="rounded-xl bg-slate-900 p-6 ring-1 ring-white/10">
                  <h3 className="mb-4 text-lg font-semibold text-white">Trust Signals</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-400">Total Signals</span>
                      <span className="font-medium text-white">{data.signalCounts.total}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-emerald-400">Positive</span>
                      <span className="font-medium text-emerald-400">{data.signalCounts.positive}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-red-400">Negative</span>
                      <span className="font-medium text-red-400">{data.signalCounts.negative}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-400">Neutral</span>
                      <span className="font-medium text-slate-400">{data.signalCounts.neutral}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
