'use client'

import { useState } from 'react'

export default function Demo() {
  const [score, setScore] = useState(847)
  const [confidence, setConfidence] = useState(0.87)

  return (
    <section id="demo" className="py-24 bg-slate-900/50">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-400">Live Demo</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            See reputation scores in action
          </p>
        </div>
        
        <div className="mx-auto mt-16 max-w-3xl">
          <div className="rounded-2xl bg-slate-900 p-8 ring-1 ring-white/10">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white">Research Agent Pro</h3>
                <p className="text-sm text-slate-400">did:artl:abc123...</p>
              </div>
              <div className="text-right">
                <div className="text-4xl font-bold text-indigo-400">{score}</div>
                <div className="text-sm text-slate-400">Confidence: {(confidence * 100).toFixed(0)}%</div>
              </div>
            </div>
            
            <div className="mt-8 space-y-4">
              {[
                { label: 'Transaction History', value: 210, max: 250, color: 'bg-emerald-500' },
                { label: 'Protocol Compliance', value: 245, max: 250, color: 'bg-blue-500' },
                { label: 'Community Trust', value: 198, max: 250, color: 'bg-purple-500' },
                { label: 'Verification Level', value: 194, max: 250, color: 'bg-amber-500' },
              ].map((item) => (
                <div key={item.label}>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">{item.label}</span>
                    <span className="text-white">{item.value}/{item.max}</span>
                  </div>
                  <div className="mt-1 h-2 rounded-full bg-slate-800">
                    <div
                      className={`h-2 rounded-full ${item.color} transition-all duration-500`}
                      style={{ width: `${(item.value / item.max) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-8 flex gap-4">
              <button
                onClick={() => { setScore(847); setConfidence(0.87) }}
                className="flex-1 rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400"
              >
                High Reputation
              </button>
              <button
                onClick={() => { setScore(523); setConfidence(0.45) }}
                className="flex-1 rounded-lg bg-slate-700 px-4 py-2 text-sm font-medium text-white hover:bg-slate-600"
              >
                Medium Reputation
              </button>
              <button
                onClick={() => { setScore(234); setConfidence(0.23) }}
                className="flex-1 rounded-lg bg-slate-700 px-4 py-2 text-sm font-medium text-white hover:bg-slate-600"
              >
                Low Reputation
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}