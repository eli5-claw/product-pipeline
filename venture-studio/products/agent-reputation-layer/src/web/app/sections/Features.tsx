'use client'

import { BarChart3, Link2, Scale, Fingerprint } from 'lucide-react'

const features = [
  {
    name: 'Universal Reputation Scoring',
    description: '0-1000 reputation score based on transaction history, protocol compliance, community trust, and verification level.',
    icon: BarChart3,
  },
  {
    name: 'Cross-Protocol Integration',
    description: 'Native support for MCP, A2A, and blockchain protocols. Reputation travels with your agents across platforms.',
    icon: Link2,
  },
  {
    name: 'Dispute Resolution',
    description: 'Built-in dispute filing and resolution system with escrow support for high-value transactions.',
    icon: Scale,
  },
  {
    name: 'Identity Verification',
    description: 'Email, domain, and enterprise verification options to increase trust and reputation scores.',
    icon: Fingerprint,
  },
]

export default function Features() {
  return (
    <section id="features" className="py-24 bg-slate-950">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-400">Features</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Everything you need to trust agents
          </p>
        </div>
        
        <div className="mx-auto mt-16 max-w-7xl">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <div key={feature.name} className="relative rounded-2xl bg-slate-900/50 p-8 ring-1 ring-white/10">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-500">
                  <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <h3 className="mt-4 text-lg font-semibold leading-8 text-white">{feature.name}</h3>
                <p className="mt-2 text-sm leading-7 text-slate-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}