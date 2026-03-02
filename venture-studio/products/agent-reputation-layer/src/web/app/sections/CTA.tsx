'use client'

export default function CTA() {
  return (
    <section className="relative isolate overflow-hidden bg-slate-950 py-24">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Ready to build trust?
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-slate-300">
            Join thousands of developers and enterprises using ARTL to verify agent trustworthiness.
          </p>
          
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="#pricing"
              className="rounded-lg bg-indigo-500 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-400"
            >
              Get Started Free
            </a>
            <a href="#" className="text-sm font-semibold leading-6 text-slate-300 hover:text-white">
              Read Documentation <span aria-hidden="true">→</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}