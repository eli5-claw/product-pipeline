'use client'

import { Check } from 'lucide-react'

const tiers = [
  {
    name: 'Free',
    id: 'free',
    price: '$0',
    description: 'Perfect for individual developers and small projects.',
    features: [
      'Up to 3 agents',
      '1,000 API calls/month',
      'Basic reputation scoring',
      'Email verification',
      'Community support',
    ],
    cta: 'Get Started',
    mostPopular: false,
  },
  {
    name: 'Pro',
    id: 'pro',
    price: '$49',
    description: 'For growing teams and businesses.',
    features: [
      'Up to 20 agents',
      '50,000 API calls/month',
      'Advanced reputation scoring',
      'Domain verification',
      'Priority support',
      'Webhook notifications',
      'Analytics dashboard',
    ],
    cta: 'Start Free Trial',
    mostPopular: true,
  },
  {
    name: 'Enterprise',
    id: 'enterprise',
    price: '$299',
    description: 'For large organizations with advanced needs.',
    features: [
      'Unlimited agents',
      '500,000 API calls/month',
      'Custom reputation models',
      'Enterprise verification',
      'SLA guarantee',
      'Dedicated support',
      'Custom integrations',
      'On-premise option',
    ],
    cta: 'Contact Sales',
    mostPopular: false,
  },
]

export default function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-slate-950">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-400">Pricing</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Simple, transparent pricing
          </p>
        </div>
        
        <div className="mx-auto mt-16 grid max-w-lg grid-cols-1 gap-8 lg:max-w-none lg:grid-cols-3">
          {tiers.map((tier) => (
            <div
              key={tier.id}
              className={`flex flex-col justify-between rounded-3xl p-8 ring-1 ${
                tier.mostPopular ? 'bg-indigo-900/20 ring-indigo-500' : 'bg-slate-900/50 ring-white/10'
              } xl:p-10`}
            >
              <div>
                <div className="flex items-center justify-between gap-x-4">
                  <h3 className={`text-lg font-semibold leading-8 ${tier.mostPopular ? 'text-indigo-400' : 'text-white'}`}>
                    {tier.name}
                  </h3>
                  {tier.mostPopular ? (
                    <p className="rounded-full bg-indigo-500/10 px-2.5 py-1 text-xs font-semibold leading-5 text-indigo-400">
                      Most popular
                    </p>
                  ) : null}
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-300">{tier.description}</p>
                
                <p className="mt-6 flex items-baseline gap-x-1">
                  <span className="text-4xl font-bold tracking-tight text-white">{tier.price}</span>
                  <span className="text-sm font-semibold leading-6 text-slate-300">/month</span>
                </p>
                
                <ul role="list" className="mt-8 space-y-3 text-sm leading-6 text-slate-300">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex gap-x-3">
                      <Check className="h-6 w-5 flex-none text-indigo-400" aria-hidden="true" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              
              <a
                href="#"
                className={`mt-8 block rounded-md px-3 py-2 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ${
                  tier.mostPopular
                    ? 'bg-indigo-500 text-white hover:bg-indigo-400 focus-visible:outline-indigo-500'
                    : 'bg-white/10 text-white hover:bg-white/20'
                }`}
              >
                {tier.cta}
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}