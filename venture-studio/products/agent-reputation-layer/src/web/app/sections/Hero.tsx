'use client'

import { Shield, Zap, Globe, Lock } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden pt-20 pb-32">
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/20 via-slate-950 to-slate-950" />
      
      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-8 flex justify-center">
            <div className="flex items-center gap-2 rounded-full bg-indigo-500/10 px-4 py-2 text-sm font-medium text-indigo-400 ring-1 ring-inset ring-indigo-500/20">
              <Shield className="h-4 w-4" />
              <span>The trust layer for AI agents</span>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl">
            Reputation infrastructure for the
            <span className="text-indigo-400"> agent economy</span>
          </h1>
          
          <p className="mt-6 text-lg leading-8 text-slate-300">
            ARTL provides universal reputation scores for AI agents across MCP, A2A, and blockchain protocols. 
            Verify trustworthiness before transacting.
          </p>
          
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="#pricing"
              className="rounded-lg bg-indigo-500 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-400"
            >
              Get Started
            </a>
            <a href="#demo" className="text-sm font-semibold leading-6 text-slate-300 hover:text-white">
              View Demo <span aria-hidden="true">→</span>
            </a>
          </div>
          
          <div className="mt-16 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[
              { icon: Shield, label: 'Verified Agents', value: '10,000+' },
              { icon: Zap, label: 'API Calls/Day', value: '1M+' },
              { icon: Globe, label: 'Protocols', value: '3' },
              { icon: Lock, label: 'Trust Signals', value: '500K+' },
            ].map((stat) => (
              <div key={stat.label} className="flex flex-col items-center rounded-lg bg-slate-900/50 p-4">
                <stat.icon className="h-6 w-6 text-indigo-400" />
                <div className="mt-2 text-2xl font-bold text-white">{stat.value}</div>
                <div className="text-sm text-slate-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}